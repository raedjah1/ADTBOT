"""
Main SmartWebBot engine that orchestrates all components.

This is the primary interface for the intelligent web automation system.
"""

import time
import asyncio
from typing import Dict, List, Optional, Any, Union, Callable
from pathlib import Path
from contextlib import contextmanager

from ..core.base_component import BaseComponent
from ..intelligence.ai_detector import AIElementDetector
from ..intelligence.decision_engine import DecisionEngine, ActionDecision, PageContext
from ..automation.web_controller import WebController
from ..automation.form_handler import FormHandler
from ..automation.navigation_manager import NavigationManager
from ..data.extractor import DataExtractor
from ..data.exporter import DataExporter
from ..utils.config_manager import get_config_manager
from ..utils.logger import BotLogger, log_performance, log_error


class SmartWebBot(BaseComponent):
    """
    Advanced intelligent web automation bot.
    
    Features:
    - AI-powered element detection
    - Intelligent decision making
    - Adaptive behavior
    - Error recovery
    - Performance optimization
    - Security features
    - Extensible plugin system
    """
    
    def __init__(self, config_path: str = None, **kwargs):
        """
        Initialize the SmartWebBot.
        
        Args:
            config_path: Path to configuration file
            **kwargs: Additional configuration options
        """
        super().__init__("smartwebbot", kwargs)
        
        # Load configuration
        self.config_manager = get_config_manager()
        if config_path:
            self.config_manager.config_path = Path(config_path)
            self.config_manager.load_configuration()
        
        # Initialize core components
        self.web_controller = None
        self.ai_detector = None
        self.decision_engine = None
        self.form_handler = None
        self.navigation_manager = None
        self.data_extractor = None
        self.data_exporter = None
        
        # Bot state
        self.current_task = None
        self.task_history = []
        self.performance_metrics = {}
        
        # Event handlers
        self.event_handlers = {}
        
        # Plugin system
        self.plugins = {}
        
    def initialize(self) -> bool:
        """Initialize the SmartWebBot and all components."""
        try:
            start_time = time.time()
            self.logger.info("Initializing SmartWebBot v2.0")
            
            # Initialize core components
            if not self._initialize_components():
                return False
            
            # Load plugins
            self._load_plugins()
            
            # Setup event handlers
            self._setup_event_handlers()
            
            # Validate system
            if not self._validate_system():
                return False
            
            initialization_time = time.time() - start_time
            log_performance("smartwebbot", "initialization", initialization_time, success=True)
            
            self.is_initialized = True
            self.logger.info(f"SmartWebBot initialized successfully in {initialization_time:.2f}s")
            
            return True
            
        except Exception as e:
            log_error("smartwebbot", e, {"operation": "initialization"})
            return False
    
    def cleanup(self) -> bool:
        """Clean up all bot resources."""
        try:
            self.logger.info("Cleaning up SmartWebBot")
            
            # Cleanup components in reverse order
            components = [
                self.data_exporter,
                self.data_extractor,
                self.navigation_manager,
                self.form_handler,
                self.decision_engine,
                self.ai_detector,
                self.web_controller
            ]
            
            for component in components:
                if component and hasattr(component, 'cleanup'):
                    try:
                        component.cleanup()
                    except Exception as e:
                        self.logger.warning(f"Component cleanup failed: {e}")
            
            # Save performance metrics
            self._save_performance_metrics()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Bot cleanup failed: {e}")
            return False
    
    def _initialize_components(self) -> bool:
        """Initialize all bot components."""
        try:
            # Web Controller (browser management)
            self.web_controller = WebController(self.config.get('web_controller', {}))
            if not self.web_controller.initialize():
                self.logger.error("Failed to initialize web controller")
                return False
            
            # AI Element Detector
            self.ai_detector = AIElementDetector(
                self.web_controller.driver, 
                self.config.get('ai_detector', {})
            )
            if not self.ai_detector.initialize():
                self.logger.error("Failed to initialize AI detector")
                return False
            
            # Decision Engine
            self.decision_engine = DecisionEngine(self.config.get('decision_engine', {}))
            if not self.decision_engine.initialize():
                self.logger.error("Failed to initialize decision engine")
                return False
            
            # Form Handler
            self.form_handler = FormHandler(
                self.web_controller.driver,
                self.ai_detector,
                self.config.get('form_handler', {})
            )
            if not self.form_handler.initialize():
                self.logger.error("Failed to initialize form handler")
                return False
            
            # Navigation Manager
            self.navigation_manager = NavigationManager(
                self.web_controller,
                self.decision_engine,
                self.config.get('navigation_manager', {})
            )
            if not self.navigation_manager.initialize():
                self.logger.error("Failed to initialize navigation manager")
                return False
            
            # Data Extractor
            self.data_extractor = DataExtractor(
                self.web_controller.driver,
                self.ai_detector,
                self.config.get('data_extractor', {})
            )
            if not self.data_extractor.initialize():
                self.logger.error("Failed to initialize data extractor")
                return False
            
            # Data Exporter
            self.data_exporter = DataExporter(self.config.get('data_exporter', {}))
            if not self.data_exporter.initialize():
                self.logger.error("Failed to initialize data exporter")
                return False
            
            # Credential Manager removed
            
            self.logger.info("All components initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Component initialization failed: {e}")
            return False
    
    def navigate_to(self, url: str, wait_for_load: bool = True) -> bool:
        """
        Navigate to a URL with intelligent waiting and error handling.
        
        Args:
            url: URL to navigate to
            wait_for_load: Wait for page to fully load
        
        Returns:
            bool: True if navigation successful
        """
        try:
            start_time = time.time()
            self.logger.info(f"Navigating to: {url}")
            
            # Use navigation manager for intelligent navigation
            success = self.navigation_manager.navigate_to(url, wait_for_load)
            
            if success:
                # Analyze page context
                context = self.decision_engine.analyze_page_context(self.web_controller.driver)
                self.logger.info(f"Page type detected: {context.page_type}")
                
                # Trigger navigation event
                self._trigger_event('navigation_completed', {
                    'url': url,
                    'context': context,
                    'duration': time.time() - start_time
                })
            
            return success
            
        except Exception as e:
            log_error("smartwebbot", e, {"operation": "navigate", "url": url})
            return False
    
    def perform_task(self, task_description: str, **kwargs) -> Dict[str, Any]:
        """
        Perform a high-level task using AI and decision making.
        
        Args:
            task_description: Natural language description of the task
            **kwargs: Additional task parameters
        
        Returns:
            Dict containing task results and metadata
        """
        try:
            start_time = time.time()
            self.logger.info(f"Performing task: {task_description}")
            
            # Analyze current page context
            context = self.decision_engine.analyze_page_context(self.web_controller.driver)
            
            # Make decision about the task
            decision = self.decision_engine.decide_action(task_description, context)
            
            # Execute the decision
            result = self._execute_decision(decision, task_description, **kwargs)
            
            # Record task completion
            task_duration = time.time() - start_time
            task_record = {
                'description': task_description,
                'decision': decision,
                'result': result,
                'duration': task_duration,
                'timestamp': time.time(),
                'context': context
            }
            
            self.task_history.append(task_record)
            
            # Update decision engine with outcome
            self.decision_engine.record_outcome(result.get('success', False), result.get('error'))
            
            log_performance("smartwebbot", "perform_task", task_duration, 
                          success=result.get('success', False))
            
            return result
            
        except Exception as e:
            log_error("smartwebbot", e, {"operation": "perform_task", "description": task_description})
            return {
                'success': False,
                'error': str(e),
                'timestamp': time.time()
            }
    
    def find_element_intelligently(self, description: str, element_type: str = None) -> Optional[Any]:
        """
        Find an element using AI-powered detection.
        
        Args:
            description: Natural language description of the element
            element_type: Type hint for the element
        
        Returns:
            WebElement if found, None otherwise
        """
        try:
            return self.ai_detector.find_element_intelligently(description, element_type)
        except Exception as e:
            log_error("smartwebbot", e, {"operation": "find_element", "description": description})
            return None
    
    def click_element(self, selector_or_description: str, intelligent: bool = True) -> bool:
        """
        Click an element using selector or intelligent detection.
        
        Args:
            selector_or_description: CSS selector or natural language description
            intelligent: Use AI detection if True
        
        Returns:
            bool: True if click successful
        """
        try:
            start_time = time.time()
            
            if intelligent:
                # Use AI detection
                element = self.find_element_intelligently(selector_or_description, "button")
                if element:
                    # Get optimal timing
                    context = self.decision_engine.analyze_page_context(self.web_controller.driver)
                    delay = self.decision_engine.decide_timing("click", context)
                    
                    # Perform click with human-like behavior
                    success = self._perform_human_like_click(element, delay)
                    
                    duration = time.time() - start_time
                    log_performance("smartwebbot", "click_element", duration, success=success)
                    
                    return success
            else:
                # Use traditional selector-based approach
                from selenium.webdriver.common.by import By
                element = self.web_controller.driver.find_element(By.CSS_SELECTOR, selector_or_description)
                element.click()
                return True
            
            return False
            
        except Exception as e:
            log_error("smartwebbot", e, {"operation": "click_element", "selector": selector_or_description})
            return False
    
    def fill_form_intelligently(self, form_data: Dict[str, str], form_description: str = None) -> bool:
        """
        Fill a form using intelligent field detection.
        
        Args:
            form_data: Dictionary of field descriptions/names to values
            form_description: Optional description of the form
        
        Returns:
            bool: True if form filled successfully
        """
        try:
            return self.form_handler.fill_form_intelligently(form_data, form_description)
        except Exception as e:
            log_error("smartwebbot", e, {"operation": "fill_form", "form_data": list(form_data.keys())})
            return False
    
    def extract_data_intelligently(self, data_description: str, 
                                 extraction_rules: Dict = None) -> List[Dict[str, Any]]:
        """
        Extract data from the current page using AI.
        
        Args:
            data_description: Description of data to extract
            extraction_rules: Optional extraction rules
        
        Returns:
            List of extracted data records
        """
        try:
            return self.data_extractor.extract_data_intelligently(data_description, extraction_rules)
        except Exception as e:
            log_error("smartwebbot", e, {"operation": "extract_data", "description": data_description})
            return []
    
    def wait_intelligently(self, condition_description: str, timeout: int = 30) -> bool:
        """
        Wait for a condition using intelligent detection.
        
        Args:
            condition_description: Description of the condition to wait for
            timeout: Maximum time to wait in seconds
        
        Returns:
            bool: True if condition met within timeout
        """
        try:
            start_time = time.time()
            
            while time.time() - start_time < timeout:
                # Check if condition is met using AI
                if self._check_condition(condition_description):
                    return True
                
                # Intelligent wait interval
                context = self.decision_engine.analyze_page_context(self.web_controller.driver)
                wait_interval = self.decision_engine.decide_timing("wait", context)
                time.sleep(min(wait_interval, 1.0))
            
            return False
            
        except Exception as e:
            log_error("smartwebbot", e, {"operation": "wait", "condition": condition_description})
            return False
    
    def take_screenshot(self, filename: str = None, full_page: bool = False) -> str:
        """
        Take a screenshot with intelligent naming.
        
        Args:
            filename: Optional filename
            full_page: Take full page screenshot
        
        Returns:
            str: Path to screenshot file
        """
        try:
            if not filename:
                # Generate intelligent filename
                context = self.decision_engine.analyze_page_context(self.web_controller.driver)
                timestamp = int(time.time())
                filename = f"{context.page_type}_{timestamp}.png"
            
            return self.web_controller.take_screenshot(filename, full_page)
            
        except Exception as e:
            log_error("smartwebbot", e, {"operation": "screenshot"})
            return ""
    
    def get_performance_report(self) -> Dict[str, Any]:
        """
        Get comprehensive performance report.
        
        Returns:
            Dict containing performance metrics
        """
        try:
            # Component metrics
            component_metrics = {}
            for name, component in [
                ('web_controller', self.web_controller),
                ('ai_detector', self.ai_detector),
                ('decision_engine', self.decision_engine),
                ('form_handler', self.form_handler),
                ('navigation_manager', self.navigation_manager),
                ('data_extractor', self.data_extractor)
            ]:
                if component:
                    component_metrics[name] = component.get_state()
            
            # Browser performance
            browser_performance = self.web_controller.get_page_performance()
            
            # Task history summary
            task_summary = {
                'total_tasks': len(self.task_history),
                'successful_tasks': sum(1 for task in self.task_history if task['result'].get('success', False)),
                'average_task_duration': sum(task['duration'] for task in self.task_history) / len(self.task_history) if self.task_history else 0
            }
            
            return {
                'component_metrics': component_metrics,
                'browser_performance': browser_performance,
                'task_summary': task_summary,
                'system_metrics': self.get_state()
            }
            
        except Exception as e:
            log_error("smartwebbot", e, {"operation": "performance_report"})
            return {}
    
    def register_plugin(self, name: str, plugin_class: type, config: Dict = None) -> bool:
        """
        Register a plugin with the bot.
        
        Args:
            name: Plugin name
            plugin_class: Plugin class
            config: Plugin configuration
        
        Returns:
            bool: True if plugin registered successfully
        """
        try:
            plugin_instance = plugin_class(config or {})
            
            # Initialize plugin if it has an initialize method
            if hasattr(plugin_instance, 'initialize'):
                if not plugin_instance.initialize():
                    self.logger.error(f"Failed to initialize plugin: {name}")
                    return False
            
            self.plugins[name] = plugin_instance
            self.logger.info(f"Plugin registered: {name}")
            
            return True
            
        except Exception as e:
            log_error("smartwebbot", e, {"operation": "register_plugin", "plugin": name})
            return False
    
    def execute_plugin(self, plugin_name: str, method_name: str, *args, **kwargs) -> Any:
        """
        Execute a plugin method.
        
        Args:
            plugin_name: Name of the plugin
            method_name: Method to execute
            *args: Method arguments
            **kwargs: Method keyword arguments
        
        Returns:
            Method result
        """
        try:
            if plugin_name not in self.plugins:
                raise ValueError(f"Plugin not found: {plugin_name}")
            
            plugin = self.plugins[plugin_name]
            
            if not hasattr(plugin, method_name):
                raise ValueError(f"Method not found: {method_name}")
            
            method = getattr(plugin, method_name)
            return method(*args, **kwargs)
            
        except Exception as e:
            log_error("smartwebbot", e, {"operation": "execute_plugin", "plugin": plugin_name})
            return None
    
    def add_event_handler(self, event_name: str, handler: Callable) -> bool:
        """
        Add an event handler.
        
        Args:
            event_name: Name of the event
            handler: Handler function
        
        Returns:
            bool: True if handler added successfully
        """
        try:
            if event_name not in self.event_handlers:
                self.event_handlers[event_name] = []
            
            self.event_handlers[event_name].append(handler)
            return True
            
        except Exception as e:
            log_error("smartwebbot", e, {"operation": "add_event_handler", "event": event_name})
            return False
    
    def _execute_decision(self, decision: ActionDecision, task_description: str, **kwargs) -> Dict[str, Any]:
        """Execute a decision made by the decision engine."""
        try:
            action_type = decision.action_type.value
            
            # Execute based on action type
            if action_type == "click":
                success = self.click_element(task_description, intelligent=True)
            elif action_type == "fill":
                form_data = kwargs.get('form_data', {})
                success = self.fill_form_intelligently(form_data, task_description)
            elif action_type == "navigate":
                url = kwargs.get('url', '')
                success = self.navigate_to(url)
            elif action_type == "wait":
                seconds = decision.parameters.get('seconds', 1)
                time.sleep(seconds)
                success = True
            elif action_type == "extract":
                data = self.extract_data_intelligently(task_description)
                success = len(data) > 0
            else:
                success = False
            
            return {
                'success': success,
                'action_type': action_type,
                'confidence': decision.confidence,
                'reasoning': decision.reasoning,
                'timestamp': time.time()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'action_type': decision.action_type.value,
                'timestamp': time.time()
            }
    
    def _perform_human_like_click(self, element, delay: float) -> bool:
        """Perform a click with human-like behavior."""
        try:
            # Scroll to element
            self.web_controller.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            
            # Random delay before click
            time.sleep(delay)
            
            # Hover before click (human-like)
            from selenium.webdriver.common.action_chains import ActionChains
            actions = ActionChains(self.web_controller.driver)
            actions.move_to_element(element).pause(0.1).click().perform()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Human-like click failed: {e}")
            return False
    
    def _check_condition(self, condition_description: str) -> bool:
        """Check if a condition is met using AI."""
        try:
            # Use AI detector to check for condition
            element = self.ai_detector.find_element_intelligently(condition_description)
            return element is not None
        except:
            return False
    
    def _trigger_event(self, event_name: str, event_data: Dict):
        """Trigger an event and call all registered handlers."""
        try:
            if event_name in self.event_handlers:
                for handler in self.event_handlers[event_name]:
                    try:
                        handler(event_data)
                    except Exception as e:
                        self.logger.warning(f"Event handler failed: {e}")
        except Exception as e:
            self.logger.error(f"Event trigger failed: {e}")
    
    def _load_plugins(self):
        """Load plugins from the plugins directory."""
        try:
            plugins_dir = Path("smartwebbot/plugins")
            if plugins_dir.exists():
                # Plugin loading logic would go here
                pass
        except Exception as e:
            self.logger.warning(f"Plugin loading failed: {e}")
    
    def _setup_event_handlers(self):
        """Setup default event handlers."""
        try:
            # Add default event handlers
            self.add_event_handler('navigation_completed', self._on_navigation_completed)
            self.add_event_handler('task_completed', self._on_task_completed)
            self.add_event_handler('error_occurred', self._on_error_occurred)
        except Exception as e:
            self.logger.warning(f"Event handler setup failed: {e}")
    
    def _validate_system(self) -> bool:
        """Validate that all systems are working correctly."""
        try:
            # Check browser connectivity
            if not self.web_controller.is_browser_active():
                self.logger.error("Browser is not active")
                return False
            
            # Test navigation
            test_url = "https://httpbin.org/html"
            if not self.navigate_to(test_url):
                self.logger.error("Navigation test failed")
                return False
            
            self.logger.info("System validation passed")
            return True
            
        except Exception as e:
            self.logger.error(f"System validation failed: {e}")
            return False
    
    def _save_performance_metrics(self):
        """Save performance metrics to file."""
        try:
            metrics_file = Path("logs/performance_metrics.json")
            metrics_file.parent.mkdir(exist_ok=True)
            
            import json
            with open(metrics_file, 'w') as f:
                json.dump(self.get_performance_report(), f, indent=2, default=str)
            
            self.logger.info(f"Performance metrics saved to {metrics_file}")
            
        except Exception as e:
            self.logger.warning(f"Failed to save performance metrics: {e}")
    
    def _on_navigation_completed(self, event_data: Dict):
        """Handle navigation completed event."""
        self.logger.debug(f"Navigation completed: {event_data['url']}")
    
    def _on_task_completed(self, event_data: Dict):
        """Handle task completed event."""
        self.logger.debug(f"Task completed: {event_data.get('description', 'Unknown')}")
    
    def _on_error_occurred(self, event_data: Dict):
        """Handle error occurred event."""
        self.logger.warning(f"Error occurred: {event_data.get('error', 'Unknown error')}")
    
    def __enter__(self):
        """Context manager entry."""
        if not self.activate():
            raise RuntimeError("Failed to activate SmartWebBot")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.deactivate()
        
        if exc_type is not None:
            self.logger.error(f"SmartWebBot exited with exception: {exc_val}")
            return False
        
        return True


# Convenience functions for quick usage
def create_bot(config_path: str = None, **kwargs) -> SmartWebBot:
    """
    Create and initialize a SmartWebBot instance.
    
    Args:
        config_path: Path to configuration file
        **kwargs: Additional configuration options
    
    Returns:
        Initialized SmartWebBot instance
    """
    bot = SmartWebBot(config_path, **kwargs)
    if bot.initialize():
        return bot
    else:
        raise RuntimeError("Failed to initialize SmartWebBot")

@contextmanager
def smart_bot(config_path: str = None, **kwargs):
    """
    Context manager for SmartWebBot.
    
    Args:
        config_path: Path to configuration file
        **kwargs: Additional configuration options
    
    Yields:
        SmartWebBot instance
    """
    bot = create_bot(config_path, **kwargs)
    try:
        yield bot
    finally:
        bot.cleanup()
