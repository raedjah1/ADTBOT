"""
Decision engine for intelligent automation decisions.

Makes smart decisions about automation strategies, timing,
and error recovery based on context and learning.
"""

import time
import random
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
from dataclasses import dataclass
from ..core.base_component import BaseComponent


class ActionType(Enum):
    """Types of automation actions."""
    CLICK = "click"
    FILL = "fill"
    SELECT = "select"
    WAIT = "wait"
    NAVIGATE = "navigate"
    SCROLL = "scroll"
    HOVER = "hover"
    KEYBOARD = "keyboard"


class ConfidenceLevel(Enum):
    """Confidence levels for decisions."""
    VERY_LOW = 0.2
    LOW = 0.4
    MEDIUM = 0.6
    HIGH = 0.8
    VERY_HIGH = 0.9


@dataclass
class ActionDecision:
    """Represents a decision about an automation action."""
    action_type: ActionType
    confidence: float
    parameters: Dict[str, Any]
    reasoning: str
    fallback_actions: List['ActionDecision'] = None
    estimated_duration: float = 1.0
    risk_level: str = "low"
    
    def __post_init__(self):
        if self.fallback_actions is None:
            self.fallback_actions = []


@dataclass
class PageContext:
    """Context information about the current page."""
    url: str
    title: str
    page_type: str = "unknown"
    loading_time: float = 0.0
    interactive_elements: int = 0
    form_elements: int = 0
    has_captcha: bool = False
    requires_authentication: bool = False
    error_indicators: List[str] = None
    
    def __post_init__(self):
        if self.error_indicators is None:
            self.error_indicators = []


