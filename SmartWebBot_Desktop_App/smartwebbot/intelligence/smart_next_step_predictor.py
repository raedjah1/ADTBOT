"""
Smart Next Step Predictor

AI system that analyzes current page state, user goals, and context to predict
and suggest the most logical next steps in web automation workflows.
"""

import json
import re
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

from ..core.base_component import BaseComponent


class StepType(Enum):
    """Types of automation steps."""
    NAVIGATION = "navigation"
    FORM_FILL = "form_fill"
    CLICK_ACTION = "click_action"
    DATA_EXTRACT = "data_extract"
    VALIDATION = "validation"
    WAIT = "wait"
    SCROLL = "scroll"
    SCREENSHOT = "screenshot"


class StepConfidence(Enum):
    """Confidence levels for step predictions."""
    VERY_HIGH = "very_high"    # 90-100% confident
    HIGH = "high"              # 75-89% confident
    MEDIUM = "medium"          # 50-74% confident
    LOW = "low"               # 25-49% confident
    VERY_LOW = "very_low"     # 0-24% confident


@dataclass
class NextStepPrediction:
    """Represents a predicted next step."""
    step_id: str
    step_type: StepType
    description: str
    confidence: StepConfidence
    confidence_score: float
    reasoning: str
    required_elements: List[str]
    expected_outcome: str
    estimated_time: float
    risk_level: str
    parameters: Dict[str, Any]
    alternatives: List[str]


@dataclass
class PageState:
    """Current page state for analysis."""
    url: str
    title: str
    elements: List[Dict[str, Any]]
    forms: List[Dict[str, Any]]
    buttons: List[Dict[str, Any]]
    links: List[Dict[str, Any]]
    text_content: str
    page_type: str  # login, form, dashboard, listing, etc.
    loading_state: str  # loading, loaded, error
    user_interactions: List[str]  # previous user actions


@dataclass
class UserGoal:
    """User's goal and context."""
    primary_goal: str
    sub_goals: List[str]
    completed_steps: List[str]
    failed_attempts: List[str]
    time_constraints: Optional[Dict[str, Any]]
    success_criteria: Dict[str, Any]
    user_preferences: Dict[str, Any]


