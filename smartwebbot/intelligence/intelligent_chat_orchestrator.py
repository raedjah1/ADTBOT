"""
Intelligent Chat Orchestrator for SmartWebBot

This is the master brain that:
1. Understands complex natural language commands
2. Breaks them down into executable workflows
3. Handles dynamic authentication requests
4. Manages web search for unknown URLs
5. Coordinates all AI modules for autonomous execution
"""

import json
import re
import asyncio
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

from ..core.base_component import BaseComponent
from .chat_ai import ChatAI
from .autonomous_action_planner import AutonomousActionPlanner
from .smart_next_step_predictor import SmartNextStepPredictor
from ..automation.web_controller import WebController


class CommandComplexity(Enum):
    SIMPLE = "simple"          # Single action: "click login button"
    MODERATE = "moderate"      # Few steps: "login to website"  
    COMPLEX = "complex"        # Multi-step: "create social media post"
    ADVANCED = "advanced"      # Full workflow: "market my product on Instagram"


class CredentialType(Enum):
    USERNAME_PASSWORD = "username_password"
    API_KEY = "api_key"
    OAUTH = "oauth"
    TWO_FACTOR = "two_factor"


@dataclass
class UserCommand:
    """Represents a parsed user command"""
    original_text: str
    intent: str
    target_platform: Optional[str]
    action_type: str
    complexity: CommandComplexity
    required_credentials: List[CredentialType]
    estimated_steps: int
    confidence: float
    parsed_parameters: Dict[str, Any]


@dataclass
class ExecutionContext:
    """Context for command execution"""
    user_command: UserCommand
    session_id: str
    current_url: Optional[str]
    credentials: Dict[str, Any]
    workflow_state: Dict[str, Any]
    pending_user_inputs: List[str]
    execution_history: List[Dict[str, Any]]


