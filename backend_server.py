"""
FastAPI Backend Server for Reconext ADT Bot

Provides REST API and WebSocket endpoints for intelligent RMA processing
and PLUS system integration middleware.
"""

import asyncio
import json
import time
from typing import Dict, List, Optional, Any
from datetime import datetime

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Import our SmartWebBot
from smartwebbot import SmartWebBot, smart_bot
from smartwebbot.utils.config_manager import get_config_manager
from smartwebbot.utils.logger import BotLogger


# Pydantic models
class TaskCreate(BaseModel):
    name: str
    description: str
    url: Optional[str] = None
    actions: List[Dict[str, Any]] = []
    settings: Dict[str, Any] = {}


class TaskExecute(BaseModel):
    task_id: str
    parameters: Dict[str, Any] = {}


class SettingsUpdate(BaseModel):
    browser: Optional[Dict[str, Any]] = None
    automation: Optional[Dict[str, Any]] = None
    ai: Optional[Dict[str, Any]] = None


class CredentialsUpdate(BaseModel):
    credentials: Dict[str, str]


# FastAPI app
app = FastAPI(
    title="SmartWebBot Desktop API",
    description="Backend API for SmartWebBot Desktop Application",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
bot_instance: Optional[SmartWebBot] = None
active_connections: List[WebSocket] = []
current_task: Optional[Dict] = None
tasks_db: Dict[str, Dict] = {}  # Simple in-memory task storage
task_counter = 0

# Security testing state
security_tester: Optional[EthicalSecurityTester] = None


# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
            except:
                # Remove dead connections
                self.active_connections.remove(connection)


manager = ConnectionManager()


# Helper functions
async def broadcast_bot_status():
    """Broadcast bot status to all connected clients."""
    status = {
        "type": "bot_update",
        "data": {
            "isRunning": bot_instance is not None,
            "currentTask": current_task,
            "timestamp": datetime.now().isoformat()
        }
    }
    await manager.broadcast(status)


async def broadcast_task_update(task_id: str, status: str, progress: int = 0):
    """Broadcast task update to all connected clients."""
    update = {
        "type": "task_update",
        "data": {
            "taskId": task_id,
            "status": status,
            "progress": progress,
            "timestamp": datetime.now().isoformat()
        }
    }
    await manager.broadcast(update)


# API Routes

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.get("/bot/status")
async def get_bot_status():
    """Get current bot status."""
    return {
        "isRunning": bot_instance is not None,
        "currentTask": current_task,
        "timestamp": datetime.now().isoformat()
    }


@app.post("/bot/start")
async def start_bot(config: Dict[str, Any] = None):
    """Start the SmartWebBot instance."""
    global bot_instance
    
    try:
        if bot_instance is not None:
            return {"message": "Bot is already running", "status": "running"}
        
        # Create bot instance
        bot_instance = SmartWebBot(config_path="config.yaml")
        
        # Initialize bot (but don't start browser yet for performance)
        # The browser will start when needed for tasks
        
        await broadcast_bot_status()
        
        return {
            "message": "Bot started successfully",
            "status": "running",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start bot: {str(e)}")


@app.post("/bot/stop")
async def stop_bot():
    """Stop the SmartWebBot instance."""
    global bot_instance, current_task
    
    try:
        if bot_instance is None:
            return {"message": "Bot is not running", "status": "stopped"}
        
        # Clean up bot
        if hasattr(bot_instance, 'cleanup'):
            bot_instance.cleanup()
        
        bot_instance = None
        current_task = None
        
        await broadcast_bot_status()
        
        return {
            "message": "Bot stopped successfully",
            "status": "stopped",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to stop bot: {str(e)}")


@app.get("/tasks")
async def get_tasks():
    """Get all tasks."""
    return {"tasks": list(tasks_db.values())}


@app.post("/tasks")
async def create_task(task: TaskCreate):
    """Create a new task."""
    global task_counter
    
    task_counter += 1
    task_id = f"task_{task_counter}"
    
    new_task = {
        "id": task_id,
        "name": task.name,
        "description": task.description,
        "url": task.url,
        "actions": task.actions,
        "settings": task.settings,
        "status": "created",
        "created_at": datetime.now().isoformat(),
        "results": None
    }
    
    tasks_db[task_id] = new_task
    
    return {"task": new_task, "message": "Task created successfully"}


@app.post("/tasks/{task_id}/execute")
async def execute_task(task_id: str, execute_params: TaskExecute = None):
    """Execute a specific task."""
    global current_task
    
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if bot_instance is None:
        raise HTTPException(status_code=400, detail="Bot is not running. Please start the bot first.")
    
    task = tasks_db[task_id]
    current_task = task
    
    try:
        # Update task status
        task["status"] = "running"
        task["started_at"] = datetime.now().isoformat()
        
        await broadcast_task_update(task_id, "running", 0)
        
        # Execute task using SmartWebBot
        # This is a simplified example - you can expand based on task type
        if task.get("url"):
            # Navigate to URL
            success = bot_instance.navigate_to(task["url"])
            await broadcast_task_update(task_id, "running", 25)
            
            if not success:
                raise Exception("Failed to navigate to URL")
            
            # Perform task-specific actions
            if task.get("actions"):
                for i, action in enumerate(task["actions"]):
                    progress = 25 + (50 * (i + 1) / len(task["actions"]))
                    
                    if action.get("type") == "fill_form":
                        bot_instance.fill_form_intelligently(action.get("data", {}))
                    elif action.get("type") == "click":
                        bot_instance.click_element(action.get("selector", ""), intelligent=True)
                    elif action.get("type") == "extract":
                        data = bot_instance.extract_data_intelligently(action.get("description", ""))
                        task["results"] = data
                    
                    await broadcast_task_update(task_id, "running", int(progress))
                    await asyncio.sleep(0.5)  # Small delay for UI updates
            
            # Take final screenshot
            screenshot_path = bot_instance.take_screenshot(f"task_{task_id}_completed")
            task["screenshot"] = screenshot_path
            
            await broadcast_task_update(task_id, "running", 100)
        
        # Mark as completed
        task["status"] = "completed"
        task["completed_at"] = datetime.now().isoformat()
        current_task = None
        
        await broadcast_task_update(task_id, "completed", 100)
        await broadcast_bot_status()
        
        return {
            "message": "Task executed successfully",
            "task": task,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        # Mark as failed
        task["status"] = "failed"
        task["error"] = str(e)
        task["completed_at"] = datetime.now().isoformat()
        current_task = None
        
        await broadcast_task_update(task_id, "failed", 0)
        await broadcast_bot_status()
        
        raise HTTPException(status_code=500, detail=f"Task execution failed: {str(e)}")


@app.get("/tasks/{task_id}/results")
async def get_task_results(task_id: str):
    """Get results for a specific task."""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = tasks_db[task_id]
    return {"task": task, "results": task.get("results")}


@app.get("/settings")
async def get_settings():
    """Get current settings."""
    try:
        config_manager = get_config_manager()
        return config_manager.get_config_summary()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get settings: {str(e)}")


@app.put("/settings")
async def update_settings(settings: SettingsUpdate):
    """Update settings."""
    try:
        config_manager = get_config_manager()
        
        # Update configuration
        if settings.browser:
            for key, value in settings.browser.items():
                config_manager.set(f"browser.{key}", value)
        
        if settings.automation:
            for key, value in settings.automation.items():
                config_manager.set(f"automation.{key}", value)
        
        if settings.ai:
            for key, value in settings.ai.items():
                config_manager.set(f"ai.{key}", value)
        
        # Save configuration
        config_manager.save_configuration()
        
        return {"message": "Settings updated successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update settings: {str(e)}")


@app.post("/tasks/run")
async def run_task_immediately(task_data: dict):
    """Run a task immediately without saving it."""
    try:
        # Create a temporary task ID
        task_id = f"temp_{int(time.time())}"
        
        # Add to tasks database temporarily
        tasks_db[task_id] = {
            "id": task_id,
            "name": task_data.get("name", "Unnamed Task"),
            "description": task_data.get("description", ""),
            "website": task_data.get("website"),
            "browser": task_data.get("browser", "chrome"),
            "actions": task_data.get("actions", []),
            "status": "running",
            "created_at": datetime.now().isoformat(),
            "started_at": datetime.now().isoformat()
        }
        
        # Start the bot with the task configuration
        config = {
            "browser": task_data.get("browser", "chrome"),
            "headless": False,  # Show browser for demo
            "wait_time": 2
        }
        
        # Initialize the bot
        bot = SmartWebBot()
        bot.initialize()
        
        # Execute the task actions
        results = []
        
        try:
            # Start browser session
            session_data = bot.start_session(config)
            
            # Navigate to the website first
            if task_data.get("website"):
                bot.navigate_to_url(task_data.get("website"))
                results.append({"action": "navigate", "url": task_data.get("website"), "result": "success"})
            
            for action in task_data.get("actions", []):
                action_type = action.get("type")
                
                if action_type == "navigate":
                    bot.navigate_to_url(action.get("value"))
                    results.append({"action": "navigate", "url": action.get("value"), "result": "success"})
                    
                elif action_type == "click":
                    result = bot.click_element(action.get("selector"))
                    results.append({"action": "click", "selector": action.get("selector"), "result": result})
                    
                elif action_type == "type":
                    result = bot.type_text(action.get("selector"), action.get("value"))
                    results.append({"action": "type", "selector": action.get("selector"), "text": action.get("value"), "result": result})
                    
                elif action_type == "wait":
                    time.sleep(action.get("waitTime", 2))
                    results.append({"action": "wait", "duration": action.get("waitTime", 2), "result": "completed"})
                    
                elif action_type == "screenshot":
                    result = bot.take_screenshot()
                    results.append({"action": "screenshot", "result": result})
                    
                elif action_type == "extract_text":
                    result = bot.extract_text_from_element(action.get("selector"))
                    results.append({"action": "extract_text", "selector": action.get("selector"), "result": result})
                    
                elif action_type == "scroll":
                    bot.scroll_page()
                    results.append({"action": "scroll", "result": "completed"})
                
                # Wait between actions
                time.sleep(action.get("waitTime", 2))
            
            # Update task status
            tasks_db[task_id]["status"] = "completed"
            tasks_db[task_id]["completed_at"] = datetime.now().isoformat()
            tasks_db[task_id]["results"] = results
            
            return {
                "message": "Task executed successfully",
                "task_id": task_id,
                "results": results
            }
            
        except Exception as e:
            # Update task status to failed
            tasks_db[task_id]["status"] = "failed"
            tasks_db[task_id]["error"] = str(e)
            tasks_db[task_id]["completed_at"] = datetime.now().isoformat()
            
            raise HTTPException(status_code=500, detail=f"Task execution failed: {str(e)}")
            
        finally:
            # Clean up bot session
            try:
                bot.cleanup()
            except:
                pass
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to run task: {str(e)}")


@app.get("/performance/report")
async def get_performance_report():
    """Get performance report."""
    try:
        # Mock performance data for now
        return {
            "total_tasks": len(tasks_db),
            "completed_tasks": len([t for t in tasks_db.values() if t["status"] == "completed"]),
            "failed_tasks": len([t for t in tasks_db.values() if t["status"] == "failed"]),
            "success_rate": 95.5,
            "average_duration": 3.2,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get performance report: {str(e)}")


@app.get("/logs")
async def get_logs(limit: int = 100):
    """Get recent logs."""
    try:
        # Mock log data for now
        logs = [
            {"level": "INFO", "message": "Bot started successfully", "timestamp": datetime.now().isoformat()},
            {"level": "INFO", "message": "Task executed", "timestamp": datetime.now().isoformat()},
        ]
        return {"logs": logs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get logs: {str(e)}")


# Security Testing Endpoints
class SecurityAuthRequest(BaseModel):
    password: str

class SecuritySessionRequest(BaseModel):
    target_url: str
    authorization_token: Optional[str] = None

class SecurityTestRequest(BaseModel):
    test_type: str
    target_element: Optional[str] = None
    custom_payload: Optional[str] = None


@app.post("/api/security/authenticate")
async def authenticate_security_access(request: SecurityAuthRequest):
    """Authenticate user for security testing access."""
    global security_tester
    
    try:
        # Initialize security tester if not exists (works independently of bot instance)
        if not security_tester:
            # Security tester can work without a browser driver for testing
            driver = None
            if bot_instance and hasattr(bot_instance, 'web_controller') and bot_instance.web_controller:
                driver = bot_instance.web_controller.driver
            security_tester = EthicalSecurityTester(driver)
            security_tester.initialize()
        
        # Authenticate
        if security_tester.authenticate(request.password):
            return {"message": "Authentication successful", "authenticated": True}
        else:
            raise HTTPException(status_code=401, detail="Invalid password")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Authentication failed: {str(e)}")


@app.post("/api/security/start-session")
async def start_security_session(request: SecuritySessionRequest):
    """Start a new security testing session."""
    global security_tester
    
    try:
        if not security_tester or not security_tester.is_authenticated:
            raise HTTPException(status_code=401, detail="Authentication required")
        
        if security_tester.start_security_session(request.target_url, request.authorization_token):
            # Send real-time event to frontend
            await manager.broadcast({
                "type": "security_event",
                "event": "session_started",
                "session_id": security_tester.current_session.session_id,
                "target_domain": security_tester.current_session.target_domain,
                "timestamp": datetime.now().isoformat()
            })
            
            return {
                "message": "Security session started",
                "session_id": security_tester.current_session.session_id,
                "target_domain": security_tester.current_session.target_domain
            }
        else:
            raise HTTPException(status_code=400, detail="Failed to start security session")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start session: {str(e)}")


@app.post("/api/security/run-test")
async def run_security_test(request: SecurityTestRequest):
    """Run a specific security test."""
    global security_tester
    
    try:
        if not security_tester or not security_tester.current_session:
            raise HTTPException(status_code=400, detail="No active security session")
        
        # Convert string to SecurityTestType enum
        try:
            test_type = SecurityTestType(request.test_type)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid test type: {request.test_type}")
        
        # Send test started event
        await manager.broadcast({
            "type": "security_event",
            "event": "test_started",
            "test_type": request.test_type,
            "target_element": request.target_element or "default",
            "target_url": security_tester.current_session.target_domain if security_tester.current_session else "Unknown",
            "payload": request.custom_payload or "default_payload",
            "timestamp": datetime.now().isoformat()
        })
        
        # Run the test
        result = security_tester.perform_security_test(
            test_type,
            request.target_element,
            request.custom_payload
        )
        
        # Send test completed event
        await manager.broadcast({
            "type": "security_event",
            "event": "test_completed",
            "result": {
                "test_type": result.test_type.value,
                "success": result.success,
                "severity": result.severity.value,
                "payload_used": result.payload_used,
                "evidence": result.evidence,
                "remediation": result.remediation
            },
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "test_type": result.test_type.value,
            "success": result.success,
            "severity": result.severity.value,
            "description": result.description,
            "payload_used": result.payload_used,
            "evidence": result.evidence,
            "remediation": result.remediation,
            "timestamp": result.timestamp.isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test execution failed: {str(e)}")


@app.get("/api/security/session-report")
async def get_security_session_report():
    """Get current security session report."""
    global security_tester
    
    try:
        if not security_tester or not security_tester.current_session:
            raise HTTPException(status_code=400, detail="No active security session")
        
        return security_tester.get_session_report()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get session report: {str(e)}")


@app.post("/api/security/end-session")
async def end_security_session():
    """End current security session."""
    global security_tester
    
    try:
        if not security_tester or not security_tester.current_session:
            raise HTTPException(status_code=400, detail="No active security session")
        
        final_report = security_tester.end_security_session()
        return final_report
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to end session: {str(e)}")


@app.post("/api/security/execute-xss-attack")
async def execute_xss_attack(request: dict):
    """Execute advanced XSS attack with real data extraction."""
    global security_tester
    
    try:
        if not security_tester or not security_tester.current_session:
            raise HTTPException(status_code=400, detail="No active security session")
        
        attack_type = request.get("attack_type")
        target_element = request.get("target_element")
        
        if not attack_type:
            raise HTTPException(status_code=400, detail="Attack type is required")
        
        # Execute the XSS attack
        result = security_tester.execute_advanced_xss_attack(attack_type, target_element)
        
        # Broadcast real-time results
        await manager.broadcast({
            "type": "xss_attack_result",
            "event": "attack_completed",
            "result": result,
            "timestamp": datetime.now().isoformat()
        })
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"XSS attack failed: {str(e)}")


@app.get("/api/security/xss-results")
async def get_xss_results():
    """Get comprehensive XSS attack results and statistics."""
    global security_tester
    
    try:
        if not security_tester:
            raise HTTPException(status_code=400, detail="Security tester not initialized")
        
        return security_tester.get_xss_attack_results()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get XSS results: {str(e)}")


# Security Results Management Endpoints
@app.get("/api/security/results/sessions")
async def get_security_sessions():
    """Get all security testing sessions."""
    global security_tester
    
    try:
        if not security_tester:
            raise HTTPException(status_code=400, detail="Security tester not initialized")
        
        sessions = security_tester.results_manager.get_all_sessions()
        return {"sessions": sessions}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get sessions: {str(e)}")


@app.get("/api/security/results/session/{session_id}")
async def get_security_session_details(session_id: str):
    """Get detailed information about a specific security session."""
    global security_tester
    
    try:
        if not security_tester:
            raise HTTPException(status_code=400, detail="Security tester not initialized")
        
        session_details = security_tester.results_manager.get_session_details(session_id)
        if not session_details:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return session_details
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get session details: {str(e)}")


@app.get("/api/security/results/summary")
async def get_vulnerability_summary():
    """Get overall vulnerability statistics and summary."""
    global security_tester
    
    try:
        if not security_tester:
            raise HTTPException(status_code=400, detail="Security tester not initialized")
        
        summary = security_tester.results_manager.get_vulnerability_summary()
        return summary
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get vulnerability summary: {str(e)}")


@app.get("/api/security/results/export/{session_id}")
async def export_security_session(session_id: str, format: str = "json"):
    """Export security session report in specified format."""
    global security_tester
    
    try:
        if not security_tester:
            raise HTTPException(status_code=400, detail="Security tester not initialized")
        
        if format not in ["json", "csv"]:
            raise HTTPException(status_code=400, detail="Format must be 'json' or 'csv'")
        
        export_path = security_tester.results_manager.export_session_report(session_id, format)
        if not export_path:
            raise HTTPException(status_code=404, detail="Session not found or export failed")
        
        # Return file download
        from fastapi.responses import FileResponse
        return FileResponse(
            path=export_path,
            filename=f"security_report_{session_id}.{format}",
            media_type="application/octet-stream"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to export session: {str(e)}")


@app.get("/api/security/status")
async def get_security_status():
    """Get security testing status."""
    global security_tester
    
    return {
        "security_module_loaded": security_tester is not None,
        "authenticated": security_tester.is_authenticated if security_tester else False,
        "session_active": security_tester.current_session is not None if security_tester else False,
        "session_id": security_tester.current_session.session_id if security_tester and security_tester.current_session else None
    }


# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates."""
    await manager.connect(websocket)
    
    try:
        # Send initial status
        await websocket.send_text(json.dumps({
            "type": "connected",
            "data": {"message": "Connected to SmartWebBot backend"}
        }))
        
        while True:
            # Keep connection alive
            await websocket.receive_text()
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)


if __name__ == "__main__":
    print("Starting Reconext ADT Bot Backend Server...")
    print("WebSocket: ws://localhost:8000/ws")
    print("API Docs: http://localhost:8000/docs")
    print("Frontend: http://localhost:3000")
    print("RMA Processing Middleware: Ready")
    
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=8000,
        log_level="info"
    )
