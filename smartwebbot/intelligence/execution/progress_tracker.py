"""
Progress Tracker for Workflow Execution.

Tracks and reports workflow execution progress with
real-time updates and detailed metrics.
"""

import time
from typing import Dict, Optional, Any
from ..core.base_chat_component import BaseChatComponent


class ProgressTracker(BaseChatComponent):
    """
    Tracks workflow execution progress and provides metrics.
    
    Features:
    - Real-time progress tracking
    - Performance metrics collection
    - Execution time estimation
    - Progress reporting
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("progress_tracker", config)
        
        # Progress tracking state
        self.tracking_sessions: Dict[str, Dict] = {}
        
        # Configuration
        self.update_interval = self.get_config_value("update_interval", 1.0)
    
    def initialize(self) -> bool:
        """Initialize the progress tracker."""
        try:
            self.logger.info("Initializing Progress Tracker...")
            
            self.is_initialized = True
            self.is_healthy = True
            
            self.logger.info("Progress Tracker initialized successfully")
            return True
            
        except Exception as e:
            self.log_error(e, "Progress tracker initialization")
            return False
    
    async def start_tracking(self, plan_id: str, total_steps: int) -> None:
        """Start tracking progress for a workflow."""
        
        tracking_session = {
            "plan_id": plan_id,
            "total_steps": total_steps,
            "completed_steps": 0,
            "failed_steps": 0,
            "start_time": time.time(),
            "last_update": time.time(),
            "estimated_completion": None,
            "progress_percentage": 0.0
        }
        
        self.tracking_sessions[plan_id] = tracking_session
        
        self.logger.info(f"Started progress tracking for workflow: {plan_id} ({total_steps} steps)")
    
    async def update_progress(self, plan_id: str, completed_steps: int, total_steps: int) -> None:
        """Update progress for a workflow."""
        
        if plan_id not in self.tracking_sessions:
            self.logger.warning(f"Progress tracking session not found: {plan_id}")
            return
        
        session = self.tracking_sessions[plan_id]
        
        # Update progress
        session["completed_steps"] = completed_steps
        session["total_steps"] = total_steps
        session["last_update"] = time.time()
        
        # Calculate progress percentage
        if total_steps > 0:
            session["progress_percentage"] = (completed_steps / total_steps) * 100
        
        # Estimate completion time
        session["estimated_completion"] = self._estimate_completion_time(session)
        
        self.logger.debug(f"Progress updated: {plan_id} - {completed_steps}/{total_steps} ({session['progress_percentage']:.1f}%)")
    
    async def stop_tracking(self, plan_id: str) -> None:
        """Stop tracking progress for a workflow."""
        
        if plan_id in self.tracking_sessions:
            session = self.tracking_sessions[plan_id]
            session["end_time"] = time.time()
            session["total_duration"] = session["end_time"] - session["start_time"]
            
            self.logger.info(f"Stopped progress tracking for workflow: {plan_id} (Duration: {session['total_duration']:.2f}s)")
            
            # Keep session for historical data (could be cleaned up later)
            # del self.tracking_sessions[plan_id]
    
    def get_progress(self, plan_id: str) -> Optional[Dict[str, Any]]:
        """Get current progress for a workflow."""
        
        if plan_id not in self.tracking_sessions:
            return None
        
        session = self.tracking_sessions[plan_id]
        
        return {
            "plan_id": plan_id,
            "progress_percentage": session["progress_percentage"],
            "completed_steps": session["completed_steps"],
            "total_steps": session["total_steps"],
            "failed_steps": session.get("failed_steps", 0),
            "elapsed_time": time.time() - session["start_time"],
            "estimated_completion": session.get("estimated_completion"),
            "last_update": session["last_update"]
        }
    
    def get_all_progress(self) -> Dict[str, Dict[str, Any]]:
        """Get progress for all tracked workflows."""
        
        return {
            plan_id: self.get_progress(plan_id) 
            for plan_id in self.tracking_sessions.keys()
        }
    
    def _estimate_completion_time(self, session: Dict) -> Optional[float]:
        """Estimate workflow completion time."""
        
        completed_steps = session["completed_steps"]
        total_steps = session["total_steps"]
        elapsed_time = time.time() - session["start_time"]
        
        if completed_steps == 0:
            return None
        
        # Calculate average time per step
        avg_time_per_step = elapsed_time / completed_steps
        
        # Estimate remaining time
        remaining_steps = total_steps - completed_steps
        remaining_time = remaining_steps * avg_time_per_step
        
        # Return estimated completion timestamp
        return time.time() + remaining_time
    
    def get_performance_metrics(self, plan_id: str) -> Optional[Dict[str, Any]]:
        """Get performance metrics for a workflow."""
        
        if plan_id not in self.tracking_sessions:
            return None
        
        session = self.tracking_sessions[plan_id]
        current_time = time.time()
        
        elapsed_time = current_time - session["start_time"]
        completed_steps = session["completed_steps"]
        total_steps = session["total_steps"]
        
        metrics = {
            "plan_id": plan_id,
            "elapsed_time": elapsed_time,
            "steps_per_second": completed_steps / elapsed_time if elapsed_time > 0 else 0,
            "completion_rate": (completed_steps / total_steps) * 100 if total_steps > 0 else 0,
            "estimated_total_time": self._estimate_completion_time(session),
            "efficiency_score": self._calculate_efficiency_score(session)
        }
        
        return metrics
    
    def _calculate_efficiency_score(self, session: Dict) -> float:
        """Calculate efficiency score for workflow execution."""
        
        completed_steps = session["completed_steps"]
        failed_steps = session.get("failed_steps", 0)
        elapsed_time = time.time() - session["start_time"]
        
        if completed_steps == 0:
            return 0.0
        
        # Base efficiency: success rate
        success_rate = completed_steps / (completed_steps + failed_steps) if (completed_steps + failed_steps) > 0 else 1.0
        
        # Time efficiency: steps per minute
        steps_per_minute = (completed_steps / elapsed_time) * 60 if elapsed_time > 0 else 0
        
        # Normalize time efficiency (assume 10 steps per minute is excellent)
        time_efficiency = min(steps_per_minute / 10.0, 1.0)
        
        # Combine metrics (weighted average)
        efficiency_score = (success_rate * 0.7) + (time_efficiency * 0.3)
        
        return round(efficiency_score * 100, 2)  # Return as percentage
    
    def cleanup_old_sessions(self, max_age_hours: int = 24) -> int:
        """Clean up old tracking sessions."""
        
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        
        old_sessions = []
        
        for plan_id, session in self.tracking_sessions.items():
            session_age = current_time - session["start_time"]
            if session_age > max_age_seconds:
                old_sessions.append(plan_id)
        
        # Remove old sessions
        for plan_id in old_sessions:
            del self.tracking_sessions[plan_id]
        
        if old_sessions:
            self.logger.info(f"Cleaned up {len(old_sessions)} old tracking sessions")
        
        return len(old_sessions)
