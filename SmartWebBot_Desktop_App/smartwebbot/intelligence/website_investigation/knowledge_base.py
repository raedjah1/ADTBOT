"""
Website Knowledge Base - Ultra-Fast Data Structure for Website Intelligence

Stores and retrieves website investigation data using optimized data structures
for lightning-fast natural language command execution.
"""

import json
import pickle
import hashlib
import time
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, asdict
from collections import defaultdict
import sqlite3
from ..core.base_chat_component import BaseChatComponent
from .website_analyzer import WebsiteInvestigationResult, DiscoveredElement, DiscoveredWorkflow


@dataclass
class ActionCommand:
    """Natural language command for website actions."""
    command_id: str
    natural_language: str
    intent: str
    workflow_id: str
    parameters: Dict[str, Any]
    confidence_score: float
    execution_time_estimate: int
    examples: List[str]


class WebsiteKnowledgeBase(BaseChatComponent):
    """
    Ultra-optimized knowledge base for website intelligence.
    
    Features:
    - Lightning-fast lookups with multiple indexes
    - Natural language to action mapping
    - Workflow pattern storage and retrieval
    - Element hierarchy and relationships
    - Performance-optimized data structures
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("website_knowledge_base", config)
        
        # Storage paths
        self.db_path = self.get_config_value("db_path", "data/website_knowledge.db")
        self.cache_path = self.get_config_value("cache_path", "data/website_cache.pkl")
        
        # In-memory indexes for ultra-fast access
        self.url_to_investigation: Dict[str, WebsiteInvestigationResult] = {}
        self.domain_to_patterns: Dict[str, List[str]] = defaultdict(list)
        self.intent_to_workflows: Dict[str, List[str]] = defaultdict(list)
        self.element_type_index: Dict[str, List[str]] = defaultdict(list)
        self.natural_language_index: Dict[str, List[ActionCommand]] = defaultdict(list)
        self.workflow_dependencies: Dict[str, Set[str]] = defaultdict(set)
        
        # SQLite connection
        self.db_connection = None
    
    def initialize(self) -> bool:
        """Initialize the knowledge base."""
        try:
            self.logger.info("Initializing Website Knowledge Base...")
            
            # Create database and tables
            self._setup_database()
            
            # Load cached data
            self._load_cache()
            
            self.is_initialized = True
            self.is_healthy = True
            
            self.logger.info("Website Knowledge Base initialized successfully")
            return True
            
        except Exception as e:
            self.log_error(e, "Knowledge base initialization failed")
            return False
    
    def store_investigation(self, investigation: WebsiteInvestigationResult) -> bool:
        """Store website investigation results with optimized indexing."""
        try:
            domain = investigation.domain
            url = investigation.url
            
            # Store in memory for fast access
            self.url_to_investigation[url] = investigation
            
            # Build indexes
            self._build_indexes_for_investigation(investigation)
            
            # Store in database
            self._store_in_database(investigation)
            
            # Update cache
            self._update_cache()
            
            self.logger.info(f"Stored investigation for {domain} with {len(investigation.discovered_elements)} elements")
            return True
            
        except Exception as e:
            self.log_error(e, f"Failed to store investigation for {investigation.url}")
            return False
    
    def get_investigation(self, url: str) -> Optional[WebsiteInvestigationResult]:
        """Get investigation results for URL."""
        return self.url_to_investigation.get(url)
    
    def find_workflows_by_intent(self, intent: str, domain: Optional[str] = None) -> List[DiscoveredWorkflow]:
        """Find workflows matching specific intent."""
        try:
            matching_workflows = []
            
            # Search in intent index
            workflow_ids = self.intent_to_workflows.get(intent.lower(), [])
            
            for workflow_id in workflow_ids:
                # Find investigation containing this workflow
                for investigation in self.url_to_investigation.values():
                    if domain and investigation.domain != domain:
                        continue
                    
                    for workflow in investigation.discovered_workflows:
                        if workflow.workflow_id == workflow_id:
                            matching_workflows.append(workflow)
            
            return matching_workflows
            
        except Exception as e:
            self.log_error(e, f"Failed to find workflows for intent: {intent}")
            return []
    
    def find_elements_by_type(self, element_type: str, domain: Optional[str] = None) -> List[DiscoveredElement]:
        """Find elements by type."""
        try:
            matching_elements = []
            
            element_ids = self.element_type_index.get(element_type.lower(), [])
            
            for element_id in element_ids:
                for investigation in self.url_to_investigation.values():
                    if domain and investigation.domain != domain:
                        continue
                    
                    for element in investigation.discovered_elements:
                        if element.element_id == element_id:
                            matching_elements.append(element)
            
            return matching_elements
            
        except Exception as e:
            self.log_error(e, f"Failed to find elements of type: {element_type}")
            return []
    
    def get_natural_language_commands(self, domain: str) -> List[ActionCommand]:
        """Get all natural language commands for a domain."""
        try:
            investigation = None
            for inv in self.url_to_investigation.values():
                if inv.domain == domain:
                    investigation = inv
                    break
            
            if not investigation:
                return []
            
            commands = []
            for nl_command in investigation.natural_language_commands:
                command = ActionCommand(
                    command_id=nl_command.get("command_id", ""),
                    natural_language=nl_command.get("command", ""),
                    intent=nl_command.get("intent", ""),
                    workflow_id=nl_command.get("workflow_id", ""),
                    parameters=nl_command.get("parameters", {}),
                    confidence_score=nl_command.get("confidence", 0.0),
                    execution_time_estimate=nl_command.get("estimated_time", 30),
                    examples=nl_command.get("examples", [])
                )
                commands.append(command)
            
            return commands
            
        except Exception as e:
            self.log_error(e, f"Failed to get commands for domain: {domain}")
            return []
    
    def search_by_natural_language(self, query: str, domain: Optional[str] = None) -> List[ActionCommand]:
        """Search for actions using natural language."""
        try:
            query_lower = query.lower()
            matching_commands = []
            
            # Keyword matching in natural language index
            for keywords, commands in self.natural_language_index.items():
                if any(word in query_lower for word in keywords.split()):
                    for command in commands:
                        if not domain or self._command_matches_domain(command, domain):
                            matching_commands.append(command)
            
            # Sort by confidence score
            matching_commands.sort(key=lambda x: x.confidence_score, reverse=True)
            
            return matching_commands[:10]  # Return top 10 matches
            
        except Exception as e:
            self.log_error(e, f"Natural language search failed for: {query}")
            return []
    
    def get_workflow_execution_plan(self, workflow_id: str, domain: str) -> Optional[Dict[str, Any]]:
        """Get detailed execution plan for workflow."""
        try:
            # Find the workflow
            workflow = None
            investigation = None
            
            for inv in self.url_to_investigation.values():
                if inv.domain == domain:
                    investigation = inv
                    for wf in inv.discovered_workflows:
                        if wf.workflow_id == workflow_id:
                            workflow = wf
                            break
                    if workflow:
                        break
            
            if not workflow or not investigation:
                return None
            
            # Build execution plan
            execution_plan = {
                "workflow_id": workflow_id,
                "name": workflow.name,
                "description": workflow.description,
                "steps": [],
                "estimated_time": workflow.estimated_time,
                "success_indicators": workflow.success_indicators,
                "prerequisites": workflow.prerequisites
            }
            
            # Add detailed step information
            for step in workflow.steps:
                detailed_step = step.copy()
                
                # Find element details if step references an element
                if "element_id" in step:
                    element_id = step["element_id"]
                    for element in investigation.discovered_elements:
                        if element.element_id == element_id:
                            detailed_step["element_details"] = {
                                "selector": element.selector,
                                "xpath": element.xpath,
                                "text_content": element.text_content,
                                "position": element.position,
                                "ai_description": element.ai_description
                            }
                            break
                
                execution_plan["steps"].append(detailed_step)
            
            return execution_plan
            
        except Exception as e:
            self.log_error(e, f"Failed to get execution plan for workflow: {workflow_id}")
            return None
    
    def _setup_database(self) -> None:
        """Setup SQLite database with optimized schema."""
        self.db_connection = sqlite3.connect(self.db_path)
        
        # Create tables with indexes
        cursor = self.db_connection.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS investigations (
                url TEXT PRIMARY KEY,
                domain TEXT NOT NULL,
                data BLOB NOT NULL,
                created_at REAL NOT NULL
            )
        """)
        
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_domain ON investigations(domain)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_created_at ON investigations(created_at)")
        
        self.db_connection.commit()
    
    def _build_indexes_for_investigation(self, investigation: WebsiteInvestigationResult) -> None:
        """Build optimized indexes for investigation."""
        domain = investigation.domain
        
        # Domain patterns
        self.domain_to_patterns[domain].extend([
            wf.category for wf in investigation.discovered_workflows
        ])
        
        # Intent to workflow mapping
        for workflow in investigation.discovered_workflows:
            self.intent_to_workflows[workflow.name.lower()].append(workflow.workflow_id)
            self.intent_to_workflows[workflow.category.lower()].append(workflow.workflow_id)
        
        # Element type indexing
        for element in investigation.discovered_elements:
            self.element_type_index[element.element_type.value].append(element.element_id)
        
        # Natural language command indexing
        for nl_command in investigation.natural_language_commands:
            command = ActionCommand(
                command_id=nl_command.get("command_id", ""),
                natural_language=nl_command.get("command", ""),
                intent=nl_command.get("intent", ""),
                workflow_id=nl_command.get("workflow_id", ""),
                parameters=nl_command.get("parameters", {}),
                confidence_score=nl_command.get("confidence", 0.0),
                execution_time_estimate=nl_command.get("estimated_time", 30),
                examples=nl_command.get("examples", [])
            )
            
            # Create keyword index
            keywords = command.natural_language.lower()
            self.natural_language_index[keywords].append(command)
        
        # Workflow dependencies
        for workflow in investigation.discovered_workflows:
            for prereq in workflow.prerequisites:
                self.workflow_dependencies[workflow.workflow_id].add(prereq)
    
    def _store_in_database(self, investigation: WebsiteInvestigationResult) -> None:
        """Store investigation in SQLite database."""
        cursor = self.db_connection.cursor()
        
        # Serialize investigation data
        data = pickle.dumps(investigation)
        
        cursor.execute("""
            INSERT OR REPLACE INTO investigations (url, domain, data, created_at)
            VALUES (?, ?, ?, ?)
        """, (investigation.url, investigation.domain, data, time.time()))
        
        self.db_connection.commit()
    
    def _load_cache(self) -> None:
        """Load cached data."""
        try:
            with open(self.cache_path, 'rb') as f:
                cache_data = pickle.load(f)
                self.url_to_investigation = cache_data.get('investigations', {})
                
                # Rebuild indexes
                for investigation in self.url_to_investigation.values():
                    self._build_indexes_for_investigation(investigation)
                    
        except FileNotFoundError:
            pass  # No cache file yet
        except Exception as e:
            self.log_error(e, "Failed to load cache")
    
    def _update_cache(self) -> None:
        """Update cache file."""
        try:
            cache_data = {
                'investigations': self.url_to_investigation,
                'updated_at': time.time()
            }
            
            with open(self.cache_path, 'wb') as f:
                pickle.dump(cache_data, f)
                
        except Exception as e:
            self.log_error(e, "Failed to update cache")
    
    def _command_matches_domain(self, command: ActionCommand, domain: str) -> bool:
        """Check if command belongs to specific domain."""
        # Find investigation containing this workflow
        for investigation in self.url_to_investigation.values():
            if investigation.domain == domain:
                for workflow in investigation.discovered_workflows:
                    if workflow.workflow_id == command.workflow_id:
                        return True
        return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get knowledge base statistics."""
        return {
            "total_investigations": len(self.url_to_investigation),
            "total_domains": len(set(inv.domain for inv in self.url_to_investigation.values())),
            "total_workflows": sum(len(inv.discovered_workflows) for inv in self.url_to_investigation.values()),
            "total_elements": sum(len(inv.discovered_elements) for inv in self.url_to_investigation.values()),
            "index_sizes": {
                "intent_index": len(self.intent_to_workflows),
                "element_type_index": len(self.element_type_index),
                "natural_language_index": len(self.natural_language_index)
            }
        }
