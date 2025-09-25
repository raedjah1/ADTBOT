"""
AI Chat Interface for SmartWebBot

Provides natural language interaction with the bot using local LLaMA or OpenAI API.
"""

import json
import re
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime

try:
    import ollama  # For local LLaMA
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

try:
    import openai  # For OpenAI API
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from ..core.base_component import BaseComponent


class ChatAI(BaseComponent):
    """
    AI Chat interface for natural language automation commands.
    
    Supports both local LLaMA (via Ollama) and OpenAI API.
    """
    
    def __init__(self, config: Dict = None):
        """Initialize the chat AI system."""
        super().__init__("chat_ai", config)
        
        # Handle both AIConfig object and dict
        if hasattr(config, 'provider'):
            # AIConfig object
            self.ai_provider = getattr(config, 'provider', 'ollama')
            self.model_name = getattr(config, 'model', 'gemma3:4b')
            self.api_key = getattr(config, 'api_key', None)
        else:
            # Dict config
            self.ai_provider = config.get("provider", "ollama") if config else "ollama"
            self.model_name = config.get("model", "gemma3:4b") if config else "gemma3:4b"
            self.api_key = config.get("api_key") if config else None
        
        # Context for conversation
        self.conversation_history = []
        self.available_commands = [
            "navigate_to", "fill_form", "click_element", "extract_data",
            "take_screenshot", "wait", "scroll", "create_jira_ticket",
            "update_jira_status", "extract_jira_issues"
        ]
        
    def initialize(self) -> bool:
        """Initialize the AI chat system."""
        try:
            if self.ai_provider == "ollama":
                if not OLLAMA_AVAILABLE:
                    self.logger.error("Ollama not installed. Install with: pip install ollama")
                    return False
                
                # Import ollama here to ensure it's available in the current context
                try:
                    import ollama as ollama_client
                except ImportError:
                    self.logger.error("Ollama package not available in current environment")
                    return False
                
                # Test connection to Ollama with retry logic
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        # Check if Ollama is available
                        models = ollama_client.list()
                        
                        # Check if our model exists
                        model_exists = any(model.model == self.model_name for model in models.models)
                        if not model_exists:
                            self.logger.warning(f"Model {self.model_name} not found. Available models: {[m.model for m in models.models]}")
                            # Try to pull the model if it doesn't exist
                            try:
                                self.logger.info(f"Attempting to pull model: {self.model_name}")
                                ollama_client.pull(self.model_name)
                                self.logger.info(f"Successfully pulled model: {self.model_name}")
                            except Exception as pull_error:
                                self.logger.error(f"Failed to pull model {self.model_name}: {pull_error}")
                        else:
                            self.logger.info(f"Found model: {self.model_name}")
                        
                        self.logger.info("Connected to local Ollama server")
                        break
                    except Exception as e:
                        if attempt < max_retries - 1:
                            self.logger.warning(f"Ollama connection attempt {attempt + 1} failed: {e}. Retrying...")
                            import time
                            time.sleep(2)
                        else:
                            self.logger.error(f"Ollama server not running after {max_retries} attempts: {e}")
                            return False
                    
            elif self.ai_provider == "openai":
                if not OPENAI_AVAILABLE or not self.api_key:
                    self.logger.error("OpenAI API key required")
                    return False
                
                openai.api_key = self.api_key
                self.logger.info("OpenAI API configured")
            
            self.is_initialized = True
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize chat AI: {e}")
            return False
    
    async def chat(self, user_message: str) -> Dict[str, Any]:
        """
        Process user message and return response with potential actions.
        
        Args:
            user_message: User's natural language input
            
        Returns:
            Dict with 'response', 'actions', and 'confidence'
        """
        try:
            # Add user message to history
            self.conversation_history.append({
                "role": "user",
                "content": user_message,
                "timestamp": datetime.now().isoformat()
            })
            
            # Create system prompt
            system_prompt = self._create_system_prompt()
            
            # Get AI response
            if self.ai_provider == "ollama":
                ai_response = await self._chat_with_ollama(system_prompt, user_message)
            elif self.ai_provider == "openai":
                ai_response = await self._chat_with_openai(system_prompt, user_message)
            else:
                raise ValueError(f"Unsupported AI provider: {self.ai_provider}")
            
            # Parse response for actions
            parsed_response = self._parse_ai_response(ai_response)
            
            # Add AI response to history
            self.conversation_history.append({
                "role": "assistant", 
                "content": parsed_response["response"],
                "actions": parsed_response.get("actions", []),
                "timestamp": datetime.now().isoformat()
            })
            
            return parsed_response
            
        except Exception as e:
            self.logger.error(f"Chat error: {e}")
            return {
                "response": f"Sorry, I encountered an error: {str(e)}",
                "actions": [],
                "confidence": 0.0
            }
    
    async def _chat_with_ollama(self, system_prompt: str, user_message: str) -> str:
        """Chat with local Ollama LLaMA model."""
        try:
            # Import ollama locally to ensure it's available
            import ollama as ollama_client
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
            
            # Add recent conversation history
            if len(self.conversation_history) > 0:
                recent_history = self.conversation_history[-4:]  # Last 2 exchanges
                for msg in recent_history:
                    messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
            
            response = ollama_client.chat(
                model=self.model_name,
                messages=messages,
                options={
                    "temperature": 0.3,  # Lower for more focused responses
                    "top_p": 0.9,
                    "max_tokens": 500
                }
            )
            
            return response['message']['content']
            
        except Exception as e:
            raise Exception(f"Ollama chat failed: {e}")
    
    async def _chat_with_openai(self, system_prompt: str, user_message: str) -> str:
        """Chat with OpenAI API."""
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-4o-mini",  # Cheapest GPT-4 model
                messages=messages,
                max_tokens=500,
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"OpenAI chat failed: {e}")
    
    def _create_system_prompt(self) -> str:
        """Create system prompt for the AI."""
        return f"""You are SmartWebBot AI Assistant, helping users automate web tasks.

Available Commands:
{', '.join(self.available_commands)}

Your job:
1. Understand user requests in natural language
2. Suggest specific automation actions
3. Provide clear, helpful responses
4. Format action suggestions as JSON

Example responses:
User: "Create a Jira ticket for login bug"
Response: "I'll help you create a Jira ticket for the login bug. Here's what I'll do:

{{
  "actions": [
    {{"type": "navigate_to", "url": "https://your-jira.atlassian.net"}},
    {{"type": "click_element", "description": "create issue button"}},
    {{"type": "fill_form", "data": {{"summary": "Login Bug", "issue_type": "Bug", "priority": "High"}}}}
  ]
}}

Would you like me to proceed with creating this ticket?"

Keep responses conversational but include actionable JSON when appropriate.
Current time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
    
    def _parse_ai_response(self, ai_response: str) -> Dict[str, Any]:
        """Parse AI response to extract actions and confidence."""
        try:
            # Look for JSON actions in the response
            json_pattern = r'\{[\s\S]*?\}'
            json_matches = re.findall(json_pattern, ai_response)
            
            actions = []
            confidence = 0.8  # Default confidence
            
            for match in json_matches:
                try:
                    parsed_json = json.loads(match)
                    if "actions" in parsed_json:
                        actions.extend(parsed_json["actions"])
                    if "confidence" in parsed_json:
                        confidence = parsed_json["confidence"]
                except json.JSONDecodeError:
                    continue
            
            # Clean response (remove JSON parts for display)
            clean_response = ai_response
            for match in json_matches:
                clean_response = clean_response.replace(match, "").strip()
            
            return {
                "response": clean_response or ai_response,
                "actions": actions,
                "confidence": confidence
            }
            
        except Exception as e:
            self.logger.error(f"Failed to parse AI response: {e}")
            return {
                "response": ai_response,
                "actions": [],
                "confidence": 0.5
            }
    
    def get_conversation_history(self) -> List[Dict]:
        """Get conversation history."""
        return self.conversation_history.copy()
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
        self.logger.info("Conversation history cleared")
    
    def cleanup(self) -> bool:
        """Clean up chat AI resources."""
        self.clear_history()
        return True


# Utility functions for easy integration
async def quick_chat(message: str, provider: str = "ollama", model: str = "llama3.2:3b") -> str:
    """Quick chat function for simple interactions."""
    chat_ai = ChatAI({
        "provider": provider,
        "model": model
    })
    
    if not chat_ai.initialize():
        return "Chat AI initialization failed"
    
    response = await chat_ai.chat(message)
    return response["response"]


def get_recommended_models() -> Dict[str, List[str]]:
    """Get recommended models for different use cases."""
    return {
        "ollama_fast": ["llama3.2:1b", "phi3:mini"],
        "ollama_balanced": ["llama3.2:3b", "mistral:7b"],
        "ollama_powerful": ["llama3.1:8b", "codellama:13b"],
        "openai_cheap": ["gpt-4o-mini"],
        "openai_powerful": ["gpt-4", "gpt-4-turbo"]
    }

