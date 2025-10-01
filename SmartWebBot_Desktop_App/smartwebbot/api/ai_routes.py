"""
AI Routes Module

Handles all AI-related API endpoints with proper separation of concerns.
"""

import asyncio
import json
from typing import Dict, List, Optional, Any
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from ..intelligence.chat_ai import ChatAI, quick_chat
from ..utils.config_manager import get_config_manager
from ..utils.logger import BotLogger

# Initialize router
router = APIRouter(prefix="/api/ai", tags=["AI"])

# Global AI instance
_ai_instance: Optional[ChatAI] = None
_logger = BotLogger().get_logger("ai_api")

# Pydantic models
class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    response: str
    actions: List[Dict[str, Any]] = []
    confidence: float = 0.0
    session_id: str
    timestamp: str

class AICapabilities(BaseModel):
    provider: str
    model: str
    available_commands: List[str]
    is_initialized: bool

class TaskSuggestion(BaseModel):
    name: str
    description: str
    actions: List[Dict[str, Any]]
    confidence: float = 0.0

# Dependency to get AI instance
async def get_ai_instance() -> ChatAI:
    """Get or create AI instance with proper initialization."""
    global _ai_instance
    
    if _ai_instance is None:
        config_manager = get_config_manager()
        config = {
            "provider": config_manager.get("ai.provider", "ollama"),
            "model": config_manager.get("ai.model", "gemma3:4b"),
            "api_key": config_manager.get("ai.api_key")
        }
        
        _ai_instance = ChatAI(config)
        
        if not _ai_instance.initialize():
            raise HTTPException(
                status_code=500, 
                detail="Failed to initialize AI system. Check Ollama is running."
            )
    
    return _ai_instance

@router.get("/status", response_model=AICapabilities)
async def get_ai_status(ai: ChatAI = Depends(get_ai_instance)):
    """Get AI system status and capabilities."""
    try:
        return AICapabilities(
            provider=ai.ai_provider,
            model=ai.model_name,
            available_commands=ai.available_commands,
            is_initialized=ai.is_initialized
        )
    except Exception as e:
        _logger.error(f"Failed to get AI status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(
    message: ChatMessage,
    ai: ChatAI = Depends(get_ai_instance)
):
    """Chat with the AI assistant."""
    try:
        # Generate session ID if not provided
        session_id = message.session_id or f"session_{int(datetime.now().timestamp())}"
        
        # Get AI response
        response = await ai.chat(message.message)
        
        return ChatResponse(
            response=response.get("response", ""),
            actions=response.get("actions", []),
            confidence=response.get("confidence", 0.0),
            session_id=session_id,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        _logger.error(f"Chat failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/quick-chat")
async def quick_chat_endpoint(message: str, model: Optional[str] = None):
    """Quick chat without session management."""
    try:
        config_manager = get_config_manager()
        model_name = model or config_manager.get("ai.model", "gemma3:4b")
        
        response = await quick_chat(message, "ollama", model_name)
        
        return {
            "response": response,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        _logger.error(f"Quick chat failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/suggest-task", response_model=TaskSuggestion)
async def suggest_task(
    description: str,
    ai: ChatAI = Depends(get_ai_instance)
):
    """Get AI task suggestions based on description."""
    try:
        # Create a specialized prompt for task generation
        task_prompt = f"""
        Based on this description: "{description}"
        
        Generate a web automation task with the following structure:
        - name: A clear task name
        - description: What the task does
        - actions: Array of automation actions
        
        Available action types: navigate_to, fill_form, click_element, extract_data, 
        take_screenshot, wait, scroll, create_jira_ticket, update_jira_status, extract_jira_issues
        
        Return only valid JSON in this format:
        {{
            "name": "Task Name",
            "description": "Task description",
            "actions": [
                {{"type": "navigate_to", "url": "https://example.com"}},
                {{"type": "click_element", "selector": "button"}}
            ],
            "confidence": 0.8
        }}
        """
        
        response = await ai.chat(task_prompt)
        
        # Try to parse the response as JSON
        try:
            # Look for JSON in the response
            import re
            json_match = re.search(r'\{.*\}', response.get("response", ""), re.DOTALL)
            if json_match:
                task_data = json.loads(json_match.group())
                return TaskSuggestion(**task_data)
        except:
            pass
        
        # Fallback: create a basic task structure
        return TaskSuggestion(
            name=f"AI Generated Task: {description[:50]}...",
            description=description,
            actions=[
                {"type": "navigate_to", "url": "https://example.com"},
                {"type": "take_screenshot", "filename": "task_screenshot"}
            ],
            confidence=0.5
        )
        
    except Exception as e:
        _logger.error(f"Task suggestion failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{session_id}")
async def get_chat_history(session_id: str, ai: ChatAI = Depends(get_ai_instance)):
    """Get chat history for a session."""
    try:
        history = ai.get_conversation_history()
        return {
            "session_id": session_id,
            "history": history,
            "count": len(history)
        }
    except Exception as e:
        _logger.error(f"Failed to get chat history: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/history/{session_id}")
async def clear_chat_history(session_id: str, ai: ChatAI = Depends(get_ai_instance)):
    """Clear chat history for a session."""
    try:
        ai.clear_history()
        return {"message": "Chat history cleared", "session_id": session_id}
    except Exception as e:
        _logger.error(f"Failed to clear chat history: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-website")
async def analyze_website(
    url: str,
    analysis_type: str = "general",
    ai: ChatAI = Depends(get_ai_instance)
):
    """Analyze a website using AI."""
    try:
        analysis_prompt = f"""
        Analyze this website: {url}
        Analysis type: {analysis_type}
        
        Provide insights about:
        - Potential automation opportunities
        - Form fields and interactive elements
        - Security considerations
        - Recommended automation approach
        
        Be specific and actionable.
        """
        
        response = await ai.chat(analysis_prompt)
        
        return {
            "url": url,
            "analysis_type": analysis_type,
            "analysis": response.get("response", ""),
            "suggestions": response.get("actions", []),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        _logger.error(f"Website analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/capabilities")
async def get_ai_capabilities(ai: ChatAI = Depends(get_ai_instance)):
    """Get detailed AI capabilities and features."""
    try:
        return {
            "provider": ai.ai_provider,
            "model": ai.model_name,
            "available_commands": ai.available_commands,
            "features": [
                "Natural language task generation",
                "Website analysis and recommendations",
                "Automation workflow suggestions",
                "Security testing guidance",
                "Form filling assistance",
                "Data extraction planning",
                "Error handling strategies"
            ],
            "supported_actions": [
                "navigate_to", "fill_form", "click_element", "extract_data",
                "take_screenshot", "wait", "scroll", "create_jira_ticket",
                "update_jira_status", "extract_jira_issues"
            ],
            "is_initialized": ai.is_initialized
        }
    except Exception as e:
        _logger.error(f"Failed to get capabilities: {e}")
        raise HTTPException(status_code=500, detail=str(e))
