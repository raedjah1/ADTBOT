"""
Core interfaces for the Intelligent Chat System.

These interfaces define the contracts between components,
enabling perfect modular design with loose coupling.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, AsyncIterator
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class CommandComplexity(Enum):
    """Complexity levels for chat commands."""
    SIMPLE = "simple"      # Single action: "click login button"
    MODERATE = "moderate"  # Few steps: "login to website"  
    COMPLEX = "complex"    # Multi-step: "create social media post"
    ADVANCED = "advanced"  # Full workflow: "market my product on Instagram"


class CredentialType(Enum):
    """Types of credentials required for authentication."""
    USERNAME_PASSWORD = "username_password"
    API_KEY = "api_key"
    OAUTH = "oauth"
    TWO_FACTOR = "two_factor"


class WorkflowStatus(Enum):
    """Status of workflow execution."""
    PLANNED = "planned"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class IParsedCommand:
    """Interface for parsed command data."""
    original_text: str
    intent: str
    target_platform: Optional[str]
    action_type: str
    complexity: CommandComplexity
    required_credentials: List[CredentialType]
    estimated_steps: int
    confidence: float
    parameters: Dict[str, Any]


@dataclass
class IWorkflowStep:
    """Interface for individual workflow step."""
    step_id: str
    step_type: str
    description: str
    parameters: Dict[str, Any]
    dependencies: List[str]
    timeout: Optional[int] = None
    retry_count: int = 3


@dataclass
class IWorkflowPlan:
    """Interface for complete workflow plan."""
    plan_id: str
    command: IParsedCommand
    steps: List[IWorkflowStep]
    estimated_duration: int
    success_criteria: Dict[str, Any]
    failure_conditions: List[str]


@dataclass
class IExecutionResult:
    """Interface for execution result."""
    step_id: str
    success: bool
    result_data: Dict[str, Any]
    error_message: Optional[str] = None
    execution_time: float = 0.0
    retry_count: int = 0


@dataclass
class ISessionContext:
    """Interface for session context."""
    session_id: str
    user_id: Optional[str]
    current_url: Optional[str]
    credentials: Dict[str, Any]
    workflow_state: Dict[str, Any]
    execution_history: List[IExecutionResult]
    created_at: datetime
    last_activity: datetime


# === CORE INTERFACES ===

class ICommandParser(ABC):
    """Interface for parsing natural language commands."""
    
    @abstractmethod
    async def parse(self, user_input: str) -> IParsedCommand:
        """Parse natural language input into structured command."""
        pass
    
    @abstractmethod
    async def validate_command(self, command: IParsedCommand) -> bool:
        """Validate if command is executable."""
        pass


class IWorkflowPlanner(ABC):
    """Interface for creating workflow execution plans."""
    
    @abstractmethod
    async def create_plan(self, command: IParsedCommand, context: ISessionContext) -> IWorkflowPlan:
        """Create detailed execution plan for command."""
        pass
    
    @abstractmethod
    async def optimize_plan(self, plan: IWorkflowPlan) -> IWorkflowPlan:
        """Optimize workflow plan for better performance."""
        pass


class IStepExecutor(ABC):
    """Interface for executing individual workflow steps."""
    
    @abstractmethod
    async def execute(self, step: IWorkflowStep, context: ISessionContext) -> IExecutionResult:
        """Execute a single workflow step."""
        pass
    
    @abstractmethod
    async def can_execute(self, step: IWorkflowStep) -> bool:
        """Check if this executor can handle the step."""
        pass


class IWorkflowExecutor(ABC):
    """Interface for executing complete workflows."""
    
    @abstractmethod
    async def execute_workflow(self, plan: IWorkflowPlan, context: ISessionContext) -> AsyncIterator[IExecutionResult]:
        """Execute complete workflow with real-time updates."""
        pass
    
    @abstractmethod
    async def pause_workflow(self, plan_id: str) -> bool:
        """Pause workflow execution."""
        pass
    
    @abstractmethod
    async def resume_workflow(self, plan_id: str) -> bool:
        """Resume paused workflow."""
        pass
    
    @abstractmethod
    async def cancel_workflow(self, plan_id: str) -> bool:
        """Cancel workflow execution."""
        pass


class ISessionManager(ABC):
    """Interface for managing chat sessions."""
    
    @abstractmethod
    async def create_session(self, user_id: Optional[str] = None) -> str:
        """Create new chat session."""
        pass
    
    @abstractmethod
    async def get_session(self, session_id: str) -> Optional[ISessionContext]:
        """Get session context by ID."""
        pass
    
    @abstractmethod
    async def update_session(self, session_id: str, updates: Dict[str, Any]) -> bool:
        """Update session context."""
        pass
    
    @abstractmethod
    async def end_session(self, session_id: str) -> bool:
        """End chat session."""
        pass


class ICredentialManager(ABC):
    """Interface for secure credential management."""
    
    @abstractmethod
    async def store_credentials(self, session_id: str, platform: str, credentials: Dict[str, Any]) -> bool:
        """Securely store credentials for session."""
        pass
    
    @abstractmethod
    async def get_credentials(self, session_id: str, platform: str) -> Optional[Dict[str, Any]]:
        """Retrieve stored credentials."""
        pass
    
    @abstractmethod
    async def has_credentials(self, session_id: str, platform: str, cred_type: CredentialType) -> bool:
        """Check if credentials are available."""
        pass
    
    @abstractmethod
    async def clear_credentials(self, session_id: str, platform: Optional[str] = None) -> bool:
        """Clear stored credentials."""
        pass


class IContextBuilder(ABC):
    """Interface for building execution context."""
    
    @abstractmethod
    async def build_context(self, session_id: str, command: IParsedCommand) -> ISessionContext:
        """Build execution context for command."""
        pass
    
    @abstractmethod
    async def enrich_context(self, context: ISessionContext, additional_data: Dict[str, Any]) -> ISessionContext:
        """Enrich context with additional data."""
        pass


class IEventDispatcher(ABC):
    """Interface for event-driven communication."""
    
    @abstractmethod
    async def dispatch(self, event_type: str, data: Dict[str, Any]) -> None:
        """Dispatch event to subscribers."""
        pass
    
    @abstractmethod
    def subscribe(self, event_type: str, handler) -> str:
        """Subscribe to event type."""
        pass
    
    @abstractmethod
    def unsubscribe(self, subscription_id: str) -> bool:
        """Unsubscribe from events."""
        pass


class IAIInterface(ABC):
    """Interface for AI chat interactions."""
    
    @abstractmethod
    async def chat(self, message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Send message to AI and get response."""
        pass
    
    @abstractmethod
    async def is_available(self) -> bool:
        """Check if AI service is available."""
        pass
    
    @abstractmethod
    async def switch_model(self, model_name: str) -> bool:
        """Switch to different AI model."""
        pass


