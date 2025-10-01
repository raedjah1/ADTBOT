"""
AI Vision Service

Provides real-time website analysis and element detection using AI.
Handles visual analysis, element identification, and action suggestions.
"""

import asyncio
import base64
import json
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from PIL import Image
import io

from ..intelligence.chat_ai import ChatAI
from ..intelligence.ai_detector import AIElementDetector
from ..automation.web_controller import WebController
from ..utils.config_manager import get_config_manager
from ..utils.logger import BotLogger

class AIVisionService:
    """
    AI-powered vision service for real-time website analysis.
    
    Features:
    - Real-time website analysis
    - Element detection and classification
    - Action suggestion based on visual context
    - Screenshot analysis with AI
    - Interactive element mapping
    """
    
    def __init__(self):
        self.logger = BotLogger().get_logger("ai_vision_service")
        self.config_manager = get_config_manager()
        
        # AI components
        self._chat_ai: Optional[ChatAI] = None
        self._element_detector: Optional[AIElementDetector] = None
        self._web_controller: Optional[WebController] = None
        
        # Configuration
        self._config = self._load_config()
        
        # Current analysis state
        self._current_url = None
        self._current_analysis = None
        self._element_map = {}
        self._action_suggestions = []
    
    def _load_config(self) -> Dict[str, Any]:
        """Load AI vision configuration."""
        return {
            "provider": self.config_manager.get("ai.provider", "ollama"),
            "model": self.config_manager.get("ai.model", "gemma3:4b"),
            "ai_endpoint": self.config_manager.get("ai.ai_endpoint", "http://localhost:11434"),
            "confidence_threshold": self.config_manager.get("ai.confidence_threshold", 0.8),
            "max_elements": self.config_manager.get("ai.max_elements", 50),
            "analysis_depth": self.config_manager.get("ai.analysis_depth", "detailed")
        }
    
    async def initialize(self) -> bool:
        """Initialize the AI vision service."""
        try:
            self.logger.info("Initializing AI Vision Service...")
            
            # Initialize Web Controller first (needed for Element Detector)
            self.logger.info("Initializing Web Controller...")
            self._web_controller = WebController(self._config)
            if not self._web_controller.initialize():
                self.logger.error("Failed to initialize Web Controller")
                return False
            self.logger.info("Web Controller initialized successfully")
            
            # Initialize Chat AI
            self.logger.info("Initializing Chat AI...")
            self._chat_ai = ChatAI(self._config)
            if not self._chat_ai.initialize():
                self.logger.error("Failed to initialize Chat AI")
                return False
            self.logger.info("Chat AI initialized successfully")
            
            # Initialize Element Detector (needs driver from web controller)
            self.logger.info("Initializing Element Detector...")
            if self._web_controller and self._web_controller.driver:
                self._element_detector = AIElementDetector(
                    self._web_controller.driver, 
                    self._config
                )
                if not self._element_detector.initialize():
                    self.logger.error("Failed to initialize Element Detector")
                    return False
                self.logger.info("Element Detector initialized successfully")
            else:
                self.logger.error("Cannot initialize Element Detector: Web Controller driver not available")
                return False
            
            self.logger.info("AI Vision Service initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize AI Vision Service: {e}")
            import traceback
            self.logger.error(f"Full traceback: {traceback.format_exc()}")
            return False
    
    async def analyze_website(self, url: str, analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """
        Perform comprehensive website analysis.
        
        Args:
            url: Website URL to analyze
            analysis_type: Type of analysis (quick, detailed, comprehensive)
            
        Returns:
            Dict containing analysis results
        """
        try:
            self.logger.info(f"Starting website analysis: {url}")
            
            # Check if web controller is initialized
            if self._web_controller is None:
                self.logger.error("Web controller is not initialized")
                raise Exception("Web controller is not initialized. Service initialization may have failed.")
            
            # Navigate to website
            if not self._web_controller.navigate_to(url):
                raise Exception(f"Failed to navigate to {url}")
            
            self._current_url = url
            
            # Take screenshot
            screenshot_path = self._web_controller.take_screenshot(f"analysis_{int(datetime.now().timestamp())}")
            
            # Get page source
            page_source = self._web_controller.driver.page_source
            
            # Perform AI analysis
            analysis = await self._perform_ai_analysis(url, screenshot_path, page_source, analysis_type)
            
            # Detect elements
            elements = await self._detect_elements()
            
            # Generate action suggestions
            actions = await self._generate_action_suggestions(analysis, elements)
            
            # Compile results
            result = {
                "url": url,
                "analysis_type": analysis_type,
                "timestamp": datetime.now().isoformat(),
                "screenshot_path": screenshot_path,
                "analysis": analysis,
                "elements": elements,
                "action_suggestions": actions,
                "page_info": {
                    "title": self._web_controller.driver.title,
                    "url": self._web_controller.driver.current_url,
                    "viewport_size": self._web_controller.driver.get_window_size()
                }
            }
            
            self._current_analysis = result
            self.logger.info(f"Website analysis completed: {url}")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Website analysis failed: {e}")
            raise
    
    async def _perform_ai_analysis(self, url: str, screenshot_path: str, page_source: str, analysis_type: str) -> Dict[str, Any]:
        """Perform AI analysis of the website."""
        try:
            # Create analysis prompt
            prompt = f"""
            Analyze this website: {url}
            
            Analysis Type: {analysis_type}
            
            Please provide a comprehensive analysis including:
            
            1. **Website Overview**:
               - Purpose and functionality
               - Target audience
               - Main features and sections
            
            2. **Interactive Elements**:
               - Forms and input fields
               - Buttons and clickable elements
               - Navigation menus
               - Links and CTAs
            
            3. **Content Structure**:
               - Headers and text content
               - Images and media
               - Data tables
               - Lists and structured content
            
            4. **Automation Opportunities**:
               - Potential tasks that could be automated
               - Form filling opportunities
               - Data extraction possibilities
               - Navigation workflows
            
            5. **Technical Details**:
               - Page structure and layout
               - Element selectors and identifiers
               - Dynamic content areas
               - Potential challenges for automation
            
            Be specific and actionable. Focus on elements that can be automated.
            """
            
            # Get AI analysis
            response = await self._chat_ai.chat(prompt)
            
            # Parse response into structured format
            analysis = {
                "overview": self._extract_section(response.get("response", ""), "Website Overview"),
                "interactive_elements": self._extract_section(response.get("response", ""), "Interactive Elements"),
                "content_structure": self._extract_section(response.get("response", ""), "Content Structure"),
                "automation_opportunities": self._extract_section(response.get("response", ""), "Automation Opportunities"),
                "technical_details": self._extract_section(response.get("response", ""), "Technical Details"),
                "confidence": response.get("confidence", 0.0),
                "raw_analysis": response.get("response", "")
            }
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"AI analysis failed: {e}")
            return {"error": str(e), "confidence": 0.0}
    
    async def _detect_elements(self) -> List[Dict[str, Any]]:
        """Detect and classify page elements."""
        try:
            elements = []
            
            # Get all interactive elements
            interactive_elements = self._web_controller.driver.find_elements("css selector", 
                "input, button, select, textarea, a[href], [onclick], [role='button']")
            
            for i, element in enumerate(interactive_elements[:self._config["max_elements"]]):
                try:
                    element_info = {
                        "id": f"element_{i}",
                        "tag": element.tag_name,
                        "type": element.get_attribute("type") or "unknown",
                        "text": element.text.strip()[:100],
                        "placeholder": element.get_attribute("placeholder") or "",
                        "value": element.get_attribute("value") or "",
                        "href": element.get_attribute("href") or "",
                        "class": element.get_attribute("class") or "",
                        "id_attr": element.get_attribute("id") or "",
                        "name": element.get_attribute("name") or "",
                        "role": element.get_attribute("role") or "",
                        "is_displayed": element.is_displayed(),
                        "is_enabled": element.is_enabled(),
                        "location": element.location,
                        "size": element.size,
                        "selector": self._generate_selector(element)
                    }
                    
                    # Classify element type
                    element_info["category"] = self._classify_element(element_info)
                    
                    # Generate action suggestions for this element
                    element_info["suggested_actions"] = self._suggest_element_actions(element_info)
                    
                    elements.append(element_info)
                    
                except Exception as e:
                    self.logger.warning(f"Failed to analyze element {i}: {e}")
                    continue
            
            return elements
            
        except Exception as e:
            self.logger.error(f"Element detection failed: {e}")
            return []
    
    def _classify_element(self, element_info: Dict[str, Any]) -> str:
        """Classify element type based on its properties."""
        tag = element_info["tag"].lower()
        element_type = element_info["type"].lower()
        role = element_info["role"].lower()
        
        if tag == "input":
            if element_type in ["text", "email", "password", "search"]:
                return "text_input"
            elif element_type in ["checkbox", "radio"]:
                return "selection_input"
            elif element_type in ["submit", "button"]:
                return "button"
            elif element_type == "file":
                return "file_input"
            else:
                return "input"
        elif tag == "button":
            return "button"
        elif tag == "select":
            return "dropdown"
        elif tag == "textarea":
            return "text_area"
        elif tag == "a":
            return "link"
        elif role == "button":
            return "button"
        else:
            return "unknown"
    
    def _suggest_element_actions(self, element_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Suggest actions for a specific element."""
        actions = []
        category = element_info["category"]
        
        if category == "text_input":
            actions.extend([
                {"action": "fill_form", "description": f"Fill {element_info['placeholder'] or 'text field'}"},
                {"action": "clear_field", "description": "Clear the field"},
                {"action": "validate_input", "description": "Validate input format"}
            ])
        elif category == "button":
            actions.extend([
                {"action": "click_element", "description": f"Click {element_info['text'] or 'button'}"},
                {"action": "hover_element", "description": "Hover over button"},
                {"action": "check_state", "description": "Check if button is enabled"}
            ])
        elif category == "link":
            actions.extend([
                {"action": "click_element", "description": f"Click link: {element_info['text']}"},
                {"action": "get_href", "description": "Get link destination"},
                {"action": "open_new_tab", "description": "Open in new tab"}
            ])
        elif category == "dropdown":
            actions.extend([
                {"action": "select_option", "description": "Select dropdown option"},
                {"action": "get_options", "description": "Get available options"},
                {"action": "clear_selection", "description": "Clear selection"}
            ])
        
        return actions
    
    def _generate_selector(self, element) -> str:
        """Generate a CSS selector for the element."""
        try:
            # Try ID first
            if element.get_attribute("id"):
                return f"#{element.get_attribute('id')}"
            
            # Try name
            if element.get_attribute("name"):
                return f"[name='{element.get_attribute('name')}']"
            
            # Try class
            if element.get_attribute("class"):
                classes = element.get_attribute("class").split()
                if classes:
                    return f".{classes[0]}"
            
            # Fallback to tag
            return element.tag_name
            
        except:
            return "unknown"
    
    def _extract_section(self, text: str, section_name: str) -> str:
        """Extract a specific section from AI response."""
        try:
            lines = text.split('\n')
            in_section = False
            section_content = []
            
            for line in lines:
                if section_name.lower() in line.lower() and ':' in line:
                    in_section = True
                    continue
                elif in_section and line.strip().startswith('**') and ':' in line:
                    break
                elif in_section and line.strip():
                    section_content.append(line.strip())
            
            return '\n'.join(section_content) if section_content else "No information available"
            
        except:
            return "Error extracting section"
    
    async def _generate_action_suggestions(self, analysis: Dict[str, Any], elements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate high-level action suggestions based on analysis."""
        try:
            suggestions = []
            
            # Count element types
            element_counts = {}
            for element in elements:
                category = element["category"]
                element_counts[category] = element_counts.get(category, 0) + 1
            
            # Generate suggestions based on what's found
            if element_counts.get("text_input", 0) > 0:
                suggestions.append({
                    "action": "fill_forms",
                    "description": f"Fill {element_counts['text_input']} form fields",
                    "confidence": 0.9,
                    "elements_affected": element_counts["text_input"]
                })
            
            if element_counts.get("button", 0) > 0:
                suggestions.append({
                    "action": "click_buttons",
                    "description": f"Interact with {element_counts['button']} buttons",
                    "confidence": 0.8,
                    "elements_affected": element_counts["button"]
                })
            
            if element_counts.get("link", 0) > 0:
                suggestions.append({
                    "action": "navigate_links",
                    "description": f"Navigate through {element_counts['link']} links",
                    "confidence": 0.7,
                    "elements_affected": element_counts["link"]
                })
            
            # Add AI-generated suggestions
            if analysis.get("automation_opportunities"):
                suggestions.append({
                    "action": "ai_suggested_workflow",
                    "description": "Execute AI-suggested automation workflow",
                    "confidence": analysis.get("confidence", 0.5),
                    "details": analysis["automation_opportunities"]
                })
            
            return suggestions
            
        except Exception as e:
            self.logger.error(f"Action suggestion generation failed: {e}")
            return []
    
    async def execute_action(self, action: str, element_id: str = None, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute a specific action on the current page."""
        try:
            if not self._web_controller or not self._web_controller.driver:
                raise Exception("Web controller not initialized")
            
            parameters = parameters or {}
            result = {"success": False, "action": action, "timestamp": datetime.now().isoformat()}
            
            if action == "click_element" and element_id:
                element = self._web_controller.driver.find_element("css selector", element_id)
                element.click()
                result["success"] = True
                result["message"] = f"Clicked element: {element_id}"
                
            elif action == "fill_form" and element_id and "value" in parameters:
                element = self._web_controller.driver.find_element("css selector", element_id)
                element.clear()
                element.send_keys(parameters["value"])
                result["success"] = True
                result["message"] = f"Filled element {element_id} with: {parameters['value']}"
                
            elif action == "navigate_to" and "url" in parameters:
                success = self._web_controller.navigate_to(parameters["url"])
                result["success"] = success
                result["message"] = f"Navigated to: {parameters['url']}"
                
            elif action == "take_screenshot":
                filename = parameters.get("filename", f"screenshot_{int(datetime.now().timestamp())}")
                screenshot_path = self._web_controller.take_screenshot(filename)
                result["success"] = True
                result["message"] = f"Screenshot saved: {screenshot_path}"
                result["screenshot_path"] = screenshot_path
                
            else:
                result["error"] = f"Unknown action: {action}"
            
            return result
            
        except Exception as e:
            self.logger.error(f"Action execution failed: {e}")
            return {"success": False, "error": str(e), "action": action}
    
    async def get_current_state(self) -> Dict[str, Any]:
        """Get current page state and analysis."""
        if not self._current_analysis:
            return {"error": "No analysis available"}
        
        return {
            "url": self._current_url,
            "analysis": self._current_analysis,
            "timestamp": datetime.now().isoformat()
        }
    
    async def cleanup(self) -> bool:
        """Cleanup AI vision service resources."""
        try:
            if self._web_controller:
                self._web_controller.cleanup()
            
            if self._chat_ai:
                self._chat_ai.cleanup()
            
            self.logger.info("AI Vision Service cleanup completed")
            return True
            
        except Exception as e:
            self.logger.error(f"AI Vision Service cleanup failed: {e}")
            return False

# Global service instance
_ai_vision_service: Optional[AIVisionService] = None

async def get_ai_vision_service() -> AIVisionService:
    """Get or create AI vision service instance."""
    global _ai_vision_service
    
    if _ai_vision_service is None:
        _ai_vision_service = AIVisionService()
        if not await _ai_vision_service.initialize():
            raise Exception("Failed to initialize AI Vision Service")
    
    return _ai_vision_service
