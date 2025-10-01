"""
AI Vision Routes Module

Handles all AI Vision and real-time automation API endpoints.
"""

import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel

from ..services.ai_vision_service import get_ai_vision_service, AIVisionService
from ..utils.logger import BotLogger

# Initialize router
router = APIRouter(prefix="/api/ai-vision", tags=["AI Vision"])

_logger = BotLogger().get_logger("ai_vision_api")

# Pydantic models
class WebsiteAnalysisRequest(BaseModel):
    url: str
    analysis_type: str = "comprehensive"  # quick, detailed, comprehensive

class ActionExecutionRequest(BaseModel):
    action: str
    element_id: Optional[str] = None
    parameters: Dict[str, Any] = {}

class ElementInteractionRequest(BaseModel):
    element_id: str
    interaction_type: str  # click, fill, hover, etc.
    data: Optional[Dict[str, Any]] = None

class WorkflowRequest(BaseModel):
    description: str
    steps: List[Dict[str, Any]] = []

@router.get("/status")
async def get_vision_status(service: AIVisionService = Depends(get_ai_vision_service)):
    """Get AI Vision service status."""
    try:
        return {
            "status": "active",
            "current_url": service._current_url,
            "has_analysis": service._current_analysis is not None,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        _logger.error(f"Failed to get vision status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze")
async def analyze_website(
    request: WebsiteAnalysisRequest,
    background_tasks: BackgroundTasks,
    service: AIVisionService = Depends(get_ai_vision_service)
):
    """Analyze a website with AI vision."""
    try:
        _logger.info(f"Starting website analysis: {request.url}")
        
        # Perform analysis
        analysis = await service.analyze_website(
            url=request.url,
            analysis_type=request.analysis_type
        )
        
        return {
            "success": True,
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        _logger.error(f"Website analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/current-state")
async def get_current_state(service: AIVisionService = Depends(get_ai_vision_service)):
    """Get current page state and analysis."""
    try:
        state = await service.get_current_state()
        return state
    except Exception as e:
        _logger.error(f"Failed to get current state: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/execute-action")
async def execute_action(
    request: ActionExecutionRequest,
    service: AIVisionService = Depends(get_ai_vision_service)
):
    """Execute a specific action on the current page."""
    try:
        result = await service.execute_action(
            action=request.action,
            element_id=request.element_id,
            parameters=request.parameters
        )
        
        return result
        
    except Exception as e:
        _logger.error(f"Action execution failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/interact-element")
async def interact_with_element(
    request: ElementInteractionRequest,
    service: AIVisionService = Depends(get_ai_vision_service)
):
    """Interact with a specific element."""
    try:
        # Map interaction types to actions
        action_map = {
            "click": "click_element",
            "fill": "fill_form",
            "hover": "hover_element",
            "select": "select_option"
        }
        
        action = action_map.get(request.interaction_type, request.interaction_type)
        parameters = request.data or {}
        
        result = await service.execute_action(
            action=action,
            element_id=request.element_id,
            parameters=parameters
        )
        
        return result
        
    except Exception as e:
        _logger.error(f"Element interaction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/suggest-workflow")
async def suggest_workflow(
    description: str,
    service: AIVisionService = Depends(get_ai_vision_service)
):
    """Get AI-suggested workflow for a task description."""
    try:
        if not service._current_analysis:
            raise HTTPException(status_code=400, detail="No website analysis available")
        
        # Create workflow suggestion prompt
        prompt = f"""
        Based on the current website analysis, suggest a workflow for: {description}
        
        Current page: {service._current_url}
        Available elements: {len(service._current_analysis.get('elements', []))}
        
        Provide a step-by-step workflow including:
        1. Navigation steps
        2. Element interactions
        3. Data extraction
        4. Form filling
        5. Validation steps
        
        Return as JSON with this structure:
        {{
            "workflow_name": "Task Name",
            "description": "What this workflow does",
            "steps": [
                {{
                    "step": 1,
                    "action": "navigate_to",
                    "description": "Navigate to login page",
                    "parameters": {{"url": "https://example.com/login"}}
                }},
                {{
                    "step": 2,
                    "action": "fill_form",
                    "description": "Fill username field",
                    "element_id": "#username",
                    "parameters": {{"value": "your_username"}}
                }}
            ],
            "estimated_time": "2-3 minutes",
            "confidence": 0.8
        }}
        """
        
        # Get AI suggestion
        response = await service._chat_ai.chat(prompt)
        
        # Try to parse JSON response
        try:
            import re
            json_match = re.search(r'\{.*\}', response.get("response", ""), re.DOTALL)
            if json_match:
                workflow = json.loads(json_match.group())
                return {
                    "success": True,
                    "workflow": workflow,
                    "timestamp": datetime.now().isoformat()
                }
        except:
            pass
        
        # Fallback response
        return {
            "success": True,
            "workflow": {
                "workflow_name": f"AI Suggested Workflow: {description}",
                "description": description,
                "steps": [
                    {
                        "step": 1,
                        "action": "navigate_to",
                        "description": "Navigate to target page",
                        "parameters": {"url": service._current_url}
                    }
                ],
                "estimated_time": "Unknown",
                "confidence": 0.5
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        _logger.error(f"Workflow suggestion failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/execute-workflow")
async def execute_workflow(
    request: WorkflowRequest,
    service: AIVisionService = Depends(get_ai_vision_service)
):
    """Execute a complete workflow."""
    try:
        results = []
        
        for step in request.steps:
            step_result = await service.execute_action(
                action=step.get("action"),
                element_id=step.get("element_id"),
                parameters=step.get("parameters", {})
            )
            
            results.append({
                "step": step.get("step", len(results) + 1),
                "action": step.get("action"),
                "description": step.get("description"),
                "result": step_result,
                "timestamp": datetime.now().isoformat()
            })
            
            # Add delay between steps
            await asyncio.sleep(1)
        
        return {
            "success": True,
            "workflow": request.description,
            "steps_executed": len(results),
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        _logger.error(f"Workflow execution failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/elements")
async def get_detected_elements(service: AIVisionService = Depends(get_ai_vision_service)):
    """Get all detected elements from current analysis."""
    try:
        if not service._current_analysis:
            raise HTTPException(status_code=400, detail="No analysis available")
        
        elements = service._current_analysis.get("elements", [])
        
        return {
            "elements": elements,
            "count": len(elements),
            "categories": list(set(elem.get("category", "unknown") for elem in elements)),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        _logger.error(f"Failed to get elements: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/suggestions")
async def get_action_suggestions(service: AIVisionService = Depends(get_ai_vision_service)):
    """Get action suggestions for current page."""
    try:
        if not service._current_analysis:
            raise HTTPException(status_code=400, detail="No analysis available")
        
        suggestions = service._current_analysis.get("action_suggestions", [])
        
        return {
            "suggestions": suggestions,
            "count": len(suggestions),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        _logger.error(f"Failed to get suggestions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/refresh-analysis")
async def refresh_analysis(
    analysis_type: str = "quick",
    service: AIVisionService = Depends(get_ai_vision_service)
):
    """Refresh analysis of current page."""
    try:
        if not service._current_url:
            raise HTTPException(status_code=400, detail="No current page to analyze")
        
        analysis = await service.analyze_website(
            url=service._current_url,
            analysis_type=analysis_type
        )
        
        return {
            "success": True,
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        _logger.error(f"Analysis refresh failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/capabilities")
async def get_vision_capabilities():
    """Get AI Vision capabilities."""
    return {
        "features": [
            "Real-time website analysis",
            "Element detection and classification",
            "Action suggestion based on visual context",
            "Interactive element mapping",
            "Workflow generation and execution",
            "Screenshot analysis with AI",
            "Multi-step automation workflows",
            "Natural language task interpretation"
        ],
        "supported_actions": [
            "navigate_to", "click_element", "fill_form", "hover_element",
            "select_option", "extract_data", "take_screenshot", "scroll",
            "wait", "validate_input", "clear_field"
        ],
        "analysis_types": ["quick", "detailed", "comprehensive"],
        "element_categories": [
            "text_input", "button", "link", "dropdown", "text_area",
            "file_input", "selection_input", "unknown"
        ]
    }