class IPlatformIntegration(ABC):
    """Interface for platform-specific integrations."""
    
    @abstractmethod
    async def get_platform_url(self, platform: str) -> Optional[str]:
        """Get URL for platform."""
        pass
    
    @abstractmethod
    async def get_platform_knowledge(self, platform: str) -> Dict[str, Any]:
        """Get platform-specific knowledge."""
        pass
    
    @abstractmethod
    async def supports_platform(self, platform: str) -> bool:
        """Check if platform is supported."""
        pass


class IHealthMonitor(ABC):
    """Interface for system health monitoring."""
    
    @abstractmethod
    async def check_health(self) -> Dict[str, Any]:
        """Get system health status."""
        pass
    
    @abstractmethod
    async def get_metrics(self) -> Dict[str, Any]:
        """Get performance metrics."""
        pass


# === FACTORY INTERFACES ===

class IComponentFactory(ABC):
    """Interface for creating components."""
    
    @abstractmethod
    def create_parser(self) -> ICommandParser:
        """Create command parser instance."""
        pass
    
    @abstractmethod
    def create_planner(self) -> IWorkflowPlanner:
        """Create workflow planner instance."""
        pass
    
    @abstractmethod
    def create_executor(self) -> IWorkflowExecutor:
        """Create workflow executor instance."""
        pass
