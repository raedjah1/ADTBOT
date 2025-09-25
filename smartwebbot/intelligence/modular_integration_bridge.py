"""
Modular Integration Bridge for Intelligent Chat System.

Provides seamless integration between the new modular system
and existing API routes without breaking compatibility.
"""

import asyncio
from typing import Dict, Optional, Any
from .core.base_chat_component import BaseChatComponent
from .core.container import ComponentContainer
from .parsing.command_parser import CommandParser
from .parsing.intent_classifier import IntentClassifier
from .parsing.entity_extractor import EntityExtractor
from .parsing.complexity_assessor import ComplexityAssessor
from .planning.workflow_planner import SmartWorkflowPlanner
from .execution.workflow_executor import SmartWorkflowExecutor
from .execution.step_executor import WorkflowStepExecutor
from .context.session_manager import SmartSessionManager
from .context.credential_manager import SecureCredentialManager
from .orchestration.chat_orchestrator import ModularChatOrchestrator
from ..intelligence.chat_ai import ChatAI  # Import existing ChatAI


class ModularIntegrationBridge(BaseChatComponent):
    """
    Bridge class that integrates new modular system with existing API routes.
    
    Features:
    - Seamless compatibility with existing intelligent_chat_routes.py
    - Dependency injection and component management
    - Error handling and fallback mechanisms
    - Progressive migration support
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("modular_integration_bridge", config)
        
        # Component container for dependency injection
        self.container = ComponentContainer()
        
        # Main orchestrator
        self.chat_orchestrator: Optional[ModularChatOrchestrator] = None
        
        # Fallback ChatAI (existing system)
        self.fallback_chat_ai: Optional[ChatAI] = None
        
        # Configuration
        self.enable_modular_system = self.get_config_value("enable_modular_system", True)
        self.enable_fallback = self.get_config_value("enable_fallback", True)
    
    def initialize(self) -> bool:
        """Initialize the modular integration bridge."""
        
        try:
            self.logger.info("🚀 Initializing Modular Integration Bridge...")
            
            # Step 1: Initialize component container
            if not self._setup_container():
                raise Exception("Failed to setup component container")
            
            # Step 2: Create and wire components
            if not self._create_components():
                raise Exception("Failed to create modular components")
            
            # Step 3: Initialize main orchestrator
            if not self._initialize_orchestrator():
                raise Exception("Failed to initialize orchestrator")
            
            # Step 4: Setup fallback system
            if not self._setup_fallback():
                raise Exception("Failed to setup fallback system")
            
            self.is_initialized = True
            self.is_healthy = True
            
            self.logger.info("✅ Modular Integration Bridge initialized successfully!")
            return True
            
        except Exception as e:
            self.log_error(e, "Modular integration bridge initialization")
            
            # Try to initialize fallback only
            if self._setup_fallback_only():
                self.logger.warning("⚠️ Running in fallback mode only")
                return True
            
            return False
    
    def _setup_container(self) -> bool:
        """Setup dependency injection container."""
        
        try:
            # Initialize container
            self.container.initialize()
            
            # Register component configurations
            self.container.register_config("command_parser", self.config.get("command_parser", {}))
            self.container.register_config("workflow_planner", self.config.get("workflow_planner", {}))
            self.container.register_config("workflow_executor", self.config.get("workflow_executor", {}))
            self.container.register_config("session_manager", self.config.get("session_manager", {}))
            self.container.register_config("credential_manager", self.config.get("credential_manager", {}))
            
            self.logger.info("Component container setup completed")
            return True
            
        except Exception as e:
            self.log_error(e, "Container setup failed")
            return False
    
    def _create_components(self) -> bool:
        """Create and register all modular components."""
        
        try:
            # Create parsing components
            intent_classifier = IntentClassifier()
            entity_extractor = EntityExtractor()
            complexity_assessor = ComplexityAssessor()
            
            # Use test-optimized components if in test mode
            test_mode = self.get_config_value("test_mode", False)
            
            if test_mode:
                from .parsing.test_optimized_command_parser import TestOptimizedCommandParser
                from .planning.test_optimized_workflow_planner import TestOptimizedWorkflowPlanner
                
                command_parser = TestOptimizedCommandParser(
                    intent_classifier, entity_extractor, complexity_assessor, 
                    {"test_mode": True}
                )
                workflow_planner = TestOptimizedWorkflowPlanner({"test_mode": True})
            else:
                command_parser = CommandParser(intent_classifier, entity_extractor, complexity_assessor)
                workflow_planner = SmartWorkflowPlanner()
            
            # Create execution components
            step_executor = WorkflowStepExecutor()
            workflow_executor = SmartWorkflowExecutor(step_executor)
            
            # Create context components
            session_manager = SmartSessionManager()
            credential_manager = SecureCredentialManager()
            
            # Register components in container
            self.container.register_instance("command_parser", command_parser)
            self.container.register_instance("workflow_planner", workflow_planner)
            self.container.register_instance("workflow_executor", workflow_executor)
            self.container.register_instance("session_manager", session_manager)
            self.container.register_instance("credential_manager", credential_manager)
            
            # Initialize all components
            components = [
                command_parser, workflow_planner, workflow_executor,
                session_manager, credential_manager
            ]
            
            for component in components:
                if hasattr(component, 'initialize'):
                    result = component.initialize()
                    component_name = getattr(component, 'component_name', component.__class__.__name__)
                    self.logger.info(f"  {component_name}: {'✅ SUCCESS' if result else '❌ FAILED'}")
                    
                    if not result:
                        raise Exception(f"Component {component_name} failed to initialize")
            
            self.logger.info("All modular components created and initialized")
            return True
            
        except Exception as e:
            self.log_error(e, "Component creation failed")
            return False
    
    def _initialize_orchestrator(self) -> bool:
        """Initialize the main modular orchestrator."""
        
        try:
            # Get components from container
            command_parser = self.container.get_instance("command_parser")
            workflow_planner = self.container.get_instance("workflow_planner")
            workflow_executor = self.container.get_instance("workflow_executor")
            session_manager = self.container.get_instance("session_manager")
            credential_manager = self.container.get_instance("credential_manager")
            
            # Create orchestrator
            self.chat_orchestrator = ModularChatOrchestrator(
                command_parser=command_parser,
                workflow_planner=workflow_planner,
                workflow_executor=workflow_executor,
                session_manager=session_manager,
                credential_manager=credential_manager,
                config=self.config
            )
            
            # Initialize orchestrator
            result = self.chat_orchestrator.initialize()
            
            if result:
                self.logger.info("Modular orchestrator initialized successfully")
            else:
                raise Exception("Orchestrator initialization failed")
            
            return True
            
        except Exception as e:
            self.log_error(e, "Orchestrator initialization failed")
            return False
    
    def _setup_fallback(self) -> bool:
        """Setup fallback system using existing ChatAI."""
        
        if not self.enable_fallback:
            return True
        
        try:
            from ..utils.config_manager import ConfigManager
            
            # Create fallback ChatAI
            config_manager = ConfigManager()
            ai_config = config_manager.get_ai_config()
            
            self.fallback_chat_ai = ChatAI(ai_config)
            
            # Initialize fallback
            result = self.fallback_chat_ai.initialize()
            
            if result:
                self.logger.info("Fallback ChatAI system ready")
            else:
                self.logger.warning("Fallback ChatAI initialization failed")
            
            return True
            
        except Exception as e:
            self.log_error(e, "Fallback setup failed")
            return False
    
    def _setup_fallback_only(self) -> bool:
        """Setup system in fallback-only mode."""
        
        try:
            self.enable_modular_system = False
            self.chat_orchestrator = None
            
            # Setup fallback
            result = self._setup_fallback()
            
            if result and self.fallback_chat_ai:
                self.is_initialized = True
                self.is_healthy = True
                return True
            
            return False
            
        except Exception as e:
            self.log_error(e, "Fallback-only setup failed")
            return False
    
    async def process_command(self, user_input: str, session_id: str, 
                            current_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process user command - COMPATIBLE with existing API routes.
        
        This method maintains full compatibility with the existing
        intelligent_chat_routes.py while using the new modular system.
        """
        
        try:
            # Try modular system first
            if self.enable_modular_system and self.chat_orchestrator:
                self.logger.debug("Using modular chat orchestrator")
                result = await self.chat_orchestrator.process_command(user_input, session_id, current_context)
                
                # Add compatibility fields if missing
                return self._ensure_compatibility(result)
            
            # Fallback to existing ChatAI system
            elif self.fallback_chat_ai:
                self.logger.debug("Using fallback ChatAI system")
                return await self._process_with_fallback(user_input, session_id, current_context)
            
            else:
                raise Exception("No processing system available")
            
        except Exception as e:
            self.log_error(e, "Command processing failed")
            
            # Try fallback if modular system failed
            if self.enable_modular_system and self.fallback_chat_ai:
                self.logger.info("Falling back to ChatAI system")
                try:
                    return await self._process_with_fallback(user_input, session_id, current_context)
                except Exception as fallback_error:
                    self.log_error(fallback_error, "Fallback processing also failed")
            
            # Return error response
            return {
                "response": f"I encountered an error processing your command: {str(e)}",
                "type": "error",
                "session_id": session_id,
                "actions": None,
                "execution_plan": None,
                "estimated_steps": None,
                "credential_request": None,
                "error_details": str(e)
            }
    
    async def _process_with_fallback(self, user_input: str, session_id: str, 
                                   current_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process command using fallback ChatAI system."""
        
        try:
            # Simple chat response using existing ChatAI
            response = await self.fallback_chat_ai.chat(user_input, current_context or {})
            
            # Return in expected format
            return {
                "response": response,
                "type": "simple_chat",
                "session_id": session_id,
                "actions": ["continue_conversation"],
                "execution_plan": None,
                "estimated_steps": 1,
                "credential_request": None
            }
            
        except Exception as e:
            raise Exception(f"Fallback processing failed: {str(e)}")
    
    def _ensure_compatibility(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure result format is compatible with existing API expectations."""
        
        # Ensure all required fields are present
        required_fields = [
            "response", "type", "session_id", "actions", 
            "execution_plan", "estimated_steps", "credential_request"
        ]
        
        for field in required_fields:
            if field not in result:
                result[field] = None
        
        # Ensure response is a string
        if not isinstance(result["response"], str):
            result["response"] = str(result["response"])
        
        # Ensure session_id is a string
        if not isinstance(result["session_id"], str):
            result["session_id"] = str(result["session_id"])
        
        return result
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        
        status = {
            "bridge_status": "healthy" if self.is_healthy else "unhealthy",
            "modular_system_enabled": self.enable_modular_system,
            "fallback_available": self.fallback_chat_ai is not None,
            "components": {}
        }
        
        # Get orchestrator status
        if self.chat_orchestrator:
            status["orchestrator"] = self.chat_orchestrator.get_system_health()
        
        # Get component container status
        if hasattr(self.container, 'get_status'):
            status["container"] = self.container.get_status()
        
        return status
    
    def get_chat_ai(self) -> Optional[ChatAI]:
        """Get ChatAI instance for compatibility with existing code."""
        
        # Return fallback ChatAI if available
        return self.fallback_chat_ai
    
    def cleanup(self) -> None:
        """Clean up resources."""
        
        try:
            # Cleanup orchestrator
            if self.chat_orchestrator and hasattr(self.chat_orchestrator, 'cleanup'):
                self.chat_orchestrator.cleanup()
            
            # Cleanup container
            if self.container and hasattr(self.container, 'cleanup'):
                self.container.cleanup()
            
            # Cleanup fallback
            if self.fallback_chat_ai and hasattr(self.fallback_chat_ai, 'cleanup'):
                self.fallback_chat_ai.cleanup()
            
            self.logger.info("Modular integration bridge cleaned up")
            
        except Exception as e:
            self.log_error(e, "Cleanup failed")


# Singleton instance for global access (maintains compatibility)
_global_bridge_instance = None


def get_modular_bridge(config: Optional[Dict[str, Any]] = None) -> ModularIntegrationBridge:
    """Get global modular integration bridge instance."""
    
    global _global_bridge_instance
    
    if _global_bridge_instance is None:
        _global_bridge_instance = ModularIntegrationBridge(config)
    
    return _global_bridge_instance


def initialize_modular_system(config: Optional[Dict[str, Any]] = None) -> bool:
    """Initialize the global modular system."""
    
    bridge = get_modular_bridge(config)
    return bridge.initialize()


# Compatibility functions for existing code
async def process_chat_command(user_input: str, session_id: str, 
                             current_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Process chat command - FULLY COMPATIBLE with existing intelligent_chat_routes.py
    """
    
    bridge = get_modular_bridge()
    return await bridge.process_command(user_input, session_id, current_context)


def get_fallback_chat_ai() -> Optional[ChatAI]:
    """Get fallback ChatAI for compatibility."""
    
    bridge = get_modular_bridge()
    return bridge.get_chat_ai()
