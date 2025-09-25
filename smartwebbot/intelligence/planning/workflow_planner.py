"""
Smart Workflow Planner for Intelligent Chat System.

Creates detailed, executable workflow plans from parsed commands
with intelligent step generation and optimization.
"""

import time
import uuid
from typing import Dict, List, Optional, Any
from ..core.base_chat_component import BaseChatComponent
from ..core.interfaces import (
    IWorkflowPlanner, IParsedCommand, ISessionContext, 
    IWorkflowPlan, IWorkflowStep, CommandComplexity
)


class SmartWorkflowPlanner(BaseChatComponent, IWorkflowPlanner):
    """
    Smart workflow planner that creates executable plans.
    
    Features:
    - Intent-driven step generation
    - Platform-specific optimization
    - Resource-aware planning
    - Dependency resolution
    - Risk assessment
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("smart_workflow_planner", config)
        
        # Planning templates
        self.workflow_templates = self._load_workflow_templates()
        self.platform_knowledge = self._load_platform_knowledge()
        
        # Configuration
        self.max_steps = self.get_config_value("max_steps", 50)
        self.optimization_level = self.get_config_value("optimization_level", "standard")
    
    def initialize(self) -> bool:
        """Initialize the workflow planner."""
        try:
            self.logger.info("Initializing Smart Workflow Planner...")
            
            # Validate templates
            if not self.workflow_templates:
                raise Exception("No workflow templates loaded")
            
            self.is_initialized = True
            self.is_healthy = True
            
            self.logger.info("Smart Workflow Planner initialized successfully")
            return True
            
        except Exception as e:
            self.log_error(e, "Workflow planner initialization")
            return False
    
    async def create_plan(self, command: IParsedCommand, context: ISessionContext) -> IWorkflowPlan:
        """Create detailed execution plan for command."""
        start_time = time.time()
        
        try:
            self.logger.debug(f"Creating workflow plan for: {command.intent}")
            
            # Step 1: Select workflow template
            template = self._select_template(command)
            
            # Step 2: Generate steps based on intent and platform
            steps = await self._generate_steps(command, context, template)
            
            # Step 3: Optimize workflow
            optimized_steps = await self._optimize_steps(steps, command)
            
            # Step 4: Add error handling and validation
            final_steps = await self._add_error_handling(optimized_steps)
            
            # Step 5: Create workflow plan
            plan = IWorkflowPlan(
                plan_id=str(uuid.uuid4()),
                command=command,
                steps=final_steps,
                estimated_duration=self._estimate_duration(final_steps),
                success_criteria=self._define_success_criteria(command),
                failure_conditions=self._define_failure_conditions(command)
            )
            
            processing_time = time.time() - start_time
            self.log_success(f"Created plan with {len(final_steps)} steps", processing_time)
            
            return plan
            
        except Exception as e:
            self.log_error(e, f"Workflow planning failed for: {command.intent}")
            return await self._create_fallback_plan(command, context)
    
    async def optimize_plan(self, plan: IWorkflowPlan) -> IWorkflowPlan:
        """Optimize existing workflow plan."""
        try:
            # Optimize step order
            optimized_steps = await self._optimize_step_order(plan.steps)
            
            # Remove redundant steps
            deduplicated_steps = self._remove_redundant_steps(optimized_steps)
            
            # Parallelize where possible
            parallelized_steps = self._add_parallelization(deduplicated_steps)
            
            # Update plan
            plan.steps = parallelized_steps
            plan.estimated_duration = self._estimate_duration(parallelized_steps)
            
            return plan
            
        except Exception as e:
            self.log_error(e, "Plan optimization failed")
            return plan
    
    def _load_workflow_templates(self) -> Dict[str, Dict]:
        """Load workflow templates for different intents."""
        return {
            "social_media_post": {
                "base_steps": [
                    "navigate_to_platform",
                    "authenticate_user", 
                    "locate_create_post",
                    "compose_content",
                    "add_media",
                    "configure_settings",
                    "publish_post",
                    "verify_success"
                ],
                "platforms": {
                    "instagram": {
                        "specific_steps": ["select_story_or_feed", "add_filters", "add_location"],
                        "constraints": {"character_limit": 2200, "media_required": True}
                    },
                    "facebook": {
                        "specific_steps": ["select_audience", "add_tags", "schedule_post"],
                        "constraints": {"character_limit": 63206, "media_optional": True}
                    },
                    "twitter": {
                        "specific_steps": ["add_thread", "add_poll"],
                        "constraints": {"character_limit": 280, "media_optional": True}
                    }
                }
            },
            "login_to_platform": {
                "base_steps": [
                    "navigate_to_platform",
                    "locate_login_form",
                    "enter_credentials", 
                    "handle_2fa_if_needed",
                    "verify_login_success"
                ],
                "error_handling": ["retry_on_failure", "handle_captcha", "handle_security_check"]
            },
            "form_interaction": {
                "base_steps": [
                    "navigate_to_form",
                    "analyze_form_fields",
                    "fill_required_fields",
                    "validate_input",
                    "submit_form",
                    "handle_confirmation"
                ],
                "validation": ["check_required_fields", "validate_format", "handle_errors"]
            },
            "marketing_campaign": {
                "base_steps": [
                    "analyze_campaign_goals",
                    "research_target_audience", 
                    "create_content_strategy",
                    "prepare_content_assets",
                    "schedule_multi_platform_posts",
                    "monitor_engagement",
                    "optimize_performance"
                ],
                "complexity": "advanced",
                "requires_approval": True
            },
            "data_extraction": {
                "base_steps": [
                    "navigate_to_data_source",
                    "authenticate_if_required",
                    "locate_target_data",
                    "extract_structured_data",
                    "validate_extraction",
                    "format_output",
                    "save_results"
                ],
                "optimization": ["pagination_handling", "rate_limit_respect", "duplicate_detection"]
            }
        }
    
    def _load_platform_knowledge(self) -> Dict[str, Dict]:
        """Load platform-specific knowledge."""
        return {
            "instagram": {
                "login_url": "https://instagram.com/accounts/login/",
                "post_creation": "//button[@aria-label='New post']",
                "auth_selectors": {
                    "username": "input[name='username']",
                    "password": "input[name='password']", 
                    "login_button": "button[type='submit']"
                },
                "rate_limits": {"posts_per_hour": 10, "actions_per_minute": 60}
            },
            "facebook": {
                "login_url": "https://facebook.com/login",
                "post_creation": "[data-testid='status-attachment-mentions-input']",
                "auth_selectors": {
                    "username": "#email",
                    "password": "#pass",
                    "login_button": "#loginbutton"
                },
                "rate_limits": {"posts_per_hour": 25, "actions_per_minute": 120}
            },
            "twitter": {
                "login_url": "https://twitter.com/i/flow/login",
                "post_creation": "[data-testid='tweetTextarea_0']",
                "auth_selectors": {
                    "username": "input[name='text']",
                    "password": "input[name='password']",
                    "login_button": "[data-testid='LoginForm_Login_Button']"
                },
                "rate_limits": {"posts_per_hour": 20, "actions_per_minute": 100}
            }
        }
    
    def _select_template(self, command: IParsedCommand) -> Dict[str, Any]:
        """Select appropriate workflow template."""
        # Direct intent mapping
        if command.intent in self.workflow_templates:
            return self.workflow_templates[command.intent]
        
        # Action-based mapping
        action_to_template = {
            "post": "social_media_post",
            "login": "login_to_platform",
            "fill_form": "form_interaction",
            "extract": "data_extraction",
            "marketing": "marketing_campaign"
        }
        
        if command.action_type in action_to_template:
            return self.workflow_templates[action_to_template[command.action_type]]
        
        # Default template for general automation
        return {
            "base_steps": [
                "analyze_request",
                "navigate_to_target",
                "perform_action",
                "verify_result"
            ]
        }
    
    async def _generate_steps(self, command: IParsedCommand, context: ISessionContext, 
                            template: Dict[str, Any]) -> List[IWorkflowStep]:
        """Generate workflow steps from template and command."""
        steps = []
        step_counter = 1
        
        # Base steps from template
        base_steps = template.get("base_steps", [])
        
        for step_name in base_steps:
            step = self._create_step(step_name, step_counter, command, context)
            steps.append(step)
            step_counter += 1
        
        # Platform-specific steps
        if command.target_platform and "platforms" in template:
            platform_info = template["platforms"].get(command.target_platform, {})
            specific_steps = platform_info.get("specific_steps", [])
            
            for step_name in specific_steps:
                step = self._create_step(step_name, step_counter, command, context, platform_specific=True)
                steps.append(step)
                step_counter += 1
        
        # Add validation steps for complex workflows
        if command.complexity in [CommandComplexity.COMPLEX, CommandComplexity.ADVANCED]:
            validation_step = self._create_validation_step(step_counter, command)
            steps.append(validation_step)
        
        return steps
    
    def _create_step(self, step_name: str, step_number: int, command: IParsedCommand, 
                    context: ISessionContext, platform_specific: bool = False) -> IWorkflowStep:
        """Create individual workflow step."""
        
        step_id = f"step_{step_number}_{step_name}"
        
        # Step type mapping
        step_types = {
            "navigate_to_platform": "navigation",
            "authenticate_user": "authentication",
            "locate_create_post": "element_interaction", 
            "compose_content": "content_creation",
            "fill_required_fields": "form_filling",
            "submit_form": "form_submission",
            "extract_structured_data": "data_extraction",
            "verify_success": "validation"
        }
        
        step_type = step_types.get(step_name, "general_action")
        
        # Generate parameters based on step type and command
        parameters = self._generate_step_parameters(step_name, command, context)
        
        # Determine dependencies
        dependencies = self._determine_dependencies(step_number, step_name)
        
        return IWorkflowStep(
            step_id=step_id,
            step_type=step_type,
            description=self._generate_step_description(step_name, command),
            parameters=parameters,
            dependencies=dependencies,
            timeout=self._determine_timeout(step_type),
            retry_count=3
        )
    
    def _generate_step_parameters(self, step_name: str, command: IParsedCommand, 
                                 context: ISessionContext) -> Dict[str, Any]:
        """Generate parameters for workflow step."""
        
        if step_name == "navigate_to_platform" and command.target_platform:
            platform_info = self.platform_knowledge.get(command.target_platform, {})
            return {
                "url": platform_info.get("login_url", f"https://{command.target_platform}.com"),
                "wait_for": "page_load",
                "timeout": 10
            }
        
        elif step_name == "authenticate_user":
            return {
                "username_selector": self._get_auth_selector(command.target_platform, "username"),
                "password_selector": self._get_auth_selector(command.target_platform, "password"),
                "submit_selector": self._get_auth_selector(command.target_platform, "login_button"),
                "require_credentials": True
            }
        
        elif step_name == "compose_content":
            content = command.parameters.get("content", "Automated post from SmartWebBot")
            return {
                "content": content,
                "content_type": "text",
                "character_limit": self._get_character_limit(command.target_platform)
            }
        
        elif step_name == "fill_required_fields":
            return {
                "field_mapping": self._generate_field_mapping(command),
                "validation_rules": self._get_validation_rules(command),
                "auto_detect_fields": True
            }
        
        else:
            # Generic parameters
            return {
                "action": step_name,
                "platform": command.target_platform,
                "context": "automated_execution"
            }
    
    def _get_auth_selector(self, platform: str, field_type: str) -> str:
        """Get authentication selector for platform."""
        if not platform or platform not in self.platform_knowledge:
            return f"input[name='{field_type}']"  # Generic fallback
        
        selectors = self.platform_knowledge[platform].get("auth_selectors", {})
        return selectors.get(field_type, f"input[name='{field_type}']")
    
    def _get_character_limit(self, platform: str) -> int:
        """Get character limit for platform."""
        limits = {
            "twitter": 280,
            "instagram": 2200,
            "facebook": 63206,
            "linkedin": 3000
        }
        return limits.get(platform, 1000)
    
    def _generate_step_description(self, step_name: str, command: IParsedCommand) -> str:
        """Generate human-readable step description."""
        descriptions = {
            "navigate_to_platform": f"Navigate to {command.target_platform or 'target website'}",
            "authenticate_user": f"Login to {command.target_platform} account",
            "locate_create_post": "Find the create post button",
            "compose_content": "Write and format the post content", 
            "fill_required_fields": "Fill out all required form fields",
            "submit_form": "Submit the form",
            "verify_success": "Verify the action completed successfully"
        }
        
        return descriptions.get(step_name, f"Execute {step_name}")
    
    def _determine_dependencies(self, step_number: int, step_name: str) -> List[str]:
        """Determine step dependencies."""
        if step_number == 1:
            return []  # First step has no dependencies
        
        # Authentication must come after navigation
        if step_name == "authenticate_user":
            return ["step_1_navigate_to_platform"]
        
        # Most steps depend on previous step
        return [f"step_{step_number-1}"]
    
    def _determine_timeout(self, step_type: str) -> int:
        """Determine appropriate timeout for step type."""
        timeouts = {
            "navigation": 30,
            "authentication": 15,
            "element_interaction": 10,
            "content_creation": 20,
            "form_filling": 15,
            "form_submission": 20,
            "data_extraction": 60,
            "validation": 10
        }
        return timeouts.get(step_type, 15)
    
    async def _optimize_steps(self, steps: List[IWorkflowStep], command: IParsedCommand) -> List[IWorkflowStep]:
        """Optimize workflow steps."""
        if self.optimization_level == "none":
            return steps
        
        optimized = steps[:]
        
        # Remove redundant steps
        optimized = self._remove_redundant_steps(optimized)
        
        # Optimize step order for efficiency
        if self.optimization_level in ["standard", "aggressive"]:
            optimized = await self._optimize_step_order(optimized)
        
        # Add parallel execution where possible
        if self.optimization_level == "aggressive":
            optimized = self._add_parallelization(optimized)
        
        return optimized
    
    def _remove_redundant_steps(self, steps: List[IWorkflowStep]) -> List[IWorkflowStep]:
        """Remove redundant steps from workflow."""
        seen_actions = set()
        filtered_steps = []
        
        for step in steps:
            step_signature = (step.step_type, step.description)
            if step_signature not in seen_actions:
                filtered_steps.append(step)
                seen_actions.add(step_signature)
        
        return filtered_steps
    
    async def _optimize_step_order(self, steps: List[IWorkflowStep]) -> List[IWorkflowStep]:
        """Optimize step order for better performance."""
        # For now, keep original order but this could be enhanced
        # with dependency graph analysis and topological sorting
        return steps
    
    def _add_parallelization(self, steps: List[IWorkflowStep]) -> List[IWorkflowStep]:
        """Add parallel execution hints where possible."""
        # Mark independent steps for parallel execution
        for i, step in enumerate(steps):
            if i > 0 and not step.dependencies:
                # This step could potentially run in parallel
                step.parameters["parallel_eligible"] = True
        
        return steps
    
    async def _add_error_handling(self, steps: List[IWorkflowStep]) -> List[IWorkflowStep]:
        """Add error handling to workflow steps."""
        enhanced_steps = []
        
        for step in steps:
            # Add error handling parameters
            step.parameters.update({
                "error_handling": {
                    "retry_count": step.retry_count,
                    "retry_delay": 2,
                    "fallback_actions": self._get_fallback_actions(step.step_type),
                    "critical": step.step_type in ["authentication", "navigation"]
                }
            })
            
            enhanced_steps.append(step)
        
        return enhanced_steps
    
    def _get_fallback_actions(self, step_type: str) -> List[str]:
        """Get fallback actions for step type."""
        fallbacks = {
            "navigation": ["refresh_page", "try_alternative_url"],
            "authentication": ["clear_cookies", "try_alternative_login"],
            "element_interaction": ["wait_longer", "try_alternative_selector"],
            "form_filling": ["clear_field", "use_keyboard_input"],
            "data_extraction": ["try_alternative_selector", "use_javascript_extraction"]
        }
        return fallbacks.get(step_type, ["retry_action"])
    
    def _estimate_duration(self, steps: List[IWorkflowStep]) -> int:
        """Estimate total workflow duration in seconds."""
        total_time = 0
        
        for step in steps:
            # Base time for step type
            base_times = {
                "navigation": 10,
                "authentication": 15,
                "element_interaction": 5,
                "content_creation": 20,
                "form_filling": 10,
                "data_extraction": 30,
                "validation": 5
            }
            
            step_time = base_times.get(step.step_type, 10)
            
            # Add timeout and retry overhead
            step_time += step.timeout + (step.retry_count * 3)
            
            total_time += step_time
        
        # Add 20% buffer
        return int(total_time * 1.2)
    
    def _define_success_criteria(self, command: IParsedCommand) -> Dict[str, Any]:
        """Define success criteria for workflow."""
        criteria = {
            "all_steps_completed": True,
            "no_critical_errors": True,
            "target_action_achieved": True
        }
        
        # Intent-specific criteria
        if command.intent == "social_media_post":
            criteria.update({
                "post_published": True,
                "content_matches_input": True
            })
        elif command.intent == "login_to_platform":
            criteria.update({
                "authentication_successful": True,
                "dashboard_accessible": True
            })
        elif command.intent == "form_interaction":
            criteria.update({
                "form_submitted": True,
                "confirmation_received": True
            })
        
        return criteria
    
    def _define_failure_conditions(self, command: IParsedCommand) -> List[str]:
        """Define conditions that indicate workflow failure."""
        conditions = [
            "authentication_failed_multiple_times",
            "target_platform_unreachable", 
            "critical_step_timeout",
            "user_intervention_required"
        ]
        
        # Intent-specific failure conditions
        if command.intent == "social_media_post":
            conditions.extend([
                "content_violates_platform_policy",
                "account_suspended",
                "rate_limit_exceeded"
            ])
        
        return conditions
    
    async def _create_fallback_plan(self, command: IParsedCommand, context: ISessionContext) -> IWorkflowPlan:
        """Create fallback plan when main planning fails."""
        fallback_step = IWorkflowStep(
            step_id="fallback_step",
            step_type="general_action",
            description=f"Execute general automation for: {command.intent}",
            parameters={
                "action": "general_automation",
                "user_input": command.original_text,
                "fallback_mode": True
            },
            dependencies=[],
            timeout=30,
            retry_count=1
        )
        
        return IWorkflowPlan(
            plan_id=f"fallback_{int(time.time())}",
            command=command,
            steps=[fallback_step],
            estimated_duration=60,
            success_criteria={"basic_execution": True},
            failure_conditions=["complete_failure"]
        )
    
    def _generate_field_mapping(self, command: IParsedCommand) -> Dict[str, str]:
        """Generate field mapping for form filling."""
        # Extract potential field values from command parameters
        field_mapping = {}
        
        if "email" in command.parameters:
            field_mapping["email"] = command.parameters["email"]
        if "name" in command.parameters:
            field_mapping["name"] = command.parameters["name"]
        if "phone" in command.parameters:
            field_mapping["phone"] = command.parameters["phone"]
        
        return field_mapping
    
    def _get_validation_rules(self, command: IParsedCommand) -> Dict[str, Any]:
        """Get validation rules for form fields."""
        return {
            "email": {"required": True, "format": "email"},
            "name": {"required": True, "min_length": 2},
            "phone": {"required": False, "format": "phone"}
        }
    
    def _create_validation_step(self, step_number: int, command: IParsedCommand) -> IWorkflowStep:
        """Create validation step for complex workflows."""
        return IWorkflowStep(
            step_id=f"step_{step_number}_validation",
            step_type="validation",
            description="Validate workflow execution results",
            parameters={
                "validation_type": "comprehensive",
                "check_success_criteria": True,
                "generate_report": True
            },
            dependencies=[f"step_{step_number-1}"],
            timeout=15,
            retry_count=1
        )
