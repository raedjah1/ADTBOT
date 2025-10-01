"""
PLUS Form Automation Module

Handles automated form filling for PLUS system forms, specifically
the Unit Receiving ADT form with intelligent field mapping and validation.
"""

import time
from typing import Dict, Any, Optional, List
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from ..utils.logger import get_logger


class PlusFormAutomator:
    """
    Automates form filling in PLUS system with intelligent field detection
    and error handling.
    """
    
    def __init__(self, web_controller, logger=None):
        """Initialize the form automator."""
        self.web_controller = web_controller
        self.logger = logger or get_logger(__name__)
        
        # Unit Receiving form field mappings
        self.unit_receiving_fields = {
            'trackingNo': {
                'selectors': [
                    '#MainContent_TextBox1',
                    'input[id="MainContent_TextBox1"]',
                    'input[name="ctl00$MainContent$TextBox1"]'
                ],
                'required': True,
                'type': 'text'
            },
            'rma': {
                'selectors': [
                    '#MainContent_TextBox2',
                    'input[id="MainContent_TextBox2"]',
                    'input[name="ctl00$MainContent$TextBox2"]'
                ],
                'required': False,
                'type': 'text'
            },
            'flaggedBoxes': {
                'selectors': [
                    '#ctl00_MainContent_ComboBox3_Input',
                    'input[id="ctl00_MainContent_ComboBox3_Input"]'
                ],
                'dropdown_selectors': [
                    '#ctl00_MainContent_ComboBox3_DropDown li.rcbItem'
                ],
                'required': True,
                'type': 'dropdown'
            },
            'techId': {
                'selectors': [
                    '#MainContent_TextBox4',
                    'input[id="MainContent_TextBox4"]',
                    'input[name="ctl00$MainContent$TextBox4"]'
                ],
                'required': True,
                'type': 'text'
            },
            'partNo': {
                'selectors': [
                    '#MainContent_TextBox5',
                    'input[id="MainContent_TextBox5"]',
                    'input[name="ctl00$MainContent$TextBox5"]'
                ],
                'required': True,
                'type': 'text'
            },
            'qtySerial': {
                'selectors': [
                    '#MainContent_TextBox6',
                    'input[id="MainContent_TextBox6"]',
                    'input[name="ctl00$MainContent$TextBox6"]'
                ],
                'required': False,
                'type': 'text'
            },
            'mac': {
                'selectors': [
                    '#MainContent_TextBox7',
                    'input[id="MainContent_TextBox7"]',
                    'input[name="ctl00$MainContent$TextBox7"]'
                ],
                'required': False,
                'type': 'text'
            },
            'imei': {
                'selectors': [
                    '#MainContent_TextBox8',
                    'input[id="MainContent_TextBox8"]',
                    'input[name="ctl00$MainContent$TextBox8"]'
                ],
                'required': False,
                'type': 'text'
            },
            'batteryRemoval': {
                'selectors': [
                    '#ctl00_MainContent_ComboBox9_Input',
                    'input[id="ctl00_MainContent_ComboBox9_Input"]'
                ],
                'dropdown_selectors': [
                    '#ctl00_MainContent_ComboBox9_DropDown li.rcbItem'
                ],
                'required': True,
                'type': 'dropdown'
            },
            'dateCode': {
                'selectors': [
                    '#MainContent_TextBox10',
                    'input[id="MainContent_TextBox10"]',
                    'input[name="ctl00$MainContent$TextBox10"]'
                ],
                'required': False,
                'type': 'text'
            },
            'dockLogId': {
                'selectors': [
                    '#MainContent_TextBox11',
                    'input[id="MainContent_TextBox11"]',
                    'input[name="ctl00$MainContent$TextBox11"]'
                ],
                'required': True,
                'type': 'text'
            },
            'disposition': {
                'selectors': [
                    '#MainContent_TextBox12',
                    'input[id="MainContent_TextBox12"]',
                    'input[name="ctl00$MainContent$TextBox12"]'
                ],
                'required': True,
                'type': 'text'
            }
        }
        
        # Form buttons
        self.form_buttons = {
            'process': {
                'selectors': [
                    '#ctl00_MainContent_AddButton_input',
                    'input[id="ctl00_MainContent_AddButton_input"]',
                    'input[value="Process"]'
                ]
            },
            'clear': {
                'selectors': [
                    '#MainContent_ClearButton',
                    'input[id="MainContent_ClearButton"]',
                    'input[value="Clear"]'
                ]
            }
        }
    
    def _find_element_by_selectors(self, selectors: List[str], timeout: int = 5):
        """Find an element using multiple selector strategies."""
        for selector in selectors:
            try:
                element = WebDriverWait(self.web_controller.driver, timeout).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                if element.is_displayed() and element.is_enabled():
                    return element
            except Exception as e:
                self.logger.debug(f"Selector failed: {selector} - {e}")
                continue
        return None
    
    def _fill_text_field(self, field_config: Dict, value: str, field_name: str) -> bool:
        """Fill a text input field."""
        element = self._find_element_by_selectors(field_config['selectors'])
        if not element:
            self.logger.error(f"Could not find {field_name} field")
            return False
        
        try:
            element.clear()
            element.send_keys(value)
            self.logger.info(f"SUCCESS: {field_name} filled with value: {value}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to fill {field_name}: {e}")
            return False
    
    def _fill_dropdown_field(self, field_config: Dict, value: str, field_name: str) -> bool:
        """Fill a dropdown field."""
        # First, click the dropdown input to open it
        input_element = self._find_element_by_selectors(field_config['selectors'])
        if not input_element:
            self.logger.error(f"Could not find {field_name} dropdown input")
            return False
        
        try:
            # Click to open dropdown
            input_element.click()
            time.sleep(0.5)  # Wait for dropdown to open
            
            # Find and click the correct option
            dropdown_items = self.web_controller.driver.find_elements(
                By.CSS_SELECTOR, field_config['dropdown_selectors'][0]
            )
            
            for item in dropdown_items:
                if item.text.strip().upper() == value.upper():
                    item.click()
                    self.logger.info(f"SUCCESS: {field_name} set to: {value}")
                    return True
            
            self.logger.error(f"Could not find option '{value}' in {field_name} dropdown")
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to fill {field_name} dropdown: {e}")
            return False
    
    def fill_unit_receiving_form(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fill the Unit Receiving ADT form with provided data.
        
        Args:
            form_data: Dictionary containing form field values
            
        Returns:
            Dict: Result with success status and details
        """
        try:
            self.logger.info("=== STARTING UNIT RECEIVING FORM AUTOMATION ===")
            
            filled_fields = []
            failed_fields = []
            skipped_fields = []
            
            # Process each field in the form data
            for field_name, value in form_data.items():
                if not value or (isinstance(value, str) and value.strip() == ''):
                    skipped_fields.append(field_name)
                    continue
                
                if field_name not in self.unit_receiving_fields:
                    self.logger.warning(f"Unknown field: {field_name}")
                    continue
                
                field_config = self.unit_receiving_fields[field_name]
                self.logger.info(f"Filling {field_name} with value: {value}")
                
                if field_config['type'] == 'text':
                    if self._fill_text_field(field_config, str(value), field_name):
                        filled_fields.append(field_name)
                    else:
                        failed_fields.append(field_name)
                        
                elif field_config['type'] == 'dropdown':
                    if self._fill_dropdown_field(field_config, str(value), field_name):
                        filled_fields.append(field_name)
                    else:
                        failed_fields.append(field_name)
                
                # Small delay between fields
                time.sleep(0.2)
            
            # Check required fields
            missing_required = []
            for field_name, field_config in self.unit_receiving_fields.items():
                if field_config['required']:
                    if field_name not in filled_fields and field_name not in form_data:
                        missing_required.append(field_name)
            
            # Take screenshot of filled form
            self.web_controller.take_screenshot("unit_receiving_form_filled.png")
            
            # Determine overall success
            success = len(failed_fields) == 0 and len(missing_required) == 0
            
            result = {
                'success': success,
                'filled_fields': filled_fields,
                'failed_fields': failed_fields,
                'skipped_fields': skipped_fields,
                'missing_required': missing_required,
                'total_fields': len(form_data),
                'message': self._generate_result_message(filled_fields, failed_fields, missing_required)
            }
            
            self.logger.info(f"Form automation completed: {result['message']}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error in form automation: {e}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            return {
                'success': False,
                'message': f"Form automation error: {str(e)}",
                'filled_fields': [],
                'failed_fields': [],
                'skipped_fields': [],
                'missing_required': []
            }
    
    def _generate_result_message(self, filled: List[str], failed: List[str], missing: List[str]) -> str:
        """Generate a human-readable result message."""
        if not failed and not missing:
            return f"SUCCESS: All {len(filled)} fields filled successfully"
        
        messages = []
        if filled:
            messages.append(f"{len(filled)} fields filled")
        if failed:
            messages.append(f"{len(failed)} fields failed")
        if missing:
            messages.append(f"{len(missing)} required fields missing")
        
        return "PARTIAL: " + ", ".join(messages)
    
    def submit_form(self) -> Dict[str, Any]:
        """Submit the Unit Receiving form."""
        try:
            self.logger.info("=== SUBMITTING UNIT RECEIVING FORM ===")
            
            # Find and click the Process button
            process_button = self._find_element_by_selectors(
                self.form_buttons['process']['selectors']
            )
            
            if not process_button:
                return {
                    'success': False,
                    'message': 'Could not find Process button'
                }
            
            # Take screenshot before submission
            self.web_controller.take_screenshot("unit_receiving_before_submit.png")
            
            # Click the Process button
            process_button.click()
            self.logger.info("Process button clicked")
            
            # Wait for form submission to complete
            time.sleep(2)
            
            # Take screenshot after submission
            self.web_controller.take_screenshot("unit_receiving_after_submit.png")
            
            return {
                'success': True,
                'message': 'Form submitted successfully',
                'current_url': self.web_controller.driver.current_url
            }
            
        except Exception as e:
            self.logger.error(f"Error submitting form: {e}")
            return {
                'success': False,
                'message': f"Form submission error: {str(e)}"
            }
    
    def clear_form(self) -> Dict[str, Any]:
        """Clear the Unit Receiving form."""
        try:
            clear_button = self._find_element_by_selectors(
                self.form_buttons['clear']['selectors']
            )
            
            if not clear_button:
                return {
                    'success': False,
                    'message': 'Could not find Clear button'
                }
            
            clear_button.click()
            self.logger.info("Form cleared")
            
            return {
                'success': True,
                'message': 'Form cleared successfully'
            }
            
        except Exception as e:
            self.logger.error(f"Error clearing form: {e}")
            return {
                'success': False,
                'message': f"Form clear error: {str(e)}"
            }
