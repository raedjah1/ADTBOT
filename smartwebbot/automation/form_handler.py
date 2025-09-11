"""
Intelligent form handling system.

Handles form detection, field mapping, and intelligent form filling.
"""

import time
from typing import Dict, List, Optional, Any
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webelement import WebElement
from ..core.base_component import BaseComponent


class FormHandler(BaseComponent):
    """
    Intelligent form handler with AI-powered field detection.
    """
    
    def __init__(self, driver, ai_detector, config: Dict = None):
        """Initialize the form handler."""
        super().__init__("form_handler", config)
        self.driver = driver
        self.ai_detector = ai_detector
        
    def initialize(self) -> bool:
        """Initialize the form handler."""
        self.is_initialized = True
        return True
    
    def cleanup(self) -> bool:
        """Clean up form handler."""
        return True
    
    def fill_form_intelligently(self, form_data: Dict[str, str], 
                               form_description: str = None) -> bool:
        """Fill a form using intelligent field detection."""
        try:
            success_count = 0
            total_fields = len(form_data)
            
            for field_description, value in form_data.items():
                if self._fill_field_intelligently(field_description, value):
                    success_count += 1
                    time.sleep(0.5)  # Brief pause between fields
            
            self.logger.info(f"Form filling: {success_count}/{total_fields} fields filled")
            return success_count == total_fields
            
        except Exception as e:
            self.logger.error(f"Form filling failed: {e}")
            return False
    
    def _fill_field_intelligently(self, field_description: str, value: str) -> bool:
        """Fill a single field using AI detection."""
        try:
            # Use AI detector to find the field
            element = self.ai_detector.find_element_intelligently(
                field_description, 
                element_type="input"
            )
            
            if element:
                # Handle different input types
                input_type = element.get_attribute("type") or "text"
                tag_name = element.tag_name.lower()
                
                if tag_name == "select":
                    return self._fill_select_field(element, value)
                elif input_type in ["text", "email", "password", "search", "tel", "url"]:
                    return self._fill_text_field(element, value)
                elif input_type == "checkbox":
                    return self._fill_checkbox_field(element, value)
                elif input_type == "radio":
                    return self._fill_radio_field(element, value)
                elif tag_name == "textarea":
                    return self._fill_textarea_field(element, value)
                else:
                    # Try generic text input
                    return self._fill_text_field(element, value)
            
            return False
            
        except Exception as e:
            self.logger.error(f"Field filling failed for '{field_description}': {e}")
            return False
    
    def _fill_text_field(self, element: WebElement, value: str) -> bool:
        """Fill a text input field."""
        try:
            element.clear()
            element.send_keys(value)
            return True
        except Exception as e:
            self.logger.error(f"Text field filling failed: {e}")
            return False
    
    def _fill_select_field(self, element: WebElement, value: str) -> bool:
        """Fill a select dropdown field."""
        try:
            select = Select(element)
            
            # Try by value first
            try:
                select.select_by_value(value)
                return True
            except:
                pass
            
            # Try by visible text
            try:
                select.select_by_visible_text(value)
                return True
            except:
                pass
            
            # Try partial text match
            for option in select.options:
                if value.lower() in option.text.lower():
                    select.select_by_visible_text(option.text)
                    return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Select field filling failed: {e}")
            return False
    
    def _fill_checkbox_field(self, element: WebElement, value: str) -> bool:
        """Fill a checkbox field."""
        try:
            should_check = value.lower() in ['true', 'yes', '1', 'on', 'checked']
            
            if should_check and not element.is_selected():
                element.click()
            elif not should_check and element.is_selected():
                element.click()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Checkbox field filling failed: {e}")
            return False
    
    def _fill_radio_field(self, element: WebElement, value: str) -> bool:
        """Fill a radio button field."""
        try:
            # For radio buttons, we need to find the specific option
            name = element.get_attribute("name")
            if name:
                radio_buttons = self.driver.find_elements(By.NAME, name)
                
                for radio in radio_buttons:
                    radio_value = radio.get_attribute("value") or ""
                    if value.lower() == radio_value.lower():
                        radio.click()
                        return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Radio field filling failed: {e}")
            return False
    
    
    def _fill_textarea_field(self, element: WebElement, value: str) -> bool:
        """Fill a textarea field."""
        try:
            element.clear()
            element.send_keys(value)
            return True
        except Exception as e:
            self.logger.error(f"Textarea field filling failed: {e}")
            return False
