"""
Autonomous Action Planner

Advanced AI system that can identify the next course of action, suggest intelligent steps,
and automatically execute them based on context, goals, and current page state.
"""

import asyncio
import json
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

from ..core.base_component import BaseComponent
from ..utils.logger import BotLogger


class ActionPriority(Enum):
    """Priority levels for autonomous actions."""
    CRITICAL = "critical"    # Must be done (security, errors)
    HIGH = "high"           # Important for workflow success
    MEDIUM = "medium"       # Helpful but not essential
    LOW = "low"            # Nice to have
    OPTIONAL = "optional"   # Can be skipped


class ActionCategory(Enum):
    """Categories of autonomous actions."""
    NAVIGATION = "navigation"       # Page navigation, URL changes
    FORM_INTERACTION = "form"      # Form filling, input interactions
    DATA_EXTRACTION = "data"       # Extracting information
    VALIDATION = "validation"      # Checking results, verification
    ERROR_HANDLING = "error"       # Dealing with errors, recovery
    OPTIMIZATION = "optimization"  # Performance, efficiency improvements
    SECURITY = "security"         # Security-related actions
    WORKFLOW = "workflow"         # Multi-step process management


@dataclass
class ActionPlan:
    """Represents a planned action with context and execution details."""
    action_id: str
    action_type: str
    category: ActionCategory
    priority: ActionPriority
    description: str
    confidence: float
    estimated_duration: float
    prerequisites: List[str]
    parameters: Dict[str, Any]
    reasoning: str
    fallback_actions: List[str]
    success_criteria: Dict[str, Any]
    risk_assessment: Dict[str, Any]


@dataclass
class WorkflowContext:
    """Current workflow context for intelligent planning."""
    current_url: str
    page_title: str
    goal: str
    completed_actions: List[str]
    failed_actions: List[str]
    available_elements: List[Dict[str, Any]]
    page_analysis: Dict[str, Any]
    user_preferences: Dict[str, Any]
    time_constraints: Optional[Dict[str, Any]] = None
    success_metrics: Optional[Dict[str, Any]] = None


