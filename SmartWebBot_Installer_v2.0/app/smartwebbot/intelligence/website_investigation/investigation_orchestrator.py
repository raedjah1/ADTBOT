"""
Website Investigation Orchestrator - The Revolutionary Controller

Orchestrates comprehensive website investigations and provides
natural language interface for perfect automation execution.
"""

import asyncio
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse
from ..core.base_chat_component import BaseChatComponent
from .website_analyzer import ComprehensiveWebsiteAnalyzer, WebsiteInvestigationResult
from .knowledge_base import WebsiteKnowledgeBase, ActionCommand


class WebsiteInvestigationOrchestrator(BaseChatComponent):
    """
    Revolutionary website investigation orchestrator.
    
    Features:
    - One-click comprehensive website analysis
    - Natural language command generation
    - Perfect workflow execution planning
    - Intelligent caching and optimization
    - Real-time investigation progress
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("website_investigation_orchestrator", config)
        
        # Core components
        self.analyzer = ComprehensiveWebsiteAnalyzer(config)
        self.knowledge_base = WebsiteKnowledgeBase(config)
        
        # Investigation cache
        self.active_investigations: Dict[str, Dict] = {}
    
    def initialize(self) -> bool:
        """Initialize the orchestrator."""
        try:
            self.logger.info("Initializing Website Investigation Orchestrator...")
            
            # Initialize components
            if not self.analyzer.initialize():
                raise Exception("Failed to initialize website analyzer")
            
            if not self.knowledge_base.initialize():
                raise Exception("Failed to initialize knowledge base")
            
            self.is_initialized = True
            self.is_healthy = True
            
            self.logger.info("Website Investigation Orchestrator initialized successfully")
            return True
            
        except Exception as e:
            self.log_error(e, "Investigation orchestrator initialization failed")
            return False
    
    async def investigate_website_comprehensive(self, url: str) -> Dict[str, Any]:
        """
        Perform comprehensive website investigation.
        
        This is the main entry point for the revolutionary system.
        """
        try:
            domain = urlparse(url).netloc
            self.logger.info(f"🚀 Starting comprehensive investigation of: {url}")
            
            # Check if investigation is already in progress
            if url in self.active_investigations:
                return {
                    "success": False,
                    "message": "Investigation already in progress for this URL",
                    "investigation_id": self.active_investigations[url]["id"]
                }
            
            # Check knowledge base for cached results
            cached_investigation = self.knowledge_base.get_investigation(url)
            if cached_investigation:
                self.logger.info(f"Found cached investigation for: {url}")
                return await self._format_investigation_response(cached_investigation, from_cache=True)
            
            # Start new investigation
            investigation_id = f"inv_{int(asyncio.get_event_loop().time() * 1000)}"
            
            self.active_investigations[url] = {
                "id": investigation_id,
                "status": "in_progress",
                "start_time": asyncio.get_event_loop().time(),
                "progress": 0
            }
            
            try:
                # Perform comprehensive analysis
                investigation_result = await self.analyzer.investigate_website(url)
                
                # Store in knowledge base
                self.knowledge_base.store_investigation(investigation_result)
                
                # Update status
                self.active_investigations[url]["status"] = "completed"
                self.active_investigations[url]["progress"] = 100
                
                # Format response
                response = await self._format_investigation_response(investigation_result)
                
                # Clean up active investigation
                del self.active_investigations[url]
                
                return response
                
            except Exception as e:
                # Update status to failed
                self.active_investigations[url]["status"] = "failed"
                self.active_investigations[url]["error"] = str(e)
                
                self.log_error(e, f"Investigation failed for: {url}")
                
                return {
                    "success": False,
                    "message": f"Investigation failed: {str(e)}",
                    "investigation_id": investigation_id,
                    "url": url
                }
            
        except Exception as e:
            self.log_error(e, f"Investigation orchestration failed for: {url}")
            return {
                "success": False,
                "message": f"Investigation orchestration failed: {str(e)}",
                "url": url
            }
    
    async def get_natural_language_commands(self, url: str) -> Dict[str, Any]:
        """Get natural language commands for a website."""
        try:
            domain = urlparse(url).netloc
            
            # Get from knowledge base
            commands = self.knowledge_base.get_natural_language_commands(domain)
            
            if not commands:
                return {
                    "success": False,
                    "message": "No investigation data found for this website. Please run investigation first.",
                    "url": url
                }
            
            # Organize commands by category
            categorized_commands = {}
            for command in commands:
                category = command.intent
                if category not in categorized_commands:
                    categorized_commands[category] = []
                categorized_commands[category].append({
                    "command": command.natural_language,
                    "confidence": command.confidence_score,
                    "estimated_time": command.execution_time_estimate,
                    "examples": command.examples,
                    "workflow_id": command.workflow_id
                })
            
            return {
                "success": True,
                "url": url,
                "domain": domain,
                "total_commands": len(commands),
                "categories": list(categorized_commands.keys()),
                "commands_by_category": categorized_commands,
                "message": f"Found {len(commands)} natural language commands for {domain}"
            }
            
        except Exception as e:
            self.log_error(e, f"Failed to get commands for: {url}")
            return {
                "success": False,
                "message": f"Failed to get commands: {str(e)}",
                "url": url
            }
    
    async def execute_natural_language_command(self, command: str, url: str) -> Dict[str, Any]:
        """Execute natural language command on website."""
        try:
            domain = urlparse(url).netloc
            
            # Search for matching commands
            matching_commands = self.knowledge_base.search_by_natural_language(command, domain)
            
            if not matching_commands:
                return {
                    "success": False,
                    "message": f"No matching commands found for: '{command}'",
                    "suggestions": await self._get_command_suggestions(domain)
                }
            
            # Get the best matching command
            best_command = matching_commands[0]
            
            # Get detailed execution plan
            execution_plan = self.knowledge_base.get_workflow_execution_plan(
                best_command.workflow_id, domain
            )
            
            if not execution_plan:
                return {
                    "success": False,
                    "message": f"Could not create execution plan for: '{command}'"
                }
            
            return {
                "success": True,
                "message": f"Execution plan created for: '{command}'",
                "command": command,
                "matched_command": best_command.natural_language,
                "confidence": best_command.confidence_score,
                "execution_plan": execution_plan,
                "estimated_time": execution_plan["estimated_time"],
                "steps_count": len(execution_plan["steps"])
            }
            
        except Exception as e:
            self.log_error(e, f"Command execution failed for: {command}")
            return {
                "success": False,
                "message": f"Command execution failed: {str(e)}",
                "command": command
            }
    
    async def get_investigation_status(self, url: str) -> Dict[str, Any]:
        """Get investigation status."""
        try:
            # Check if investigation is active
            if url in self.active_investigations:
                investigation = self.active_investigations[url]
                return {
                    "status": investigation["status"],
                    "progress": investigation["progress"],
                    "investigation_id": investigation["id"],
                    "elapsed_time": asyncio.get_event_loop().time() - investigation["start_time"],
                    "url": url
                }
            
            # Check if investigation is cached
            domain = urlparse(url).netloc
            cached_investigation = self.knowledge_base.get_investigation(url)
            
            if cached_investigation:
                return {
                    "status": "completed",
                    "progress": 100,
                    "investigation_id": f"cached_{domain}",
                    "url": url,
                    "cached": True,
                    "investigation_time": cached_investigation.investigation_timestamp
                }
            
            return {
                "status": "not_found",
                "progress": 0,
                "url": url,
                "message": "No investigation found for this URL"
            }
            
        except Exception as e:
            self.log_error(e, f"Status check failed for: {url}")
            return {
                "status": "error",
                "message": str(e),
                "url": url
            }
    
    async def _format_investigation_response(self, investigation: WebsiteInvestigationResult, 
                                           from_cache: bool = False) -> Dict[str, Any]:
        """Format investigation results for API response."""
        
        return {
            "success": True,
            "message": f"Investigation {'retrieved from cache' if from_cache else 'completed successfully'}",
            "url": investigation.url,
            "domain": investigation.domain,
            "title": investigation.title,
            "investigation_summary": {
                "total_elements": len(investigation.discovered_elements),
                "total_workflows": len(investigation.discovered_workflows),
                "total_commands": len(investigation.natural_language_commands),
                "investigation_time": investigation.investigation_timestamp,
                "from_cache": from_cache
            },
            "discovered_capabilities": {
                "authentication": len(investigation.authentication_methods),
                "forms": len(investigation.form_patterns),
                "ecommerce": len(investigation.e_commerce_features),
                "search": bool(investigation.search_capabilities),
                "social": len(investigation.social_features)
            },
            "workflow_categories": list(set(wf.category for wf in investigation.discovered_workflows)),
            "sample_commands": investigation.natural_language_commands[:5],  # First 5 commands
            "ai_insights": investigation.ai_insights[:3],  # Top 3 insights
            "performance_score": investigation.performance_metrics.get("overall_score", 0),
            "accessibility_score": investigation.accessibility_info.get("score", 0),
            "technology_stack": investigation.technology_stack[:10]  # Top 10 technologies
        }
    
    async def _get_command_suggestions(self, domain: str) -> List[str]:
        """Get command suggestions for domain."""
        try:
            commands = self.knowledge_base.get_natural_language_commands(domain)
            
            # Return top 5 most confident commands
            suggestions = [cmd.natural_language for cmd in 
                         sorted(commands, key=lambda x: x.confidence_score, reverse=True)[:5]]
            
            return suggestions
            
        except Exception:
            return []
    
    def get_system_statistics(self) -> Dict[str, Any]:
        """Get comprehensive system statistics."""
        kb_stats = self.knowledge_base.get_statistics()
        
        return {
            "knowledge_base": kb_stats,
            "active_investigations": len(self.active_investigations),
            "system_health": {
                "analyzer_healthy": self.analyzer.is_healthy,
                "knowledge_base_healthy": self.knowledge_base.is_healthy,
                "orchestrator_healthy": self.is_healthy
            },
            "capabilities": {
                "comprehensive_analysis": True,
                "natural_language_commands": True,
                "workflow_execution": True,
                "real_time_investigation": True,
                "intelligent_caching": True
            }
        }
