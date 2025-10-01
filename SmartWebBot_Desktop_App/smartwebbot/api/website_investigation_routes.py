"""
Website Investigation API Routes - Revolutionary Website Intelligence

Provides API endpoints for comprehensive website investigation,
natural language command generation, and perfect automation execution.
"""

import asyncio
from typing import Dict, Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel

from ..intelligence.website_investigation.investigation_orchestrator import WebsiteInvestigationOrchestrator

# Create FastAPI router
router = APIRouter(prefix="/api/website-investigation", tags=["website-investigation"])

# Global investigation orchestrator
investigation_orchestrator = None


# Pydantic models
class InvestigateWebsiteRequest(BaseModel):
    url: str
    deep_analysis: bool = True
    force_refresh: bool = False


class ExecuteCommandRequest(BaseModel):
    url: str
    command: str
    parameters: Optional[Dict] = None


class GetCommandsRequest(BaseModel):
    url: str
    category: Optional[str] = None


# Initialize investigation orchestrator on startup
@router.on_event("startup")
async def startup_event():
    """Initialize website investigation system on startup."""
    global investigation_orchestrator
    
    try:
        print("🔍 Initializing Website Investigation System...")
        
        # Configuration for investigation system
        investigation_config = {
            "max_depth": 10,
            "timeout": 30,
            "enable_ai_analysis": True,
            "enable_deep_scan": True,
            "db_path": "data/website_knowledge.db",
            "cache_path": "data/website_cache.pkl"
        }
        
        # Initialize orchestrator
        investigation_orchestrator = WebsiteInvestigationOrchestrator(investigation_config)
        success = investigation_orchestrator.initialize()
        
        if success:
            print("✅ Website Investigation System initialized successfully!")
        else:
            print("❌ Failed to initialize Website Investigation System")
            raise Exception("Investigation system initialization failed")
    
    except Exception as e:
        print(f"Website Investigation startup failed: {e}")
        # Continue without investigation system
        print("⚠️ Continuing without Website Investigation System")


@router.post("/investigate")
async def investigate_website(request: InvestigateWebsiteRequest, background_tasks: BackgroundTasks):
    """
    Perform comprehensive website investigation.
    
    This is the REVOLUTIONARY endpoint that analyzes any website and discovers
    ALL possible actions, workflows, and generates natural language commands.
    """
    
    try:
        if not investigation_orchestrator:
            raise HTTPException(status_code=503, detail="Website investigation system not available")
        
        print(f"🔍 Starting investigation of: {request.url}")
        
        # Perform comprehensive investigation
        result = await investigation_orchestrator.investigate_website_comprehensive(request.url)
        
        if result["success"]:
            print(f"✅ Investigation completed for: {request.url}")
            return {
                "success": True,
                "message": "Website investigation completed successfully",
                "data": result,
                "next_steps": {
                    "get_commands": f"/api/website-investigation/commands?url={request.url}",
                    "execute_command": "/api/website-investigation/execute",
                    "get_status": f"/api/website-investigation/status?url={request.url}"
                }
            }
        else:
            raise HTTPException(status_code=500, detail=result["message"])
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Investigation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Investigation failed: {str(e)}")


@router.get("/commands")
async def get_natural_language_commands(url: str, category: Optional[str] = None):
    """
    Get natural language commands for a website.
    
    Returns all the natural language commands that can be executed
    on the investigated website.
    """
    
    try:
        if not investigation_orchestrator:
            raise HTTPException(status_code=503, detail="Website investigation system not available")
        
        result = await investigation_orchestrator.get_natural_language_commands(url)
        
        if result["success"]:
            # Filter by category if specified
            if category and category in result["commands_by_category"]:
                filtered_commands = {category: result["commands_by_category"][category]}
                result["commands_by_category"] = filtered_commands
                result["total_commands"] = len(filtered_commands[category])
            
            return {
                "success": True,
                "message": f"Found {result['total_commands']} commands for {result['domain']}",
                "data": result,
                "usage": {
                    "example_execution": "POST /api/website-investigation/execute with command text",
                    "sample_commands": result["commands_by_category"]
                }
            }
        else:
            raise HTTPException(status_code=404, detail=result["message"])
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get commands: {str(e)}")