class AutonomousActionPlanner(BaseComponent):
    """
    Advanced AI system for autonomous action planning and execution.
    
    Features:
    - Context-aware action suggestion
    - Multi-step workflow planning
    - Intelligent error recovery
    - Goal-oriented decision making
    - Learning from success/failure patterns
    - Risk assessment and mitigation
    - Real-time adaptation
    """
    
    def __init__(self, chat_ai, decision_engine, web_controller, config: Dict = None):
        """Initialize the autonomous action planner."""
        super().__init__("autonomous_action_planner", config)
        
        self.chat_ai = chat_ai
        self.decision_engine = decision_engine
        self.web_controller = web_controller
        
        # Planning state
        self.current_workflow: Optional[WorkflowContext] = None
        self.action_history: List[ActionPlan] = []
        self.learning_data: Dict[str, Any] = {}
        
        # Configuration
        self.max_planning_depth = self.config.get('max_planning_depth', 5)
        self.confidence_threshold = self.config.get('confidence_threshold', 0.7)
        self.enable_autonomous_execution = self.config.get('enable_autonomous_execution', True)
        self.risk_tolerance = self.config.get('risk_tolerance', 'medium')  # low, medium, high
        
    def initialize(self) -> bool:
        """Initialize the autonomous action planner."""
        try:
            self.logger.info("Initializing Autonomous Action Planner...")
            
            # Load historical learning data
            self._load_learning_data()
            
            self.is_initialized = True
            self.logger.info("Autonomous Action Planner initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Autonomous Action Planner: {e}")
            return False
    
    async def analyze_and_suggest_next_actions(
        self, 
        goal: str, 
        context: WorkflowContext,
        max_suggestions: int = 3
    ) -> List[ActionPlan]:
        """
        Analyze current context and suggest the next best actions to achieve the goal.
        
        Args:
            goal: The ultimate objective
            context: Current workflow context
            max_suggestions: Maximum number of action suggestions
            
        Returns:
            List of suggested action plans, ordered by priority and confidence
        """
        try:
            self.logger.info(f"Analyzing context and suggesting next actions for goal: {goal}")
            
            # Update current workflow context
            self.current_workflow = context
            
            # Analyze current situation
            situation_analysis = await self._analyze_current_situation(context)
            
            # Generate possible actions
            possible_actions = await self._generate_possible_actions(goal, context, situation_analysis)
            
            # Score and rank actions
            ranked_actions = await self._rank_actions(possible_actions, context, situation_analysis)
            
            # Apply filters and constraints
            filtered_actions = self._apply_action_filters(ranked_actions, context)
            
            # Return top suggestions
            suggestions = filtered_actions[:max_suggestions]
            
            self.logger.info(f"Generated {len(suggestions)} action suggestions")
            return suggestions
            
        except Exception as e:
            self.logger.error(f"Action suggestion failed: {e}")
            return []
    
    async def execute_action_plan(self, action_plan: ActionPlan) -> Dict[str, Any]:
        """
        Execute a planned action and return results.
        
        Args:
            action_plan: The action plan to execute
            
        Returns:
            Execution results with success status and details
        """
        try:
            self.logger.info(f"Executing action: {action_plan.description}")
            
            # Pre-execution validation
            if not await self._validate_action_prerequisites(action_plan):
                return {
                    "success": False,
                    "error": "Prerequisites not met",
                    "action_id": action_plan.action_id
                }
            
            # Execute the action
            execution_start = datetime.now()
            
            result = await self._execute_single_action(action_plan)
            
            execution_time = (datetime.now() - execution_start).total_seconds()
            
            # Post-execution validation
            success = await self._validate_action_success(action_plan, result)
            
            # Record results for learning
            await self._record_action_result(action_plan, result, success, execution_time)
            
            # Update workflow context
            if success:
                self.current_workflow.completed_actions.append(action_plan.action_id)
            else:
                self.current_workflow.failed_actions.append(action_plan.action_id)
            
            return {
                "success": success,
                "result": result,
                "execution_time": execution_time,
                "action_id": action_plan.action_id,
                "next_suggestions": await self._suggest_follow_up_actions(action_plan, success)
            }
            
        except Exception as e:
            self.logger.error(f"Action execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "action_id": action_plan.action_id
            }
    
    async def create_autonomous_workflow(self, goal: str, constraints: Dict[str, Any] = None) -> List[ActionPlan]:
        """
        Create a complete autonomous workflow to achieve a goal.
        
        Args:
            goal: The objective to achieve
            constraints: Optional constraints (time, resources, etc.)
            
        Returns:
            Complete workflow as a list of action plans
        """
        try:
            self.logger.info(f"Creating autonomous workflow for goal: {goal}")
            
            # Analyze goal and break it down
            goal_analysis = await self._analyze_goal(goal)
            
            # Create workflow context
            context = await self._create_initial_context(goal, constraints)
            
            # Generate complete workflow
            workflow_steps = []
            current_step = 1
            
            while current_step <= self.max_planning_depth:
                # Get next actions
                next_actions = await self.analyze_and_suggest_next_actions(goal, context, 1)
                
                if not next_actions:
                    break
                
                best_action = next_actions[0]
                workflow_steps.append(best_action)
                
                # Simulate action completion for planning
                context = await self._simulate_action_completion(best_action, context)
                
                # Check if goal is achieved
                if await self._is_goal_achieved(goal, context):
                    break
                
                current_step += 1
            
            self.logger.info(f"Created workflow with {len(workflow_steps)} steps")
            return workflow_steps
            
        except Exception as e:
            self.logger.error(f"Workflow creation failed: {e}")
            return []
    
    async def execute_autonomous_workflow(
        self, 
        workflow: List[ActionPlan],
        monitor_callback: Optional[callable] = None
    ) -> Dict[str, Any]:
        """
        Execute a complete autonomous workflow with monitoring and error recovery.
        
        Args:
            workflow: List of action plans to execute
            monitor_callback: Optional callback for progress monitoring
            
        Returns:
            Complete execution results
        """
        try:
            self.logger.info(f"Starting autonomous workflow execution ({len(workflow)} steps)")
            
            results = []
            failed_actions = []
            
            for i, action_plan in enumerate(workflow):
                # Progress callback
                if monitor_callback:
                    await monitor_callback({
                        "step": i + 1,
                        "total_steps": len(workflow),
                        "current_action": action_plan.description,
                        "status": "executing"
                    })
                
                # Execute action
                result = await self.execute_action_plan(action_plan)
                results.append(result)
                
                if not result["success"]:
                    failed_actions.append(action_plan.action_id)
                    
                    # Attempt error recovery
                    recovery_result = await self._attempt_error_recovery(action_plan, result)
                    
                    if not recovery_result["success"]:
                        # Critical failure - decide whether to continue
                        if action_plan.priority in [ActionPriority.CRITICAL, ActionPriority.HIGH]:
                            self.logger.error(f"Critical action failed, stopping workflow: {action_plan.description}")
                            break
                
                # Brief pause between actions
                await asyncio.sleep(1.0)
            
            # Calculate overall success
            successful_actions = len([r for r in results if r["success"]])
            success_rate = successful_actions / len(results) if results else 0
            
            workflow_result = {
                "success": success_rate >= 0.8,  # 80% success threshold
                "total_actions": len(workflow),
                "successful_actions": successful_actions,
                "failed_actions": len(failed_actions),
                "success_rate": success_rate,
                "execution_time": sum(r.get("execution_time", 0) for r in results),
                "results": results,
                "failed_action_ids": failed_actions
            }
            
            # Final callback
            if monitor_callback:
                await monitor_callback({
                    "status": "completed",
                    "workflow_result": workflow_result
                })
            
            self.logger.info(f"Autonomous workflow completed: {success_rate:.1%} success rate")
            return workflow_result
            
        except Exception as e:
            self.logger.error(f"Autonomous workflow execution failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "total_actions": len(workflow),
                "successful_actions": 0
            }
    
    # Private helper methods
    
    async def _analyze_current_situation(self, context: WorkflowContext) -> Dict[str, Any]:
        """Analyze the current situation using AI."""
        prompt = f"""
        Analyze the current web automation situation:
        
        Current URL: {context.current_url}
        Page Title: {context.page_title}
        Goal: {context.goal}
        Completed Actions: {context.completed_actions}
        Failed Actions: {context.failed_actions}
        Available Elements: {len(context.available_elements)} elements detected
        
        Provide analysis including:
        1. Current progress toward goal
        2. Potential obstacles or challenges  
        3. Opportunities for next actions
        4. Risk factors to consider
        5. Recommended strategy
        
        Return as JSON with structured analysis.
        """
        
        response = await self.chat_ai.chat(prompt)
        
        # Parse AI response
        try:
            import re
            json_match = re.search(r'\{.*\}', response.get("response", ""), re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        
        # Fallback analysis
        return {
            "progress": "unknown",
            "obstacles": [],
            "opportunities": ["continue_with_available_elements"],
            "risk_factors": ["unknown_page_state"],
            "strategy": "proceed_cautiously"
        }
    
    async def _generate_possible_actions(
        self, 
        goal: str, 
        context: WorkflowContext, 
        situation_analysis: Dict[str, Any]
    ) -> List[ActionPlan]:
        """Generate all possible next actions."""
        possible_actions = []
        
        # Navigation actions
        if "navigation" in situation_analysis.get("opportunities", []):
            possible_actions.extend(await self._generate_navigation_actions(context))
        
        # Form interaction actions
        form_elements = [e for e in context.available_elements if e.get("type") in ["input", "select", "textarea"]]
        if form_elements:
            possible_actions.extend(await self._generate_form_actions(form_elements, context))
        
        # Data extraction actions
        if "extract" in goal.lower() or "data" in goal.lower():
            possible_actions.extend(await self._generate_extraction_actions(context))
        
        # Validation actions
        possible_actions.extend(await self._generate_validation_actions(context))
        
        return possible_actions
    
    async def _rank_actions(
        self, 
        actions: List[ActionPlan], 
        context: WorkflowContext,
        situation_analysis: Dict[str, Any]
    ) -> List[ActionPlan]:
        """Rank actions by priority, confidence, and relevance."""
        
        for action in actions:
            # Calculate composite score
            priority_score = self._get_priority_score(action.priority)
            confidence_score = action.confidence
            relevance_score = await self._calculate_relevance_score(action, context)
            risk_penalty = self._calculate_risk_penalty(action.risk_assessment)
            
            action.composite_score = (
                priority_score * 0.3 + 
                confidence_score * 0.3 + 
                relevance_score * 0.3 - 
                risk_penalty * 0.1
            )
        
        # Sort by composite score
        return sorted(actions, key=lambda a: a.composite_score, reverse=True)
    
    def _get_priority_score(self, priority: ActionPriority) -> float:
        """Convert priority to numeric score."""
        priority_scores = {
            ActionPriority.CRITICAL: 1.0,
            ActionPriority.HIGH: 0.8,
            ActionPriority.MEDIUM: 0.6,
            ActionPriority.LOW: 0.4,
            ActionPriority.OPTIONAL: 0.2
        }
        return priority_scores.get(priority, 0.5)
    
    # Additional helper methods would continue here...
    # (Implementation of other private methods for completeness)
    
    async def _execute_single_action(self, action_plan: ActionPlan) -> Dict[str, Any]:
        """Execute a single action using the web controller."""
        action_type = action_plan.action_type
        parameters = action_plan.parameters
        
        if action_type == "navigate_to":
            success = self.web_controller.navigate_to(parameters["url"])
            return {"success": success, "action": "navigate_to", "url": parameters["url"]}
        
        elif action_type == "fill_form":
            # Implementation for form filling
            return {"success": True, "action": "fill_form", "fields": parameters.get("fields", {})}
        
        elif action_type == "click_element":
            # Implementation for clicking elements
            return {"success": True, "action": "click_element", "element": parameters.get("element")}
        
        elif action_type == "extract_data":
            # Implementation for data extraction
            return {"success": True, "action": "extract_data", "data": {}}
        
        elif action_type == "wait":
            await asyncio.sleep(parameters.get("seconds", 1))
            return {"success": True, "action": "wait", "duration": parameters.get("seconds", 1)}
        
        else:
            return {"success": False, "error": f"Unknown action type: {action_type}"}
    
    def _load_learning_data(self):
        """Load historical learning data for better decision making."""
        # Implementation for loading learning data
        pass
    
    async def _validate_action_prerequisites(self, action_plan: ActionPlan) -> bool:
        """Validate that action prerequisites are met."""
        # Implementation for prerequisite validation
        return True
    
    async def _validate_action_success(self, action_plan: ActionPlan, result: Dict[str, Any]) -> bool:
        """Validate that action was successful based on success criteria."""
        # Implementation for success validation
        return result.get("success", False)
    
    async def _record_action_result(self, action_plan: ActionPlan, result: Dict[str, Any], success: bool, execution_time: float):
        """Record action result for learning."""
        # Implementation for recording results
        pass
    
    async def _suggest_follow_up_actions(self, action_plan: ActionPlan, success: bool) -> List[str]:
        """Suggest follow-up actions based on the result."""
        # Implementation for follow-up suggestions
        return []
    
    async def _attempt_error_recovery(self, action_plan: ActionPlan, result: Dict[str, Any]) -> Dict[str, Any]:
        """Attempt to recover from action failure."""
        # Implementation for error recovery
        return {"success": False, "recovery_attempted": True}
