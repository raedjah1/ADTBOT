"""
Comprehensive Website Analyzer - The Revolutionary Brain

Performs deep website analysis to understand structure, functionality,
and all possible automation opportunities with AI-powered intelligence.
"""

import asyncio
import time
import json
from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlparse
from ..core.base_chat_component import BaseChatComponent


class ElementType(Enum):
    """Types of interactive elements discovered."""
    BUTTON = "button"
    LINK = "link"
    INPUT_FIELD = "input_field"
    DROPDOWN = "dropdown"
    CHECKBOX = "checkbox"
    RADIO_BUTTON = "radio_button"
    FORM = "form"
    MODAL = "modal"
    MENU = "menu"
    TAB = "tab"
    SLIDER = "slider"
    UPLOAD = "file_upload"
    SEARCH_BOX = "search_box"
    LOGIN_FORM = "login_form"
    SHOPPING_CART = "shopping_cart"
    PAGINATION = "pagination"


class ActionType(Enum):
    """Types of actions that can be performed."""
    CLICK = "click"
    TYPE = "type"
    SELECT = "select"
    HOVER = "hover"
    SCROLL = "scroll"
    SUBMIT = "submit"
    NAVIGATE = "navigate"
    UPLOAD = "upload"
    DOWNLOAD = "download"
    LOGIN = "login"
    SEARCH = "search"
    ADD_TO_CART = "add_to_cart"
    CHECKOUT = "checkout"
    FILTER = "filter"
    SORT = "sort"


@dataclass
class DiscoveredElement:
    """Represents a discovered interactive element."""
    element_id: str
    element_type: ElementType
    tag_name: str
    selector: str
    xpath: str
    text_content: str
    attributes: Dict[str, str]
    position: Tuple[int, int]
    size: Tuple[int, int]
    is_visible: bool
    is_enabled: bool
    parent_context: str
    children_count: int
    action_types: List[ActionType]
    confidence_score: float
    ai_description: str


@dataclass
class DiscoveredWorkflow:
    """Represents a discovered workflow pattern."""
    workflow_id: str
    name: str
    description: str
    steps: List[Dict[str, Any]]
    category: str
    complexity: int
    success_indicators: List[str]
    prerequisites: List[str]
    estimated_time: int
    confidence_score: float


@dataclass
class WebsiteInvestigationResult:
    """Complete website investigation results."""
    url: str
    domain: str
    title: str
    description: str
    investigation_timestamp: float
    page_structure: Dict[str, Any]
    discovered_elements: List[DiscoveredElement]
    discovered_workflows: List[DiscoveredWorkflow]
    navigation_patterns: Dict[str, List[str]]
    form_patterns: List[Dict[str, Any]]
    authentication_methods: List[Dict[str, Any]]
    e_commerce_features: List[Dict[str, Any]]
    search_capabilities: Dict[str, Any]
    social_features: List[Dict[str, Any]]
    performance_metrics: Dict[str, float]
    accessibility_info: Dict[str, Any]
    technology_stack: List[str]
    api_endpoints: List[str]
    security_features: List[str]
    mobile_compatibility: Dict[str, Any]
    ai_insights: List[str]
    natural_language_commands: List[Dict[str, Any]]