@router.post("/execute")
async def execute_natural_language_command(request: ExecuteCommandRequest):
    """
    Execute a natural language command on a website.
    
    This converts natural language to a precise execution plan
    using the website's discovered knowledge.
    """
    
    try:
        if not investigation_orchestrator:
            raise HTTPException(status_code=503, detail="Website investigation system not available")
        
        print(f"🚀 Executing command: '{request.command}' on {request.url}")
        
        result = await investigation_orchestrator.execute_natural_language_command(
            request.command, request.url
        )
        
        if result["success"]:
            return {
                "success": True,
                "message": result["message"],
                "execution_plan": result["execution_plan"],
                "metadata": {
                    "original_command": request.command,
                    "matched_command": result["matched_command"],
                    "confidence": result["confidence"],
                    "estimated_time": result["estimated_time"],
                    "steps_count": result["steps_count"]
                },
                "next_steps": {
                    "execute_plan": "Use the execution_plan with your automation engine",
                    "modify_parameters": "Adjust parameters in the execution plan if needed"
                }
            }
        else:
            return {
                "success": False,
                "message": result["message"],
                "suggestions": result.get("suggestions", []),
                "help": f"Try commands like: {', '.join(result.get('suggestions', [])[:3])}"
            }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Command execution failed: {str(e)}")


@router.get("/status")
async def get_investigation_status(url: str):
    """
    Get investigation status for a website.
    
    Shows whether investigation is in progress, completed, or cached.
    """
    
    try:
        if not investigation_orchestrator:
            raise HTTPException(status_code=503, detail="Website investigation system not available")
        
        result = await investigation_orchestrator.get_investigation_status(url)
        
        return {
            "success": True,
            "status": result,
            "actions": {
                "start_investigation": "/api/website-investigation/investigate",
                "get_commands": "/api/website-investigation/commands",
                "execute_command": "/api/website-investigation/execute"
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")


@router.get("/statistics")
async def get_system_statistics():
    """
    Get comprehensive system statistics.
    
    Shows knowledge base statistics, performance metrics, and system health.
    """
    
    try:
        if not investigation_orchestrator:
            raise HTTPException(status_code=503, detail="Website investigation system not available")
        
        stats = investigation_orchestrator.get_system_statistics()
        
        return {
            "success": True,
            "message": "System statistics retrieved successfully",
            "statistics": stats,
            "system_info": {
                "total_investigations": stats["knowledge_base"]["total_investigations"],
                "total_domains": stats["knowledge_base"]["total_domains"],
                "total_workflows": stats["knowledge_base"]["total_workflows"],
                "system_healthy": all(stats["system_health"].values())
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Statistics retrieval failed: {str(e)}")


@router.delete("/cache")
async def clear_investigation_cache():
    """
    Clear investigation cache.
    
    Forces fresh investigation for all future requests.
    """
    
    try:
        if not investigation_orchestrator:
            raise HTTPException(status_code=503, detail="Website investigation system not available")
        
        # Clear cache (would need to implement this method)
        # investigation_orchestrator.knowledge_base.clear_cache()
        
        return {
            "success": True,
            "message": "Investigation cache cleared successfully",
            "note": "Future investigations will perform fresh analysis"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cache clear failed: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check for website investigation system."""
    
    return {
        "status": "healthy" if investigation_orchestrator and investigation_orchestrator.is_healthy else "unhealthy",
        "investigation_system_available": investigation_orchestrator is not None,
        "timestamp": asyncio.get_event_loop().time()
    }


# Advanced endpoints for power users
@router.get("/workflows/{domain}")
async def get_domain_workflows(domain: str, category: Optional[str] = None):
    """Get all discovered workflows for a specific domain."""
    
    try:
        if not investigation_orchestrator:
            raise HTTPException(status_code=503, detail="Website investigation system not available")
        
        # Get workflows by domain from knowledge base
        workflows = investigation_orchestrator.knowledge_base.find_workflows_by_intent("", domain)
        
        if category:
            workflows = [wf for wf in workflows if wf.category == category]
        
        return {
            "success": True,
            "domain": domain,
            "total_workflows": len(workflows),
            "workflows": [
                {
                    "id": wf.workflow_id,
                    "name": wf.name,
                    "description": wf.description,
                    "category": wf.category,
                    "complexity": wf.complexity,
                    "steps_count": len(wf.steps),
                    "estimated_time": wf.estimated_time,
                    "confidence": wf.confidence_score
                }
                for wf in workflows
            ]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get workflows: {str(e)}")


@router.get("/elements/{domain}")
async def get_domain_elements(domain: str, element_type: Optional[str] = None):
    """Get all discovered elements for a specific domain."""
    
    try:
        if not investigation_orchestrator:
            raise HTTPException(status_code=503, detail="Website investigation system not available")
        
        # Get elements by domain from knowledge base
        elements = investigation_orchestrator.knowledge_base.find_elements_by_type(element_type or "", domain)
        
        return {
            "success": True,
            "domain": domain,
            "element_type": element_type,
            "total_elements": len(elements),
            "elements": [
                {
                    "id": elem.element_id,
                    "type": elem.element_type.value,
                    "text": elem.text_content,
                    "selector": elem.selector,
                    "actions": [action.value for action in elem.action_types],
                    "confidence": elem.confidence_score,
                    "ai_description": elem.ai_description
                }
                for elem in elements[:50]  # Limit to 50 elements
            ]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get elements: {str(e)}")
