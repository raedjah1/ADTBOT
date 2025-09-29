"""
AI Chat Interface for SmartWebBot

Provides natural language interaction with the bot using local LLaMA or OpenAI API.
"""

import json
import re
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime

# Dynamic import checks - don't rely on global import state
def _check_ollama_available():
    """Check if ollama is available at runtime."""
    try:
        import ollama
        return True
    except ImportError:
        return False

def _check_openai_available():
    """Check if openai is available at runtime."""
    try:
        import openai
        return True
    except ImportError:
        return False

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
                # Dynamic check for ollama availability
                if not _check_ollama_available():
                    self.logger.error("Ollama not installed. Install with: pip install ollama")
                    return False
                
                # Import ollama dynamically
                try:
                    import ollama as ollama_client
                    self.logger.info("Ollama package loaded successfully in current environment")
                except ImportError as e:
                    self.logger.error(f"Ollama package not available in current environment: {e}")
                    return False
                
                # Test connection to Ollama with robust retry logic
                if not self._test_ollama_connection_sync(ollama_client):
                    return False
                    
            elif self.ai_provider == "openai":
                if not _check_openai_available():
                    self.logger.error("OpenAI not installed. Install with: pip install openai")
                    return False
                    
                if not self.api_key:
                    self.logger.error("OpenAI API key required")
                    return False
                
                try:
                    import openai
                    openai.api_key = self.api_key
                    self.logger.info("OpenAI API configured")
                except ImportError as e:
                    self.logger.error(f"OpenAI package not available: {e}")
                    return False
            
            self.is_initialized = True
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize chat AI: {e}")
            return False
    
    def _test_ollama_connection_sync(self, ollama_client) -> bool:
        """Test Ollama connection with robust synchronous retry logic."""
        max_attempts = 3
        
        for attempt in range(max_attempts):
            try:
                self.logger.info(f"Testing Ollama connection (attempt {attempt + 1}/{max_attempts})...")
                
                # Get available models
                models_response = ollama_client.list()
                
                if not hasattr(models_response, 'models'):
                    self.logger.error(f"Invalid Ollama response format: {type(models_response)}")
                    continue
                
                available_models = [model.model for model in models_response.models]
                
                if not available_models:
                    self.logger.warning("No models available in Ollama")
                    continue
                
                self.logger.info(f"Found {len(available_models)} models: {available_models}")
                
                # Check if our target model is available
                model_available = any(self.model_name in model for model in available_models)
                
                if model_available:
                    self.logger.info(f"Target model {self.model_name} is available")
                    return True
                else:
                    self.logger.warning(f"Model {self.model_name} not found. Available: {available_models}")
                    # Use the first available model as fallback
                    if available_models:
                        original_model = self.model_name
                        self.model_name = available_models[0]
                        self.logger.info(f"Using fallback model: {self.model_name} (originally requested: {original_model})")
                        return True
                
            except Exception as e:
                self.logger.warning(f"Ollama connection attempt {attempt + 1} failed: {e}")
                
                if attempt < max_attempts - 1:
                    self.logger.info(f"Retrying in 2 seconds...")
                    import time
                    time.sleep(2)
                else:
                    self.logger.error(f"Ollama server not accessible after {max_attempts} attempts: {e}")
                    
                    # Try one more time with a different approach
                    try:
                        self.logger.info("Attempting final connection test...")
                        test_response = ollama_client.list()
                        if test_response:
                            self.logger.info("Ollama responding but model detection failed - using default initialization")
                            return True
                    except:
                        pass
        
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

