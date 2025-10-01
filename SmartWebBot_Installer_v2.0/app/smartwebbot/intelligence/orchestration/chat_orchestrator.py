"""
Modular Chat Orchestrator - The New Intelligent Brain

This replaces the monolithic intelligent_chat_orchestrator.py with
a clean, modular design that coordinates all components perfectly.
"""

import time
from typing import Dict, List, Optional, Any
from ..core.base_chat_component import BaseChatComponent
from ..core.interfaces import (
    ICommandParser, IWorkflowPlanner, IWorkflowExecutor, 
    ISessionManager, ICredentialManager, IEventDispatcher,
    IParsedCommand, IWorkflowPlan, ISessionContext
)
from ..core.events import ChatEvent, InMemoryEventDispatcher


class ModularChatOrchestrator(BaseChatComponent):
    """
    Modular chat orchestrator that coordinates all intelligence components.
    
    This is the NEW brain - much smaller, cleaner, and more powerful
    than the old monolithic version.
    """
    
    def __init__(self, 
                 command_parser: ICommandParser,
                 workflow_planner: IWorkflowPlanner, 
                 workflow_executor: IWorkflowExecutor,
                 session_manager: ISessionManager,
                 credential_manager: ICredentialManager,
                 config: Optional[Dict[str, Any]] = None):
        super().__init__("modular_chat_orchestrator", config)
        
        # Injected dependencies (perfect separation!)
        self.command_parser = command_parser
        self.workflow_planner = workflow_planner
        self.workflow_executor = workflow_executor
        self.session_manager = session_manager
        self.credential_manager = credential_manager
        
        # Event system
        self.event_dispatcher = InMemoryEventDispatcher()
        
        # Subscribe to events
        self._setup_event_subscriptions()
        
        # Configuration
        self.auto_execute_simple = self.get_config_value("auto_execute_simple", True)
        self.require_confirmation_complex = self.get_config_value("require_confirmation_complex", True)
    
    def initialize(self) -> bool:
        """Initialize the modular orchestrator."""
        try:
            self.logger.info("Initializing Modular Chat Orchestrator...")
            
            # Initialize all components
            components = [
                self.command_parser,
                self.workflow_planner, 
                self.workflow_executor,
                self.session_manager,
                self.credential_manager
            ]
            
            init_results = []
            for component in components:
                if hasattr(component, 'initialize'):
                    result = component.initialize()
                    component_name = getattr(component, 'component_name', component.__class__.__name__)
                    self.logger.info(f"  {component_name}: {'✅ SUCCESS' if result else '❌ FAILED'}")
                    init_results.append(result)
                else:
                    init_results.append(True)  # Assume OK if no initialize method
            
            if not all(init_results):
                raise Exception("Some components failed to initialize")
            
            self.is_initialized = True
            self.is_healthy = True
            self.logger.info("Modular Chat Orchestrator initialized successfully ✅")
            return True
            
        except Exception as e:
            self.log_error(e, "Modular orchestrator initialization")
            return False
    
    async def process_command(self, user_input: str, session_id: str, 
                            current_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process user command through modular pipeline.
        
        This is the main entry point - much cleaner than the old version!
        """
        start_time = time.time()
        
        try:
            self.logger.info(f"Processing command: {user_input[:100]}...")
            
            # Step 1: Parse command with modular parser
            await self.event_dispatcher.dispatch(
                ChatEvent.COMMAND_RECEIVED, 
                "modular_chat_orchestrator",
                session_id,
                {"user_input": user_input}
            )
            
            parsed_command = await self.command_parser.parse(user_input)
            
            await self.event_dispatcher.dispatch(
                ChatEvent.COMMAND_PARSED,
                "command_parser", 
                session_id,
                {"parsed_command": parsed_command.__dict__}
            )
            
            # Step 2: Get or create session context
            session_context = await self._get_session_context(session_id, parsed_command, current_context)
            
            # Step 3: Check credentials if needed
            if parsed_command.required_credentials:
                has_credentials = await self._check_credentials(session_context, parsed_command)
                if not has_credentials:
                    return await self._request_credentials(session_context, parsed_command)
            
            # Step 4: Create workflow plan
            workflow_plan = await self.workflow_planner.create_plan(parsed_command, session_context)
            
            await self.event_dispatcher.dispatch(
                ChatEvent.WORKFLOW_PLANNED,
                "workflow_planner",
                session_id, 
                {"plan": workflow_plan.__dict__}
            )
            
            # Step 5: Execute or return plan based on complexity
            if self._should_auto_execute(parsed_command, workflow_plan):
                return await self._execute_workflow(workflow_plan, session_context)
            else:
                return await self._return_execution_plan(workflow_plan, session_context)
            
        except Exception as e:
            self.log_error(e, f"Command processing failed for: {user_input}")
            
            # Return error response
            return {
                "response": f"I encountered an error processing your command: {str(e)}",
                "type": "error", 
                "session_id": session_id,
                "error_details": str(e)
            }
        finally:
            processing_time = time.time() - start_time
            self.log_success("Command processed", processing_time)
    
    async def _get_session_context(self, session_id: str, command: IParsedCommand, 
                                 current_context: Optional[Dict] = None) -> ISessionContext:
        """Get or create session context."""
        
        # Try to get existing session
        session_context = await self.session_manager.get_session(session_id)
        
        if not session_context:
            # Create new session
            new_session_id = await self.session_manager.create_session()
            session_context = await self.session_manager.get_session(new_session_id)
            
            await self.event_dispatcher.dispatch(
                ChatEvent.SESSION_CREATED,
                "session_manager",
                session_id,
                {"session_context": session_context.__dict__}
            )
        
        # Update context with current info
        if current_context:
            await self.session_manager.update_session(session_id, current_context)
            session_context = await self.session_manager.get_session(session_id)
        
        return session_context
    
    async def _check_credentials(self, context: ISessionContext, command: IParsedCommand) -> bool:
        """Check if required credentials are available."""
        
        if not command.target_platform:
            return True
        
        for cred_type in command.required_credentials:
            has_cred = await self.credential_manager.has_credentials(
                context.session_id, 
                command.target_platform,
                cred_type
            )
            if not has_cred:
                return False
        
        return True
    
    async def _request_credentials(self, context: ISessionContext, command: IParsedCommand) -> Dict[str, Any]:
        """Request credentials from user."""
        
        await self.event_dispatcher.dispatch(
            ChatEvent.CREDENTIALS_REQUIRED,
            "modular_chat_orchestrator",
            context.session_id,
            {"required_credentials": [c.value for c in command.required_credentials]}
        )
        
        return {
            "response": f"I need your credentials to access {command.target_platform}. Please provide them to continue.",
            "type": "credential_request",
            "session_id": context.session_id,
            "credential_request": {
                "platform": command.target_platform,
                "required_fields": [c.value for c in command.required_credentials],
                "request_id": f"cred_req_{int(time.time())}"
            }
        }
    
    def _should_auto_execute(self, command: IParsedCommand, plan: IWorkflowPlan) -> bool:
        """Determine if workflow should be auto-executed."""
        
        # Auto-execute simple commands
        if self.auto_execute_simple and command.complexity.value in ["simple", "moderate"]:
            return True
        
        # Require confirmation for complex workflows
        if self.require_confirmation_complex and command.complexity.value in ["complex", "advanced"]:
            return False
        
        # Check plan size
        if len(plan.steps) <= 3:
            return True
        
        return False
    
    async def _execute_workflow(self, plan: IWorkflowPlan, context: ISessionContext) -> Dict[str, Any]:
        """Execute workflow immediately."""
        
        await self.event_dispatcher.dispatch(
            ChatEvent.WORKFLOW_STARTED,
            "modular_chat_orchestrator", 
            context.session_id,
            {"plan_id": plan.plan_id}
        )
        
        # Execute workflow
        results = []
        async for result in self.workflow_executor.execute_workflow(plan, context):
            results.append(result)
        
        # Check if successful
        successful_steps = [r for r in results if r.success]
        failed_steps = [r for r in results if not r.success]
        
        if failed_steps:
            await self.event_dispatcher.dispatch(
                ChatEvent.WORKFLOW_FAILED,
                "workflow_executor",
                context.session_id,
                {"plan_id": plan.plan_id, "failed_steps": len(failed_steps)}
            )
            
            return {
                "response": f"Workflow partially completed. {len(successful_steps)} steps succeeded, {len(failed_steps)} failed.",
                "type": "execution_partial",
                "session_id": context.session_id,
                "results": [r.__dict__ for r in results],
                "success_count": len(successful_steps),
                "failure_count": len(failed_steps)
            }
        else:
            await self.event_dispatcher.dispatch(
                ChatEvent.WORKFLOW_COMPLETED,
                "workflow_executor", 
                context.session_id,
                {"plan_id": plan.plan_id, "total_steps": len(results)}
            )
            
            return {
                "response": f"Successfully completed: {plan.command.intent}",
                "type": "execution_complete",
                "session_id": context.session_id,
                "results": [r.__dict__ for r in results],
                "total_steps": len(results)
            }
    
    async def _return_execution_plan(self, plan: IWorkflowPlan, context: ISessionContext) -> Dict[str, Any]:
        """Return execution plan for user approval."""
        
        return {
            "response": f"I've created a plan to {plan.command.intent}. Here's what I'll do:",
            "type": "execution_plan",
            "session_id": context.session_id,
            "execution_plan": [
                {
                    "step_id": step.step_id,
                    "description": step.description, 
                    "type": step.step_type,
                    "parameters": step.parameters
                }
                for step in plan.steps
            ],
            "estimated_steps": len(plan.steps),
            "estimated_duration": plan.estimated_duration,
            "actions": ["confirm_execution"],
            "plan_id": plan.plan_id
        }
    
    def _setup_event_subscriptions(self) -> None:
        """Set up event subscriptions for monitoring."""
        
        # Subscribe to important events for logging
        self.event_dispatcher.subscribe(ChatEvent.COMMAND_PARSED, self._log_command_parsed)
        self.event_dispatcher.subscribe(ChatEvent.WORKFLOW_COMPLETED, self._log_workflow_completed)
        self.event_dispatcher.subscribe(ChatEvent.WORKFLOW_FAILED, self._log_workflow_failed)
    
    async def _log_command_parsed(self, event_data) -> None:
        """Log command parsing events."""
        parsed_command = event_data.data.get("parsed_command", {})
        self.logger.debug(f"Command parsed: {parsed_command.get('intent', 'unknown')}")
    
    async def _log_workflow_completed(self, event_data) -> None:
        """Log workflow completion events."""
        plan_id = event_data.data.get("plan_id")
        total_steps = event_data.data.get("total_steps", 0)
        self.logger.info(f"Workflow {plan_id} completed successfully with {total_steps} steps")
    
    async def _log_workflow_failed(self, event_data) -> None:
        """Log workflow failure events."""
        plan_id = event_data.data.get("plan_id")
        failed_steps = event_data.data.get("failed_steps", 0)
        self.logger.error(f"Workflow {plan_id} failed with {failed_steps} failed steps")
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get health status of all components."""
        health_status = {
            "orchestrator": self.get_health_status(),
            "components": {}
        }
        
        components = [
            ("command_parser", self.command_parser),
            ("workflow_planner", self.workflow_planner),
            ("workflow_executor", self.workflow_executor),
            ("session_manager", self.session_manager),
            ("credential_manager", self.credential_manager)
        ]
        
        for name, component in components:
            if hasattr(component, 'get_health_status'):
                health_status["components"][name] = component.get_health_status()
            else:
                health_status["components"][name] = {"status": "unknown"}
        
        return health_status