class SmartNextStepPredictor(BaseComponent):
    """
    AI-powered system that predicts the most logical next steps in automation workflows.
    
    Features:
    - Context-aware step prediction
    - Multi-scenario analysis
    - Confidence scoring
    - Alternative path suggestions
    - Learning from user patterns
    - Risk assessment
    - Time estimation
    """
    
    def __init__(self, chat_ai, web_controller, config: Dict = None):
        """Initialize the smart next step predictor."""
        super().__init__("smart_next_step_predictor", config)
        
        self.chat_ai = chat_ai
        self.web_controller = web_controller
        
        # Prediction models
        self.pattern_database = {}
        self.success_patterns = {}
        self.failure_patterns = {}
        
        # Configuration
        self.max_predictions = self.config.get('max_predictions', 5)
        self.min_confidence_threshold = self.config.get('min_confidence_threshold', 0.3)
        self.enable_learning = self.config.get('enable_learning', True)
        
    def initialize(self) -> bool:
        """Initialize the predictor."""
        try:
            self.logger.info("Initializing Smart Next Step Predictor...")
            
            # Load pattern database
            self._load_pattern_database()
            
            self.is_initialized = True
            self.logger.info("Smart Next Step Predictor initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Smart Next Step Predictor: {e}")
            return False
    
    def cleanup(self) -> bool:
        """Clean up resources used by the predictor."""
        try:
            self.logger.info("Cleaning up Smart Next Step Predictor...")
            
            # Clear pattern databases
            self.pattern_database.clear()
            self.success_patterns.clear()
            self.failure_patterns.clear()
            
            self.logger.info("Smart Next Step Predictor cleanup completed")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup Smart Next Step Predictor: {e}")
            return False
    
    async def predict_next_steps(
        self, 
        page_state: PageState, 
        user_goal: UserGoal,
        max_predictions: Optional[int] = None
    ) -> List[NextStepPrediction]:
        """
        Predict the most logical next steps based on current state and user goal.
        
        Args:
            page_state: Current page state
            user_goal: User's goal and context
            max_predictions: Maximum number of predictions to return
            
        Returns:
            List of next step predictions, ordered by confidence
        """
        try:
            self.logger.info(f"Predicting next steps for goal: {user_goal.primary_goal}")
            
            max_pred = max_predictions or self.max_predictions
            
            # Analyze current context
            context_analysis = await self._analyze_context(page_state, user_goal)
            
            # Generate predictions using different strategies
            predictions = []
            
            # Strategy 1: Pattern-based predictions
            pattern_predictions = await self._predict_from_patterns(page_state, user_goal, context_analysis)
            predictions.extend(pattern_predictions)
            
            # Strategy 2: AI-powered predictions
            ai_predictions = await self._predict_with_ai(page_state, user_goal, context_analysis)
            predictions.extend(ai_predictions)
            
            # Strategy 3: Element-based predictions
            element_predictions = await self._predict_from_elements(page_state, user_goal)
            predictions.extend(element_predictions)
            
            # Strategy 4: Goal-based predictions
            goal_predictions = await self._predict_from_goal_analysis(user_goal, page_state)
            predictions.extend(goal_predictions)
            
            # Remove duplicates and rank predictions
            unique_predictions = self._deduplicate_predictions(predictions)
            ranked_predictions = await self._rank_predictions(unique_predictions, context_analysis)
            
            # Filter by confidence threshold
            filtered_predictions = [
                p for p in ranked_predictions 
                if p.confidence_score >= self.min_confidence_threshold
            ]
            
            # Return top predictions
            final_predictions = filtered_predictions[:max_pred]
            
            self.logger.info(f"Generated {len(final_predictions)} next step predictions")
            return final_predictions
            
        except Exception as e:
            self.logger.error(f"Next step prediction failed: {e}")
            return []
    
    async def predict_complete_workflow(
        self, 
        starting_state: PageState, 
        user_goal: UserGoal,
        max_steps: int = 10
    ) -> List[NextStepPrediction]:
        """
        Predict a complete workflow from current state to goal completion.
        
        Args:
            starting_state: Starting page state
            user_goal: User's goal
            max_steps: Maximum steps to predict
            
        Returns:
            Complete predicted workflow
        """
        try:
            self.logger.info(f"Predicting complete workflow for: {user_goal.primary_goal}")
            
            workflow = []
            current_state = starting_state
            
            for step_num in range(max_steps):
                # Predict next step
                next_steps = await self.predict_next_steps(current_state, user_goal, 1)
                
                if not next_steps:
                    break
                
                best_step = next_steps[0]
                workflow.append(best_step)
                
                # Simulate step completion for next prediction
                current_state = await self._simulate_step_completion(best_step, current_state)
                
                # Update user goal with completed step
                user_goal.completed_steps.append(best_step.step_id)
                
                # Check if goal is likely achieved
                if await self._is_goal_likely_achieved(user_goal, current_state):
                    break
            
            self.logger.info(f"Predicted complete workflow with {len(workflow)} steps")
            return workflow
            
        except Exception as e:
            self.logger.error(f"Complete workflow prediction failed: {e}")
            return []
    
    async def validate_prediction(
        self, 
        prediction: NextStepPrediction, 
        current_state: PageState
    ) -> Dict[str, Any]:
        """
        Validate if a prediction is still valid given the current state.
        
        Args:
            prediction: The prediction to validate
            current_state: Current page state
            
        Returns:
            Validation results with updated confidence and recommendations
        """
        try:
            validation_result = {
                "is_valid": True,
                "confidence_adjustment": 0.0,
                "blocking_issues": [],
                "recommendations": [],
                "updated_parameters": {}
            }
            
            # Check if required elements are still available
            for required_element in prediction.required_elements:
                if not self._is_element_available(required_element, current_state):
                    validation_result["is_valid"] = False
                    validation_result["blocking_issues"].append(f"Required element not found: {required_element}")
                    validation_result["confidence_adjustment"] -= 0.3
            
            # Check if page state has changed significantly
            state_change_impact = await self._assess_state_change_impact(prediction, current_state)
            validation_result["confidence_adjustment"] += state_change_impact
            
            # Generate recommendations if validation fails
            if not validation_result["is_valid"]:
                validation_result["recommendations"] = await self._generate_alternative_recommendations(
                    prediction, current_state
                )
            
            return validation_result
            
        except Exception as e:
            self.logger.error(f"Prediction validation failed: {e}")
            return {"is_valid": False, "error": str(e)}
    
    async def learn_from_execution(
        self, 
        prediction: NextStepPrediction, 
        execution_result: Dict[str, Any],
        actual_outcome: str
    ):
        """
        Learn from prediction execution results to improve future predictions.
        
        Args:
            prediction: The original prediction
            execution_result: Result of executing the prediction
            actual_outcome: What actually happened
        """
        try:
            if not self.enable_learning:
                return
            
            # Record success/failure patterns
            success = execution_result.get("success", False)
            
            learning_entry = {
                "prediction_id": prediction.step_id,
                "step_type": prediction.step_type.value,
                "predicted_confidence": prediction.confidence_score,
                "actual_success": success,
                "execution_time": execution_result.get("execution_time", 0),
                "actual_outcome": actual_outcome,
                "expected_outcome": prediction.expected_outcome,
                "timestamp": datetime.now().isoformat()
            }
            
            if success:
                # Update success patterns
                pattern_key = f"{prediction.step_type.value}_{prediction.parameters.get('context', 'general')}"
                if pattern_key not in self.success_patterns:
                    self.success_patterns[pattern_key] = []
                self.success_patterns[pattern_key].append(learning_entry)
            else:
                # Update failure patterns
                failure_reason = execution_result.get("error", "unknown")
                pattern_key = f"{prediction.step_type.value}_{failure_reason}"
                if pattern_key not in self.failure_patterns:
                    self.failure_patterns[pattern_key] = []
                self.failure_patterns[pattern_key].append(learning_entry)
            
            # Update confidence calibration
            await self._update_confidence_calibration(prediction, success)
            
            self.logger.info(f"Learned from execution: {prediction.step_id} ({'success' if success else 'failure'})")
            
        except Exception as e:
            self.logger.error(f"Learning from execution failed: {e}")
    
    # Private helper methods
    
    async def _analyze_context(self, page_state: PageState, user_goal: UserGoal) -> Dict[str, Any]:
        """Analyze current context using AI."""
        prompt = f"""
        Analyze the current web automation context:
        
        Page URL: {page_state.url}
        Page Title: {page_state.title}
        Page Type: {page_state.page_type}
        Available Elements: {len(page_state.elements)} elements
        Forms: {len(page_state.forms)} forms
        Buttons: {len(page_state.buttons)} buttons
        Links: {len(page_state.links)} links
        
        User Goal: {user_goal.primary_goal}
        Completed Steps: {user_goal.completed_steps}
        Failed Attempts: {user_goal.failed_attempts}
        
        Analyze and provide:
        1. Current progress assessment
        2. Immediate opportunities
        3. Potential obstacles
        4. Recommended next action type
        5. Risk factors
        
        Return as JSON with structured analysis.
        """
        
        response = await self.chat_ai.chat(prompt)
        
        try:
            json_match = re.search(r'\{.*\}', response.get("response", ""), re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        
        return {
            "progress": "unknown",
            "opportunities": ["continue"],
            "obstacles": [],
            "recommended_action": "analyze_elements",
            "risk_factors": []
        }
    
    async def _predict_from_patterns(
        self, 
        page_state: PageState, 
        user_goal: UserGoal, 
        context_analysis: Dict[str, Any]
    ) -> List[NextStepPrediction]:
        """Generate predictions based on learned patterns."""
        predictions = []
        
        # Look for matching patterns in success database
        for pattern_key, pattern_data in self.success_patterns.items():
            if self._pattern_matches_context(pattern_key, page_state, user_goal):
                # Generate prediction based on successful pattern
                prediction = self._create_pattern_based_prediction(pattern_key, pattern_data, page_state)
                if prediction:
                    predictions.append(prediction)
        
        return predictions
    
    async def _predict_with_ai(
        self, 
        page_state: PageState, 
        user_goal: UserGoal, 
        context_analysis: Dict[str, Any]
    ) -> List[NextStepPrediction]:
        """Generate predictions using AI analysis."""
        prompt = f"""
        Based on the current state and goal, predict the next logical steps:
        
        Current Context: {json.dumps(context_analysis, indent=2)}
        Goal: {user_goal.primary_goal}
        Page Type: {page_state.page_type}
        
        Generate 2-3 next step predictions with:
        - Step type (navigation, form_fill, click_action, data_extract, validation, wait)
        - Description of the action
        - Confidence level (0.0-1.0)
        - Reasoning
        - Required elements
        - Expected outcome
        - Estimated time in seconds
        
        Return as JSON array of predictions.
        """
        
        response = await self.chat_ai.chat(prompt)
        
        try:
            json_match = re.search(r'\[.*\]', response.get("response", ""), re.DOTALL)
            if json_match:
                ai_predictions_data = json.loads(json_match.group())
                return [self._convert_ai_data_to_prediction(data) for data in ai_predictions_data]
        except:
            pass
        
        return []
    
    async def _predict_from_elements(self, page_state: PageState, user_goal: UserGoal) -> List[NextStepPrediction]:
        """Generate predictions based on available page elements."""
        predictions = []
        
        # Form-based predictions
        if page_state.forms and "fill" in user_goal.primary_goal.lower():
            for form in page_state.forms:
                prediction = NextStepPrediction(
                    step_id=f"fill_form_{form.get('id', 'unknown')}",
                    step_type=StepType.FORM_FILL,
                    description=f"Fill form: {form.get('name', 'unnamed form')}",
                    confidence=StepConfidence.HIGH,
                    confidence_score=0.8,
                    reasoning="Form detected and goal involves filling",
                    required_elements=[form.get('id', 'form')],
                    expected_outcome="Form fields populated",
                    estimated_time=30.0,
                    risk_level="low",
                    parameters={"form_id": form.get('id'), "form_data": {}},
                    alternatives=[]
                )
                predictions.append(prediction)
        
        # Button-based predictions
        if page_state.buttons:
            for button in page_state.buttons:
                button_text = button.get('text', '').lower()
                if any(keyword in button_text for keyword in ['submit', 'save', 'continue', 'next']):
                    prediction = NextStepPrediction(
                        step_id=f"click_button_{button.get('id', 'unknown')}",
                        step_type=StepType.CLICK_ACTION,
                        description=f"Click button: {button.get('text', 'button')}",
                        confidence=StepConfidence.MEDIUM,
                        confidence_score=0.6,
                        reasoning="Important action button detected",
                        required_elements=[button.get('id', 'button')],
                        expected_outcome="Action executed, possible page change",
                        estimated_time=5.0,
                        risk_level="medium",
                        parameters={"element_id": button.get('id'), "element_type": "button"},
                        alternatives=[]
                    )
                    predictions.append(prediction)
        
        return predictions
    
    def _load_pattern_database(self):
        """Load historical pattern database."""
        # Implementation for loading patterns from storage
        pass
    
    def _deduplicate_predictions(self, predictions: List[NextStepPrediction]) -> List[NextStepPrediction]:
        """Remove duplicate predictions."""
        seen_descriptions = set()
        unique_predictions = []
        
        for prediction in predictions:
            if prediction.description not in seen_descriptions:
                seen_descriptions.add(prediction.description)
                unique_predictions.append(prediction)
        
        return unique_predictions
    
    async def _rank_predictions(
        self, 
        predictions: List[NextStepPrediction], 
        context_analysis: Dict[str, Any]
    ) -> List[NextStepPrediction]:
        """Rank predictions by relevance and confidence."""
        # Sort by confidence score (highest first)
        return sorted(predictions, key=lambda p: p.confidence_score, reverse=True)
    
    def _convert_ai_data_to_prediction(self, data: Dict[str, Any]) -> NextStepPrediction:
        """Convert AI prediction data to NextStepPrediction object."""
        return NextStepPrediction(
            step_id=f"ai_pred_{hash(data.get('description', ''))}"[:16],
            step_type=StepType(data.get('step_type', 'click_action')),
            description=data.get('description', 'AI suggested action'),
            confidence=StepConfidence.MEDIUM,
            confidence_score=data.get('confidence', 0.5),
            reasoning=data.get('reasoning', 'AI analysis'),
            required_elements=data.get('required_elements', []),
            expected_outcome=data.get('expected_outcome', 'Unknown'),
            estimated_time=data.get('estimated_time', 10.0),
            risk_level=data.get('risk_level', 'medium'),
            parameters=data.get('parameters', {}),
            alternatives=data.get('alternatives', [])
        )
    
    # Additional helper methods would continue here...
    # (Placeholder implementations for completeness)
    
    async def _predict_from_goal_analysis(self, user_goal: UserGoal, page_state: PageState) -> List[NextStepPrediction]:
        """Generate predictions based on goal analysis."""
        return []
    
    def _pattern_matches_context(self, pattern_key: str, page_state: PageState, user_goal: UserGoal) -> bool:
        """Check if a pattern matches the current context."""
        return False
    
    def _create_pattern_based_prediction(self, pattern_key: str, pattern_data: List, page_state: PageState) -> Optional[NextStepPrediction]:
        """Create a prediction based on a successful pattern."""
        return None
    
    async def _simulate_step_completion(self, step: NextStepPrediction, current_state: PageState) -> PageState:
        """Simulate step completion for workflow prediction."""
        return current_state
    
    async def _is_goal_likely_achieved(self, user_goal: UserGoal, current_state: PageState) -> bool:
        """Check if the goal is likely achieved."""
        return len(user_goal.completed_steps) >= 5  # Simple heuristic
    
    def _is_element_available(self, element_id: str, current_state: PageState) -> bool:
        """Check if an element is available on the current page."""
        return any(elem.get('id') == element_id for elem in current_state.elements)
    
    async def _assess_state_change_impact(self, prediction: NextStepPrediction, current_state: PageState) -> float:
        """Assess impact of state changes on prediction validity."""
        return 0.0
    
    async def _generate_alternative_recommendations(self, prediction: NextStepPrediction, current_state: PageState) -> List[str]:
        """Generate alternative recommendations when prediction is invalid."""
        return ["retry_with_different_approach", "wait_for_page_load", "refresh_page"]
    
    async def _update_confidence_calibration(self, prediction: NextStepPrediction, success: bool):
        """Update confidence calibration based on results."""
        pass
