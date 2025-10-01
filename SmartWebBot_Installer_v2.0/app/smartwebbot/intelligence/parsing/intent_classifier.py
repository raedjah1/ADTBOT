"""
Intent Classifier for Intelligent Chat System.

Classifies user intent from natural language commands
using pattern matching and AI-powered classification.
"""

import re
from typing import Dict, Optional, Any
from ..core.base_chat_component import BaseChatComponent


class IntentClassifier(BaseChatComponent):
    """
    Classifies user intent from command text.
    
    Features:
    - Pattern-based classification
    - Confidence scoring
    - Intent hierarchy
    - Fallback handling
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("intent_classifier", config)
        
        # Classification patterns
        self.intent_patterns = self._load_intent_patterns()
        self.intent_hierarchy = self._load_intent_hierarchy()
    
    def initialize(self) -> bool:
        """Initialize the intent classifier."""
        try:
            self.logger.info("Initializing Intent Classifier...")
            
            self.is_initialized = True
            self.is_healthy = True
            
            self.logger.info("Intent Classifier initialized successfully")
            return True
            
        except Exception as e:
            self.log_error(e, "Intent classifier initialization")
            return False
    
    async def classify(self, text: str) -> str:
        """Classify intent from text."""
        
        try:
            # Score all intents
            intent_scores = {}
            
            for intent, patterns in self.intent_patterns.items():
                score = self._calculate_intent_score(text, patterns)
                if score > 0:
                    intent_scores[intent] = score
            
            # Return highest scoring intent
            if intent_scores:
                best_intent = max(intent_scores, key=intent_scores.get)
                self.logger.debug(f"Classified intent: {best_intent} (score: {intent_scores[best_intent]:.2f})")
                return best_intent
            
            # Fallback
            return "general_automation"
            
        except Exception as e:
            self.log_error(e, f"Intent classification failed for: {text}")
            return "general_automation"
    
    def _calculate_intent_score(self, text: str, patterns: list) -> float:
        """Calculate score for an intent based on patterns."""
        
        score = 0.0
        text_lower = text.lower()
        
        for pattern_info in patterns:
            if isinstance(pattern_info, dict):
                pattern = pattern_info["pattern"]
                weight = pattern_info.get("weight", 1.0)
            else:
                pattern = pattern_info
                weight = 1.0
            
            if re.search(pattern, text_lower):
                score += weight
        
        return score
    
    def _load_intent_patterns(self) -> Dict[str, list]:
        """Load intent classification patterns."""
        
        return {
            "social_media_post": [
                {"pattern": r"post.*on|create.*post|share.*on", "weight": 2.0},
                {"pattern": r"instagram.*post|facebook.*post|twitter.*post", "weight": 2.5},
                {"pattern": r"social.*media.*content", "weight": 1.5},
                {"pattern": r"upload.*to|publish.*on", "weight": 1.8},
                {"pattern": r"story.*on|reel.*on", "weight": 2.0}
            ],
            "login_to_platform": [
                {"pattern": r"login.*to|sign.*in.*to|log.*into", "weight": 2.5},
                {"pattern": r"authenticate.*with|access.*account", "weight": 2.0},
                {"pattern": r"enter.*credentials|provide.*login", "weight": 1.8}
            ],
            "form_interaction": [
                {"pattern": r"fill.*form|complete.*form|submit.*form", "weight": 2.5},
                {"pattern": r"enter.*information|provide.*details", "weight": 2.0},
                {"pattern": r"contact.*form|registration.*form", "weight": 2.2},
                {"pattern": r"input.*data|type.*in.*fields", "weight": 1.8}
            ],
            "data_extraction": [
                {"pattern": r"extract.*data|scrape.*from|get.*information", "weight": 2.5},
                {"pattern": r"collect.*data|gather.*from", "weight": 2.0},
                {"pattern": r"download.*from|save.*data", "weight": 1.8},
                {"pattern": r"export.*to|retrieve.*data", "weight": 1.5}
            ],
            "navigation": [
                {"pattern": r"navigate.*to|go.*to|visit.*website", "weight": 2.0},
                {"pattern": r"open.*page|browse.*to", "weight": 1.8},
                {"pattern": r"redirect.*to|load.*page", "weight": 1.5}
            ],
            "marketing_campaign": [
                {"pattern": r"marketing.*campaign|promote.*product", "weight": 2.5},
                {"pattern": r"advertise.*on|market.*my", "weight": 2.2},
                {"pattern": r"run.*ads|create.*campaign", "weight": 2.0},
                {"pattern": r"boost.*post|promote.*content", "weight": 1.8}
            ],
            "e_commerce": [
                {"pattern": r"buy.*from|purchase.*on|shop.*at", "weight": 2.0},
                {"pattern": r"add.*to.*cart|checkout|order.*from", "weight": 2.2},
                {"pattern": r"product.*page|item.*details", "weight": 1.5}
            ],
            "search_operation": [
                {"pattern": r"search.*for|find.*on|look.*for", "weight": 2.0},
                {"pattern": r"query.*database|search.*results", "weight": 1.8},
                {"pattern": r"filter.*by|sort.*by", "weight": 1.5}
            ],
            "content_creation": [
                {"pattern": r"create.*content|write.*post|generate.*text", "weight": 2.0},
                {"pattern": r"compose.*message|draft.*email", "weight": 1.8},
                {"pattern": r"design.*graphic|make.*image", "weight": 1.5}
            ],
            "automation_workflow": [
                {"pattern": r"automate.*process|workflow.*for", "weight": 2.5},
                {"pattern": r"repeat.*action|batch.*process", "weight": 2.0},
                {"pattern": r"schedule.*task|run.*automatically", "weight": 1.8}
            ]
        }
    
    def _load_intent_hierarchy(self) -> Dict[str, list]:
        """Load intent hierarchy for fallback."""
        
        return {
            "social_media_post": ["content_creation", "general_automation"],
            "marketing_campaign": ["social_media_post", "content_creation", "automation_workflow"],
            "data_extraction": ["search_operation", "automation_workflow"],
            "form_interaction": ["automation_workflow", "general_automation"],
            "e_commerce": ["navigation", "form_interaction"],
            "login_to_platform": ["authentication", "navigation"],
            "navigation": ["general_automation"],
            "search_operation": ["navigation", "general_automation"],
            "content_creation": ["general_automation"],
            "automation_workflow": ["general_automation"]
        }
    
    def get_intent_confidence(self, text: str, intent: str) -> float:
        """Get confidence score for a specific intent."""
        
        patterns = self.intent_patterns.get(intent, [])
        if not patterns:
            return 0.0
        
        score = self._calculate_intent_score(text, patterns)
        max_possible_score = sum(p.get("weight", 1.0) if isinstance(p, dict) else 1.0 for p in patterns)
        
        return min(score / max_possible_score, 1.0) if max_possible_score > 0 else 0.0