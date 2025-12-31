"""
Response Action Types and Models for Gulltoppr
Defines all possible response actions that Heimdall can take
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from datetime import datetime, timezone


class ResponseActionType(Enum):
    """
    Enumeration of all possible response action types.
    Organized by category for better safety management.
    """
    # Security Actions (Highest Priority)
    FIREWALL_BLOCK = "firewall_block"
    FIREWALL_ALLOW = "firewall_allow"
    SECURITY_ALERT = "security_alert"
    
    # Communication Actions
    VOICE_RESPONSE = "voice_response"
    TEXT_TO_SPEECH = "text_to_speech"
    TEXT_RESPONSE = "text_response"
    
    # Processing Actions
    REAL_TIME_THINKING = "real_time_thinking"
    BACKGROUND_PROCESSING = "background_processing"
    
    # Query Actions
    WEB_SEARCH = "web_search"
    DATABASE_QUERY = "database_query"
    API_CALL = "api_call"
    
    # Control Actions
    NO_ACTION = "no_action"
    ERROR_RESPONSE = "error_response"
    REDIRECT = "redirect"
    
    @property
    def requires_elevated_permission(self) -> bool:
        """Check if action requires elevated permissions"""
        return self in {
            ResponseActionType.FIREWALL_BLOCK,
            ResponseActionType.FIREWALL_ALLOW,
            ResponseActionType.DATABASE_QUERY,
        }
    
    @property
    def is_security_action(self) -> bool:
        """Check if action is security-related"""
        return self in {
            ResponseActionType.FIREWALL_BLOCK,
            ResponseActionType.FIREWALL_ALLOW,
            ResponseActionType.SECURITY_ALERT,
        }


@dataclass
class ResponseAction:
    """
    Represents a single response action to be executed.
    Includes metadata for safety tracking and auditing.
    """
    action_type: ResponseActionType
    payload: Dict[str, Any]
    priority: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    validated: bool = False
    validation_errors: list = field(default_factory=list)
    
    def __post_init__(self):
        """Validate action on creation"""
        if not isinstance(self.action_type, ResponseActionType):
            raise TypeError("action_type must be a ResponseActionType enum")
        
        if not isinstance(self.payload, dict):
            raise TypeError("payload must be a dictionary")
        
        # Set default priority based on action type
        if self.priority == 0:
            if self.action_type.is_security_action:
                self.priority = 10  # Highest priority
            elif self.action_type == ResponseActionType.ERROR_RESPONSE:
                self.priority = 8
            else:
                self.priority = 5  # Normal priority
    
    def mark_validated(self):
        """Mark action as validated"""
        self.validated = True
    
    def add_validation_error(self, error: str):
        """Add a validation error"""
        self.validation_errors.append(error)
        self.validated = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'action_type': self.action_type.value,
            'payload': self.payload,
            'priority': self.priority,
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat(),
            'validated': self.validated,
            'validation_errors': self.validation_errors,
        }
