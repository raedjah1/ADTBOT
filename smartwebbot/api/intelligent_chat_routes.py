"""
API Routes for Intelligent Chat System

Provides endpoints for the intelligent chat orchestrator that can handle
complex natural language commands and execute autonomous workflows.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import asyncio
import logging

from ..intelligence.intelligent_chat_orchestrator import IntelligentChatOrchestrator
from ..intelligence.dynamic_credential_manager import DynamicCredentialManager, CredentialType
from ..intelligence.web_search_integration import WebSearchIntegration

logger = logging.getLogger(__name__)

# Initialize components (will be properly initialized when the app starts)
chat_orchestrator = None
credential_manager = None
web_search = None

router = APIRouter(prefix="/api/intelligent-chat", tags=["intelligent-chat"])


# Pydantic models for request/response
class ChatCommandRequest(BaseModel):
    message: str
    session_id: str
    current_context: Optional[Dict[str, Any]] = None


class ChatCommandResponse(BaseModel):
    response: str
    type: str
    session_id: str
    actions: Optional[List[str]] = None
    execution_plan: Optional[List[Dict[str, Any]]] = None
    estimated_steps: Optional[int] = None
    credential_request: Optional[Dict[str, Any]] = None


class CredentialSubmissionRequest(BaseModel):
    session_id: str
    request_id: Optional[str] = None
    credentials: Dict[str, str]


class ExecuteWorkflowRequest(BaseModel):
    session_id: str
    confirm_execution: bool = True


class SearchRequest(BaseModel):
    query: str
    result_type: str = "url"
    max_results: int = 10


class PlatformUrlRequest(BaseModel):
    platform_name: str
    additional_context: Optional[str] = None


@router.on_event("startup")
async def initialize_intelligent_chat():
    """Initialize intelligent chat components"""
    global chat_orchestrator, credential_manager, web_search
    
    try:
        logger.info("Starting intelligent chat components initialization...")
        
        # Initialize components with default config
        config = {
            "chat_ai": {"provider": "ollama", "model": "gemma3:4b"},
            "max_workflow_steps": 50,
            "auto_search_enabled": True
        }
        
        # Initialize each component individually with better error handling
        try:
            chat_orchestrator = IntelligentChatOrchestrator(config)
            chat_init_success = chat_orchestrator.initialize()
            logger.info(f"Chat orchestrator initialization: {'SUCCESS' if chat_init_success else 'FAILED'}")
        except Exception as e:
            logger.error(f"Failed to initialize chat orchestrator: {e}")
            chat_orchestrator = None
            chat_init_success = False
        
        try:
            credential_manager = DynamicCredentialManager()
            cred_init_success = credential_manager.initialize()
            logger.info(f"Credential manager initialization: {'SUCCESS' if cred_init_success else 'FAILED'}")
        except Exception as e:
            logger.error(f"Failed to initialize credential manager: {e}")
            credential_manager = None
            cred_init_success = False
        
        try:
            web_search = WebSearchIntegration()
            search_init_success = web_search.initialize()
            logger.info(f"Web search initialization: {'SUCCESS' if search_init_success else 'FAILED'}")
        except Exception as e:
            logger.error(f"Failed to initialize web search: {e}")
            web_search = None
            search_init_success = False
        
        # Check overall initialization status
        total_success = chat_init_success and cred_init_success and search_init_success
        
        if total_success:
            logger.info("Intelligent chat system initialized successfully")
        else:
            logger.warning("Some intelligent chat components failed to initialize, but system will continue with limited functionality")
    
    except Exception as e:
        logger.error(f"Critical failure in intelligent chat system initialization: {e}")
        # Set components to None to ensure we don't try to use them
        chat_orchestrator = None
        credential_manager = None
        web_search = None


@router.post("/command", response_model=ChatCommandResponse)
async def process_chat_command(request: ChatCommandRequest):
    """
    Process a natural language command and return execution plan or results.
    
    This is the main endpoint that handles commands like:
    - "Go to Instagram and post my product"
    - "Login to my Facebook account" 
    - "Market my business on social media"
    """
    
    if not chat_orchestrator or not chat_orchestrator.is_initialized:
        # Try to provide a fallback response using basic AI chat
        try:
            from ..intelligence.chat_ai import ChatAI
            from ..utils.config_manager import get_config_manager
            
            config_manager = get_config_manager()
            config = {
                "provider": config_manager.get("ai.provider", "ollama"),
                "model": config_manager.get("ai.model", "gemma3:4b"),
                "api_key": config_manager.get("ai.api_key")
            }
            
            fallback_ai = ChatAI(config)
            if fallback_ai.initialize():
                ai_response = await fallback_ai.chat(request.message)
                return ChatCommandResponse(
                    response=f"(Fallback mode) {ai_response.get('response', 'I understand you want help, but the full intelligent chat system is not available right now.')}", 
                    type="fallback",
                    session_id=request.session_id,
                    actions=ai_response.get('actions', []),
                    execution_plan=None,
                    estimated_steps=None,
                    credential_request=None
                )
        except Exception as fallback_error:
            logger.error(f"Fallback AI also failed: {fallback_error}")
        
        raise HTTPException(status_code=503, detail="Intelligent chat system not available. Please check server logs.")
    
    try:
        result = await chat_orchestrator.process_command(
            user_input=request.message,
            session_id=request.session_id,
            current_context=request.current_context
        )
        
        return ChatCommandResponse(
            response=result.get("response", ""),
            type=result.get("type", "unknown"),
            session_id=result.get("session_id", request.session_id),
            actions=result.get("actions"),
            execution_plan=result.get("execution_plan"),
            estimated_steps=result.get("estimated_steps"),
            credential_request=result.get("credential_request")
        )
    
    except Exception as e:
        logger.error(f"Command processing error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process command: {str(e)}")


@router.post("/credentials/submit")
async def submit_credentials(request: CredentialSubmissionRequest):
    """
    Submit credentials requested by the chat system.
    
    Used when the AI requests authentication information from the user.
    """
    
    if not chat_orchestrator or not credential_manager:
        raise HTTPException(status_code=503, detail="Intelligent chat system not initialized")
    
    try:
        if request.request_id:
            # Fulfill a specific credential request
            result = await credential_manager.fulfill_credential_request(
                request_id=request.request_id,
                credentials=request.credentials
            )
        else:
            # Provide credentials directly to session
            result = await chat_orchestrator.provide_credentials(
                session_id=request.session_id,
                credentials=request.credentials
            )
        
        return {"success": True, "result": result}
    
    except Exception as e:
        logger.error(f"Credential submission error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to submit credentials: {str(e)}")


@router.post("/workflow/execute")
async def execute_workflow(request: ExecuteWorkflowRequest, background_tasks: BackgroundTasks):
    """
    Execute a confirmed workflow in the background.
    
    Used after the user confirms they want to execute a complex workflow.
    """
    
    if not chat_orchestrator:
        raise HTTPException(status_code=503, detail="Intelligent chat system not initialized")
    
    try:
        # Start workflow execution in background
        background_tasks.add_task(
            _execute_workflow_background,
            request.session_id
        )
        
        return {
            "success": True,
            "message": "Workflow execution started in background",
            "session_id": request.session_id
        }
    
    except Exception as e:
        logger.error(f"Workflow execution error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to start workflow: {str(e)}")


async def _execute_workflow_background(session_id: str):
    """Execute workflow in background task"""
    
    try:
        # This would execute the planned workflow
        # Implementation depends on the specific workflow execution system
        logger.info(f"Executing workflow for session {session_id}")
        
        # Placeholder for actual execution
        await asyncio.sleep(1)
        
        logger.info(f"Workflow completed for session {session_id}")
    
    except Exception as e:
        logger.error(f"Background workflow execution failed for session {session_id}: {e}")


@router.get("/session/{session_id}/status")
async def get_session_status(session_id: str):
    """Get the current status of a chat session"""
    
    if not chat_orchestrator or not credential_manager:
        raise HTTPException(status_code=503, detail="Intelligent chat system not initialized")
    
    try:
        # Get session information
        credentials = await credential_manager.get_session_credentials(session_id)
        
        return {
            "session_id": session_id,
            "active": session_id in chat_orchestrator.active_sessions,
            "credentials_stored": len(credentials),
            "last_activity": "2024-01-01T00:00:00"  # Placeholder
        }
    
    except Exception as e:
        logger.error(f"Session status error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get session status: {str(e)}")


@router.delete("/session/{session_id}")
async def cleanup_session(session_id: str):
    """Clean up a chat session and all associated data"""
    
    if not credential_manager:
        raise HTTPException(status_code=503, detail="Intelligent chat system not initialized")
    
    try:
        # Clean up credentials
        await credential_manager.cleanup_session_credentials(session_id)
        
        # Clean up orchestrator session
        if chat_orchestrator and session_id in chat_orchestrator.active_sessions:
            del chat_orchestrator.active_sessions[session_id]
        
        return {"success": True, "message": f"Session {session_id} cleaned up"}
    
    except Exception as e:
        logger.error(f"Session cleanup error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to cleanup session: {str(e)}")


@router.post("/search", response_model=List[Dict[str, Any]])
async def web_search(request: SearchRequest):
    """
    Perform web search to find URLs or information.
    
    Used by the AI to find platform URLs or gather information needed for tasks.
    """
    
    if not web_search:
        raise HTTPException(status_code=503, detail="Web search not initialized")
    
    try:
        from ..intelligence.web_search_integration import ResultType
        
        result_type = getattr(ResultType, request.result_type.upper(), ResultType.URL)
        results = await web_search.search(
            query=request.query,
            result_type=result_type,
            max_results=request.max_results
        )
        
        return [
            {
                "title": result.title,
                "url": result.url,
                "snippet": result.snippet,
                "confidence": result.confidence,
                "type": result.result_type.value
            }
            for result in results
        ]
    
    except Exception as e:
        logger.error(f"Web search error: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.post("/search/platform-url")
async def find_platform_url(request: PlatformUrlRequest):
    """
    Find the main URL for a specific platform.
    
    Used when the AI needs to navigate to a platform but doesn't know the URL.
    """
    
    if not web_search:
        raise HTTPException(status_code=503, detail="Web search not initialized")
    
    try:
        result = await web_search.find_platform_url(
            platform_name=request.platform_name,
            additional_context=request.additional_context
        )
        
        if result:
            return result
        else:
            raise HTTPException(status_code=404, detail=f"Could not find URL for platform: {request.platform_name}")
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Platform URL search error: {e}")
        raise HTTPException(status_code=500, detail=f"Platform URL search failed: {str(e)}")


@router.get("/credentials/active-requests")
async def get_active_credential_requests():
    """Get all active credential requests across all sessions"""
    
    if not credential_manager:
        raise HTTPException(status_code=503, detail="Credential manager not initialized")
    
    try:
        requests = await credential_manager.get_active_requests()
        return {"active_requests": requests}
    
    except Exception as e:
        logger.error(f"Active requests error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get active requests: {str(e)}")


@router.get("/system/stats")
async def get_system_stats():
    """Get system statistics and status"""
    
    stats = {
        "chat_orchestrator": {
            "initialized": chat_orchestrator is not None and chat_orchestrator.is_initialized,
            "active_sessions": len(chat_orchestrator.active_sessions) if chat_orchestrator else 0
        },
        "credential_manager": {
            "initialized": credential_manager is not None and credential_manager.is_initialized,
            "stats": credential_manager.get_storage_stats() if credential_manager else {}
        },
        "web_search": {
            "initialized": web_search is not None and web_search.is_initialized,
            "cache_stats": web_search.get_cache_stats() if web_search else {}
        }
    }
    
    return stats


@router.post("/demo/simple-command")
async def demo_simple_command():
    """
    Demo endpoint to test simple command processing.
    
    Shows how the system handles a basic command.
    """
    
    if not chat_orchestrator:
        raise HTTPException(status_code=503, detail="Intelligent chat system not initialized")
    
    demo_request = ChatCommandRequest(
        message="Go to Instagram",
        session_id="demo_session",
        current_context={}
    )
    
    return await process_chat_command(demo_request)


@router.post("/demo/complex-command")
async def demo_complex_command():
    """
    Demo endpoint to test complex command processing.
    
    Shows how the system handles advanced commands that require planning.
    """
    
    if not chat_orchestrator:
        raise HTTPException(status_code=503, detail="Intelligent chat system not initialized")
    
    demo_request = ChatCommandRequest(
        message="Market my product on Instagram by creating a post with my product image",
        session_id="demo_complex_session",
        current_context={}
    )
    
    return await process_chat_command(demo_request)