class DecisionEngine(BaseComponent):
    """
    Intelligent decision engine for web automation.
    
    Features:
    - Context-aware decision making
    - Risk assessment
    - Adaptive timing
    - Learning from outcomes
    - Fallback strategy generation
    """
    
    def __init__(self, config: Dict = None):
        """
        Initialize the decision engine.
        
        Args:
            config: Configuration dictionary
        """
        super().__init__("decision_engine", config)
        
        # Decision history for learning
        self.decision_history = []
        self.success_patterns = {}
        self.failure_patterns = {}
        
        # Page type classifiers
        self.page_classifiers = {
            'login': self._is_login_page,
            'search': self._is_search_page,
            'form': self._is_form_page,
            'ecommerce': self._is_ecommerce_page,
            'social': self._is_social_media_page
        }
        
        # Risk assessment rules
        self.risk_rules = {
            'financial': ['bank', 'payment', 'credit', 'money'],
            'authentication': ['login', 'password', 'auth'],
            'destructive': ['delete', 'remove', 'cancel'],
            'submission': ['submit', 'send', 'post']
        }
        
    def initialize(self) -> bool:
        """Initialize the decision engine."""
        try:
            self.logger.info("Initializing Decision Engine")
            
            # Load historical patterns
            self._load_decision_patterns()
            
            # Initialize adaptive parameters
            self._init_adaptive_parameters()
            
            self.is_initialized = True
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize decision engine: {e}")
            return False
    
    def cleanup(self) -> bool:
        """Clean up decision engine resources."""
        try:
            # Save learned patterns
            self._save_decision_patterns()
            return True
        except Exception as e:
            self.logger.error(f"Decision engine cleanup failed: {e}")
            return False
    
    def analyze_page_context(self, driver) -> PageContext:
        """
        Analyze the current page context.
        
        Args:
            driver: Selenium WebDriver instance
        
        Returns:
            PageContext object with analysis results
        """
        try:
            start_time = time.time()
            
            # Basic page information
            url = driver.current_url
            title = driver.title
            
            # Classify page type
            page_type = self._classify_page_type(driver)
            
            # Count interactive elements
            interactive_elements = len(driver.find_elements("tag name", "button")) + \
                                 len(driver.find_elements("tag name", "input")) + \
                                 len(driver.find_elements("tag name", "select")) + \
                                 len(driver.find_elements("tag name", "a"))
            
            # Count form elements
            form_elements = len(driver.find_elements("tag name", "form"))
            
            # Check for CAPTCHA
            has_captcha = self._detect_captcha(driver)
            
            # Check authentication requirements
            requires_auth = self._requires_authentication(driver)
            
            # Detect error indicators
            error_indicators = self._detect_errors(driver)
            
            loading_time = time.time() - start_time
            
            context = PageContext(
                url=url,
                title=title,
                page_type=page_type,
                loading_time=loading_time,
                interactive_elements=interactive_elements,
                form_elements=form_elements,
                has_captcha=has_captcha,
                requires_authentication=requires_auth,
                error_indicators=error_indicators
            )
            
            self.logger.debug(f"Page context analyzed: {page_type}")
            return context
            
        except Exception as e:
            self.logger.error(f"Page context analysis failed: {e}")
            return PageContext(url="", title="", page_type="error")
    
    def decide_action(self, intent: str, context: PageContext, 
                     available_elements: List = None) -> ActionDecision:
        """
        Decide on the best action to take.
        
        Args:
            intent: User intent description
            context: Current page context
            available_elements: List of available elements
        
        Returns:
            ActionDecision with recommended action
        """
        try:
            self.logger.info(f"Deciding action for intent: {intent}")
            
            # Analyze intent
            intent_analysis = self._analyze_intent(intent)
            
            # Assess risk
            risk_level = self._assess_risk(intent, context)
            
            # Generate action candidates
            candidates = self._generate_action_candidates(intent_analysis, context, available_elements)
            
            # Score and rank candidates
            best_candidate = self._select_best_candidate(candidates, context)
            
            # Generate fallback strategies
            fallbacks = self._generate_fallback_strategies(best_candidate, candidates)
            
            # Create final decision
            decision = ActionDecision(
                action_type=best_candidate['action_type'],
                confidence=best_candidate['confidence'],
                parameters=best_candidate['parameters'],
                reasoning=best_candidate['reasoning'],
                fallback_actions=fallbacks,
                estimated_duration=best_candidate.get('duration', 1.0),
                risk_level=risk_level
            )
            
            # Record decision for learning
            self._record_decision(decision, intent, context)
            
            self.update_metrics("decide_action", True)
            return decision
            
        except Exception as e:
            self.logger.error(f"Action decision failed: {e}")
            self.update_metrics("decide_action", False)
            
            # Return safe fallback decision
            return ActionDecision(
                action_type=ActionType.WAIT,
                confidence=0.1,
                parameters={'seconds': 1},
                reasoning="Fallback due to decision error",
                risk_level="high"
            )
    
    def decide_timing(self, action_type: ActionType, context: PageContext) -> float:
        """
        Decide on optimal timing for an action.
        
        Args:
            action_type: Type of action to perform
            context: Current page context
        
        Returns:
            Recommended delay in seconds
        """
        base_delay = self.config.get('base_delay', 1.0)
        
        # Adjust based on action type
        action_multipliers = {
            ActionType.CLICK: 1.0,
            ActionType.FILL: 0.5,
            ActionType.SELECT: 0.8,
            ActionType.WAIT: 1.0,
            ActionType.NAVIGATE: 2.0,
            ActionType.SCROLL: 0.3,
            ActionType.HOVER: 0.2,
            ActionType.KEYBOARD: 0.1
        }
        
        delay = base_delay * action_multipliers.get(action_type, 1.0)
        
        # Adjust based on page context
        if context.has_captcha:
            delay *= 2.0
        
        if context.page_type == 'form':
            delay *= 0.8
        
        if len(context.error_indicators) > 0:
            delay *= 1.5
        
        # Add human-like randomization
        if self.config.get('human_like_timing', True):
            randomization = random.uniform(0.8, 1.2)
            delay *= randomization
        
        return max(delay, 0.1)  # Minimum delay
    
    def should_retry(self, action: ActionDecision, failure_count: int, 
                    error: Exception = None) -> bool:
        """
        Decide whether to retry a failed action.
        
        Args:
            action: The failed action
            failure_count: Number of previous failures
            error: The error that occurred
        
        Returns:
            True if should retry, False otherwise
        """
        max_retries = self.config.get('max_retries', 3)
        
        # Don't retry if max attempts reached
        if failure_count >= max_retries:
            return False
        
        # Don't retry high-risk actions multiple times
        if action.risk_level == "high" and failure_count >= 1:
            return False
        
        # Don't retry if confidence is very low
        if action.confidence < 0.3:
            return False
        
        # Analyze error type
        if error:
            error_type = type(error).__name__
            
            # Don't retry certain error types
            non_retryable_errors = [
                'ElementNotInteractableException',
                'InvalidElementStateException'
            ]
            
            if error_type in non_retryable_errors:
                return False
        
        self.logger.info(f"Deciding to retry action (attempt {failure_count + 1})")
        return True
    
    def _classify_page_type(self, driver) -> str:
        """Classify the type of the current page."""
        for page_type, classifier in self.page_classifiers.items():
            if classifier(driver):
                return page_type
        return "unknown"
    
    def _is_login_page(self, driver) -> bool:
        """Check if current page is a login page."""
        indicators = [
            'password', 'login', 'sign in', 'auth', 'username'
        ]
        
        page_text = driver.page_source.lower()
        return any(indicator in page_text for indicator in indicators)
    
    def _is_search_page(self, driver) -> bool:
        """Check if current page is a search page."""
        try:
            search_inputs = driver.find_elements("css selector", 
                "input[type='search'], input[name*='search'], input[placeholder*='search']")
            return len(search_inputs) > 0
        except:
            return False
    
    def _is_form_page(self, driver) -> bool:
        """Check if current page has forms."""
        try:
            forms = driver.find_elements("tag name", "form")
            return len(forms) > 0
        except:
            return False
    
    def _is_ecommerce_page(self, driver) -> bool:
        """Check if current page is an e-commerce page."""
        indicators = ['cart', 'buy', 'price', 'product', 'shop']
        page_text = driver.page_source.lower()
        return sum(indicator in page_text for indicator in indicators) >= 2
    
    def _is_social_media_page(self, driver) -> bool:
        """Check if current page is a social media page."""
        social_domains = ['facebook', 'twitter', 'instagram', 'linkedin']
        current_url = driver.current_url.lower()
        return any(domain in current_url for domain in social_domains)
    
    def _detect_captcha(self, driver) -> bool:
        """Detect if page has CAPTCHA."""
        captcha_indicators = [
            'recaptcha', 'captcha', 'hcaptcha', 'challenge'
        ]
        
        page_source = driver.page_source.lower()
        return any(indicator in page_source for indicator in captcha_indicators)
    
    def _requires_authentication(self, driver) -> bool:
        """Check if page requires authentication."""
        auth_indicators = [
            'login', 'sign in', 'authenticate', 'unauthorized'
        ]
        
        page_text = driver.page_source.lower()
        return any(indicator in page_text for indicator in auth_indicators)
    
    def _detect_errors(self, driver) -> List[str]:
        """Detect error messages on the page."""
        error_indicators = []
        
        # Common error selectors
        error_selectors = [
            '.error', '.alert-error', '.danger', '.warning',
            '[role="alert"]', '.error-message'
        ]
        
        for selector in error_selectors:
            try:
                elements = driver.find_elements("css selector", selector)
                for element in elements:
                    if element.is_displayed() and element.text.strip():
                        error_indicators.append(element.text.strip())
            except:
                continue
        
        return error_indicators
    
    def _analyze_intent(self, intent: str) -> Dict:
        """Analyze user intent to determine action type."""
        intent_lower = intent.lower()
        
        # Intent patterns
        patterns = {
            'click': ['click', 'press', 'tap', 'select', 'choose'],
            'fill': ['fill', 'enter', 'type', 'input', 'write'],
            'navigate': ['go to', 'visit', 'navigate', 'open'],
            'search': ['search', 'find', 'look for'],
            'submit': ['submit', 'send', 'post', 'save'],
            'wait': ['wait', 'pause', 'delay']
        }
        
        detected_intents = []
        for action_type, keywords in patterns.items():
            if any(keyword in intent_lower for keyword in keywords):
                detected_intents.append(action_type)
        
        return {
            'primary_intent': detected_intents[0] if detected_intents else 'unknown',
            'all_intents': detected_intents,
            'confidence': 0.8 if detected_intents else 0.3
        }
    
    def _assess_risk(self, intent: str, context: PageContext) -> str:
        """Assess the risk level of the intended action."""
        risk_score = 0
        
        intent_lower = intent.lower()
        
        # Check for risky keywords
        for risk_category, keywords in self.risk_rules.items():
            if any(keyword in intent_lower for keyword in keywords):
                if risk_category == 'financial':
                    risk_score += 3
                elif risk_category == 'destructive':
                    risk_score += 2
                else:
                    risk_score += 1
        
        # Context-based risk assessment
        if context.requires_authentication:
            risk_score += 1
        
        if context.has_captcha:
            risk_score += 1
        
        if len(context.error_indicators) > 0:
            risk_score += 2
        
        # Determine risk level
        if risk_score >= 4:
            return "high"
        elif risk_score >= 2:
            return "medium"
        else:
            return "low"
    
    def _generate_action_candidates(self, intent_analysis: Dict, 
                                  context: PageContext, 
                                  available_elements: List) -> List[Dict]:
        """Generate candidate actions based on intent and context."""
        candidates = []
        
        primary_intent = intent_analysis['primary_intent']
        confidence = intent_analysis['confidence']
        
        # Generate candidates based on intent
        if primary_intent == 'click':
            candidates.append({
                'action_type': ActionType.CLICK,
                'confidence': confidence,
                'parameters': {},
                'reasoning': 'Direct click action based on intent',
                'duration': 1.0
            })
        
        elif primary_intent == 'fill':
            candidates.append({
                'action_type': ActionType.FILL,
                'confidence': confidence,
                'parameters': {},
                'reasoning': 'Fill action based on intent',
                'duration': 2.0
            })
        
        elif primary_intent == 'navigate':
            candidates.append({
                'action_type': ActionType.NAVIGATE,
                'confidence': confidence,
                'parameters': {},
                'reasoning': 'Navigation action based on intent',
                'duration': 5.0
            })
        
        # Add context-based candidates
        if context.page_type == 'form' and primary_intent in ['fill', 'unknown']:
            candidates.append({
                'action_type': ActionType.FILL,
                'confidence': 0.7,
                'parameters': {},
                'reasoning': 'Form context suggests fill action',
                'duration': 2.0
            })
        
        return candidates
    
    def _select_best_candidate(self, candidates: List[Dict], context: PageContext) -> Dict:
        """Select the best candidate action."""
        if not candidates:
            return {
                'action_type': ActionType.WAIT,
                'confidence': 0.1,
                'parameters': {'seconds': 1},
                'reasoning': 'No viable candidates found',
                'duration': 1.0
            }
        
        # Score candidates
        scored_candidates = []
        for candidate in candidates:
            score = candidate['confidence']
            
            # Adjust score based on context
            if context.page_type == 'login' and candidate['action_type'] == ActionType.FILL:
                score *= 1.2
            
            scored_candidates.append((candidate, score))
        
        # Sort by score
        scored_candidates.sort(key=lambda x: x[1], reverse=True)
        
        return scored_candidates[0][0]
    
    def _generate_fallback_strategies(self, primary_action: Dict, 
                                    all_candidates: List[Dict]) -> List[ActionDecision]:
        """Generate fallback strategies for the primary action."""
        fallbacks = []
        
        # Add other candidates as fallbacks
        for candidate in all_candidates:
            if candidate != primary_action:
                fallback = ActionDecision(
                    action_type=candidate['action_type'],
                    confidence=candidate['confidence'] * 0.8,
                    parameters=candidate['parameters'],
                    reasoning=f"Fallback: {candidate['reasoning']}"
                )
                fallbacks.append(fallback)
        
        # Add generic fallbacks
        if primary_action['action_type'] != ActionType.WAIT:
            wait_fallback = ActionDecision(
                action_type=ActionType.WAIT,
                confidence=0.5,
                parameters={'seconds': 2},
                reasoning="Generic wait fallback"
            )
            fallbacks.append(wait_fallback)
        
        return fallbacks[:3]  # Limit to 3 fallbacks
    
    def _record_decision(self, decision: ActionDecision, intent: str, context: PageContext):
        """Record decision for learning purposes."""
        decision_record = {
            'timestamp': time.time(),
            'intent': intent,
            'decision': decision,
            'context': context,
            'outcome': None  # To be filled when outcome is known
        }
        
        self.decision_history.append(decision_record)
        
        # Limit history size
        if len(self.decision_history) > 1000:
            self.decision_history = self.decision_history[-500:]
    
    def record_outcome(self, success: bool, error: Exception = None):
        """Record the outcome of the last decision."""
        if self.decision_history:
            last_decision = self.decision_history[-1]
            last_decision['outcome'] = {
                'success': success,
                'error': str(error) if error else None,
                'timestamp': time.time()
            }
            
            # Update learning patterns
            if success:
                self._update_success_patterns(last_decision)
            else:
                self._update_failure_patterns(last_decision)
    
    def _update_success_patterns(self, decision_record: Dict):
        """Update successful decision patterns."""
        pattern_key = f"{decision_record['intent']}_{decision_record['context'].page_type}"
        
        if pattern_key not in self.success_patterns:
            self.success_patterns[pattern_key] = []
        
        self.success_patterns[pattern_key].append({
            'action_type': decision_record['decision'].action_type,
            'confidence': decision_record['decision'].confidence,
            'timestamp': decision_record['timestamp']
        })
    
    def _update_failure_patterns(self, decision_record: Dict):
        """Update failed decision patterns."""
        pattern_key = f"{decision_record['intent']}_{decision_record['context'].page_type}"
        
        if pattern_key not in self.failure_patterns:
            self.failure_patterns[pattern_key] = []
        
        self.failure_patterns[pattern_key].append({
            'action_type': decision_record['decision'].action_type,
            'confidence': decision_record['decision'].confidence,
            'error': decision_record['outcome']['error'],
            'timestamp': decision_record['timestamp']
        })
    
    def _load_decision_patterns(self):
        """Load historical decision patterns."""
        # This would load from a file or database
        # For now, initialize empty
        self.success_patterns = {}
        self.failure_patterns = {}
    
    def _save_decision_patterns(self):
        """Save learned decision patterns."""
        # This would save to a file or database
        self.logger.info(f"Saving {len(self.success_patterns)} success patterns")
        self.logger.info(f"Saving {len(self.failure_patterns)} failure patterns")
    
    def _init_adaptive_parameters(self):
        """Initialize adaptive parameters."""
        # Set default adaptive parameters
        self.adaptive_params = {
            'confidence_threshold': 0.6,
            'retry_multiplier': 1.0,
            'timing_multiplier': 1.0
        }