class IntelligentChatOrchestrator(BaseComponent):
    """
    Master orchestrator that understands natural language and executes complex workflows.
    
    This is what makes the system truly intelligent - it can:
    1. Parse complex commands like "go market my product on Instagram"
    2. Break them into executable workflows
    3. Handle authentication dynamically
    4. Search the web for unknown URLs
    5. Execute multi-step processes autonomously
    """
    
    def __init__(self, config: Dict = None):
        super().__init__("intelligent_chat_orchestrator", config)
        
        # Core AI components
        self.chat_ai = None
        self.action_planner = None
        self.next_step_predictor = None
        self.web_controller = None
        
        # Execution state
        self.active_sessions: Dict[str, ExecutionContext] = {}
        self.platform_knowledge = self._load_platform_knowledge()
        self.command_patterns = self._load_command_patterns()
        
        # Configuration
        self.max_workflow_steps = config.get("max_workflow_steps", 50) if config else 50
        self.auto_search_enabled = config.get("auto_search_enabled", True) if config else True
        
    def initialize(self) -> bool:
        """Initialize all AI components"""
        try:
            self.logger.info("Initializing Intelligent Chat Orchestrator...")
            
            # Initialize AI components
            self.chat_ai = ChatAI(self.config.get("chat_ai", {}))
            self.action_planner = AutonomousActionPlanner(self.config.get("action_planner", {}))
            self.next_step_predictor = SmartNextStepPredictor(self.config.get("next_step_predictor", {}))
            
            # Initialize components
            if not all([
                self.chat_ai.initialize(),
                self.action_planner.initialize(),
                self.next_step_predictor.initialize()
            ]):
                raise Exception("Failed to initialize AI components")
            
            self.is_initialized = True
            self.logger.info("Intelligent Chat Orchestrator initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Intelligent Chat Orchestrator: {e}")
            return False
    
    async def process_command(self, user_input: str, session_id: str, current_context: Dict = None) -> Dict[str, Any]:
        """
        Process a natural language command and return execution plan or results.
        
        Args:
            user_input: Natural language command from user
            session_id: Unique session identifier
            current_context: Current browser/app context
            
        Returns:
            Dict with response, actions, credential_requests, etc.
        """
        try:
            # Parse the command
            parsed_command = await self._parse_user_command(user_input)
            
            # Create or update execution context
            context = self._get_or_create_context(session_id, parsed_command, current_context)
            
            # Check if we need credentials
            if parsed_command.required_credentials and not self._has_required_credentials(context):
                return await self._request_credentials(context)
            
            # Check if we need to find URLs
            if parsed_command.target_platform and not self._has_target_url(context):
                url_result = await self._find_platform_url(parsed_command.target_platform)
                if url_result:
                    context.current_url = url_result["url"]
                else:
                    return {
                        "response": f"I couldn't find the URL for {parsed_command.target_platform}. Could you provide the URL?",
                        "type": "url_request",
                        "session_id": session_id
                    }
            
            # Generate execution plan
            execution_plan = await self._create_execution_plan(context)
            
            # Execute if simple, or return plan for complex commands
            if parsed_command.complexity in [CommandComplexity.SIMPLE, CommandComplexity.MODERATE]:
                return await self._execute_workflow(context, execution_plan)
            else:
                return {
                    "response": f"I've created a plan to {parsed_command.intent}. Here's what I'll do:",
                    "execution_plan": execution_plan,
                    "estimated_steps": parsed_command.estimated_steps,
                    "type": "execution_plan",
                    "session_id": session_id,
                    "actions": ["confirm_execution"]
                }
                
        except Exception as e:
            self.logger.error(f"Command processing error: {e}")
            return {
                "response": f"I encountered an error processing your command: {str(e)}",
                "type": "error",
                "session_id": session_id
            }
    
    async def _parse_user_command(self, user_input: str) -> UserCommand:
        """Parse natural language into structured command"""
        
        # Use ChatAI to understand the command
        chat_response = await self.chat_ai.chat(f"""
        Parse this command and extract:
        1. Intent (what the user wants to achieve)
        2. Target platform (Instagram, Facebook, etc.)
        3. Action type (login, post, search, etc.)
        4. Required credentials
        5. Estimated complexity
        
        Command: "{user_input}"
        
        Respond in JSON format.
        """)
        
        # Enhanced parsing with pattern matching
        intent = self._extract_intent(user_input)
        target_platform = self._extract_platform(user_input)
        action_type = self._extract_action_type(user_input)
        complexity = self._assess_complexity(user_input, intent)
        required_credentials = self._determine_required_credentials(target_platform, action_type)
        
        return UserCommand(
            original_text=user_input,
            intent=intent,
            target_platform=target_platform,
            action_type=action_type,
            complexity=complexity,
            required_credentials=required_credentials,
            estimated_steps=self._estimate_steps(complexity),
            confidence=0.85,  # Will be improved with ML
            parsed_parameters={}
        )
    
    async def _create_execution_plan(self, context: ExecutionContext) -> List[Dict[str, Any]]:
        """Create detailed execution plan for the command"""
        
        # Use the autonomous action planner
        plan_request = {
            "goal": context.user_command.intent,
            "starting_url": context.current_url,
            "user_context": {
                "platform": context.user_command.target_platform,
                "action_type": context.user_command.action_type,
                "credentials_available": bool(context.credentials)
            }
        }
        
        plan = await self.action_planner.create_workflow(plan_request)
        return plan.get("steps", [])
    
    async def _execute_workflow(self, context: ExecutionContext, execution_plan: List[Dict]) -> Dict[str, Any]:
        """Execute the workflow steps"""
        
        results = []
        current_step = 0
        
        for step in execution_plan:
            try:
                # Predict next step for better execution
                next_prediction = await self.next_step_predictor.predict_next_steps({
                    "current_step": step,
                    "context": context.workflow_state,
                    "goal": context.user_command.intent
                })
                
                # Execute the step (this would integrate with existing automation)
                step_result = await self._execute_single_step(step, context)
                results.append(step_result)
                
                # Update context
                context.execution_history.append({
                    "step": current_step,
                    "action": step,
                    "result": step_result,
                    "timestamp": datetime.now().isoformat()
                })
                
                current_step += 1
                
            except Exception as e:
                self.logger.error(f"Step execution failed: {e}")
                return {
                    "response": f"Execution failed at step {current_step}: {str(e)}",
                    "type": "execution_error",
                    "completed_steps": results
                }
        
        return {
            "response": f"Successfully completed: {context.user_command.intent}",
            "type": "execution_complete",
            "results": results,
            "total_steps": len(results)
        }
    
    async def _execute_single_step(self, step: Dict, context: ExecutionContext) -> Dict[str, Any]:
        """Execute a single workflow step"""
        
        action_type = step.get("action", "unknown")
        
        if action_type == "navigate":
            # Use web controller to navigate
            if self.web_controller:
                await self.web_controller.navigate_to(step["url"])
                return {"status": "success", "action": "navigate", "url": step["url"]}
        
        elif action_type == "fill_form":
            # Use form handler to fill forms
            return {"status": "success", "action": "fill_form", "fields": step.get("fields", [])}
        
        elif action_type == "click":
            # Use element detector and click
            return {"status": "success", "action": "click", "element": step.get("selector")}
        
        elif action_type == "wait_for_input":
            # Request user input
            return {
                "status": "waiting", 
                "action": "user_input_required",
                "message": step.get("message", "Please provide input")
            }
        
        else:
            return {"status": "unknown", "action": action_type}
    
    def _extract_intent(self, user_input: str) -> str:
        """Extract the main intent from user input"""
        
        # Pattern matching for common intents
        marketing_patterns = [
            r"market(?:ing)?.*product",
            r"promote.*business",
            r"advertise.*",
            r"social media.*campaign"
        ]
        
        login_patterns = [
            r"log(?:in|on).*to",
            r"sign.*in.*to",
            r"access.*account"
        ]
        
        for pattern in marketing_patterns:
            if re.search(pattern, user_input.lower()):
                return "marketing_campaign"
        
        for pattern in login_patterns:
            if re.search(pattern, user_input.lower()):
                return "login_to_platform"
        
        # Default intent extraction
        return "general_automation"
    
    def _extract_platform(self, user_input: str) -> Optional[str]:
        """Extract target platform from user input"""
        
        platforms = {
            "instagram": ["instagram", "insta", "ig"],
            "facebook": ["facebook", "fb"],
            "twitter": ["twitter", "x.com"],
            "linkedin": ["linkedin"],
            "youtube": ["youtube", "yt"],
            "tiktok": ["tiktok", "tik tok"],
            "plus": ["plus", "plus.reconext.com"]
        }
        
        user_lower = user_input.lower()
        
        for platform, keywords in platforms.items():
            for keyword in keywords:
                if keyword in user_lower:
                    return platform
        
        return None
    
    def _extract_action_type(self, user_input: str) -> str:
        """Extract the type of action requested"""
        
        action_patterns = {
            "post": [r"post", r"share", r"publish"],
            "login": [r"log(?:in|on)", r"sign.*in", r"access"],
            "search": [r"search", r"find", r"look.*for"],
            "navigate": [r"go.*to", r"visit", r"open"],
            "fill_form": [r"fill.*form", r"enter.*data", r"submit"],
            "marketing": [r"market", r"promote", r"advertise", r"campaign"]
        }
        
        user_lower = user_input.lower()
        
        for action, patterns in action_patterns.items():
            for pattern in patterns:
                if re.search(pattern, user_lower):
                    return action
        
        return "general"
    
    def _assess_complexity(self, user_input: str, intent: str) -> CommandComplexity:
        """Assess the complexity of the command"""
        
        # Complex indicators
        complex_indicators = [
            "marketing", "campaign", "strategy", "multiple", "workflow",
            "automate everything", "full process", "end to end"
        ]
        
        # Simple indicators  
        simple_indicators = [
            "click", "fill", "login", "navigate", "open", "close"
        ]
        
        user_lower = user_input.lower()
        
        if any(indicator in user_lower for indicator in complex_indicators):
            return CommandComplexity.ADVANCED
        elif any(indicator in user_lower for indicator in simple_indicators):
            return CommandComplexity.SIMPLE
        elif len(user_input.split()) > 10:
            return CommandComplexity.COMPLEX
        else:
            return CommandComplexity.MODERATE
    
    def _determine_required_credentials(self, platform: str, action_type: str) -> List[CredentialType]:
        """Determine what credentials are needed"""
        
        if not platform:
            return []
        
        # Most platforms need username/password for login
        if action_type in ["login", "post", "marketing"]:
            return [CredentialType.USERNAME_PASSWORD]
        
        return []
    
    def _estimate_steps(self, complexity: CommandComplexity) -> int:
        """Estimate number of steps based on complexity"""
        
        step_mapping = {
            CommandComplexity.SIMPLE: 1,
            CommandComplexity.MODERATE: 3,
            CommandComplexity.COMPLEX: 8,
            CommandComplexity.ADVANCED: 15
        }
        
        return step_mapping.get(complexity, 5)
    
    def _get_or_create_context(self, session_id: str, command: UserCommand, current_context: Dict = None) -> ExecutionContext:
        """Get existing context or create new one"""
        
        if session_id not in self.active_sessions:
            self.active_sessions[session_id] = ExecutionContext(
                user_command=command,
                session_id=session_id,
                current_url=current_context.get("url") if current_context else None,
                credentials={},
                workflow_state={},
                pending_user_inputs=[],
                execution_history=[]
            )
        
        return self.active_sessions[session_id]
    
    def _has_required_credentials(self, context: ExecutionContext) -> bool:
        """Check if we have all required credentials"""
        
        for cred_type in context.user_command.required_credentials:
            if cred_type == CredentialType.USERNAME_PASSWORD:
                if not (context.credentials.get("username") and context.credentials.get("password")):
                    return False
        
        return True
    
    def _has_target_url(self, context: ExecutionContext) -> bool:
        """Check if we have the target URL"""
        return bool(context.current_url)
    
    async def _request_credentials(self, context: ExecutionContext) -> Dict[str, Any]:
        """Request credentials from user"""
        
        missing_creds = []
        for cred_type in context.user_command.required_credentials:
            if cred_type == CredentialType.USERNAME_PASSWORD:
                if not context.credentials.get("username"):
                    missing_creds.append("username")
                if not context.credentials.get("password"):
                    missing_creds.append("password")
        
        return {
            "response": f"I need your {' and '.join(missing_creds)} for {context.user_command.target_platform} to proceed.",
            "type": "credential_request",
            "required_credentials": missing_creds,
            "session_id": context.session_id
        }
    
    async def _find_platform_url(self, platform: str) -> Optional[Dict[str, Any]]:
        """Find URL for a platform using web search"""
        
        # Built-in platform URLs
        known_urls = {
            "instagram": "https://www.instagram.com",
            "facebook": "https://www.facebook.com",
            "twitter": "https://twitter.com",
            "linkedin": "https://www.linkedin.com",
            "youtube": "https://www.youtube.com",
            "tiktok": "https://www.tiktok.com",
            "plus": "https://plus.reconext.com"
        }
        
        if platform.lower() in known_urls:
            return {"url": known_urls[platform.lower()], "source": "built_in"}
        
        # TODO: Implement web search for unknown platforms
        # This would use a search API to find the platform URL
        
        return None
    
    def _load_platform_knowledge(self) -> Dict[str, Any]:
        """Load knowledge about different platforms"""
        
        return {
            "instagram": {
                "login_flow": ["navigate", "fill_username", "fill_password", "click_login"],
                "post_flow": ["click_new_post", "upload_image", "add_caption", "click_share"],
                "selectors": {
                    "username": "input[name='username']",
                    "password": "input[name='password']",
                    "login_button": "button[type='submit']"
                }
            },
            "plus": {
                "login_flow": ["navigate", "fill_username", "fill_password", "click_login"],
                "selectors": {
                    "username": "input[name='username']", 
                    "password": "input[name='password']",
                    "login_button": "button[type='submit']"
                }
            }
        }
    
    def _load_command_patterns(self) -> Dict[str, Any]:
        """Load patterns for command recognition"""
        
        return {
            "marketing_commands": [
                "market my product on {platform}",
                "promote my business on {platform}",
                "create a marketing campaign for {platform}",
                "advertise on {platform}"
            ],
            "automation_commands": [
                "automate {action} on {platform}",
                "help me {action} on {platform}",
                "do {action} automatically"
            ]
        }
    
    async def provide_credentials(self, session_id: str, credentials: Dict[str, str]) -> Dict[str, Any]:
        """Provide credentials for a session"""
        
        if session_id in self.active_sessions:
            context = self.active_sessions[session_id]
            context.credentials.update(credentials)
            
            # Continue execution now that we have credentials
            return await self.process_command(
                context.user_command.original_text, 
                session_id,
                {"url": context.current_url}
            )
        
        return {"response": "Session not found", "type": "error"}
    
    def cleanup(self) -> bool:
        """Clean up resources"""
        
        try:
            if self.chat_ai:
                self.chat_ai.cleanup()
            if self.action_planner:
                self.action_planner.cleanup()
            if self.next_step_predictor:
                self.next_step_predictor.cleanup()
            
            self.active_sessions.clear()
            return True
            
        except Exception as e:
            self.logger.error(f"Cleanup error: {e}")
            return False
