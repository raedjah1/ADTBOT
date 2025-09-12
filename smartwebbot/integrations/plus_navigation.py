"""
PLUS Navigation Module

Handles all navigation tasks within the PLUS system after login.
Provides reusable, maintainable navigation functions for different PLUS pages.
"""

import time
from typing import Dict, Any, Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from ..utils.logger import get_logger


class PlusNavigator:
    """
    Handles navigation within the PLUS system.
    
    Features:
    - Modular navigation functions
    - Screenshot capture at each step
    - Robust error handling with fallbacks
    - Detailed logging for debugging
    """
    
    def __init__(self, web_controller, logger=None):
        """
        Initialize PLUS Navigator.
        
        Args:
            web_controller: WebController instance
            logger: Logger instance (optional)
        """
        self.web_controller = web_controller
        self.logger = logger or get_logger(__name__)
        
        # Navigation selectors for different elements
        self.selectors = {
            "search_button": [
                "#searchLink",
                "a[id='searchLink']",
                ".dropdown-toggle[title='Search']",
                "a[data-toggle='collapse'][data-target='#search']"
            ],
            "search_input_desktop": [
                "#ctl00_cbMenuSearch_Input",
                "input[id='ctl00_cbMenuSearch_Input']",
                ".rcbInput[value='Search Menu Item']",
                "input.rcbInput.radPreventDecorate.rcbEmptyMessage"
            ],
            "search_input_mobile": [
                "#ctl00_cbMenuSearchMobile_Input", 
                "input[id='ctl00_cbMenuSearchMobile_Input']",
                "input[name='ctl00$cbMenuSearchMobile']"
            ]
        }
    
    def _take_screenshot(self, filename: str) -> None:
        """Take a screenshot for debugging purposes."""
        try:
            self.web_controller.take_screenshot(filename)
            self.logger.debug(f"Screenshot saved: {filename}")
        except Exception as e:
            self.logger.warning(f"Could not take screenshot {filename}: {e}")
    
    def _click_element_by_selectors(self, selectors: list, element_name: str, timeout: int = 5) -> bool:
        """
        Try to click an element using multiple selectors.
        
        Args:
            selectors: List of CSS selectors to try
            element_name: Name of element for logging
            timeout: Wait timeout for each selector
            
        Returns:
            bool: True if successfully clicked
        """
        for selector in selectors:
            try:
                element = WebDriverWait(self.web_controller.driver, timeout).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                element.click()
                self.logger.info(f"SUCCESS: {element_name} clicked using selector: {selector}")
                return True
            except Exception as e:
                self.logger.debug(f"{element_name} selector failed: {selector} - {e}")
                continue
        
        return False
    
    def _javascript_click_fallback(self, js_code: str, element_name: str) -> bool:
        """
        Fallback JavaScript click method.
        
        Args:
            js_code: JavaScript code to execute
            element_name: Name of element for logging
            
        Returns:
            bool: True if successfully clicked
        """
        try:
            result = self.web_controller.driver.execute_script(js_code)
            if result:
                self.logger.info(f"SUCCESS: {element_name} clicked using JavaScript fallback")
                return True
            else:
                self.logger.error(f"JavaScript could not find {element_name}")
                return False
        except Exception as e:
            self.logger.error(f"JavaScript {element_name} click failed: {e}")
            return False
    
    def open_search_dropdown(self) -> bool:
        """
        Open the search dropdown menu.
        
        Returns:
            bool: True if search dropdown was opened successfully
        """
        self.logger.info("=== OPENING SEARCH DROPDOWN ===")
        self._take_screenshot("plus_before_search.png")
        
        # Try to click search button
        if self._click_element_by_selectors(self.selectors["search_button"], "search button"):
            time.sleep(0.5)  # Reduced wait time for dropdown to appear
            self._take_screenshot("plus_search_opened.png")
            return True
        
        # JavaScript fallback
        js_code = """
            var searchButton = document.querySelector('#searchLink') || 
                             document.querySelector('a[title="Search"]');
            if (searchButton) {
                searchButton.click();
                return true;
            }
            return false;
        """
        
        if self._javascript_click_fallback(js_code, "search button"):
            time.sleep(0.5)
            self._take_screenshot("plus_search_opened.png")
            return True
        
        self.logger.error("Could not open search dropdown")
        return False
    
    def search_menu_item(self, search_term: str) -> bool:
        """
        Search for a menu item in the search dropdown.
        
        Args:
            search_term: The term to search for
            
        Returns:
            bool: True if search was successful
        """
        self.logger.info(f"=== SEARCHING FOR: {search_term} ===")
        
        # Try desktop search input first
        for selector in self.selectors["search_input_desktop"]:
            try:
                element = WebDriverWait(self.web_controller.driver, 3).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                element.click()
                element.clear()
                element.send_keys(search_term)
                self.logger.info(f"SUCCESS: Search term entered using selector: {selector}")
                time.sleep(0.5)  # Reduced wait for dropdown options to appear
                self._take_screenshot("plus_search_typed.png")
                return True
            except Exception as e:
                self.logger.debug(f"Search input selector failed: {selector} - {e}")
                continue
        
        # Try mobile search input
        for selector in self.selectors["search_input_mobile"]:
            try:
                element = WebDriverWait(self.web_controller.driver, 3).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                element.click()
                element.clear()
                element.send_keys(search_term)
                self.logger.info(f"SUCCESS: Search term entered using mobile selector: {selector}")
                time.sleep(0.5)
                self._take_screenshot("plus_search_typed.png")
                return True
            except Exception as e:
                self.logger.debug(f"Mobile search input selector failed: {selector} - {e}")
                continue
        
        # JavaScript fallback for search input
        self.logger.info("Trying JavaScript fallback for search input")
        try:
            js_result = self.web_controller.driver.execute_script(f"""
                // Try to find any search input field
                var searchInputs = [
                    document.querySelector('#ctl00_cbMenuSearch_Input'),
                    document.querySelector('#ctl00_cbMenuSearchMobile_Input'),
                    document.querySelector('input[value="Search Menu Item"]'),
                    document.querySelector('.rcbInput')
                ];
                
                for (var i = 0; i < searchInputs.length; i++) {{
                    var input = searchInputs[i];
                    if (input && input.offsetParent !== null) {{
                        input.focus();
                        input.click();
                        input.value = '';
                        input.value = '{search_term}';
                        
                        // Trigger events to make sure the search activates
                        var event = new Event('input', {{ bubbles: true }});
                        input.dispatchEvent(event);
                        
                        var keyupEvent = new KeyboardEvent('keyup', {{ bubbles: true }});
                        input.dispatchEvent(keyupEvent);
                        
                        return true;
                    }}
                }}
                return false;
            """)
            
            if js_result:
                self.logger.info("SUCCESS: Search term entered using JavaScript fallback")
                time.sleep(1)  # Reduced wait for dropdown to populate
                self._take_screenshot("plus_search_typed.png")
                return True
            else:
                self.logger.error("JavaScript could not find any search input field")
        except Exception as e:
            self.logger.error(f"JavaScript search input fallback failed: {e}")
        
        self.logger.error("Could not find or activate search input field")
        return False
    
    def select_menu_option(self, option_text: str) -> bool:
        """
        Select a specific option from the search dropdown.
        
        Args:
            option_text: The text of the option to select
            
        Returns:
            bool: True if option was selected successfully
        """
        self.logger.info(f"=== SELECTING OPTION: {option_text} ===")
        
        # Try XPath approach first with shorter wait
        try:
            option_element = WebDriverWait(self.web_controller.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, f"//li[@class='rcbItem' and contains(text(), '{option_text}')]"))
            )
            option_element.click()
            self.logger.info(f"SUCCESS: {option_text} option clicked")
            time.sleep(1)  # Reduced wait for page navigation
            self._take_screenshot("plus_option_selected.png")
            return True
        except Exception as e:
            self.logger.debug(f"XPath {option_text} click failed: {e}")
        
        # JavaScript fallback
        js_code = f"""
            var items = document.querySelectorAll('li.rcbItem');
            for (var i = 0; i < items.length; i++) {{
                if (items[i].textContent.includes('{option_text}')) {{
                    items[i].click();
                    return true;
                }}
            }}
            return false;
        """
        
        if self._javascript_click_fallback(js_code, option_text):
            time.sleep(1)
            self._take_screenshot("plus_option_selected.png")
            return True
        
        self.logger.error(f"Could not select {option_text} option")
        return False
    
    def navigate_to_page(self, page_name: str, menu_search_term: str = None) -> Dict[str, Any]:
        """
        Navigate to a specific page using the search menu.
        
        Args:
            page_name: Display name of the page
            menu_search_term: Search term to use (defaults to page_name)
            
        Returns:
            Dict: Navigation result with success status and details
        """
        search_term = menu_search_term or page_name
        
        try:
            self.logger.info(f"Starting navigation to {page_name}")
            
            # Step 1: Open search dropdown
            if not self.open_search_dropdown():
                return {
                    "success": False,
                    "message": "Could not open search dropdown",
                    "current_url": self.web_controller.driver.current_url
                }
            
            # Step 2: Search for the menu item
            if not self.search_menu_item(search_term):
                return {
                    "success": False,
                    "message": f"Could not search for {search_term}",
                    "current_url": self.web_controller.driver.current_url
                }
            
            # Step 3: Select the menu option
            if not self.select_menu_option(search_term):
                return {
                    "success": False,
                    "message": f"Could not select {search_term} option",
                    "current_url": self.web_controller.driver.current_url
                }
            
            # Step 4: Verify navigation
            current_url = self.web_controller.driver.current_url
            self.logger.info(f"Navigation completed. Current URL: {current_url}")
            
            return {
                "success": True,
                "message": f"Successfully navigated to {page_name}",
                "current_url": current_url
            }
            
        except Exception as e:
            self.logger.error(f"Error navigating to {page_name}: {e}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            return {
                "success": False,
                "message": f"Navigation error: {str(e)}",
                "current_url": self.web_controller.driver.current_url if self.web_controller and self.web_controller.driver else None
            }


class PlusPageNavigator:
    """
    High-level navigation functions for specific PLUS pages.
    Uses PlusNavigator for the actual navigation work.
    """
    
    def __init__(self, web_controller, logger=None):
        """Initialize page navigator."""
        self.navigator = PlusNavigator(web_controller, logger)
        self.logger = logger or get_logger(__name__)
    
    def navigate_to_unit_receiving_adt(self) -> Dict[str, Any]:
        """
        Navigate to the Unit Receiving ADT page.
        
        Returns:
            Dict: Navigation result
        """
        return self.navigator.navigate_to_page(
            page_name="Unit Receiving ADT",
            menu_search_term="Unit Receiving ADT"
        )
    
    def navigate_to_work_order(self) -> Dict[str, Any]:
        """Navigate to Work Order page."""
        return self.navigator.navigate_to_page("Work Order")
    
    def navigate_to_ship_order(self) -> Dict[str, Any]:
        """Navigate to Ship Order page."""
        return self.navigator.navigate_to_page("Ship Order")
    
    def navigate_to_receive_order(self) -> Dict[str, Any]:
        """Navigate to Receive Order page."""
        return self.navigator.navigate_to_page("Receive Order")
    
    # Add more page-specific navigation methods as needed
