"""
Response action handlers for Gulltoppr module.
Executes the various types of response actions.
"""

from typing import Any, Dict, List
from .actions import ResponseAction, ResponseActionType


class ResponseHandler:
    """
    Handles execution of response actions.
    This is the main interface for processing Gulltoppr response actions.
    """
    
    def __init__(self):
        """Initialize the response handler."""
        self._handlers = {
            ResponseActionType.VOICE_RESPONSE: self._handle_voice_response,
            ResponseActionType.TEXT_TO_SPEECH: self._handle_text_to_speech,
            ResponseActionType.TEXT_RESPONSE: self._handle_text_response,
            ResponseActionType.FORMATTED_RESPONSE: self._handle_formatted_response,
            ResponseActionType.REAL_TIME_THINKING: self._handle_real_time_thinking,
            ResponseActionType.BACKGROUND_PROCESSING: self._handle_background_processing,
            ResponseActionType.FIREWALL_BLOCK: self._handle_firewall_block,
            ResponseActionType.FIREWALL_ALLOW: self._handle_firewall_allow,
            ResponseActionType.SECURITY_ALERT: self._handle_security_alert,
            ResponseActionType.WEB_SEARCH: self._handle_web_search,
            ResponseActionType.DATABASE_QUERY: self._handle_database_query,
            ResponseActionType.API_CALL: self._handle_api_call,
            ResponseActionType.NO_ACTION: self._handle_no_action,
            ResponseActionType.ERROR_RESPONSE: self._handle_error_response,
            ResponseActionType.REDIRECT: self._handle_redirect,
        }
    
    def execute(self, action: ResponseAction) -> Dict[str, Any]:
        """
        Execute a response action.
        
        Args:
            action: The ResponseAction to execute
            
        Returns:
            Dictionary containing the execution result
            
        Raises:
            ValueError: If the action type is not supported
        """
        handler = self._handlers.get(action.action_type)
        if not handler:
            raise ValueError(f"No handler found for action type: {action.action_type}")
        
        return handler(action)
    
    def execute_batch(self, actions: List[ResponseAction]) -> List[Dict[str, Any]]:
        """
        Execute multiple response actions in order of priority.
        
        Args:
            actions: List of ResponseActions to execute
            
        Returns:
            List of execution results
        """
        # Sort by priority (highest first)
        sorted_actions = sorted(actions, key=lambda a: a.priority, reverse=True)
        return [self.execute(action) for action in sorted_actions]
    
    def _build_response(self, action: ResponseAction, message: str, 
                       status: str = "success") -> Dict[str, Any]:
        """
        Build a standardized response dictionary.
        
        Args:
            action: The ResponseAction being processed
            message: Human-readable message describing the result
            status: Status of the execution (default: "success")
            
        Returns:
            Standardized response dictionary
        """
        return {
            "status": status,
            "action_type": action.action_type.value,
            "message": message,
            "data": action.payload
        }
    
    # Handler methods for each action type
    
    def _handle_voice_response(self, action: ResponseAction) -> Dict[str, Any]:
        """Handle voice response action."""
        return self._build_response(action, "Voice response prepared")
    
    def _handle_text_to_speech(self, action: ResponseAction) -> Dict[str, Any]:
        """Handle text-to-speech conversion action."""
        return self._build_response(action, "Text converted to speech")
    
    def _handle_text_response(self, action: ResponseAction) -> Dict[str, Any]:
        """Handle text response action."""
        return self._build_response(action, "Text response generated")
    
    def _handle_formatted_response(self, action: ResponseAction) -> Dict[str, Any]:
        """Handle formatted response action."""
        return self._build_response(action, "Formatted response generated")
    
    def _handle_real_time_thinking(self, action: ResponseAction) -> Dict[str, Any]:
        """Handle real-time thinking action."""
        return self._build_response(action, "Real-time thinking process initiated")
    
    def _handle_background_processing(self, action: ResponseAction) -> Dict[str, Any]:
        """Handle background processing action."""
        return self._build_response(action, "Background processing started")
    
    def _handle_firewall_block(self, action: ResponseAction) -> Dict[str, Any]:
        """Handle firewall block action."""
        return self._build_response(action, "Firewall block applied")
    
    def _handle_firewall_allow(self, action: ResponseAction) -> Dict[str, Any]:
        """Handle firewall allow action."""
        return self._build_response(action, "Firewall allow rule applied")
    
    def _handle_security_alert(self, action: ResponseAction) -> Dict[str, Any]:
        """Handle security alert action."""
        return self._build_response(action, "Security alert triggered")
    
    def _handle_web_search(self, action: ResponseAction) -> Dict[str, Any]:
        """Handle web search action."""
        return self._build_response(action, "Web search initiated")
    
    def _handle_database_query(self, action: ResponseAction) -> Dict[str, Any]:
        """Handle database query action."""
        return self._build_response(action, "Database query executed")
    
    def _handle_api_call(self, action: ResponseAction) -> Dict[str, Any]:
        """Handle API call action."""
        return self._build_response(action, "API call executed")
    
    def _handle_no_action(self, action: ResponseAction) -> Dict[str, Any]:
        """Handle no action."""
        return self._build_response(action, "No action required")
    
    def _handle_error_response(self, action: ResponseAction) -> Dict[str, Any]:
        """Handle error response action."""
        # Extract error details from payload for better error messages
        error_msg = action.payload.get('message', 'Error occurred')
        if 'error_code' in action.payload:
            error_msg = f"{action.payload['error_code']}: {error_msg}"
        return self._build_response(action, error_msg, status="error")
    
    def _handle_redirect(self, action: ResponseAction) -> Dict[str, Any]:
        """Handle redirect action."""
        return self._build_response(action, "Redirect initiated")
