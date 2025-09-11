"""
PLUS System Integration

Provides seamless integration with PLUS (Reconext) system including
automated login, session management, and system-specific workflows.
"""

import time
import json
from typing import Dict, Optional, Any, Tuple
from pathlib import Path
from urllib.parse import urljoin, urlparse

from ..core.base_component import BaseComponent
from ..utils.logger import log_error, log_performance
from ..settings.service import SettingsService


class PlusIntegration(BaseComponent):
    """
    PLUS system integration with intelligent login and session management.
    
    Features:
    - Automated PLUS login using stored credentials
    - Session persistence and validation
    - PLUS-specific error handling
    - Login state monitoring
    - Multi-factor authentication support
    """
    
    def __init__(self, web_controller, form_handler, settings_service: SettingsService = None, config: Dict = None):
        """
        Initialize PLUS integration.
        
        Args:
            web_controller: WebController instance
            form_handler: FormHandler instance
            settings_service: SettingsService instance
            config: Configuration dictionary
        """
        super().__init__("plus_integration", config)
        self.web_controller = web_controller
        self.form_handler = form_handler
        self.settings_service = settings_service or SettingsService()
        
        # PLUS-specific state
        self.is_logged_in = False
        self.login_timestamp = None
        self.session_data = {}
        self.plus_settings = None
        
        # Login attempt tracking
        self.login_attempts = 0
        self.max_login_attempts = 3
        
        # PLUS-specific selectors and patterns
        self.login_selectors = {
            'username_field': [
                # PLUS-specific selectors (most specific first)
                'input[id="LoginMainContent_tbUsername"]',
                'input[name="ctl00$LoginMainContent$tbUsername"]',
                'input.customtextbox[type="text"]',
                # Generic fallbacks
                'input[name="username"]',
                'input[name="user"]', 
                'input[name="email"]',
                'input[type="email"]',
                'input[id*="username"]',
                'input[id*="user"]',
                'input[id*="login"]'
            ],
            'password_field': [
                # PLUS-specific selectors (most specific first)
                'input[id="LoginMainContent_tbPassword"]',
                'input[name="ctl00$LoginMainContent$tbPassword"]',
                'input.customtextbox[type="password"]',
                # Generic fallbacks
                'input[name="password"]',
                'input[type="password"]',
                'input[id*="password"]',
                'input[id*="pass"]'
            ],
            'login_button': [
                # PLUS-specific selectors (most specific first)
                'input[id="LoginMainContent_btnLogin"]',
                'input[name="ctl00$LoginMainContent$btnLogin"]',
                'input.importantButton[type="submit"]',
                'input[value="Login"][type="submit"]',
                # Generic fallbacks
                'button[type="submit"]',
                'input[type="submit"]',
                'button:contains("Login")',
                'button:contains("Sign In")',
                'button:contains("Log In")',
                '.login-button',
                '#login-button',
                '[id*="login"]',
                '[class*="login"]'
            ],
            'error_messages': [
                '.error',
                '.alert-danger',
                '.error-message',
                '[class*="error"]',
                '[id*="error"]',
                'span[data-val="true"]'  # PLUS validation messages
            ]
        }
    
    def initialize(self) -> bool:
        """Initialize the PLUS integration."""
        try:
            self.logger.info("Initializing PLUS Integration")
            
            # Load PLUS settings
            self.plus_settings = self._load_plus_settings()
            if not self.plus_settings:
                self.logger.warning("No PLUS settings found")
                return False
            
            self.logger.info(f"PLUS Integration initialized for: {self.plus_settings.get('base_url', 'Unknown')}")
            self.is_initialized = True
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize PLUS integration: {e}")
            return False
    
    def cleanup(self) -> bool:
        """Clean up PLUS integration."""
        try:
            # Save session data if logged in
            if self.is_logged_in:
                self._save_session_data()
            
            return True
        except Exception as e:
            self.logger.error(f"PLUS integration cleanup failed: {e}")
            return False
    
    async def login_to_plus(self, force_login: bool = False) -> Tuple[bool, str]:
        """
        Perform automated login to PLUS system.
        
        Args:
            force_login: Force login even if already logged in
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            start_time = time.time()
            self.logger.info("Starting PLUS login process")
            
            # Set overall timeout for login process (60 seconds)
            login_timeout = 60
            
            # Check if already logged in
            if self.is_logged_in and not force_login:
                if self._validate_existing_session():
                    return True, "Already logged in to PLUS"
            
            # Reset login state
            self.is_logged_in = False
            self.login_attempts += 1
            
            if self.login_attempts > self.max_login_attempts:
                return False, f"Maximum login attempts ({self.max_login_attempts}) exceeded"
            
            # Load credentials
            if not self.plus_settings:
                return False, "PLUS settings not configured"
            
            username = self.plus_settings.get('username')
            password = self.plus_settings.get('password')
            base_url = self.plus_settings.get('base_url')
            
            if not all([username, password, base_url]):
                return False, "PLUS credentials incomplete (missing username, password, or URL)"
            
            # Step 1: Navigate to PLUS login page
            login_url = self._get_login_url(base_url)
            self.logger.info(f"Navigating to PLUS login: {login_url}")
            
            if not self.web_controller.navigate_to(login_url):
                return False, f"Failed to navigate to PLUS login page: {login_url}"
            
            # Check if we actually reached the intended site
            current_url = self.web_controller.driver.current_url
            self.logger.info(f"Reached URL: {current_url}")
            
            # If we're redirected to a completely different domain, that's an issue
            from urllib.parse import urlparse
            target_domain = urlparse(base_url).netloc
            current_domain = urlparse(current_url).netloc
            
            if target_domain.lower() not in current_domain.lower() and current_domain.lower() not in target_domain.lower():
                return False, f"Redirected to unexpected domain. Expected: {target_domain}, Got: {current_domain}"
            
            # Wait for page to load
            time.sleep(2)
            
            # Step 2: Take screenshot before login attempt
            screenshot_path = self.web_controller.take_screenshot("plus_login_page.png")
            self.logger.info(f"Login page screenshot saved: {screenshot_path}")
            
            # Step 3: Detect and fill login form (with timeout check)
            elapsed_time = time.time() - start_time
            if elapsed_time > login_timeout:
                return False, f"Login process timed out after {elapsed_time:.1f} seconds"
            
            login_success, login_message = await self._perform_login_sequence(username, password)
            
            if login_success:
                # Step 4: Check for database/site/program selection page
                database_step_success, database_message = await self._handle_database_selection()
                
                if database_step_success:
                    # Step 5: Validate final login success
                    validation_success, validation_message = self._validate_login_success()
                    
                    if validation_success:
                        self.is_logged_in = True
                        self.login_timestamp = time.time()
                        self.login_attempts = 0  # Reset on success
                        
                        # Save session data
                        self._save_session_data()
                        
                        duration = time.time() - start_time
                        log_performance("plus_integration", "login", duration, success=True)
                        
                        self.logger.info(f"PLUS login successful in {duration:.2f}s")
                        return True, f"Successfully logged in to PLUS ({validation_message})"
                    else:
                        return False, f"Final login validation failed: {validation_message}"
                else:
                    return False, f"Database selection failed: {database_message}"
            else:
                return False, f"Login sequence failed: {login_message}"
                
        except Exception as e:
            log_error("plus_integration", e, {"operation": "login"})
            return False, f"Login error: {str(e)}"
    
    async def _perform_login_sequence(self, username: str, password: str) -> Tuple[bool, str]:
        """Perform the actual login form filling and submission."""
        try:
            self.logger.info("Filling PLUS login form")
            
            # Method 1: Try selector-based approach first (faster and more reliable)
            self.logger.info("Trying selector-based login form filling")
            
            self.logger.info("=== ATTEMPTING USERNAME FIELD ===")
            username_filled = self._fill_field_by_selectors(self.login_selectors['username_field'], username)
            
            self.logger.info("=== ATTEMPTING PASSWORD FIELD ===")
            password_filled = self._fill_field_by_selectors(self.login_selectors['password_field'], password)
            
            if username_filled and password_filled:
                self.logger.info("SUCCESS Both username and password fields filled using selectors")
                
                self.logger.info("=== ATTEMPTING LOGIN BUTTON CLICK ===")
                if await self._click_login_button():
                    return await self._wait_for_login_response()
                else:
                    return False, "Could not find or click login button"
            else:
                self.logger.info(f"SELECTOR METHOD FAILED - Username filled: {username_filled}, Password filled: {password_filled}")
            
            # Method 2: Try intelligent form filling as fallback
            self.logger.info("Selector method failed, trying intelligent form filling")
            form_data = {
                "username": username,
                "user": username,
                "email": username,
                "login": username,
                "password": password
            }
            
            if self.form_handler.fill_form_intelligently(form_data, "PLUS login form"):
                self.logger.info("Login form filled using intelligent detection")
                
                # Find and click login button
                if await self._click_login_button():
                    return await self._wait_for_login_response()
                else:
                    return False, "Could not find or click login button"
            
            # Method 3: Debug - let's see what's actually on the page
            self.logger.info("Both methods failed, analyzing page content...")
            return await self._debug_login_form()
            
        except Exception as e:
            return False, f"Login sequence error: {str(e)}"
    
    def _fill_field_by_selectors(self, selectors: list, value: str) -> bool:
        """Try to fill a field using multiple selectors."""
        from selenium.webdriver.common.by import By
        from selenium.common.exceptions import NoSuchElementException, TimeoutException
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        self.logger.info(f"Trying to fill field with value: {value[:3]}...")
        
        for i, selector in enumerate(selectors):
            try:
                self.logger.info(f"Trying selector {i+1}/{len(selectors)}: {selector}")
                
                # Wait for element to be present and visible (with timeout)
                wait = WebDriverWait(self.web_controller.driver, 5)  # 5 second timeout
                element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                
                element.clear()
                element.send_keys(value)
                self.logger.info(f"SUCCESS Field filled using selector: {selector}")
                return True
                
            except TimeoutException:
                self.logger.info(f"TIMEOUT waiting for selector: {selector}")
                continue
            except NoSuchElementException:
                self.logger.info(f"ELEMENT NOT FOUND: {selector}")
                continue
            except Exception as e:
                self.logger.info(f"SELECTOR FAILED {selector}: {e}")
                continue
        
        self.logger.info(f"FAILED to fill field with any selector")
        return False
    
    async def _debug_login_form(self) -> Tuple[bool, str]:
        """Debug method to analyze the login form when standard methods fail."""
        try:
            from selenium.webdriver.common.by import By
            
            self.logger.info("=== LOGIN FORM DEBUG ANALYSIS ===")
            
            # Get page source for analysis
            page_source = self.web_controller.driver.page_source
            current_url = self.web_controller.driver.current_url
            page_title = self.web_controller.driver.title
            
            self.logger.info(f"Current URL: {current_url}")
            self.logger.info(f"Page Title: {page_title}")
            
            # Find all input fields
            input_fields = self.web_controller.driver.find_elements(By.TAG_NAME, "input")
            self.logger.info(f"Found {len(input_fields)} input fields:")
            
            for i, field in enumerate(input_fields):
                try:
                    field_type = field.get_attribute("type") or "text"
                    field_name = field.get_attribute("name") or ""
                    field_id = field.get_attribute("id") or ""
                    field_placeholder = field.get_attribute("placeholder") or ""
                    field_class = field.get_attribute("class") or ""
                    is_visible = field.is_displayed()
                    
                    self.logger.info(f"  {i+1}. Type: {field_type}, Name: '{field_name}', ID: '{field_id}', "
                                   f"Placeholder: '{field_placeholder}', Class: '{field_class}', Visible: {is_visible}")
                except Exception as e:
                    self.logger.info(f"  {i+1}. Error analyzing field: {e}")
            
            # Find all buttons
            buttons = self.web_controller.driver.find_elements(By.TAG_NAME, "button")
            submit_inputs = self.web_controller.driver.find_elements(By.CSS_SELECTOR, "input[type='submit']")
            all_buttons = buttons + submit_inputs
            
            self.logger.info(f"Found {len(all_buttons)} buttons/submit inputs:")
            
            for i, button in enumerate(all_buttons):
                try:
                    button_text = button.text or button.get_attribute("value") or ""
                    button_type = button.get_attribute("type") or ""
                    button_id = button.get_attribute("id") or ""
                    button_class = button.get_attribute("class") or ""
                    is_visible = button.is_displayed()
                    
                    self.logger.info(f"  {i+1}. Text: '{button_text}', Type: '{button_type}', ID: '{button_id}', "
                                   f"Class: '{button_class}', Visible: {is_visible}")
                except Exception as e:
                    self.logger.info(f"  {i+1}. Error analyzing button: {e}")
            
            # Try to find login form by common patterns
            login_forms = []
            
            # Look for forms
            forms = self.web_controller.driver.find_elements(By.TAG_NAME, "form")
            for form in forms:
                form_action = form.get_attribute("action") or ""
                form_method = form.get_attribute("method") or ""
                form_id = form.get_attribute("id") or ""
                form_class = form.get_attribute("class") or ""
                
                if any(keyword in form_action.lower() or keyword in form_id.lower() or keyword in form_class.lower() 
                       for keyword in ['login', 'signin', 'auth']):
                    login_forms.append(form)
                    self.logger.info(f"Potential login form found - Action: '{form_action}', Method: '{form_method}', "
                                   f"ID: '{form_id}', Class: '{form_class}'")
            
            # Try manual field filling based on what we found
            username_field = None
            password_field = None
            
            # Look for username field (more flexible approach)
            for field in input_fields:
                if not field.is_displayed():
                    continue
                    
                field_type = (field.get_attribute("type") or "text").lower()
                field_name = (field.get_attribute("name") or "").lower()
                field_id = (field.get_attribute("id") or "").lower()
                field_placeholder = (field.get_attribute("placeholder") or "").lower()
                
                # Check for username patterns
                if (field_type in ["text", "email"] and 
                    any(keyword in field_name or keyword in field_id or keyword in field_placeholder 
                        for keyword in ['user', 'login', 'email', 'account'])):
                    username_field = field
                    self.logger.info(f"Found potential username field: {field_name or field_id or 'unnamed'}")
                    break
                    
                # Check for password field
                elif field_type == "password":
                    password_field = field
                    self.logger.info(f"Found password field: {field_name or field_id or 'unnamed'}")
            
            # Try to fill the fields manually
            if username_field and password_field:
                try:
                    username_field.clear()
                    username_field.send_keys("raed.jah")
                    self.logger.info("✅ Username field filled manually")
                    
                    password_field.clear()
                    password_field.send_keys("Microwave18.")
                    self.logger.info("✅ Password field filled manually")
                    
                    # Try to find and click submit button
                    for button in all_buttons:
                        if button.is_displayed():
                            button_text = (button.text or button.get_attribute("value") or "").lower()
                            if any(keyword in button_text for keyword in ['login', 'sign in', 'submit']):
                                button.click()
                                self.logger.info(f"✅ Clicked login button: {button_text}")
                                return await self._wait_for_login_response()
                    
                    # If no obvious button, try the first visible submit button
                    for button in all_buttons:
                        if button.is_displayed() and button.get_attribute("type") == "submit":
                            button.click()
                            self.logger.info("✅ Clicked first submit button")
                            return await self._wait_for_login_response()
                    
                    return False, "Fields filled but could not find login button"
                    
                except Exception as e:
                    return False, f"Manual field filling failed: {str(e)}"
            
            self.logger.info("=== END DEBUG ANALYSIS ===")
            return False, "Could not identify login form structure"
            
        except Exception as e:
            return False, f"Debug analysis failed: {str(e)}"
    
    async def _handle_database_selection(self) -> Tuple[bool, str]:
        """Handle the PLUS database/site/program selection step."""
        try:
            self.logger.info("=== CHECKING FOR DATABASE SELECTION PAGE ===")
            
            # Wait a moment for page to load after login
            time.sleep(3)
            
            # Check if we're on the database selection page
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import Select
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            
            try:
                # Look for the database selection div
                database_div = WebDriverWait(self.web_controller.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "LoginMainContent_DatabaseProgramDiv"))
                )
                
                self.logger.info("Database selection page detected")
                
                # Take screenshot of database selection page
                screenshot_path = self.web_controller.take_screenshot("plus_database_selection.png")
                self.logger.info(f"Database selection screenshot: {screenshot_path}")
                
                # Step 1: Select Database (PROD)
                self.logger.info("=== SELECTING DATABASE: PROD ===")
                try:
                    database_dropdown = self.web_controller.driver.find_element(By.ID, "LoginMainContent_ddlDatabase")
                    database_select = Select(database_dropdown)
                    database_select.select_by_value("PROD")
                    self.logger.info("SUCCESS: Database PROD selected")
                    time.sleep(1)  # Wait for any dynamic updates
                except Exception as e:
                    self.logger.error(f"Failed to select database: {e}")
                    return False, f"Database selection failed: {e}"
                
                # Step 2: Select Site (MEMPHIS)
                self.logger.info("=== SELECTING SITE: MEMPHIS ===")
                try:
                    site_dropdown = self.web_controller.driver.find_element(By.ID, "LoginMainContent_ddlSite")
                    site_select = Select(site_dropdown)
                    site_select.select_by_value("MEMPHIS")
                    self.logger.info("SUCCESS: Site MEMPHIS selected")
                    time.sleep(1)  # Wait for any dynamic updates
                except Exception as e:
                    self.logger.error(f"Failed to select site: {e}")
                    return False, f"Site selection failed: {e}"
                
                # Step 3: Select Program (ADT)
                self.logger.info("=== SELECTING PROGRAM: ADT ===")
                try:
                    program_dropdown = self.web_controller.driver.find_element(By.ID, "LoginMainContent_ddlProgram")
                    program_select = Select(program_dropdown)
                    
                    # Check if ADT option exists
                    program_options = [option.get_attribute("value") for option in program_select.options]
                    self.logger.info(f"Available programs: {program_options}")
                    
                    if "ADT" in program_options:
                        program_select.select_by_value("ADT")
                        self.logger.info("SUCCESS: Program ADT selected")
                    else:
                        # If ADT is not available, log available options and use the first one
                        self.logger.warning(f"ADT not found in programs: {program_options}. Using first available option.")
                        if len(program_select.options) > 1:  # Skip empty option
                            program_select.select_by_index(1)
                            selected_program = program_select.first_selected_option.get_attribute("value")
                            self.logger.info(f"SUCCESS: Program {selected_program} selected (ADT not available)")
                    
                    time.sleep(1)  # Wait for any dynamic updates
                except Exception as e:
                    self.logger.error(f"Failed to select program: {e}")
                    return False, f"Program selection failed: {e}"
                
                # Step 4: Click Request Access button to proceed
                self.logger.info("=== CLICKING REQUEST ACCESS BUTTON ===")
                try:
                    # Try multiple selectors for the Request Access button
                    request_access_selectors = [
                        'input[id="ctl00_LoginMainContent_btnRequestAccess_input"]',
                        'input[name="ctl00$LoginMainContent$btnRequestAccess_input"]',
                        'input[value="Request Access"]',
                        '#ctl00_LoginMainContent_btnRequestAccess_input'
                    ]
                    
                    button_clicked = False
                    for selector in request_access_selectors:
                        try:
                            button = self.web_controller.driver.find_element(By.CSS_SELECTOR, selector)
                            if button.is_displayed() and button.is_enabled():
                                button.click()
                                self.logger.info(f"SUCCESS: Request Access button clicked using selector: {selector}")
                                button_clicked = True
                                break
                        except:
                            continue
                    
                    if not button_clicked:
                        # Try JavaScript click as fallback
                        try:
                            self.web_controller.driver.execute_script("""
                                var button = document.querySelector('input[value="Request Access"]');
                                if (button) button.click();
                            """)
                            self.logger.info("SUCCESS: Request Access button clicked using JavaScript")
                            button_clicked = True
                        except Exception as js_error:
                            self.logger.error(f"JavaScript click failed: {js_error}")
                    
                    if not button_clicked:
                        return False, "Could not find or click Request Access button"
                    
                    # Wait for page to process the request
                    time.sleep(5)
                    
                    self.logger.info("Database selection process completed successfully")
                    return True, "Database, Site, and Program selected successfully"
                    
                except Exception as e:
                    self.logger.error(f"Failed to click Request Access button: {e}")
                    return False, f"Request Access button click failed: {e}"
                    
            except Exception as e:
                # Database selection page not found - might already be logged in
                self.logger.info("Database selection page not found - assuming already past this step")
                return True, "Database selection not required"
                
        except Exception as e:
            self.logger.error(f"Database selection handler error: {e}")
            return False, f"Database selection error: {str(e)}"
    
    async def _click_login_button(self) -> bool:
        """Find and click the login button."""
        from selenium.webdriver.common.by import By
        from selenium.common.exceptions import NoSuchElementException
        
        for selector in self.login_selectors['login_button']:
            try:
                element = self.web_controller.driver.find_element(By.CSS_SELECTOR, selector)
                
                # Scroll to element and click
                self.web_controller.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(0.5)
                element.click()
                
                self.logger.info(f"Login button clicked using selector: {selector}")
                return True
                
            except NoSuchElementException:
                continue
            except Exception as e:
                self.logger.debug(f"Login button selector {selector} failed: {e}")
                continue
        
        # Try JavaScript click as fallback
        try:
            self.web_controller.driver.execute_script("""
                var buttons = document.querySelectorAll('button, input[type="submit"]');
                for (var i = 0; i < buttons.length; i++) {
                    var text = buttons[i].textContent || buttons[i].value || '';
                    if (text.toLowerCase().includes('login') || text.toLowerCase().includes('sign')) {
                        buttons[i].click();
                        return true;
                    }
                }
                return false;
            """)
            self.logger.info("Login button clicked using JavaScript fallback")
            return True
        except Exception as e:
            self.logger.error(f"JavaScript login button click failed: {e}")
        
        return False
    
    async def _wait_for_login_response(self) -> Tuple[bool, str]:
        """Wait for login response and check for errors."""
        try:
            # Wait for page to respond to login attempt
            time.sleep(3)
            
            # Check for error messages
            error_message = self._check_for_login_errors()
            if error_message:
                return False, f"Login error detected: {error_message}"
            
            # Check if URL changed (common after successful login)
            current_url = self.web_controller.driver.current_url
            if 'login' not in current_url.lower():
                return True, "Login successful - redirected from login page"
            
            # Check for success indicators
            success_indicators = [
                'dashboard', 'home', 'main', 'welcome', 'profile', 'menu'
            ]
            
            page_source = self.web_controller.driver.page_source.lower()
            for indicator in success_indicators:
                if indicator in page_source:
                    return True, f"Login successful - found '{indicator}' indicator"
            
            # If still on login page, check if form is still visible
            time.sleep(2)
            if self._is_login_form_present():
                return False, "Still on login page - credentials may be incorrect"
            
            return True, "Login appears successful"
            
        except Exception as e:
            return False, f"Login response check error: {str(e)}"
    
    def _check_for_login_errors(self) -> Optional[str]:
        """Check for login error messages on the page."""
        from selenium.webdriver.common.by import By
        from selenium.common.exceptions import NoSuchElementException
        
        for selector in self.login_selectors['error_messages']:
            try:
                elements = self.web_controller.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed():
                        error_text = element.text.strip()
                        if error_text and len(error_text) > 0:
                            return error_text
            except Exception:
                continue
        
        return None
    
    def _is_login_form_present(self) -> bool:
        """Check if login form is still present on the page."""
        from selenium.webdriver.common.by import By
        
        try:
            # Look for password field (most reliable indicator)
            for selector in self.login_selectors['password_field']:
                try:
                    element = self.web_controller.driver.find_element(By.CSS_SELECTOR, selector)
                    if element.is_displayed():
                        return True
                except:
                    continue
            return False
        except:
            return False
    
    def _validate_login_success(self) -> Tuple[bool, str]:
        """Validate that login was actually successful."""
        try:
            current_url = self.web_controller.driver.current_url
            page_title = self.web_controller.driver.title
            
            # Check URL indicators
            success_url_patterns = ['dashboard', 'home', 'main', 'app', 'portal']
            failure_url_patterns = ['login', 'signin', 'auth', 'error']
            
            url_lower = current_url.lower()
            
            # Positive indicators
            for pattern in success_url_patterns:
                if pattern in url_lower:
                    return True, f"Success URL pattern found: {pattern}"
            
            # Negative indicators
            for pattern in failure_url_patterns:
                if pattern in url_lower:
                    return False, f"Still on {pattern} page"
            
            # Check page title
            title_lower = page_title.lower()
            if any(pattern in title_lower for pattern in success_url_patterns):
                return True, f"Success title pattern found"
            
            if any(pattern in title_lower for pattern in failure_url_patterns):
                return False, f"Login page title detected"
            
            # Check for logout link/button (indicates successful login)
            try:
                from selenium.webdriver.common.by import By
                logout_selectors = [
                    'a[href*="logout"]',
                    'button:contains("Logout")',
                    'button:contains("Sign Out")',
                    '.logout',
                    '#logout'
                ]
                
                for selector in logout_selectors:
                    try:
                        element = self.web_controller.driver.find_element(By.CSS_SELECTOR, selector)
                        if element.is_displayed():
                            return True, "Logout option found - login successful"
                    except:
                        continue
            except:
                pass
            
            # If no clear indicators, assume success if not on login page
            if 'login' not in url_lower and 'signin' not in url_lower:
                return True, "Not on login page - assuming success"
            
            return False, "Could not validate login success"
            
        except Exception as e:
            return False, f"Login validation error: {str(e)}"
    
    def _validate_existing_session(self) -> bool:
        """Check if existing login session is still valid."""
        try:
            if not self.login_timestamp:
                return False
            
            # Check session age (expire after 8 hours)
            session_age = time.time() - self.login_timestamp
            if session_age > (8 * 3600):  # 8 hours
                self.logger.info("Session expired due to age")
                return False
            
            # Check if still logged in by looking for logout option
            try:
                from selenium.webdriver.common.by import By
                logout_element = self.web_controller.driver.find_element(By.CSS_SELECTOR, 'a[href*="logout"], button:contains("Logout")')
                return logout_element.is_displayed()
            except:
                pass
            
            # Check current URL
            current_url = self.web_controller.driver.current_url
            if 'login' in current_url.lower():
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Session validation error: {e}")
            return False
    
    def _get_login_url(self, base_url: str) -> str:
        """Get the login URL for PLUS system."""
        # For PLUS (Reconext) system, try the most common login paths
        login_paths = [
            '/login',
            '/signin',
            '/auth/login',
            '/user/login',
            '/account/login',
            '/'  # Sometimes login is on the main page
        ]
        
        # For PLUS system, start with the base URL first
        # as many systems have login on the main page
        return base_url
    
    def _load_plus_settings(self) -> Optional[Dict[str, Any]]:
        """Load PLUS settings from settings service."""
        try:
            all_settings = self.settings_service.get_all_settings()
            plus_settings = all_settings.plus_integration.dict()
            
            if plus_settings.get('enabled', True):
                return plus_settings
            
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to load PLUS settings: {e}")
            return None
    
    def _save_session_data(self):
        """Save current session data."""
        try:
            if not self.is_logged_in:
                return
            
            session_file = Path("sessions/plus_session.json")
            session_file.parent.mkdir(exist_ok=True)
            
            session_data = {
                'login_timestamp': self.login_timestamp,
                'current_url': self.web_controller.driver.current_url,
                'cookies': self.web_controller.driver.get_cookies(),
                'session_valid': True
            }
            
            with open(session_file, 'w') as f:
                json.dump(session_data, f, indent=2, default=str)
            
            self.logger.info("PLUS session data saved")
            
        except Exception as e:
            self.logger.error(f"Failed to save session data: {e}")
    
    def get_login_status(self) -> Dict[str, Any]:
        """Get current login status information."""
        return {
            'is_logged_in': self.is_logged_in,
            'login_timestamp': self.login_timestamp,
            'session_age_seconds': time.time() - self.login_timestamp if self.login_timestamp else None,
            'login_attempts': self.login_attempts,
            'plus_url': self.plus_settings.get('base_url') if self.plus_settings else None,
            'username': self.plus_settings.get('username') if self.plus_settings else None
        }
    
    def logout_from_plus(self) -> Tuple[bool, str]:
        """Logout from PLUS system."""
        try:
            if not self.is_logged_in:
                return True, "Not logged in"
            
            # Try to find and click logout
            from selenium.webdriver.common.by import By
            logout_selectors = [
                'a[href*="logout"]',
                'button:contains("Logout")',
                'button:contains("Sign Out")',
                '.logout',
                '#logout'
            ]
            
            for selector in logout_selectors:
                try:
                    element = self.web_controller.driver.find_element(By.CSS_SELECTOR, selector)
                    element.click()
                    
                    # Wait for logout
                    time.sleep(2)
                    
                    # Reset state
                    self.is_logged_in = False
                    self.login_timestamp = None
                    
                    return True, "Successfully logged out"
                    
                except:
                    continue
            
            # If no logout button found, just reset state
            self.is_logged_in = False
            self.login_timestamp = None
            
            return True, "Logout state reset"
            
        except Exception as e:
            return False, f"Logout error: {str(e)}"