class ComprehensiveWebsiteAnalyzer(BaseChatComponent):
    """
    Revolutionary website analyzer that discovers everything.
    
    Features:
    - Deep DOM analysis with AI enhancement
    - Interactive element discovery and classification
    - Workflow pattern recognition
    - Natural language command generation
    - Performance and accessibility analysis
    - Technology stack detection
    - API endpoint discovery
    - Security feature analysis
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("comprehensive_website_analyzer", config)
        
        # Analysis configuration
        self.max_depth = self.get_config_value("max_depth", 10)
        self.timeout = self.get_config_value("timeout", 30)
        self.enable_ai_analysis = self.get_config_value("enable_ai_analysis", True)
        self.enable_deep_scan = self.get_config_value("enable_deep_scan", True)
        
        # Browser setup
        self.driver = None
        self.wait = None
        
        # Analysis results cache
        self.investigation_cache: Dict[str, WebsiteInvestigationResult] = {}
    
    def initialize(self) -> bool:
        """Initialize the website analyzer."""
        try:
            self.logger.info("Initializing Comprehensive Website Analyzer...")
            
            # Setup browser options for analysis
            self._setup_browser_options()
            
            self.is_initialized = True
            self.is_healthy = True
            
            self.logger.info("Comprehensive Website Analyzer initialized successfully")
            return True
            
        except Exception as e:
            self.log_error(e, "Website analyzer initialization")
            return False
    
    async def investigate_website(self, url: str, deep_analysis: bool = True) -> WebsiteInvestigationResult:
        """
        Perform comprehensive website investigation.
        
        This is the main method that performs the revolutionary analysis.
        """
        start_time = time.time()
        
        try:
            self.logger.info(f"🔍 Starting comprehensive investigation of: {url}")
            
            # Check cache first
            domain = urlparse(url).netloc
            cache_key = f"{domain}_{deep_analysis}"
            
            if cache_key in self.investigation_cache:
                cached_result = self.investigation_cache[cache_key]
                if time.time() - cached_result.investigation_timestamp < 3600:  # 1 hour cache
                    self.logger.info(f"Returning cached investigation for: {url}")
                    return cached_result
            
            # Initialize browser
            await self._initialize_browser()
            
            # Phase 1: Basic page analysis
            self.logger.info("Phase 1: Basic page analysis...")
            basic_info = await self._analyze_basic_page_info(url)
            
            # Phase 2: DOM structure analysis
            self.logger.info("Phase 2: DOM structure analysis...")
            page_structure = await self._analyze_page_structure()
            
            # Phase 3: Interactive element discovery
            self.logger.info("Phase 3: Interactive element discovery...")
            discovered_elements = await self._discover_interactive_elements()
            
            # Phase 4: Workflow pattern recognition
            self.logger.info("Phase 4: Workflow pattern recognition...")
            discovered_workflows = await self._discover_workflow_patterns(discovered_elements)
            
            # Phase 5: Navigation pattern analysis
            self.logger.info("Phase 5: Navigation pattern analysis...")
            navigation_patterns = await self._analyze_navigation_patterns()
            
            # Phase 6: Form analysis
            self.logger.info("Phase 6: Form analysis...")
            form_patterns = await self._analyze_forms()
            
            # Phase 7: Authentication method detection
            self.logger.info("Phase 7: Authentication analysis...")
            auth_methods = await self._detect_authentication_methods()
            
            # Phase 8: E-commerce feature detection
            self.logger.info("Phase 8: E-commerce analysis...")
            ecommerce_features = await self._detect_ecommerce_features()
            
            # Phase 9: Search capability analysis
            self.logger.info("Phase 9: Search capability analysis...")
            search_capabilities = await self._analyze_search_capabilities()
            
            # Phase 10: Technology stack detection
            self.logger.info("Phase 10: Technology stack detection...")
            tech_stack = await self._detect_technology_stack()
            
            # Phase 11: API endpoint discovery
            self.logger.info("Phase 11: API endpoint discovery...")
            api_endpoints = await self._discover_api_endpoints()
            
            # Phase 12: Performance analysis
            self.logger.info("Phase 12: Performance analysis...")
            performance_metrics = await self._analyze_performance()
            
            # Phase 13: AI-powered insights
            self.logger.info("Phase 13: AI-powered insights generation...")
            ai_insights = await self._generate_ai_insights(discovered_elements, discovered_workflows)
            
            # Phase 14: Natural language command generation
            self.logger.info("Phase 14: Natural language command generation...")
            nl_commands = await self._generate_natural_language_commands(discovered_workflows)
            
            # Create comprehensive investigation result
            investigation_result = WebsiteInvestigationResult(
                url=url,
                domain=domain,
                title=basic_info.get("title", ""),
                description=basic_info.get("description", ""),
                investigation_timestamp=time.time(),
                page_structure=page_structure,
                discovered_elements=discovered_elements,
                discovered_workflows=discovered_workflows,
                navigation_patterns=navigation_patterns,
                form_patterns=form_patterns,
                authentication_methods=auth_methods,
                e_commerce_features=ecommerce_features,
                search_capabilities=search_capabilities,
                social_features=await self._detect_social_features(),
                performance_metrics=performance_metrics,
                accessibility_info=await self._analyze_accessibility(),
                technology_stack=tech_stack,
                api_endpoints=api_endpoints,
                security_features=await self._detect_security_features(),
                mobile_compatibility=await self._analyze_mobile_compatibility(),
                ai_insights=ai_insights,
                natural_language_commands=nl_commands
            )
            
            # Cache the result
            self.investigation_cache[cache_key] = investigation_result
            
            investigation_time = time.time() - start_time
            self.logger.info(f"✅ Website investigation completed in {investigation_time:.2f}s")
            self.logger.info(f"Discovered {len(discovered_elements)} elements and {len(discovered_workflows)} workflows")
            
            return investigation_result
            
        except Exception as e:
            self.log_error(e, f"Website investigation failed for: {url}")
            raise
        
        finally:
            if self.driver:
                await self._cleanup_browser()
    
    async def _initialize_browser(self) -> None:
        """Initialize browser for analysis."""
        try:
            from selenium.webdriver.chrome.options import Options
            
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
            
            self.driver = webdriver.Chrome(options=options)
            self.wait = WebDriverWait(self.driver, self.timeout)
            
        except Exception as e:
            self.log_error(e, "Browser initialization failed")
            raise
    
    async def _analyze_basic_page_info(self, url: str) -> Dict[str, Any]:
        """Analyze basic page information."""
        try:
            self.driver.get(url)
            await asyncio.sleep(2)  # Wait for page load
            
            basic_info = {
                "title": self.driver.title,
                "description": "",
                "keywords": "",
                "canonical_url": url,
                "language": "",
                "viewport": ""
            }
            
            # Extract meta information
            try:
                description_element = self.driver.find_element(By.CSS_SELECTOR, 'meta[name="description"]')
                basic_info["description"] = description_element.get_attribute("content") or ""
            except NoSuchElementException:
                pass
            
            try:
                keywords_element = self.driver.find_element(By.CSS_SELECTOR, 'meta[name="keywords"]')
                basic_info["keywords"] = keywords_element.get_attribute("content") or ""
            except NoSuchElementException:
                pass
            
            return basic_info
            
        except Exception as e:
            self.log_error(e, f"Basic page analysis failed for: {url}")
            return {}
    
    async def _analyze_page_structure(self) -> Dict[str, Any]:
        """Analyze the page structure and hierarchy."""
        try:
            # Get page source and parse with BeautifulSoup
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            structure = {
                "html_structure": self._build_dom_tree(soup),
                "semantic_sections": self._identify_semantic_sections(soup),
                "layout_type": self._detect_layout_type(soup),
                "responsive_breakpoints": self._detect_responsive_breakpoints(),
                "component_hierarchy": self._analyze_component_hierarchy(soup)
            }
            
            return structure
            
        except Exception as e:
            self.log_error(e, "Page structure analysis failed")
            return {}
    
    async def _discover_interactive_elements(self) -> List[DiscoveredElement]:
        """Discover and classify all interactive elements."""
        try:
            discovered_elements = []
            element_counter = 0
            
            # Define selectors for different element types
            element_selectors = {
                ElementType.BUTTON: [
                    "button", "input[type='button']", "input[type='submit']", 
                    "[role='button']", ".btn", ".button"
                ],
                ElementType.LINK: ["a[href]", "[role='link']"],
                ElementType.INPUT_FIELD: [
                    "input[type='text']", "input[type='email']", "input[type='password']",
                    "input[type='number']", "input[type='tel']", "textarea"
                ],
                ElementType.DROPDOWN: ["select", "[role='listbox']", "[role='combobox']"],
                ElementType.CHECKBOX: ["input[type='checkbox']"],
                ElementType.RADIO_BUTTON: ["input[type='radio']"],
                ElementType.FORM: ["form"],
                ElementType.SEARCH_BOX: ["input[type='search']", "[role='searchbox']"],
                ElementType.UPLOAD: ["input[type='file']"],
                ElementType.SLIDER: ["input[type='range']", "[role='slider']"]
            }
            
            for element_type, selectors in element_selectors.items():
                for selector in selectors:
                    try:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        
                        for element in elements:
                            try:
                                # Skip hidden or non-interactive elements
                                if not element.is_displayed():
                                    continue
                                
                                discovered_element = await self._analyze_element(
                                    element, element_type, element_counter
                                )
                                
                                if discovered_element:
                                    discovered_elements.append(discovered_element)
                                    element_counter += 1
                                
                            except Exception as e:
                                continue  # Skip problematic elements
                                
                    except Exception as e:
                        continue  # Skip problematic selectors
            
            # Sort by confidence score
            discovered_elements.sort(key=lambda x: x.confidence_score, reverse=True)
            
            return discovered_elements
            
        except Exception as e:
            self.log_error(e, "Interactive element discovery failed")
            return []
    
    async def _analyze_element(self, element, element_type: ElementType, element_id: int) -> Optional[DiscoveredElement]:
        """Analyze individual element in detail."""
        try:
            # Get element properties
            tag_name = element.tag_name
            text_content = element.text.strip()[:200]  # Limit text length
            
            # Generate selectors
            css_selector = self._generate_css_selector(element)
            xpath = self._generate_xpath(element)
            
            # Get attributes
            attributes = {}
            for attr in ['id', 'class', 'name', 'type', 'role', 'aria-label', 'title', 'placeholder']:
                value = element.get_attribute(attr)
                if value:
                    attributes[attr] = value
            
            # Get position and size
            location = element.location
            size = element.size
            
            # Determine possible actions
            action_types = self._determine_element_actions(element, element_type)
            
            # Calculate confidence score
            confidence_score = self._calculate_element_confidence(
                element, element_type, text_content, attributes
            )
            
            # Generate AI description
            ai_description = await self._generate_element_ai_description(
                element_type, text_content, attributes
            )
            
            return DiscoveredElement(
                element_id=f"element_{element_id}",
                element_type=element_type,
                tag_name=tag_name,
                selector=css_selector,
                xpath=xpath,
                text_content=text_content,
                attributes=attributes,
                position=(location['x'], location['y']),
                size=(size['width'], size['height']),
                is_visible=element.is_displayed(),
                is_enabled=element.is_enabled(),
                parent_context=self._get_parent_context(element),
                children_count=len(element.find_elements(By.XPATH, "./*")),
                action_types=action_types,
                confidence_score=confidence_score,
                ai_description=ai_description
            )
            
        except Exception as e:
            return None
    
    async def _discover_workflow_patterns(self, elements: List[DiscoveredElement]) -> List[DiscoveredWorkflow]:
        """Discover common workflow patterns from elements."""
        try:
            workflows = []
            workflow_id = 0
            
            # Login workflow detection
            login_workflow = await self._detect_login_workflow(elements)
            if login_workflow:
                login_workflow.workflow_id = f"workflow_{workflow_id}"
                workflows.append(login_workflow)
                workflow_id += 1
            
            # Search workflow detection
            search_workflow = await self._detect_search_workflow(elements)
            if search_workflow:
                search_workflow.workflow_id = f"workflow_{workflow_id}"
                workflows.append(search_workflow)
                workflow_id += 1
            
            # Form submission workflows
            form_workflows = await self._detect_form_workflows(elements)
            for workflow in form_workflows:
                workflow.workflow_id = f"workflow_{workflow_id}"
                workflows.append(workflow)
                workflow_id += 1
            
            # E-commerce workflows
            ecommerce_workflows = await self._detect_ecommerce_workflows(elements)
            for workflow in ecommerce_workflows:
                workflow.workflow_id = f"workflow_{workflow_id}"
                workflows.append(workflow)
                workflow_id += 1
            
            # Navigation workflows
            nav_workflows = await self._detect_navigation_workflows(elements)
            for workflow in nav_workflows:
                workflow.workflow_id = f"workflow_{workflow_id}"
                workflows.append(workflow)
                workflow_id += 1
            
            return workflows
            
        except Exception as e:
            self.log_error(e, "Workflow pattern discovery failed")
            return []
    
    async def _detect_login_workflow(self, elements: List[DiscoveredElement]) -> Optional[DiscoveredWorkflow]:
        """Detect login workflow pattern."""
        try:
            # Look for username/email and password fields
            username_fields = [e for e in elements if 
                             e.element_type == ElementType.INPUT_FIELD and
                             any(term in str(e.attributes).lower() for term in ['username', 'email', 'login'])]
            
            password_fields = [e for e in elements if 
                             e.element_type == ElementType.INPUT_FIELD and
                             'password' in str(e.attributes).lower()]
            
            submit_buttons = [e for e in elements if 
                            e.element_type == ElementType.BUTTON and
                            any(term in e.text_content.lower() for term in ['login', 'sign in', 'submit'])]
            
            if username_fields and password_fields and submit_buttons:
                steps = [
                    {
                        "step": 1,
                        "action": "type",
                        "element_id": username_fields[0].element_id,
                        "description": "Enter username or email",
                        "selector": username_fields[0].selector,
                        "parameter_type": "username"
                    },
                    {
                        "step": 2,
                        "action": "type",
                        "element_id": password_fields[0].element_id,
                        "description": "Enter password",
                        "selector": password_fields[0].selector,
                        "parameter_type": "password"
                    },
                    {
                        "step": 3,
                        "action": "click",
                        "element_id": submit_buttons[0].element_id,
                        "description": "Click login button",
                        "selector": submit_buttons[0].selector
                    }
                ]
                
                return DiscoveredWorkflow(
                    workflow_id="",  # Will be set by caller
                    name="User Login",
                    description="Complete user authentication workflow",
                    steps=steps,
                    category="authentication",
                    complexity=2,
                    success_indicators=["dashboard", "profile", "logout"],
                    prerequisites=["valid_credentials"],
                    estimated_time=15,
                    confidence_score=0.9
                )
            
            return None
            
        except Exception as e:
            return None
    
    # ... [Additional helper methods for comprehensive analysis]
    
    def _setup_browser_options(self) -> None:
        """Setup browser options for analysis."""
        pass  # Implementation details
    
    async def _cleanup_browser(self) -> None:
        """Clean up browser resources."""
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
        except Exception:
            pass
    
    # ... [Many more helper methods for complete analysis]
