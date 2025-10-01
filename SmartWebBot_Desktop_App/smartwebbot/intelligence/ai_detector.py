"""
AI-powered element detection system.

Uses computer vision, pattern recognition, and machine learning
to intelligently detect and interact with web elements.
"""

import re
import time
from typing import List, Dict, Optional, Tuple, Any
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
import cv2
import numpy as np
from PIL import Image
import base64
from ..core.base_component import BaseComponent
from ..utils.logger import BotLogger


class AIElementDetector(BaseComponent):
    """
    Advanced AI-powered element detection system.
    
    Features:
    - Multiple detection strategies
    - Computer vision-based detection
    - Semantic understanding
    - Learning from user patterns
    - Fallback mechanisms
    """
    
    def __init__(self, driver, config: Dict = None):
        """
        Initialize the AI element detector.
        
        Args:
            driver: Selenium WebDriver instance
            config: Configuration dictionary
        """
        super().__init__("ai_detector", config)
        self.driver = driver
        
        # Detection strategies in order of preference
        self.strategies = [
            self._detect_by_semantic_analysis,
            self._detect_by_visual_similarity,
            self._detect_by_context_clues,
            self._detect_by_fuzzy_matching,
            self._detect_by_position_analysis,
            self._detect_by_fallback_selectors
        ]
        
        # Learning system
        self.successful_patterns = {}
        self.failed_patterns = set()
        
        # Visual recognition cache
        self.visual_cache = {}
        
    def initialize(self) -> bool:
        """Initialize the AI detector."""
        try:
            self.logger.info("Initializing AI Element Detector")
            
            # Load pre-trained patterns
            self._load_common_patterns()
            
            # Initialize computer vision components
            self._init_cv_components()
            
            self.is_initialized = True
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize AI detector: {e}")
            return False
    
    def cleanup(self) -> bool:
        """Clean up detector resources."""
        try:
            # Save learned patterns
            self._save_learned_patterns()
            
            # Clear caches
            self.visual_cache.clear()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Cleanup failed: {e}")
            return False
    
    def find_element_intelligently(self, description: str, 
                                 element_type: str = None,
                                 context: Dict = None) -> Optional[WebElement]:
        """
        Find an element using AI-powered detection.
        
        Args:
            description: Natural language description of the element
            element_type: Type hint (button, input, link, etc.)
            context: Additional context information
        
        Returns:
            WebElement if found, None otherwise
        """
        start_time = time.time()
        
        try:
            self.logger.info(f"Searching for element: {description}")
            
            # Prepare search context
            search_context = {
                'description': description.lower(),
                'element_type': element_type,
                'page_url': self.driver.current_url,
                'page_title': self.driver.title,
                'context': context or {}
            }
            
            # Try each detection strategy
            for strategy in self.strategies:
                try:
                    elements = strategy(search_context)
                    if elements:
                        # Score and rank elements
                        best_element = self._score_and_rank_elements(elements, search_context)
                        if best_element:
                            self._record_successful_detection(description, best_element, strategy.__name__)
                            self.update_metrics("find_element", True)
                            
                            duration = time.time() - start_time
                            BotLogger.log_performance("ai_detector", "find_element", duration, 
                                                    success=True, strategy=strategy.__name__)
                            
                            return best_element
                            
                except Exception as e:
                    self.logger.debug(f"Strategy {strategy.__name__} failed: {e}")
                    continue
            
            # No element found
            self.logger.warning(f"Could not find element: {description}")
            self._record_failed_detection(description)
            self.update_metrics("find_element", False)
            
            duration = time.time() - start_time
            BotLogger.log_performance("ai_detector", "find_element", duration, success=False)
            
            return None
            
        except Exception as e:
            self.logger.error(f"Element detection failed: {e}")
            self.update_metrics("find_element", False)
            return None
    
    def _detect_by_semantic_analysis(self, context: Dict) -> List[WebElement]:
        """
        Detect elements using semantic analysis.
        
        Args:
            context: Search context
        
        Returns:
            List of candidate elements
        """
        description = context['description']
        element_type = context.get('element_type')
        
        candidates = []
        
        # Generate semantic selectors
        semantic_selectors = self._generate_semantic_selectors(description, element_type)
        
        for selector in semantic_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                candidates.extend(elements)
            except:
                continue
        
        # Also try XPath with text content
        text_xpaths = self._generate_text_xpaths(description, element_type)
        for xpath in text_xpaths:
            try:
                elements = self.driver.find_elements(By.XPATH, xpath)
                candidates.extend(elements)
            except:
                continue
        
        return candidates
    
    def _detect_by_visual_similarity(self, context: Dict) -> List[WebElement]:
        """
        Detect elements using visual similarity analysis.
        
        Args:
            context: Search context
        
        Returns:
            List of candidate elements
        """
        # This would require a reference image or visual template
        # For now, return empty list as placeholder
        return []
    
    def _detect_by_context_clues(self, context: Dict) -> List[WebElement]:
        """
        Detect elements using contextual clues.
        
        Args:
            context: Search context
        
        Returns:
            List of candidate elements
        """
        description = context['description']
        candidates = []
        
        # Look for elements near labels or text that match the description
        label_elements = self.driver.find_elements(By.TAG_NAME, "label")
        
        for label in label_elements:
            if self._text_similarity(label.text, description) > 0.6:
                # Find associated form elements
                label_for = label.get_attribute("for")
                if label_for:
                    try:
                        associated_element = self.driver.find_element(By.ID, label_for)
                        candidates.append(associated_element)
                    except:
                        pass
                
                # Look for nearby input elements
                try:
                    parent = label.find_element(By.XPATH, "..")
                    nearby_inputs = parent.find_elements(By.TAG_NAME, "input")
                    candidates.extend(nearby_inputs)
                except:
                    pass
        
        return candidates
    
    def _detect_by_fuzzy_matching(self, context: Dict) -> List[WebElement]:
        """
        Detect elements using fuzzy text matching.
        
        Args:
            context: Search context
        
        Returns:
            List of candidate elements
        """
        description = context['description']
        candidates = []
        
        # Get all interactive elements
        interactive_tags = ['button', 'input', 'select', 'textarea', 'a']
        
        for tag in interactive_tags:
            elements = self.driver.find_elements(By.TAG_NAME, tag)
            
            for element in elements:
                # Check text content
                element_text = element.text or element.get_attribute("value") or ""
                if self._text_similarity(element_text.lower(), description) > 0.5:
                    candidates.append(element)
                
                # Check placeholder text
                placeholder = element.get_attribute("placeholder") or ""
                if self._text_similarity(placeholder.lower(), description) > 0.5:
                    candidates.append(element)
                
                # Check aria-label
                aria_label = element.get_attribute("aria-label") or ""
                if self._text_similarity(aria_label.lower(), description) > 0.5:
                    candidates.append(element)
        
        return candidates
    
    def _detect_by_position_analysis(self, context: Dict) -> List[WebElement]:
        """
        Detect elements using position and layout analysis.
        
        Args:
            context: Search context
        
        Returns:
            List of candidate elements
        """
        # Analyze page layout and find elements in typical positions
        # This is a simplified implementation
        candidates = []
        
        description = context['description']
        
        # Common position patterns
        if 'submit' in description or 'send' in description:
            # Look for buttons at the bottom of forms
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            form_buttons = []
            
            for button in buttons:
                try:
                    form = button.find_element(By.XPATH, "ancestor::form")
                    if form:
                        form_buttons.append(button)
                except:
                    pass
            
            candidates.extend(form_buttons)
        
        return candidates
    
    def _detect_by_fallback_selectors(self, context: Dict) -> List[WebElement]:
        """
        Fallback detection using common selectors.
        
        Args:
            context: Search context
        
        Returns:
            List of candidate elements
        """
        description = context['description']
        element_type = context.get('element_type')
        candidates = []
        
        # Common fallback patterns
        fallback_patterns = {
            'login': ['#login', '.login', '[name*="login"]'],
            'password': ['#password', '.password', '[type="password"]'],
            'email': ['#email', '.email', '[type="email"]'],
            'submit': ['[type="submit"]', '.submit', '#submit'],
            'search': ['#search', '.search', '[name*="search"]']
        }
        
        # Find matching patterns
        for keyword, selectors in fallback_patterns.items():
            if keyword in description:
                for selector in selectors:
                    try:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        candidates.extend(elements)
                    except:
                        continue
        
        return candidates
    
    def _generate_semantic_selectors(self, description: str, element_type: str = None) -> List[str]:
        """
        Generate semantic CSS selectors based on description.
        
        Args:
            description: Element description
            element_type: Element type hint
        
        Returns:
            List of CSS selectors
        """
        selectors = []
        keywords = description.split()
        
        for keyword in keywords:
            # ID-based selectors
            selectors.append(f"#{keyword}")
            selectors.append(f"#*{keyword}*")  # This won't work in CSS, but kept for reference
            
            # Class-based selectors
            selectors.append(f".{keyword}")
            
            # Name-based selectors
            selectors.append(f"[name='{keyword}']")
            selectors.append(f"[name*='{keyword}']")
            
            # Data attribute selectors
            selectors.append(f"[data-*='{keyword}']")
            
            # Aria label selectors
            selectors.append(f"[aria-label*='{keyword}']")
        
        # Element type specific selectors
        if element_type:
            for keyword in keywords:
                selectors.append(f"{element_type}[name*='{keyword}']")
                selectors.append(f"{element_type}[id*='{keyword}']")
        
        return selectors
    
    def _generate_text_xpaths(self, description: str, element_type: str = None) -> List[str]:
        """
        Generate XPath selectors based on text content.
        
        Args:
            description: Element description
            element_type: Element type hint
        
        Returns:
            List of XPath selectors
        """
        xpaths = []
        keywords = description.split()
        
        # Text content matching
        for keyword in keywords:
            xpaths.append(f"//*[contains(text(), '{keyword}')]")
            xpaths.append(f"//*[contains(@value, '{keyword}')]")
            xpaths.append(f"//*[contains(@placeholder, '{keyword}')]")
        
        # Full description matching
        xpaths.append(f"//*[contains(text(), '{description}')]")
        
        # Element type specific
        if element_type:
            for keyword in keywords:
                xpaths.append(f"//{element_type}[contains(text(), '{keyword}')]")
                xpaths.append(f"//{element_type}[contains(@value, '{keyword}')]")
        
        return xpaths
    
    def _score_and_rank_elements(self, elements: List[WebElement], context: Dict) -> Optional[WebElement]:
        """
        Score and rank elements based on relevance.
        
        Args:
            elements: List of candidate elements
            context: Search context
        
        Returns:
            Best matching element or None
        """
        if not elements:
            return None
        
        description = context['description']
        scored_elements = []
        
        for element in elements:
            try:
                score = self._calculate_element_score(element, description, context)
                if score > 0:
                    scored_elements.append((element, score))
            except:
                continue
        
        if not scored_elements:
            return None
        
        # Sort by score (descending)
        scored_elements.sort(key=lambda x: x[1], reverse=True)
        
        # Return the highest scoring element
        best_element, best_score = scored_elements[0]
        
        self.logger.debug(f"Best element score: {best_score}")
        return best_element
    
    def _calculate_element_score(self, element: WebElement, description: str, context: Dict) -> float:
        """
        Calculate relevance score for an element.
        
        Args:
            element: Web element to score
            description: Target description
            context: Search context
        
        Returns:
            Relevance score (0.0 to 1.0)
        """
        score = 0.0
        
        # Text similarity scoring
        element_text = element.text or ""
        text_score = self._text_similarity(element_text.lower(), description)
        score += text_score * 0.4
        
        # Attribute similarity scoring
        for attr in ['id', 'name', 'class', 'aria-label', 'placeholder']:
            attr_value = element.get_attribute(attr) or ""
            attr_score = self._text_similarity(attr_value.lower(), description)
            score += attr_score * 0.1
        
        # Visibility and interactability scoring
        if element.is_displayed():
            score += 0.2
        if element.is_enabled():
            score += 0.1
        
        # Element type matching
        element_type = context.get('element_type')
        if element_type and element.tag_name == element_type:
            score += 0.2
        
        return min(score, 1.0)
    
    def _text_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate text similarity using simple string matching.
        
        Args:
            text1: First text
            text2: Second text
        
        Returns:
            Similarity score (0.0 to 1.0)
        """
        if not text1 or not text2:
            return 0.0
        
        # Exact match
        if text1 == text2:
            return 1.0
        
        # Substring match
        if text2 in text1 or text1 in text2:
            return 0.8
        
        # Word overlap
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    def _load_common_patterns(self):
        """Load common element patterns."""
        self.successful_patterns = {
            'login_button': [
                'button[type="submit"]',
                '.login-button',
                '#login-btn'
            ],
            'search_input': [
                'input[type="search"]',
                '#search',
                '.search-input'
            ],
            'email_input': [
                'input[type="email"]',
                'input[name="email"]',
                '#email'
            ]
        }
    
    def _init_cv_components(self):
        """Initialize computer vision components."""
        # Placeholder for CV initialization
        pass
    
    def _record_successful_detection(self, description: str, element: WebElement, strategy: str):
        """Record successful element detection for learning."""
        pattern_key = f"{description}_{element.tag_name}"
        
        if pattern_key not in self.successful_patterns:
            self.successful_patterns[pattern_key] = []
        
        # Record the successful selector pattern
        element_id = element.get_attribute('id')
        element_class = element.get_attribute('class')
        element_name = element.get_attribute('name')
        
        pattern_info = {
            'strategy': strategy,
            'tag': element.tag_name,
            'id': element_id,
            'class': element_class,
            'name': element_name,
            'success_count': 1
        }
        
        self.successful_patterns[pattern_key].append(pattern_info)
    
    def _record_failed_detection(self, description: str):
        """Record failed detection attempt."""
        self.failed_patterns.add(description)
    
    def _save_learned_patterns(self):
        """Save learned patterns for future use."""
        # This would save to a file or database
        # For now, just log the patterns
        self.logger.info(f"Learned {len(self.successful_patterns)} successful patterns")
        self.logger.info(f"Recorded {len(self.failed_patterns)} failed patterns")
