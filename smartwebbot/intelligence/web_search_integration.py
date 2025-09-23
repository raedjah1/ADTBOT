"""
Web Search Integration for SmartWebBot

Automatically finds URLs and information when the AI needs to navigate to unknown platforms
or find specific information to complete user tasks.
"""

import json
import re
import asyncio
import aiohttp
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
from urllib.parse import urlparse, urljoin

from ..core.base_component import BaseComponent


class SearchEngine(Enum):
    DUCKDUCKGO = "duckduckgo"
    GOOGLE = "google"
    BING = "bing"


class ResultType(Enum):
    URL = "url"
    INFORMATION = "information"
    CONTACT = "contact"
    SOCIAL_MEDIA = "social_media"


@dataclass
class SearchResult:
    """Represents a search result"""
    title: str
    url: str
    snippet: str
    result_type: ResultType
    confidence: float
    metadata: Dict[str, Any]


@dataclass
class SearchQuery:
    """Represents a search query"""
    query: str
    intent: str
    target_platform: Optional[str]
    search_type: str
    filters: Dict[str, Any]


class WebSearchIntegration(BaseComponent):
    """
    Integrates web search capabilities to find URLs and information automatically.
    
    Features:
    - Multiple search engine support
    - Intelligent query generation
    - Result filtering and ranking
    - Platform-specific URL detection
    - Cached results for performance
    """
    
    def __init__(self, config: Dict = None):
        super().__init__("web_search_integration", config)
        
        # Configuration
        self.default_search_engine = SearchEngine(config.get("default_search_engine", "duckduckgo")) if config else SearchEngine.DUCKDUCKGO
        self.max_results_per_query = config.get("max_results_per_query", 10) if config else 10
        self.cache_results = config.get("cache_results", True) if config else True
        self.user_agent = config.get("user_agent", "SmartWebBot/2.0 (Automated Browser)") if config else "SmartWebBot/2.0 (Automated Browser)"
        
        # Search engine configurations
        self.search_engines = {
            SearchEngine.DUCKDUCKGO: {
                "base_url": "https://api.duckduckgo.com/",
                "instant_answer_url": "https://api.duckduckgo.com/",
                "requires_api_key": False
            },
            SearchEngine.GOOGLE: {
                "base_url": "https://www.googleapis.com/customsearch/v1",
                "requires_api_key": True,
                "api_key": config.get("google_api_key") if config else None,
                "search_engine_id": config.get("google_search_engine_id") if config else None
            },
            SearchEngine.BING: {
                "base_url": "https://api.bing.microsoft.com/v7.0/search",
                "requires_api_key": True,
                "api_key": config.get("bing_api_key") if config else None
            }
        }
        
        # Caching
        self.search_cache: Dict[str, List[SearchResult]] = {}
        self.platform_url_cache: Dict[str, str] = {}
        
        # Known platforms and patterns
        self.platform_patterns = self._load_platform_patterns()
        self.common_platforms = self._load_common_platforms()
    
    def initialize(self) -> bool:
        """Initialize the web search integration"""
        try:
            self.logger.info("Initializing Web Search Integration...")
            
            # Validate search engine configuration
            engine_config = self.search_engines[self.default_search_engine]
            if engine_config["requires_api_key"] and not engine_config.get("api_key"):
                self.logger.warning(f"{self.default_search_engine.value} requires API key but none provided")
                # Fall back to DuckDuckGo if available
                if self.default_search_engine != SearchEngine.DUCKDUCKGO:
                    self.logger.info("Falling back to DuckDuckGo search")
                    self.default_search_engine = SearchEngine.DUCKDUCKGO
            
            self.is_initialized = True
            self.logger.info("Web Search Integration initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Web Search Integration: {e}")
            return False
    
    async def find_platform_url(self, platform_name: str, additional_context: str = None) -> Optional[Dict[str, Any]]:
        """
        Find the main URL for a platform (e.g., "Instagram" -> "https://www.instagram.com").
        
        Args:
            platform_name: Name of the platform
            additional_context: Additional context to help with search
            
        Returns:
            Dictionary with URL and metadata or None if not found
        """
        
        # Check cache first
        cache_key = platform_name.lower()
        if cache_key in self.platform_url_cache:
            return {
                "url": self.platform_url_cache[cache_key],
                "source": "cache",
                "confidence": 1.0
            }
        
        # Check known platforms
        if cache_key in self.common_platforms:
            url = self.common_platforms[cache_key]
            self.platform_url_cache[cache_key] = url
            return {
                "url": url,
                "source": "built_in",
                "confidence": 1.0
            }
        
        # Search for the platform
        search_query = f"{platform_name} official website login"
        if additional_context:
            search_query += f" {additional_context}"
        
        results = await self.search(search_query, result_type=ResultType.URL)
        
        # Find the most likely official URL
        official_url = self._find_official_platform_url(platform_name, results)
        
        if official_url:
            self.platform_url_cache[cache_key] = official_url["url"]
            return official_url
        
        return None
    
    async def search(self, 
                    query: str,
                    result_type: ResultType = ResultType.URL,
                    max_results: int = None) -> List[SearchResult]:
        """
        Perform a web search and return filtered results.
        
        Args:
            query: Search query
            result_type: Type of results to prioritize
            max_results: Maximum number of results to return
            
        Returns:
            List of SearchResult objects
        """
        
        max_results = max_results or self.max_results_per_query
        
        # Check cache
        cache_key = f"{query}_{result_type.value}_{max_results}"
        if self.cache_results and cache_key in self.search_cache:
            self.logger.info(f"Returning cached results for: {query}")
            return self.search_cache[cache_key]
        
        # Perform search based on configured engine
        if self.default_search_engine == SearchEngine.DUCKDUCKGO:
            results = await self._search_duckduckgo(query, max_results)
        elif self.default_search_engine == SearchEngine.GOOGLE:
            results = await self._search_google(query, max_results)
        elif self.default_search_engine == SearchEngine.BING:
            results = await self._search_bing(query, max_results)
        else:
            results = []
        
        # Filter and rank results based on type
        filtered_results = self._filter_and_rank_results(results, result_type)
        
        # Cache results
        if self.cache_results:
            self.search_cache[cache_key] = filtered_results
        
        self.logger.info(f"Found {len(filtered_results)} results for: {query}")
        return filtered_results
    
    async def _search_duckduckgo(self, query: str, max_results: int) -> List[SearchResult]:
        """Search using DuckDuckGo Instant Answer API"""
        
        try:
            async with aiohttp.ClientSession() as session:
                params = {
                    'q': query,
                    'format': 'json',
                    'no_html': '1',
                    'skip_disambig': '1'
                }
                
                async with session.get(
                    self.search_engines[SearchEngine.DUCKDUCKGO]["instant_answer_url"],
                    params=params,
                    headers={'User-Agent': self.user_agent}
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        return self._parse_duckduckgo_results(data, max_results)
                    else:
                        self.logger.error(f"DuckDuckGo search failed: {response.status}")
                        return []
        
        except Exception as e:
            self.logger.error(f"DuckDuckGo search error: {e}")
            return []
    
    async def _search_google(self, query: str, max_results: int) -> List[SearchResult]:
        """Search using Google Custom Search API"""
        
        config = self.search_engines[SearchEngine.GOOGLE]
        if not config.get("api_key") or not config.get("search_engine_id"):
            self.logger.error("Google search requires API key and search engine ID")
            return []
        
        try:
            async with aiohttp.ClientSession() as session:
                params = {
                    'key': config["api_key"],
                    'cx': config["search_engine_id"],
                    'q': query,
                    'num': min(max_results, 10)  # Google API max is 10
                }
                
                async with session.get(
                    config["base_url"],
                    params=params,
                    headers={'User-Agent': self.user_agent}
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        return self._parse_google_results(data, max_results)
                    else:
                        self.logger.error(f"Google search failed: {response.status}")
                        return []
        
        except Exception as e:
            self.logger.error(f"Google search error: {e}")
            return []
    
    async def _search_bing(self, query: str, max_results: int) -> List[SearchResult]:
        """Search using Bing Search API"""
        
        config = self.search_engines[SearchEngine.BING]
        if not config.get("api_key"):
            self.logger.error("Bing search requires API key")
            return []
        
        try:
            async with aiohttp.ClientSession() as session:
                params = {
                    'q': query,
                    'count': max_results,
                    'mkt': 'en-US'
                }
                
                headers = {
                    'Ocp-Apim-Subscription-Key': config["api_key"],
                    'User-Agent': self.user_agent
                }
                
                async with session.get(
                    config["base_url"],
                    params=params,
                    headers=headers
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        return self._parse_bing_results(data, max_results)
                    else:
                        self.logger.error(f"Bing search failed: {response.status}")
                        return []
        
        except Exception as e:
            self.logger.error(f"Bing search error: {e}")
            return []
    
    def _parse_duckduckgo_results(self, data: Dict, max_results: int) -> List[SearchResult]:
        """Parse DuckDuckGo API response"""
        
        results = []
        
        # Parse instant answer
        if data.get('AbstractText') and data.get('AbstractURL'):
            results.append(SearchResult(
                title=data.get('Heading', 'Instant Answer'),
                url=data['AbstractURL'],
                snippet=data['AbstractText'],
                result_type=ResultType.INFORMATION,
                confidence=0.9,
                metadata={'source': 'instant_answer'}
            ))
        
        # Parse related topics
        for topic in data.get('RelatedTopics', [])[:max_results]:
            if isinstance(topic, dict) and topic.get('FirstURL'):
                results.append(SearchResult(
                    title=topic.get('Text', '').split(' - ')[0] if ' - ' in topic.get('Text', '') else topic.get('Text', ''),
                    url=topic['FirstURL'],
                    snippet=topic.get('Text', ''),
                    result_type=ResultType.URL,
                    confidence=0.7,
                    metadata={'source': 'related_topic'}
                ))
        
        return results[:max_results]
    
    def _parse_google_results(self, data: Dict, max_results: int) -> List[SearchResult]:
        """Parse Google Custom Search API response"""
        
        results = []
        
        for item in data.get('items', [])[:max_results]:
            results.append(SearchResult(
                title=item.get('title', ''),
                url=item.get('link', ''),
                snippet=item.get('snippet', ''),
                result_type=ResultType.URL,
                confidence=0.8,
                metadata={'source': 'google_search'}
            ))
        
        return results
    
    def _parse_bing_results(self, data: Dict, max_results: int) -> List[SearchResult]:
        """Parse Bing Search API response"""
        
        results = []
        
        for item in data.get('webPages', {}).get('value', [])[:max_results]:
            results.append(SearchResult(
                title=item.get('name', ''),
                url=item.get('url', ''),
                snippet=item.get('snippet', ''),
                result_type=ResultType.URL,
                confidence=0.8,
                metadata={'source': 'bing_search'}
            ))
        
        return results
    
    def _filter_and_rank_results(self, results: List[SearchResult], preferred_type: ResultType) -> List[SearchResult]:
        """Filter and rank results based on relevance and type"""
        
        # Boost results that match preferred type
        for result in results:
            if result.result_type == preferred_type:
                result.confidence += 0.1
        
        # Sort by confidence
        results.sort(key=lambda x: x.confidence, reverse=True)
        
        return results
    
    def _find_official_platform_url(self, platform_name: str, results: List[SearchResult]) -> Optional[Dict[str, Any]]:
        """Find the most likely official URL for a platform from search results"""
        
        platform_lower = platform_name.lower()
        
        for result in results:
            url_lower = result.url.lower()
            domain = urlparse(result.url).netloc.lower()
            
            # Check if domain contains platform name
            if platform_lower in domain:
                # Prefer exact matches or www versions
                if domain == f"{platform_lower}.com" or domain == f"www.{platform_lower}.com":
                    return {
                        "url": result.url,
                        "source": "search",
                        "confidence": 0.95,
                        "title": result.title
                    }
                elif platform_lower in domain:
                    return {
                        "url": result.url,
                        "source": "search",
                        "confidence": 0.8,
                        "title": result.title
                    }
        
        # If no domain match, look for platform name in title or snippet
        for result in results:
            title_lower = result.title.lower()
            snippet_lower = result.snippet.lower()
            
            if (platform_lower in title_lower and 
                any(keyword in title_lower for keyword in ['official', 'login', 'sign in', 'home'])):
                return {
                    "url": result.url,
                    "source": "search",
                    "confidence": 0.7,
                    "title": result.title
                }
        
        return None
    
    def _load_platform_patterns(self) -> Dict[str, List[str]]:
        """Load patterns for identifying platform URLs"""
        
        return {
            "social_media": [
                r".*\.(com|net|org)/(login|signin|auth)",
                r".*(facebook|instagram|twitter|linkedin|tiktok|youtube).*",
                r".*social.*"
            ],
            "business": [
                r".*\.(com|net|org)/(business|enterprise|corporate)",
                r".*(crm|erp|dashboard|admin).*"
            ],
            "ecommerce": [
                r".*\.(com|net|org)/(shop|store|cart|checkout)",
                r".*(amazon|ebay|shopify|woocommerce).*"
            ]
        }
    
    def _load_common_platforms(self) -> Dict[str, str]:
        """Load common platform URLs"""
        
        return {
            "instagram": "https://www.instagram.com",
            "facebook": "https://www.facebook.com",
            "twitter": "https://twitter.com",
            "x": "https://x.com",
            "linkedin": "https://www.linkedin.com",
            "youtube": "https://www.youtube.com",
            "tiktok": "https://www.tiktok.com",
            "snapchat": "https://www.snapchat.com",
            "pinterest": "https://www.pinterest.com",
            "reddit": "https://www.reddit.com",
            "discord": "https://discord.com",
            "slack": "https://slack.com",
            "zoom": "https://zoom.us",
            "teams": "https://teams.microsoft.com",
            "gmail": "https://mail.google.com",
            "outlook": "https://outlook.live.com",
            "amazon": "https://www.amazon.com",
            "ebay": "https://www.ebay.com",
            "paypal": "https://www.paypal.com",
            "stripe": "https://dashboard.stripe.com",
            "shopify": "https://www.shopify.com",
            "wordpress": "https://wordpress.com",
            "github": "https://github.com",
            "gitlab": "https://gitlab.com",
            "plus": "https://plus.reconext.com",
            "reconext": "https://plus.reconext.com"
        }
    
    async def search_for_information(self, query: str, information_type: str = "general") -> List[Dict[str, Any]]:
        """
        Search for specific information to help with task completion.
        
        Args:
            query: Information to search for
            information_type: Type of information (contact, address, hours, etc.)
            
        Returns:
            List of information results
        """
        
        # Enhance query based on information type
        enhanced_query = self._enhance_information_query(query, information_type)
        
        results = await self.search(enhanced_query, result_type=ResultType.INFORMATION)
        
        # Extract relevant information from results
        information_results = []
        for result in results:
            info = {
                "source_url": result.url,
                "source_title": result.title,
                "information": result.snippet,
                "confidence": result.confidence,
                "type": information_type
            }
            information_results.append(info)
        
        return information_results
    
    def _enhance_information_query(self, query: str, information_type: str) -> str:
        """Enhance search query based on information type"""
        
        enhancements = {
            "contact": "contact information phone email",
            "address": "address location where",
            "hours": "hours open closed schedule",
            "pricing": "price cost pricing plans",
            "features": "features capabilities what does",
            "tutorial": "how to guide tutorial instructions",
            "login": "login sign in access account"
        }
        
        enhancement = enhancements.get(information_type, "")
        return f"{query} {enhancement}".strip()
    
    def clear_cache(self):
        """Clear all cached search results"""
        self.search_cache.clear()
        self.platform_url_cache.clear()
        self.logger.info("Search cache cleared")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return {
            "search_cache_size": len(self.search_cache),
            "platform_url_cache_size": len(self.platform_url_cache),
            "default_search_engine": self.default_search_engine.value
        }
    
    def cleanup(self) -> bool:
        """Clean up resources"""
        try:
            self.clear_cache()
            self.logger.info("Web Search Integration cleanup completed")
            return True
        except Exception as e:
            self.logger.error(f"Cleanup error: {e}")
            return False
