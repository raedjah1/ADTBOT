"""
Advanced web controller for browser automation.

Handles browser lifecycle, driver management, and low-level interactions.
"""

import os
import time
import json
from typing import Dict, Optional, Any, List
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from ..core.base_component import BaseComponent
from ..utils.config_manager import get_config_manager
from ..security.stealth_operations import STEALTH_ENGINE, activate_maximum_stealth


class WebController(BaseComponent):
    """
    Advanced web browser controller.
    
    Features:
    - Multi-browser support
    - Anti-detection measures
    - Session persistence
    - Performance optimization
    - Mobile emulation
    - Proxy support
    """
    
    def __init__(self, config: Dict = None):
        """
        Initialize the web controller.
        
        Args:
            config: Configuration dictionary
        """
        super().__init__("web_controller", config)
        self.driver = None
        self.wait = None
        self.current_session = None
        self.browser_type = None
        
        # Load configuration
        self.config_manager = get_config_manager()
        self.browser_config = self.config_manager.browser
        
        # Anti-detection features
        self.stealth_mode = self.config.get('stealth_mode', True)
        self.human_like_behavior = self.config.get('human_like_behavior', True)
        self.maximum_stealth = self.config.get('maximum_stealth', False)
        self.ghost_mode = self.config.get('ghost_mode', False)
        
        # Stealth operations
        self.stealth_profile = None
        self.stealth_operations = None
        
        # Performance tracking
        self.page_load_times = []
        self.interaction_times = []
    
    def initialize(self) -> bool:
        """Initialize the web controller."""
        try:
            self.logger.info("Initializing Web Controller")
            
            # Create necessary directories
            self._create_directories()
            
            # Initialize stealth operations if enabled
            if self.maximum_stealth or self.ghost_mode:
                self.logger.info("🥷 ACTIVATING MAXIMUM STEALTH OPERATIONS")
                self.stealth_operations = activate_maximum_stealth()
                self.stealth_profile = self.stealth_operations['stealth_profile']
            
            # Initialize browser
            if not self.start_browser():
                return False
            
            self.is_initialized = True
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize web controller: {e}")
            return False
    
    def cleanup(self) -> bool:
        """Clean up web controller resources."""
        try:
            if self.driver:
                self.stop_browser()
            return True
        except Exception as e:
            self.logger.error(f"Web controller cleanup failed: {e}")
            return False
    
    def start_browser(self, browser_type: str = None, headless: bool = None, 
                     profile_path: str = None, proxy: str = None) -> bool:
        """
        Start the web browser with advanced configuration.
        
        Args:
            browser_type: Browser type (chrome, firefox, edge)
            headless: Run in headless mode
            profile_path: Path to browser profile
            proxy: Proxy configuration
        
        Returns:
            bool: True if browser started successfully
        """
        try:
            browser_type = browser_type or self.browser_config.default_browser
            headless = headless if headless is not None else self.browser_config.headless
            
            self.logger.info(f"Starting {browser_type} browser")
            
            if browser_type.lower() == 'chrome':
                self.driver = self._start_chrome(headless, profile_path, proxy)
            elif browser_type.lower() == 'firefox':
                self.driver = self._start_firefox(headless, profile_path, proxy)
            elif browser_type.lower() == 'edge':
                self.driver = self._start_edge(headless, profile_path, proxy)
            else:
                raise ValueError(f"Unsupported browser: {browser_type}")
            
            if self.driver is None:
                self.logger.error("Failed to create browser driver")
                return False
            
            self.browser_type = browser_type
            
            # Configure timeouts
            self.driver.implicitly_wait(self.browser_config.implicit_wait)
            self.driver.set_page_load_timeout(self.browser_config.page_load_timeout)
            
            # Set window size
            if not headless:
                self.driver.set_window_size(*self.browser_config.window_size)
            
            # Initialize WebDriverWait
            self.wait = WebDriverWait(self.driver, 10)
            
            # Apply anti-detection measures
            if self.stealth_mode:
                self._apply_stealth_measures()
            
            # Apply maximum stealth if enabled
            if self.maximum_stealth or self.ghost_mode:
                self.logger.info("💉 INJECTING MAXIMUM STEALTH PAYLOAD")
                STEALTH_ENGINE.execute_stealth_injection(self.driver)
            
            self.logger.info(f"Browser {browser_type} started successfully")
            self.update_metrics("start_browser", True)
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start browser: {e}")
            self.update_metrics("start_browser", False)
            return False
    
    def _start_chrome(self, headless: bool, profile_path: str = None, proxy: str = None):
        """Start Chrome browser with advanced options."""
        options = ChromeOptions()
        
        # Basic options
        if headless:
            options.add_argument('--headless=new')
        
        # Anti-detection options
        if self.stealth_mode:
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument('--disable-web-security')
            options.add_argument('--allow-running-insecure-content')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-plugins')
            options.add_argument('--disable-images')  # Faster loading
        
        # Maximum stealth configuration
        if self.maximum_stealth or self.ghost_mode:
            self.logger.info("🌫️ CONFIGURING PHANTOM BROWSER - MAXIMUM STEALTH")
            STEALTH_ENGINE.configure_phantom_browser(options)
        
        # User agent
        if self.browser_config.user_agent:
            options.add_argument(f'--user-agent={self.browser_config.user_agent}')
        
        # Profile
        if profile_path:
            options.add_argument(f'--user-data-dir={profile_path}')
        
        # Proxy
        if proxy or self.browser_config.proxy:
            proxy_setting = proxy or self.browser_config.proxy
            options.add_argument(f'--proxy-server={proxy_setting}')
        
        # Download directory
        if self.browser_config.download_directory:
            prefs = {
                "download.default_directory": os.path.abspath(self.browser_config.download_directory),
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            }
            options.add_experimental_option("prefs", prefs)
        
        # Extensions
        for extension in self.browser_config.extensions:
            if os.path.exists(extension):
                options.add_extension(extension)
        
        # Performance options
        options.add_argument('--no-first-run')
        options.add_argument('--disable-default-apps')
        options.add_argument('--disable-popup-blocking')
        
        try:
            # Create service
            service = ChromeService(ChromeDriverManager().install())
            
            # Create driver
            driver = webdriver.Chrome(service=service, options=options)
            
            return driver
        except Exception as e:
            self.logger.error(f"Failed to start Chrome driver: {e}")
            return None
    
    def _start_firefox(self, headless: bool, profile_path: str = None, proxy: str = None):
        """Start Firefox browser with advanced options."""
        options = FirefoxOptions()
        
        if headless:
            options.add_argument('--headless')
        
        # Profile
        if profile_path:
            options.add_argument(f'--profile={profile_path}')
        
        # Proxy
        if proxy or self.browser_config.proxy:
            proxy_setting = proxy or self.browser_config.proxy
            # Firefox proxy configuration would go here
            pass
        
        try:
            # Create service
            service = FirefoxService(GeckoDriverManager().install())
            
            # Create driver
            driver = webdriver.Firefox(service=service, options=options)
            
            return driver
        except Exception as e:
            self.logger.error(f"Failed to start Firefox driver: {e}")
            return None
    
    def _start_edge(self, headless: bool, profile_path: str = None, proxy: str = None):
        """Start Edge browser with advanced options."""
        options = EdgeOptions()
        
        if headless:
            options.add_argument('--headless')
        
        # Similar configuration to Chrome
        if self.stealth_mode:
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
        
        try:
            # Create service
            service = EdgeService(EdgeChromiumDriverManager().install())
            
            # Create driver
            driver = webdriver.Edge(service=service, options=options)
            
            return driver
        except Exception as e:
            self.logger.error(f"Failed to start Edge driver: {e}")
            return None
    
    def _apply_stealth_measures(self):
        """Apply anti-detection measures to the browser."""
        try:
            # Execute stealth JavaScript
            stealth_js = """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            
            // Remove automation indicators
            delete navigator.__proto__.webdriver;
            
            // Override plugins
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            
            // Override languages
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en'],
            });
            
            // Override permissions
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
            );
            """
            
            self.driver.execute_script(stealth_js)
            self.logger.debug("Applied stealth measures")
            
        except Exception as e:
            self.logger.warning(f"Failed to apply stealth measures: {e}")
    
    def activate_ghost_mode(self) -> bool:
        """
        🥷 ACTIVATE GHOST MODE 🥷
        Enable maximum stealth for invisible operations
        """
        try:
            self.logger.info("👻 ACTIVATING GHOST MODE - MAXIMUM STEALTH ENGAGED")
            
            # Activate stealth operations
            if not self.stealth_operations:
                self.stealth_operations = activate_maximum_stealth()
                self.stealth_profile = self.stealth_operations['stealth_profile']
            
            # Apply stealth injection to current browser
            if self.driver:
                STEALTH_ENGINE.execute_stealth_injection(self.driver)
            
            self.ghost_mode = True
            self.maximum_stealth = True
            
            self.logger.info("✅ GHOST MODE ACTIVE - OPERATING IN MAXIMUM STEALTH")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to activate ghost mode: {e}")
            return False
    
    def get_stealth_report(self) -> Dict[str, Any]:
        """
        📊 GET STEALTH REPORT 📊
        Generate comprehensive stealth operations report
        """
        if self.stealth_operations:
            return STEALTH_ENGINE.generate_operational_report()
        else:
            return {
                'operational_status': 'BASIC STEALTH',
                'stealth_level': 'STANDARD',
                'capabilities': 'LIMITED'
            }
    
    def stop_browser(self) -> bool:
        """Stop the browser and clean up."""
        try:
            if self.driver:
                # Save session if configured
                if self.browser_config.save_session:
                    self._save_session()
                
                self.driver.quit()
                self.driver = None
                self.wait = None
                
                self.logger.info("Browser stopped successfully")
                return True
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to stop browser: {e}")
            return False
    
    def navigate_to(self, url: str, wait_for_load: bool = True) -> bool:
        """
        Navigate to a URL with advanced loading detection.
        
        Args:
            url: URL to navigate to
            wait_for_load: Wait for page to fully load
        
        Returns:
            bool: True if navigation successful
        """
        try:
            start_time = time.time()
            self.logger.info(f"Navigating to: {url}")
            
            # Navigate
            self.driver.get(url)
            
            # Wait for page load
            if wait_for_load:
                self._wait_for_page_load()
            
            load_time = time.time() - start_time
            self.page_load_times.append(load_time)
            
            self.logger.info(f"Navigation completed in {load_time:.2f}s")
            self.update_metrics("navigate", True)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Navigation failed: {e}")
            self.update_metrics("navigate", False)
            return False
    
    def _wait_for_page_load(self, timeout: int = 30):
        """Wait for page to fully load."""
        try:
            # Wait for document ready state
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            # Wait for jQuery if present
            try:
                WebDriverWait(self.driver, 5).until(
                    lambda driver: driver.execute_script("return typeof jQuery === 'undefined' || jQuery.active === 0")
                )
            except:
                pass  # jQuery not present or timeout
            
            # Additional wait for dynamic content
            time.sleep(1)
            
        except Exception as e:
            self.logger.warning(f"Page load wait timeout: {e}")
    
    def take_screenshot(self, filename: str = None, full_page: bool = False) -> str:
        """
        Take a screenshot with advanced options.
        
        Args:
            filename: Screenshot filename
            full_page: Take full page screenshot
        
        Returns:
            str: Path to screenshot file
        """
        try:
            if not filename:
                timestamp = int(time.time())
                filename = f"screenshot_{timestamp}.png"
            
            # Ensure screenshots directory exists
            screenshot_dir = Path("screenshots")
            screenshot_dir.mkdir(exist_ok=True)
            
            filepath = screenshot_dir / filename
            
            if full_page:
                # Full page screenshot
                original_size = self.driver.get_window_size()
                required_width = self.driver.execute_script('return document.body.parentNode.scrollWidth')
                required_height = self.driver.execute_script('return document.body.parentNode.scrollHeight')
                
                self.driver.set_window_size(required_width, required_height)
                self.driver.save_screenshot(str(filepath))
                self.driver.set_window_size(original_size['width'], original_size['height'])
            else:
                # Regular screenshot
                self.driver.save_screenshot(str(filepath))
            
            self.logger.info(f"Screenshot saved: {filepath}")
            return str(filepath)
            
        except Exception as e:
            self.logger.error(f"Screenshot failed: {e}")
            return ""
    
    def execute_javascript(self, script: str, *args) -> Any:
        """
        Execute JavaScript with error handling.
        
        Args:
            script: JavaScript code to execute
            *args: Arguments to pass to the script
        
        Returns:
            Script execution result
        """
        try:
            result = self.driver.execute_script(script, *args)
            self.logger.debug("JavaScript executed successfully")
            return result
        except Exception as e:
            self.logger.error(f"JavaScript execution failed: {e}")
            return None
    
    def get_page_performance(self) -> Dict[str, Any]:
        """
        Get page performance metrics.
        
        Returns:
            Dict containing performance data
        """
        try:
            performance_script = """
            const perfData = performance.getEntriesByType('navigation')[0];
            return {
                domContentLoaded: perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart,
                loadComplete: perfData.loadEventEnd - perfData.loadEventStart,
                firstPaint: performance.getEntriesByType('paint')[0]?.startTime || 0,
                firstContentfulPaint: performance.getEntriesByType('paint')[1]?.startTime || 0
            };
            """
            
            perf_data = self.execute_javascript(performance_script)
            
            if perf_data:
                perf_data['averagePageLoadTime'] = sum(self.page_load_times) / len(self.page_load_times) if self.page_load_times else 0
                perf_data['totalPageLoads'] = len(self.page_load_times)
            
            return perf_data or {}
            
        except Exception as e:
            self.logger.error(f"Failed to get performance metrics: {e}")
            return {}
    
    def clear_cache_and_cookies(self):
        """Clear browser cache and cookies."""
        try:
            self.driver.delete_all_cookies()
            
            # Clear local storage
            self.execute_javascript("localStorage.clear();")
            
            # Clear session storage
            self.execute_javascript("sessionStorage.clear();")
            
            self.logger.info("Cache and cookies cleared")
            
        except Exception as e:
            self.logger.error(f"Failed to clear cache: {e}")
    
    def set_cookie(self, name: str, value: str, domain: str = None, path: str = "/"):
        """
        Set a cookie.
        
        Args:
            name: Cookie name
            value: Cookie value
            domain: Cookie domain
            path: Cookie path
        """
        try:
            cookie = {
                'name': name,
                'value': value,
                'path': path
            }
            
            if domain:
                cookie['domain'] = domain
            
            self.driver.add_cookie(cookie)
            self.logger.debug(f"Cookie set: {name}")
            
        except Exception as e:
            self.logger.error(f"Failed to set cookie: {e}")
    
    def get_current_url(self) -> str:
        """Get the current URL."""
        try:
            if self.driver is None:
                self.logger.warning("Driver not initialized - returning empty URL")
                return ""
            return self.driver.current_url
        except:
            return ""
    
    def get_page_title(self) -> str:
        """Get the current page title."""
        try:
            return self.driver.title
        except:
            return ""
    
    def get_page_source(self) -> str:
        """Get the current page source."""
        try:
            return self.driver.page_source
        except:
            return ""
    
    def _create_directories(self):
        """Create necessary directories."""
        directories = [
            "screenshots",
            "downloads", 
            "sessions",
            self.browser_config.download_directory
        ]
        
        for directory in directories:
            if directory:
                Path(directory).mkdir(exist_ok=True)
    
    def _save_session(self):
        """Save current browser session."""
        try:
            session_data = {
                'cookies': self.driver.get_cookies(),
                'current_url': self.driver.current_url,
                'timestamp': time.time()
            }
            
            session_file = Path("sessions") / f"session_{int(time.time())}.json"
            
            with open(session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
            
            self.logger.info(f"Session saved: {session_file}")
            
        except Exception as e:
            self.logger.error(f"Failed to save session: {e}")
    
    def load_session(self, session_file: str) -> bool:
        """
        Load a saved browser session.
        
        Args:
            session_file: Path to session file
        
        Returns:
            bool: True if session loaded successfully
        """
        try:
            with open(session_file, 'r') as f:
                session_data = json.load(f)
            
            # Navigate to the saved URL
            if session_data.get('current_url'):
                self.navigate_to(session_data['current_url'])
            
            # Restore cookies
            for cookie in session_data.get('cookies', []):
                try:
                    self.driver.add_cookie(cookie)
                except:
                    continue  # Skip invalid cookies
            
            self.logger.info(f"Session loaded: {session_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load session: {e}")
            return False
    
    def is_browser_active(self) -> bool:
        """Check if browser is active and responsive."""
        try:
            if not self.driver:
                return False
            
            # Try to get current URL
            self.driver.current_url
            return True
            
        except:
            return False
