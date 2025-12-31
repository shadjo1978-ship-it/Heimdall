"""
Response action definitions for Gulltoppr module.
Defines the types of actions the AI assistant can take in response to queries.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Any, Dict, Optional


class ResponseActionType(Enum):
    """Types of response actions that Gulltoppr can execute."""
    
    # Voice responses
    VOICE_RESPONSE = "voice_response"
    TEXT_TO_SPEECH = "text_to_speech"
    
    # Text responses
    TEXT_RESPONSE = "text_response"
    FORMATTED_RESPONSE = "formatted_response"
    
    # Thinking/Processing
    REAL_TIME_THINKING = "real_time_thinking"
    BACKGROUND_PROCESSING = "background_processing"
    
    # Firewall/Security actions
    FIREWALL_BLOCK = "firewall_block"
    FIREWALL_ALLOW = "firewall_allow"
    SECURITY_ALERT = "security_alert"
    
    # Query actions
    WEB_SEARCH = "web_search"
    DATABASE_QUERY = "database_query"
    API_CALL = "api_call"
    
    # Control actions
    NO_ACTION = "no_action"
    ERROR_RESPONSE = "error_response"
    REDIRECT = "redirect"


@dataclass
class ResponseAction:
    """
    Represents a response action to be executed by Gulltoppr.
    
    Attributes:
        action_type: The type of action to execute
        payload: Data associated with the action
        priority: Priority level (0-10, higher is more urgent)
        metadata: Additional metadata for the action
    """
    action_type: ResponseActionType
    payload: Dict[str, Any]
    priority: int = 5
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Validate the response action after initialization."""
        if not isinstance(self.action_type, ResponseActionType):
            raise ValueError(f"Invalid action_type: {self.action_type}")
        
        if not 0 <= self.priority <= 10:
            raise ValueError(f"Priority must be between 0 and 10, got {self.priority}")
        
        if self.metadata is None:
            self.metadata = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the response action to a dictionary."""
        return {
            "action_type": self.action_type.value,
            "payload": self.payload,
            "priority": self.priority,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ResponseAction':
        """Create a ResponseAction from a dictionary."""
        return cls(
            action_type=ResponseActionType(data["action_type"]),
            payload=data["payload"],
            priority=data.get("priority", 5),
            metadata=data.get("metadata")
        )
