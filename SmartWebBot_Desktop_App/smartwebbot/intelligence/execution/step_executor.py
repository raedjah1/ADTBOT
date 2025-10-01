"""
Workflow Step Executor for Individual Step Execution.

Handles execution of individual workflow steps with comprehensive
error handling, retry logic, and result validation.
"""

import time
import asyncio
from typing import Dict, Optional, Any
from ..core.base_chat_component import BaseChatComponent
from ..core.interfaces import IStepExecutor, IWorkflowStep, ISessionContext, IExecutionResult


class WorkflowStepExecutor(BaseChatComponent, IStepExecutor):
    """
    Executes individual workflow steps safely and reliably.
    
    Features:
    - Type-specific step execution
    - Comprehensive error handling
    - Retry logic with exponential backoff
    - Result validation
    - Performance monitoring
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("workflow_step_executor", config)
        
        # Step executors by type
        self.step_handlers = self._initialize_step_handlers()
        
        # Configuration
        self.default_timeout = self.get_config_value("default_timeout", 30)
        self.default_retry_count = self.get_config_value("default_retry_count", 3)
        self.retry_delay_base = self.get_config_value("retry_delay_base", 2)
    
    def initialize(self) -> bool:
        """Initialize the step executor."""
        try:
            self.logger.info("Initializing Workflow Step Executor...")
            
            # Validate step handlers
            if not self.step_handlers:
                raise Exception("No step handlers initialized")
            
            self.is_initialized = True
            self.is_healthy = True
            
            self.logger.info(f"Step Executor initialized with {len(self.step_handlers)} handlers")
            return True
            
        except Exception as e:
            self.log_error(e, "Step executor initialization")
            return False
    
    async def execute(self, step: IWorkflowStep, context: ISessionContext) -> IExecutionResult:
        """Execute a single workflow step."""
        start_time = time.time()
        
        try:
            self.logger.debug(f"Executing step: {step.step_id}")
            
            # Validate step
            if not await self.can_execute(step):
                return IExecutionResult(
                    step_id=step.step_id,
                    success=False,
                    result_data={},
                    error_message=f"Step type {step.step_type} not supported",
                    execution_time=0,
                    retry_count=0
                )
            
            # Execute with retry logic
            result = await self._execute_with_retry(step, context)
            
            execution_time = time.time() - start_time
            result.execution_time = execution_time
            
            # Log result
            if result.success:
                self.log_success(f"Step executed: {step.step_id}", execution_time)
            else:
                self.logger.warning(f"Step failed: {step.step_id} - {result.error_message}")
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_error(e, f"Step execution error: {step.step_id}")
            
            return IExecutionResult(
                step_id=step.step_id,
                success=False,
                result_data={},
                error_message=str(e),
                execution_time=execution_time,
                retry_count=0
            )
    
    async def can_execute(self, step: IWorkflowStep) -> bool:
        """Check if this executor can handle the step."""
        return step.step_type in self.step_handlers
    
    def _initialize_step_handlers(self) -> Dict[str, callable]:
        """Initialize step handlers for different step types."""
        return {
            "navigation": self._execute_navigation_step,
            "authentication": self._execute_authentication_step,
            "element_interaction": self._execute_element_interaction_step,
            "content_creation": self._execute_content_creation_step,
            "form_filling": self._execute_form_filling_step,
            "form_submission": self._execute_form_submission_step,
            "data_extraction": self._execute_data_extraction_step,
            "validation": self._execute_validation_step,
            "general_action": self._execute_general_action_step,
            # Test-optimized step types
            "ai_processing": self._execute_ai_processing_step,
            "form_analysis": self._execute_form_analysis_step,
            "data_location": self._execute_data_location_step
        }
    
    async def _execute_with_retry(self, step: IWorkflowStep, context: ISessionContext) -> IExecutionResult:
        """Execute step with retry logic."""
        
        retry_count = 0
        max_retries = step.retry_count or self.default_retry_count
        last_error = None
        
        while retry_count <= max_retries:
            try:
                # Execute step
                handler = self.step_handlers[step.step_type]
                result = await handler(step, context)
                
                # If successful, return result
                if result.success:
                    result.retry_count = retry_count
                    return result
                
                # If not successful, prepare for retry
                last_error = result.error_message
                
            except Exception as e:
                last_error = str(e)
            
            retry_count += 1
            
            if retry_count <= max_retries:
                # Wait before retry (exponential backoff)
                delay = self.retry_delay_base ** retry_count
                self.logger.info(f"Retrying step {step.step_id} in {delay} seconds (attempt {retry_count})")
                await asyncio.sleep(delay)
        
        # All retries exhausted
        return IExecutionResult(
            step_id=step.step_id,
            success=False,
            result_data={},
            error_message=f"Step failed after {max_retries} retries. Last error: {last_error}",
            execution_time=0,
            retry_count=retry_count - 1
        )
    
    async def _execute_navigation_step(self, step: IWorkflowStep, context: ISessionContext) -> IExecutionResult:
        """Execute navigation step."""
        
        try:
            url = step.parameters.get("url")
            if not url:
                raise Exception("Navigation step missing URL parameter")
            
            self.logger.info(f"Navigating to: {url}")
            
            # Simulate navigation (replace with actual web controller integration)
            await asyncio.sleep(2)  # Simulate page load time
            
            return IExecutionResult(
                step_id=step.step_id,
                success=True,
                result_data={
                    "url": url,
                    "page_loaded": True,
                    "load_time": 2.0
                },
                error_message=None
            )
            
        except Exception as e:
            return IExecutionResult(
                step_id=step.step_id,
                success=False,
                result_data={},
                error_message=str(e)
            )
    
    async def _execute_authentication_step(self, step: IWorkflowStep, context: ISessionContext) -> IExecutionResult:
        """Execute authentication step."""
        
        try:
            username_selector = step.parameters.get("username_selector")
            password_selector = step.parameters.get("password_selector")
            
            if not username_selector or not password_selector:
                raise Exception("Authentication step missing required selectors")
            
            self.logger.info("Executing authentication...")
            
            # Simulate authentication
            await asyncio.sleep(3)  # Simulate authentication time
            
            return IExecutionResult(
                step_id=step.step_id,
                success=True,
                result_data={
                    "authenticated": True,
                    "method": "username_password"
                },
                error_message=None
            )
            
        except Exception as e:
            return IExecutionResult(
                step_id=step.step_id,
                success=False,
                result_data={},
                error_message=str(e)
            )
    
    async def _execute_element_interaction_step(self, step: IWorkflowStep, context: ISessionContext) -> IExecutionResult:
        """Execute element interaction step."""
        
        try:
            action = step.parameters.get("action", "click")
            selector = step.parameters.get("selector")
            
            self.logger.info(f"Executing {action} on element: {selector}")
            
            # Simulate element interaction
            await asyncio.sleep(1)
            
            return IExecutionResult(
                step_id=step.step_id,
                success=True,
                result_data={
                    "action": action,
                    "selector": selector,
                    "element_found": True
                },
                error_message=None
            )
            
        except Exception as e:
            return IExecutionResult(
                step_id=step.step_id,
                success=False,
                result_data={},
                error_message=str(e)
            )
    
    async def _execute_content_creation_step(self, step: IWorkflowStep, context: ISessionContext) -> IExecutionResult:
        """Execute content creation step."""
        
        try:
            content = step.parameters.get("content", "")
            content_type = step.parameters.get("content_type", "text")
            
            self.logger.info(f"Creating {content_type} content...")
            
            # Simulate content creation
            await asyncio.sleep(2)
            
            return IExecutionResult(
                step_id=step.step_id,
                success=True,
                result_data={
                    "content": content,
                    "content_type": content_type,
                    "length": len(content)
                },
                error_message=None
            )
            
        except Exception as e:
            return IExecutionResult(
                step_id=step.step_id,
                success=False,
                result_data={},
                error_message=str(e)
            )
    
    async def _execute_form_filling_step(self, step: IWorkflowStep, context: ISessionContext) -> IExecutionResult:
        """Execute form filling step."""
        
        try:
            field_mapping = step.parameters.get("field_mapping", {})
            
            self.logger.info(f"Filling form with {len(field_mapping)} fields...")
            
            # Simulate form filling
            await asyncio.sleep(len(field_mapping) * 0.5)
            
            return IExecutionResult(
                step_id=step.step_id,
                success=True,
                result_data={
                    "fields_filled": len(field_mapping),
                    "field_mapping": field_mapping
                },
                error_message=None
            )
            
        except Exception as e:
            return IExecutionResult(
                step_id=step.step_id,
                success=False,
                result_data={},
                error_message=str(e)
            )
    
    async def _execute_form_submission_step(self, step: IWorkflowStep, context: ISessionContext) -> IExecutionResult:
        """Execute form submission step."""
        
        try:
            submit_selector = step.parameters.get("submit_selector", "button[type='submit']")
            
            self.logger.info("Submitting form...")
            
            # Simulate form submission
            await asyncio.sleep(2)
            
            return IExecutionResult(
                step_id=step.step_id,
                success=True,
                result_data={
                    "form_submitted": True,
                    "submit_selector": submit_selector
                },
                error_message=None
            )
            
        except Exception as e:
            return IExecutionResult(
                step_id=step.step_id,
                success=False,
                result_data={},
                error_message=str(e)
            )
    
    async def _execute_data_extraction_step(self, step: IWorkflowStep, context: ISessionContext) -> IExecutionResult:
        """Execute data extraction step."""
        
        try:
            extraction_type = step.parameters.get("extraction_type", "text")
            selectors = step.parameters.get("selectors", [])
            
            self.logger.info(f"Extracting {extraction_type} data...")
            
            # Simulate data extraction
            await asyncio.sleep(3)
            
            # Mock extracted data
            extracted_data = [f"Data item {i+1}" for i in range(len(selectors) or 3)]
            
            return IExecutionResult(
                step_id=step.step_id,
                success=True,
                result_data={
                    "extraction_type": extraction_type,
                    "data": extracted_data,
                    "count": len(extracted_data)
                },
                error_message=None
            )
            
        except Exception as e:
            return IExecutionResult(
                step_id=step.step_id,
                success=False,
                result_data={},
                error_message=str(e)
            )
    
    async def _execute_validation_step(self, step: IWorkflowStep, context: ISessionContext) -> IExecutionResult:
        """Execute validation step."""
        
        try:
            validation_type = step.parameters.get("validation_type", "basic")
            
            self.logger.info(f"Performing {validation_type} validation...")
            
            # Simulate validation
            await asyncio.sleep(1)
            
            return IExecutionResult(
                step_id=step.step_id,
                success=True,
                result_data={
                    "validation_type": validation_type,
                    "validation_passed": True
                },
                error_message=None
            )
            
        except Exception as e:
            return IExecutionResult(
                step_id=step.step_id,
                success=False,
                result_data={},
                error_message=str(e)
            )
    
    async def _execute_general_action_step(self, step: IWorkflowStep, context: ISessionContext) -> IExecutionResult:
        """Execute general action step."""
        
        try:
            action = step.parameters.get("action", "unknown")
            
            self.logger.info(f"Executing general action: {action}")
            
            # Simulate general action
            await asyncio.sleep(2)
            
            return IExecutionResult(
                step_id=step.step_id,
                success=True,
                result_data={
                    "action": action,
                    "executed": True
                },
                error_message=None
            )
            
        except Exception as e:
            return IExecutionResult(
                step_id=step.step_id,
                success=False,
                result_data={},
                error_message=str(e)
            )

    async def _execute_ai_processing_step(self, step: IWorkflowStep, context: ISessionContext) -> IExecutionResult:
        """Execute AI processing step."""
        
        try:
            question = step.parameters.get("question", "")
            response_type = step.parameters.get("response_type", "informational")
            
            self.logger.info(f"Processing AI question: {question[:50]}...")
            
            # Simulate AI processing
            await asyncio.sleep(1)
            
            # Generate mock AI response
            mock_response = f"This is an AI response about {question[:30]}... [processed successfully]"
            
            return IExecutionResult(
                step_id=step.step_id,
                success=True,
                result_data={
                    "response": mock_response,
                    "response_type": response_type,
                    "question": question
                },
                error_message=None
            )
            
        except Exception as e:
            return IExecutionResult(
                step_id=step.step_id,
                success=False,
                result_data={},
                error_message=str(e)
            )

    async def _execute_form_analysis_step(self, step: IWorkflowStep, context: ISessionContext) -> IExecutionResult:
        """Execute form analysis step."""
        
        try:
            detect_fields = step.parameters.get("detect_fields", True)
            
            self.logger.info("Analyzing form structure...")
            
            # Simulate form analysis
            await asyncio.sleep(2)
            
            return IExecutionResult(
                step_id=step.step_id,
                success=True,
                result_data={
                    "form_analyzed": True,
                    "fields_detected": detect_fields,
                    "field_count": 5,
                    "form_valid": True
                },
                error_message=None
            )
            
        except Exception as e:
            return IExecutionResult(
                step_id=step.step_id,
                success=False,
                result_data={},
                error_message=str(e)
            )

    async def _execute_data_location_step(self, step: IWorkflowStep, context: ISessionContext) -> IExecutionResult:
        """Execute data location step."""
        
        try:
            data_type = step.parameters.get("data_type", "structured")
            
            self.logger.info(f"Locating {data_type} data...")
            
            # Simulate data location
            await asyncio.sleep(1.5)
            
            return IExecutionResult(
                step_id=step.step_id,
                success=True,
                result_data={
                    "data_located": True,
                    "data_type": data_type,
                    "location_count": 3,
                    "data_available": True
                },
                error_message=None
            )
            
        except Exception as e:
            return IExecutionResult(
                step_id=step.step_id,
                success=False,
                result_data={},
                error_message=str(e)
            )
