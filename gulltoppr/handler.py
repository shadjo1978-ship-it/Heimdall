"""
Action Handler for Gulltoppr Response Actions
Executes validated actions in a safe and controlled manner
"""

import logging
from typing import List, Optional, Dict, Any, Callable
from queue import PriorityQueue
from .actions import ResponseAction, ResponseActionType
from .safety import SafetyValidator

logger = logging.getLogger(__name__)


class ActionHandler:
    """
    Handles execution of response actions with safety validation.
    Uses priority queue for action ordering.
    """
    
    def __init__(self, validator: Optional[SafetyValidator] = None):
        """
        Initialize action handler.
        
        Args:
            validator: Optional SafetyValidator instance. Creates default if not provided.
        """
        self.validator = validator or SafetyValidator()
        self.action_queue = PriorityQueue()
        self.executors: Dict[ResponseActionType, Callable] = {}
        self._register_default_executors()
        self.execution_history: List[Dict[str, Any]] = []
        self._counter = 0  # Counter for ensuring unique ordering in priority queue
    
    def _register_default_executors(self):
        """Register default action executors"""
        self.executors = {
            ResponseActionType.FIREWALL_BLOCK: self._execute_firewall_block,
            ResponseActionType.FIREWALL_ALLOW: self._execute_firewall_allow,
            ResponseActionType.SECURITY_ALERT: self._execute_security_alert,
            ResponseActionType.VOICE_RESPONSE: self._execute_voice_response,
            ResponseActionType.TEXT_TO_SPEECH: self._execute_text_to_speech,
            ResponseActionType.TEXT_RESPONSE: self._execute_text_response,
            ResponseActionType.REAL_TIME_THINKING: self._execute_real_time_thinking,
            ResponseActionType.BACKGROUND_PROCESSING: self._execute_background_processing,
            ResponseActionType.WEB_SEARCH: self._execute_web_search,
            ResponseActionType.DATABASE_QUERY: self._execute_database_query,
            ResponseActionType.API_CALL: self._execute_api_call,
            ResponseActionType.NO_ACTION: self._execute_no_action,
            ResponseActionType.ERROR_RESPONSE: self._execute_error_response,
            ResponseActionType.REDIRECT: self._execute_redirect,
        }
    
    def register_executor(self, action_type: ResponseActionType, executor: Callable):
        """
        Register a custom executor for an action type.
        
        Args:
            action_type: The action type to register executor for
            executor: Callable that executes the action
        """
        self.executors[action_type] = executor
        logger.info(f"Registered custom executor for {action_type.value}")
    
    def submit_action(self, action: ResponseAction) -> bool:
        """
        Submit an action for execution after validation.
        
        Args:
            action: The response action to execute
            
        Returns:
            True if action was validated and queued, False otherwise
        """
        # Validate action first (safety first!)
        if not self.validator.validate(action):
            logger.error(f"Action validation failed: {action.validation_errors}")
            return False
        
        # Add to priority queue (negative priority for correct ordering, counter for tie-breaking)
        self.action_queue.put((-action.priority, self._counter, action))
        self._counter += 1
        logger.info(f"Action queued: {action.action_type.value} with priority {action.priority}")
        return True
    
    def execute_next(self) -> Optional[Dict[str, Any]]:
        """
        Execute the next action in the priority queue.
        
        Returns:
            Execution result dictionary or None if queue is empty
        """
        if self.action_queue.empty():
            return None
        
        _, _, action = self.action_queue.get()
        return self._execute_action(action)
    
    def execute_all(self) -> List[Dict[str, Any]]:
        """
        Execute all queued actions in priority order.
        
        Returns:
            List of execution results
        """
        results = []
        while not self.action_queue.empty():
            result = self.execute_next()
            if result:
                results.append(result)
        return results
    
    def _execute_action(self, action: ResponseAction) -> Dict[str, Any]:
        """
        Execute a single action.
        
        Args:
            action: The action to execute
            
        Returns:
            Execution result dictionary
        """
        executor = self.executors.get(action.action_type)
        
        if not executor:
            error_msg = f"No executor registered for {action.action_type.value}"
            logger.error(error_msg)
            return {
                'action_type': action.action_type.value,
                'success': False,
                'error': error_msg,
            }
        
        try:
            result = executor(action)
            
            # Log execution
            execution_record = {
                'action': action.to_dict(),
                'result': result,
            }
            self.execution_history.append(execution_record)
            
            logger.info(f"Action executed: {action.action_type.value} - Success: {result.get('success', False)}")
            return result
            
        except Exception as e:
            error_msg = f"Error executing {action.action_type.value}: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {
                'action_type': action.action_type.value,
                'success': False,
                'error': error_msg,
            }
    
    # Default executor implementations (safe placeholders)
    
    def _execute_firewall_block(self, action: ResponseAction) -> Dict[str, Any]:
        """Execute firewall block action"""
        ip_address = action.payload.get('ip_address')
        reason = action.payload.get('reason')
        
        # Placeholder: In production, this would interact with actual firewall
        logger.warning(f"FIREWALL BLOCK: {ip_address} - Reason: {reason}")
        
        return {
            'action_type': action.action_type.value,
            'success': True,
            'message': f"Blocked IP {ip_address}",
            'details': action.payload,
        }
    
    def _execute_firewall_allow(self, action: ResponseAction) -> Dict[str, Any]:
        """Execute firewall allow action"""
        ip_address = action.payload.get('ip_address')
        reason = action.payload.get('reason')
        
        # Placeholder: In production, this would interact with actual firewall
        logger.info(f"FIREWALL ALLOW: {ip_address} - Reason: {reason}")
        
        return {
            'action_type': action.action_type.value,
            'success': True,
            'message': f"Allowed IP {ip_address}",
            'details': action.payload,
        }
    
    def _execute_security_alert(self, action: ResponseAction) -> Dict[str, Any]:
        """Execute security alert action"""
        alert_message = action.payload.get('message', 'Security alert triggered')
        severity = action.payload.get('severity', 'medium')
        
        logger.warning(f"SECURITY ALERT [{severity}]: {alert_message}")
        
        return {
            'action_type': action.action_type.value,
            'success': True,
            'message': alert_message,
            'severity': severity,
        }
    
    def _execute_voice_response(self, action: ResponseAction) -> Dict[str, Any]:
        """Execute voice response action"""
        text = action.payload.get('text', '')
        
        # Placeholder: Would integrate with voice synthesis
        logger.info(f"VOICE RESPONSE: {text[:100]}...")
        
        return {
            'action_type': action.action_type.value,
            'success': True,
            'message': 'Voice response initiated',
        }
    
    def _execute_text_to_speech(self, action: ResponseAction) -> Dict[str, Any]:
        """Execute text-to-speech action"""
        text = action.payload.get('text', '')
        voice = action.payload.get('voice', 'default')
        
        # Placeholder: Would integrate with TTS engine
        logger.info(f"TEXT-TO-SPEECH [{voice}]: {text[:100]}...")
        
        return {
            'action_type': action.action_type.value,
            'success': True,
            'message': 'Text-to-speech initiated',
        }
    
    def _execute_text_response(self, action: ResponseAction) -> Dict[str, Any]:
        """Execute text response action"""
        text = action.payload.get('text', '')
        
        logger.info(f"TEXT RESPONSE: {text[:100]}...")
        
        return {
            'action_type': action.action_type.value,
            'success': True,
            'message': text,
        }
    
    def _execute_real_time_thinking(self, action: ResponseAction) -> Dict[str, Any]:
        """Execute real-time thinking action"""
        thought = action.payload.get('thought', '')
        
        logger.info(f"REAL-TIME THINKING: {thought[:100]}...")
        
        return {
            'action_type': action.action_type.value,
            'success': True,
            'thought': thought,
        }
    
    def _execute_background_processing(self, action: ResponseAction) -> Dict[str, Any]:
        """Execute background processing action"""
        task = action.payload.get('task', '')
        
        # Placeholder: Would queue background task
        logger.info(f"BACKGROUND PROCESSING: {task}")
        
        return {
            'action_type': action.action_type.value,
            'success': True,
            'message': 'Background task queued',
        }
    
    def _execute_web_search(self, action: ResponseAction) -> Dict[str, Any]:
        """Execute web search action"""
        query = action.payload.get('query', '')
        
        # Placeholder: Would integrate with search API
        logger.info(f"WEB SEARCH: {query}")
        
        return {
            'action_type': action.action_type.value,
            'success': True,
            'query': query,
            'message': 'Search initiated',
        }
    
    def _execute_database_query(self, action: ResponseAction) -> Dict[str, Any]:
        """Execute database query action"""
        query = action.payload.get('query', '')
        
        # Placeholder: Would execute safe database query
        logger.info(f"DATABASE QUERY: {query[:100]}...")
        
        return {
            'action_type': action.action_type.value,
            'success': True,
            'message': 'Query executed',
        }
    
    def _execute_api_call(self, action: ResponseAction) -> Dict[str, Any]:
        """Execute API call action"""
        url = action.payload.get('url', '')
        method = action.payload.get('method', 'GET')
        
        # Placeholder: Would make actual API call
        logger.info(f"API CALL: {method} {url}")
        
        return {
            'action_type': action.action_type.value,
            'success': True,
            'message': 'API call completed',
        }
    
    def _execute_no_action(self, action: ResponseAction) -> Dict[str, Any]:
        """Execute no-action (essentially a no-op)"""
        logger.debug("NO ACTION executed")
        
        return {
            'action_type': action.action_type.value,
            'success': True,
            'message': 'No action taken',
        }
    
    def _execute_error_response(self, action: ResponseAction) -> Dict[str, Any]:
        """Execute error response action"""
        error_message = action.payload.get('error', 'An error occurred')
        
        logger.error(f"ERROR RESPONSE: {error_message}")
        
        return {
            'action_type': action.action_type.value,
            'success': True,
            'error': error_message,
        }
    
    def _execute_redirect(self, action: ResponseAction) -> Dict[str, Any]:
        """Execute redirect action"""
        target = action.payload.get('target', '')
        
        logger.info(f"REDIRECT: {target}")
        
        return {
            'action_type': action.action_type.value,
            'success': True,
            'target': target,
        }
    
    def get_execution_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get execution history for auditing"""
        if limit:
            return self.execution_history[-limit:]
        return self.execution_history.copy()
    
    def clear_queue(self):
        """Clear the action queue"""
        while not self.action_queue.empty():
            self.action_queue.get()
        logger.info("Action queue cleared")
