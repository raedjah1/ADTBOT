"""
Core abstractions and interfaces for the Intelligent Chat System.

This module provides the foundational interfaces and base classes
that enable perfect modular design with loose coupling.
"""

from .interfaces import *
from .base_chat_component import BaseChatComponent
from .events import ChatEvent, ChatEventData
from .container import ComponentContainer

__all__ = [
    # Interfaces
    "ICommandParser", "IParsedCommand", "IWorkflowPlanner", "IWorkflowPlan", 
    "IStepExecutor", "IExecutionResult", "ISessionManager", "ICredentialManager",
    "IContextBuilder", "IEventDispatcher",
    
    # Base classes
    "BaseChatComponent",
    
    # Events
    "ChatEvent", "ChatEventData",
    
    # Container
    "ComponentContainer"
]
