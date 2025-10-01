"""
Command Parser for Intelligent Chat System.

Parses natural language commands into structured data
with intent recognition and parameter extraction.
"""

import re
import time
from typing import Dict, List, Optional, Any
from ..core.base_chat_component import BaseChatComponent
from ..core.interfaces import ICommandParser, IParsedCommand, CommandComplexity, CredentialType


class CommandParser(BaseChatComponent, ICommandParser):
    """
    Parses natural language commands into structured format.
    
    Features:
    - Intent recognition
    - Platform detection  
    - Parameter extraction
    - Complexity assessment
    - Credential requirement detection
    """
    
    def __init__(self, intent_classifier=None, entity_extractor=None, complexity_assessor=None, config: Optional[Dict[str, Any]] = None):
        super().__init__("command_parser", config)
        
        # Sub-components (can be injected)
        self.intent_classifier = intent_classifier
        self.entity_extractor = entity_extractor
        self.complexity_assessor = complexity_assessor
        
        # Parsing patterns
        self.platform_patterns = self._load_platform_patterns()
        self.action_patterns = self._load_action_patterns()
        self.credential_indicators = self._load_credential_indicators()
    
    def initialize(self) -> bool:
        """Initialize the command parser."""
        try:
            self.logger.info("Initializing Command Parser...")
            
            # Initialize sub-components
            if self.intent_classifier and hasattr(self.intent_classifier, 'initialize'):
                if not self.intent_classifier.initialize():
                    self.logger.warning("Intent classifier initialization failed")
            
            if self.entity_extractor and hasattr(self.entity_extractor, 'initialize'):
                if not self.entity_extractor.initialize():
                    self.logger.warning("Entity extractor initialization failed")
            
            if self.complexity_assessor and hasattr(self.complexity_assessor, 'initialize'):
                if not self.complexity_assessor.initialize():
                    self.logger.warning("Complexity assessor initialization failed")
            
            self.is_initialized = True
            self.is_healthy = True
            
            self.logger.info("Command Parser initialized successfully")
            return True
            
        except Exception as e:
            self.log_error(e, "Command parser initialization")
            return False
    
    async def parse(self, user_input: str) -> IParsedCommand:
        """Parse natural language input into structured command."""
        
        try:
            self.logger.debug(f"Parsing command: {user_input}")
            
            # Step 1: Basic text processing
            processed_text = self._preprocess_text(user_input)
            
            # Step 2: Extract intent
            intent = await self._extract_intent(processed_text)
            
            # Step 3: Detect target platform
            target_platform = self._detect_platform(processed_text)
            
            # Step 4: Determine action type
            action_type = self._determine_action_type(processed_text, intent)
            
            # Step 5: Extract parameters
            parameters = await self._extract_parameters(processed_text)
            
            # Step 6: Assess complexity
            complexity = await self._assess_complexity(processed_text, intent, parameters)
            
            # Step 7: Determine required credentials
            required_credentials = self._determine_required_credentials(target_platform, action_type)
            
            # Step 8: Estimate steps
            estimated_steps = self._estimate_steps(complexity, action_type)
            
            # Step 9: Calculate confidence
            confidence = self._calculate_confidence(intent, target_platform, action_type)
            
            # Create parsed command
            parsed_command = IParsedCommand(
                original_text=user_input,
                intent=intent,
                target_platform=target_platform,
                action_type=action_type,
                complexity=complexity,
                required_credentials=required_credentials,
                estimated_steps=estimated_steps,
                confidence=confidence,
                parameters=parameters
            )
            
            self.logger.debug(f"Command parsed successfully: {intent} on {target_platform}")
            return parsed_command
            
        except Exception as e:
            self.log_error(e, f"Command parsing failed for: {user_input}")
            
            # Return fallback parsed command
            return IParsedCommand(
                original_text=user_input,
                intent="general_automation",
                target_platform=None,
                action_type="unknown",
                complexity=CommandComplexity.SIMPLE,
                required_credentials=[],
                estimated_steps=1,
                confidence=0.3,
                parameters={"user_input": user_input}
            )
    
    async def validate_command(self, command: IParsedCommand) -> bool:
        """Validate if command is executable."""
        
        try:
            # Check confidence threshold
            if command.confidence < 0.3:
                return False
            
            # Check if we have intent
            if not command.intent or command.intent == "unknown":
                return False
            
            # Command is valid if it meets basic criteria
            return True
            
        except Exception as e:
            self.log_error(e, "Command validation failed")
            return False
    
    def _preprocess_text(self, text: str) -> str:
        """Preprocess input text."""
        
        # Clean up text
        processed = text.strip().lower()
        
        # Remove extra whitespace
        processed = re.sub(r'\s+', ' ', processed)
        
        # Handle common variations
        processed = processed.replace("instagram", "instagram")
        processed = processed.replace("fb", "facebook")
        processed = processed.replace("ig", "instagram")
        
        return processed
    
    async def _extract_intent(self, text: str) -> str:
        """Extract intent from text."""
        
        if self.intent_classifier:
            try:
                return await self.intent_classifier.classify(text)
            except Exception as e:
                self.logger.warning(f"Intent classifier failed: {e}")
        
        # Fallback to pattern-based intent extraction
        return self._extract_intent_patterns(text)
    
    def _extract_intent_patterns(self, text: str) -> str:
        """Extract intent using patterns."""
        
        intent_patterns = {
            "social_media_post": [
                r"post.*on|create.*post|share.*on|upload.*to",
                r"instagram.*post|facebook.*post|twitter.*post",
                r"social.*media.*content"
            ],
            "login_to_platform": [
                r"login.*to|sign.*in.*to|log.*into",
                r"authenticate.*with|access.*account"
            ],
            "form_interaction": [
                r"fill.*form|complete.*form|submit.*form",
                r"enter.*information|provide.*details"
            ],
            "data_extraction": [
                r"extract.*data|scrape.*from|get.*information",
                r"collect.*data|gather.*from"
            ],
            "navigation": [
                r"navigate.*to|go.*to|visit.*website",
                r"open.*page|browse.*to"
            ],
            "marketing_campaign": [
                r"marketing.*campaign|promote.*product",
                r"advertise.*on|market.*my"
            ]
        }
        
        for intent, patterns in intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    return intent
        
        # Default intent
        return "general_automation"
    
    def _detect_platform(self, text: str) -> Optional[str]:
        """Detect target platform from text."""
        
        for platform, patterns in self.platform_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    return platform
        
        return None
    
    def _determine_action_type(self, text: str, intent: str) -> str:
        """Determine the type of action."""
        
        # Map from intent to action type
        intent_to_action = {
            "social_media_post": "post",
            "login_to_platform": "login",
            "form_interaction": "fill_form",
            "data_extraction": "extract",
            "navigation": "navigate",
            "marketing_campaign": "marketing"
        }
        
        action = intent_to_action.get(intent, "unknown")
        
        # Refine based on text patterns
        for action_type, patterns in self.action_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    return action_type
        
        return action
    
    async def _extract_parameters(self, text: str) -> Dict[str, Any]:
        """Extract parameters from text."""
        
        parameters = {}
        
        if self.entity_extractor:
            try:
                entities = await self.entity_extractor.extract(text)
                parameters.update(entities)
            except Exception as e:
                self.logger.warning(f"Entity extraction failed: {e}")
        
        # Fallback parameter extraction
        self._extract_basic_parameters(text, parameters)
        
        return parameters
    
    def _extract_basic_parameters(self, text: str, parameters: Dict[str, Any]) -> None:
        """Extract basic parameters using patterns."""
        
        # Extract URLs
        url_pattern = r'https?://[^\s]+'
        urls = re.findall(url_pattern, text)
        if urls:
            parameters["urls"] = urls
            parameters["url"] = urls[0]
        
        # Extract email addresses
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            parameters["emails"] = emails
            parameters["email"] = emails[0]
        
        # Extract quoted content (potential post content)
        quoted_pattern = r'"([^"]+)"'
        quotes = re.findall(quoted_pattern, text)
        if quotes:
            parameters["content"] = quotes[0]
        
        # Extract hashtags
        hashtag_pattern = r'#\w+'
        hashtags = re.findall(hashtag_pattern, text)
        if hashtags:
            parameters["hashtags"] = hashtags
        
        # Extract mentions
        mention_pattern = r'@\w+'
        mentions = re.findall(mention_pattern, text)
        if mentions:
            parameters["mentions"] = mentions
    
    async def _assess_complexity(self, text: str, intent: str, parameters: Dict[str, Any]) -> CommandComplexity:
        """Assess command complexity."""
        
        if self.complexity_assessor:
            try:
                return await self.complexity_assessor.assess(text, intent, parameters)
            except Exception as e:
                self.logger.warning(f"Complexity assessment failed: {e}")
        
        # Fallback complexity assessment
        return self._assess_complexity_fallback(text, intent, parameters)
    
    def _assess_complexity_fallback(self, text: str, intent: str, parameters: Dict[str, Any]) -> CommandComplexity:
        """Fallback complexity assessment."""
        
        # Simple heuristics
        word_count = len(text.split())
        
        if intent in ["marketing_campaign"]:
            return CommandComplexity.ADVANCED
        elif intent in ["social_media_post", "data_extraction"]:
            return CommandComplexity.COMPLEX
        elif intent in ["login_to_platform", "form_interaction"]:
            return CommandComplexity.MODERATE
        elif word_count > 20:
            return CommandComplexity.COMPLEX
        elif word_count > 10:
            return CommandComplexity.MODERATE
        else:
            return CommandComplexity.SIMPLE
    
    def _determine_required_credentials(self, platform: str, action_type: str) -> List[CredentialType]:
        """Determine what credentials are required."""
        
        credentials = []
        
        # Platform-based requirements
        if platform in ["instagram", "facebook", "twitter", "linkedin"]:
            credentials.append(CredentialType.USERNAME_PASSWORD)
        
        # Action-based requirements
        if action_type in ["login", "post", "marketing"]:
            if CredentialType.USERNAME_PASSWORD not in credentials:
                credentials.append(CredentialType.USERNAME_PASSWORD)
        
        return credentials
    
    def _estimate_steps(self, complexity: CommandComplexity, action_type: str) -> int:
        """Estimate number of execution steps."""
        
        base_steps = {
            CommandComplexity.SIMPLE: 3,
            CommandComplexity.MODERATE: 7,
            CommandComplexity.COMPLEX: 15,
            CommandComplexity.ADVANCED: 25
        }
        
        step_count = base_steps.get(complexity, 5)
        
        # Adjust based on action type
        if action_type == "marketing":
            step_count += 10
        elif action_type == "extract":
            step_count += 5
        
        return step_count
    
    def _calculate_confidence(self, intent: str, platform: str, action_type: str) -> float:
        """Calculate parsing confidence."""
        
        confidence = 0.5  # Base confidence
        
        # Boost confidence for recognized patterns
        if intent != "general_automation":
            confidence += 0.2
        
        if platform is not None:
            confidence += 0.2
        
        if action_type != "unknown":
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def _load_platform_patterns(self) -> Dict[str, List[str]]:
        """Load platform detection patterns."""
        
        return {
            "instagram": [r"instagram", r"insta", r"ig\b"],
            "facebook": [r"facebook", r"fb\b"],
            "twitter": [r"twitter", r"tweet"],
            "linkedin": [r"linkedin"],
            "google": [r"google"],
            "youtube": [r"youtube"],
            "tiktok": [r"tiktok", r"tik tok"],
            "pinterest": [r"pinterest"]
        }
    
    def _load_action_patterns(self) -> Dict[str, List[str]]:
        """Load action type patterns."""
        
        return {
            "post": [r"post\b", r"share\b", r"upload\b", r"publish\b"],
            "login": [r"login", r"sign in", r"log in", r"authenticate"],
            "navigate": [r"go to", r"visit", r"navigate", r"browse to"],
            "extract": [r"extract", r"scrape", r"get data", r"collect"],
            "fill_form": [r"fill", r"complete", r"enter"],
            "click": [r"click", r"press", r"tap"],
            "search": [r"search", r"find", r"look for"]
        }
    
    def _load_credential_indicators(self) -> List[str]:
        """Load indicators that credentials might be needed."""
        
        return [
            "login", "sign in", "authenticate", "account", "password",
            "username", "email", "credentials", "access"
        ]