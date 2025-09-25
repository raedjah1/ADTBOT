"""
Smart Workflow Executor for Intelligent Chat System.

Executes complete workflows with comprehensive error handling,
progress tracking, and real-time status updates.
"""

import asyncio
import time
from typing import Dict, List, Optional, Any, AsyncIterator
from ..core.base_chat_component import BaseChatComponent
from ..core.interfaces import (
    IWorkflowExecutor, IWorkflowPlan, ISessionContext,
    IExecutionResult, IStepExecutor, WorkflowStatus
)
from .step_executor import WorkflowStepExecutor
from .progress_tracker import ProgressTracker


class SmartWorkflowExecutor(BaseChatComponent, IWorkflowExecutor):
    """
    Smart workflow executor with comprehensive execution management.
    
    Features:
    - Step-by-step execution with real-time updates
    - Intelligent error handling and recovery
    - Progress tracking and reporting
    - Parallel execution where possible
    - Resource management and throttling
    """
    
    def __init__(self, step_executor: IStepExecutor = None, config: Optional[Dict[str, Any]] = None):
        super().__init__("smart_workflow_executor", config)
        
        # Inject step executor or create default
        self.step_executor = step_executor or WorkflowStepExecutor()
        self.progress_tracker = ProgressTracker()
        
        # Execution state
        self.active_workflows: Dict[str, Dict] = {}
        
        # Configuration
        self.max_concurrent_workflows = self.get_config_value("max_concurrent_workflows", 5)
        self.step_timeout_default = self.get_config_value("step_timeout_default", 30)
        self.enable_parallel_steps = self.get_config_value("enable_parallel_steps", True)
    
    def initialize(self) -> bool:
        """Initialize the workflow executor."""
        try:
            self.logger.info("Initializing Smart Workflow Executor...")
            
            # Initialize components
            components = [self.step_executor, self.progress_tracker]
            
            for component in components:
                if hasattr(component, 'initialize'):
                    result = component.initialize()
                    if not result:
                        raise Exception(f"Failed to initialize {component}")
            
            self.is_initialized = True
            self.is_healthy = True
            
            self.logger.info("Smart Workflow Executor initialized successfully")
            return True
            
        except Exception as e:
            self.log_error(e, "Workflow executor initialization")
            return False
    
    async def execute_workflow(self, plan: IWorkflowPlan, context: ISessionContext) -> AsyncIterator[IExecutionResult]:
        """Execute complete workflow with real-time updates."""
        
        if len(self.active_workflows) >= self.max_concurrent_workflows:
            raise Exception(f"Maximum concurrent workflows ({self.max_concurrent_workflows}) reached")
        
        # Initialize workflow execution
        execution_state = {
            "plan_id": plan.plan_id,
            "status": WorkflowStatus.RUNNING,
            "start_time": time.time(),
            "completed_steps": 0,
            "failed_steps": 0,
            "current_step": None
        }
        
        self.active_workflows[plan.plan_id] = execution_state
        
        try:
            self.logger.info(f"Starting workflow execution: {plan.plan_id}")
            
            # Start progress tracking
            await self.progress_tracker.start_tracking(plan.plan_id, len(plan.steps))
            
            # Execute steps
            async for result in self._execute_steps(plan, context, execution_state):
                yield result
            
            # Mark workflow as completed
            execution_state["status"] = WorkflowStatus.COMPLETED
            execution_state["end_time"] = time.time()
            
            self.logger.info(f"Workflow completed: {plan.plan_id}")
            
        except Exception as e:
            self.log_error(e, f"Workflow execution failed: {plan.plan_id}")
            execution_state["status"] = WorkflowStatus.FAILED
            execution_state["error"] = str(e)
            
            # Yield error result
            yield IExecutionResult(
                step_id="workflow_error",
                success=False,
                result_data={},
                error_message=str(e),
                execution_time=0,
                retry_count=0
            )
        
        finally:
            # Cleanup
            await self.progress_tracker.stop_tracking(plan.plan_id)
            if plan.plan_id in self.active_workflows:
                del self.active_workflows[plan.plan_id]
    
    async def pause_workflow(self, plan_id: str) -> bool:
        """Pause workflow execution."""
        if plan_id not in self.active_workflows:
            return False
        
        try:
            self.active_workflows[plan_id]["status"] = WorkflowStatus.PAUSED
            self.logger.info(f"Workflow paused: {plan_id}")
            return True
        except Exception as e:
            self.log_error(e, f"Failed to pause workflow: {plan_id}")
            return False
    
    async def resume_workflow(self, plan_id: str) -> bool:
        """Resume paused workflow."""
        if plan_id not in self.active_workflows:
            return False
        
        try:
            self.active_workflows[plan_id]["status"] = WorkflowStatus.RUNNING
            self.logger.info(f"Workflow resumed: {plan_id}")
            return True
        except Exception as e:
            self.log_error(e, f"Failed to resume workflow: {plan_id}")
            return False
    
    async def cancel_workflow(self, plan_id: str) -> bool:
        """Cancel workflow execution."""
        if plan_id not in self.active_workflows:
            return False
        
        try:
            self.active_workflows[plan_id]["status"] = WorkflowStatus.CANCELLED
            await self.progress_tracker.stop_tracking(plan_id)
            
            if plan_id in self.active_workflows:
                del self.active_workflows[plan_id]
            
            self.logger.info(f"Workflow cancelled: {plan_id}")
            return True
        except Exception as e:
            self.log_error(e, f"Failed to cancel workflow: {plan_id}")
            return False
    
    async def _execute_steps(self, plan: IWorkflowPlan, context: ISessionContext, 
                           execution_state: Dict) -> AsyncIterator[IExecutionResult]:
        """Execute workflow steps with dependency resolution."""
        
        completed_steps = set()
        failed_steps = set()
        
        # Create dependency graph
        dependency_graph = self._build_dependency_graph(plan.steps)
        
        while len(completed_steps) < len(plan.steps):
            # Check if workflow is paused
            if execution_state["status"] == WorkflowStatus.PAUSED:
                await asyncio.sleep(1)
                continue
            
            # Check if workflow is cancelled
            if execution_state["status"] == WorkflowStatus.CANCELLED:
                break
            
            # Find steps ready to execute
            ready_steps = self._get_ready_steps(plan.steps, dependency_graph, completed_steps, failed_steps)
            
            if not ready_steps:
                # No steps ready - check if we're blocked by failures
                if failed_steps:
                    self.logger.error(f"Workflow blocked by failed steps: {failed_steps}")
                    break
                else:
                    # Circular dependency or other issue
                    self.logger.error("No steps ready to execute - possible circular dependency")
                    break
            
            # Execute ready steps (parallel if enabled)
            if self.enable_parallel_steps and len(ready_steps) > 1:
                results = await self._execute_steps_parallel(ready_steps, context, execution_state)
            else:
                results = await self._execute_steps_sequential(ready_steps, context, execution_state)
            
            # Process results
            for result in results:
                if result.success:
                    completed_steps.add(result.step_id)
                    execution_state["completed_steps"] += 1
                else:
                    failed_steps.add(result.step_id)
                    execution_state["failed_steps"] += 1
                
                # Update progress
                await self.progress_tracker.update_progress(
                    plan.plan_id, 
                    len(completed_steps), 
                    len(plan.steps)
                )
                
                # Yield result
                yield result
    
    def _build_dependency_graph(self, steps: List) -> Dict[str, List[str]]:
        """Build dependency graph from workflow steps."""
        graph = {}
        
        for step in steps:
            graph[step.step_id] = step.dependencies[:]
        
        return graph
    
    def _get_ready_steps(self, steps: List, dependency_graph: Dict, 
                        completed_steps: set, failed_steps: set) -> List:
        """Get steps that are ready to execute."""
        ready_steps = []
        
        for step in steps:
            # Skip already processed steps
            if step.step_id in completed_steps or step.step_id in failed_steps:
                continue
            
            # Check if all dependencies are completed
            dependencies = dependency_graph.get(step.step_id, [])
            
            if not dependencies:
                # No dependencies - ready to execute
                ready_steps.append(step)
            else:
                # Check if all dependencies are completed
                if all(dep in completed_steps for dep in dependencies):
                    ready_steps.append(step)
        
        return ready_steps
    
    async def _execute_steps_sequential(self, steps: List, context: ISessionContext, 
                                      execution_state: Dict) -> List[IExecutionResult]:
        """Execute steps sequentially."""
        results = []
        
        for step in steps:
            execution_state["current_step"] = step.step_id
            result = await self.step_executor.execute(step, context)
            results.append(result)
            
            # Short delay between steps
            await asyncio.sleep(0.5)
        
        return results
    
    async def _execute_steps_parallel(self, steps: List, context: ISessionContext,
                                    execution_state: Dict) -> List[IExecutionResult]:
        """Execute steps in parallel where possible."""
        
        # Create execution tasks
        tasks = []
        for step in steps:
            task = asyncio.create_task(self.step_executor.execute(step, context))
            tasks.append(task)
        
        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                # Task failed with exception
                processed_results.append(IExecutionResult(
                    step_id=steps[i].step_id,
                    success=False,
                    result_data={},
                    error_message=str(result),
                    execution_time=0,
                    retry_count=0
                ))
            else:
                processed_results.append(result)
        
        return processed_results
    
    def get_workflow_status(self, plan_id: str) -> Optional[Dict[str, Any]]:
        """Get current status of workflow execution."""
        if plan_id not in self.active_workflows:
            return None
        
        execution_state = self.active_workflows[plan_id]
        
        return {
            "plan_id": plan_id,
            "status": execution_state["status"].value if hasattr(execution_state["status"], 'value') else str(execution_state["status"]),
            "start_time": execution_state.get("start_time"),
            "end_time": execution_state.get("end_time"),
            "completed_steps": execution_state.get("completed_steps", 0),
            "failed_steps": execution_state.get("failed_steps", 0),
            "current_step": execution_state.get("current_step"),
            "error": execution_state.get("error")
        }
    
    def get_active_workflows(self) -> List[Dict[str, Any]]:
        """Get all active workflow executions."""
        return [self.get_workflow_status(plan_id) for plan_id in self.active_workflows.keys()]
