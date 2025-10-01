"""
Orchestration module for intelligent chat system.

Handles high-level coordination between all modular components
with perfect integration and error handling.
"""

from .chat_orchestrator import ModularChatOrchestrator

__all__ = [
    "ModularChatOrchestrator"
]