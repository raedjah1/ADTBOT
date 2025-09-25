"""
Event System for Intelligent Chat System.

Provides event-driven communication between modular components
with proper async support and error handling.
"""

import asyncio
import uuid
from typing import Dict, List, Any, Callable, Union
from dataclasses import dataclass
from enum import Enum


class ChatEvent(Enum):
    """Chat system events."""
    COMMAND_RECEIVED = "command_received"
    COMMAND_PARSED = "command_parsed"
    WORKFLOW_PLANNED = "workflow_planned"
    WORKFLOW_STARTED = "workflow_started"
    WORKFLOW_COMPLETED = "workflow_completed"
    WORKFLOW_FAILED = "workflow_failed"
    SESSION_CREATED = "session_created"
    CREDENTIALS_REQUIRED = "credentials_required"


@dataclass
class ChatEventData:
    """Event data structure."""
    event_type: ChatEvent
    source: str
    session_id: str
    data: Dict[str, Any]
    timestamp: float


@dataclass
class EventSubscription:
    """Event subscription information."""
    subscription_id: str
    event_type: ChatEvent
    handler: Union[Callable, Callable[..., Any]]
    source_filter: str = None


class InMemoryEventDispatcher:
    """
    In-memory event dispatcher with async support.
    
    Features:
    - Async and sync handler support
    - Error isolation between handlers
    - Event filtering by source
    - Subscription management
    """
    
    def __init__(self):
        self.subscriptions: Dict[ChatEvent, List[EventSubscription]] = {}
        self.subscription_counter = 0
    
    async def dispatch(self, event_type: ChatEvent, source: str, session_id: str, data: Dict[str, Any]) -> None:
        """Dispatch event to all subscribers."""
        event_data = ChatEventData(
            event_type=event_type,
            source=source,
            session_id=session_id,
            data=data,
            timestamp=asyncio.get_event_loop().time()
        )
        
        # Get subscriptions for this event type
        if event_type not in self.subscriptions:
            return
        
        # Create tasks for all handlers
        tasks = []
        for subscription in self.subscriptions[event_type]:
            # Apply source filter if specified
            if subscription.source_filter and subscription.source_filter != source:
                continue
            
            # Create task for handler
            task = asyncio.create_task(self._invoke_handler(subscription, event_data))
            tasks.append(task)
        
        # Wait for all handlers to complete (don't raise on individual failures)
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _invoke_handler(self, subscription: EventSubscription, event_data: ChatEventData) -> None:
        """Invoke event handler safely."""
        try:
            if asyncio.iscoroutinefunction(subscription.handler):
                # Async handler
                await subscription.handler(event_data)
            else:
                # Sync handler
                subscription.handler(event_data)
        except Exception as e:
            # Log error but don't stop other handlers
            print(f"Error in event handler {subscription.subscription_id}: {e}")
    
    def subscribe(self, event_type: ChatEvent, handler: Union[Callable, Callable[..., Any]], 
                  source_filter: str = None) -> str:
        """Subscribe to event type."""
        subscription_id = str(uuid.uuid4())
        
        subscription = EventSubscription(
            subscription_id=subscription_id,
            event_type=event_type,
            handler=handler,
            source_filter=source_filter
        )
        
        if event_type not in self.subscriptions:
            self.subscriptions[event_type] = []
        
        self.subscriptions[event_type].append(subscription)
        return subscription_id
    
    def unsubscribe(self, subscription_id: str) -> bool:
        """Unsubscribe from events."""
        for event_subscriptions in self.subscriptions.values():
            for i, subscription in enumerate(event_subscriptions):
                if subscription.subscription_id == subscription_id:
                    del event_subscriptions[i]
                    return True
        return False
    
    def clear_subscriptions(self) -> None:
        """Clear all subscriptions."""
        self.subscriptions.clear()