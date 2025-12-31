"""
Safety Validator for Gulltoppr Response Actions
Implements comprehensive safety checks before action execution
"""

import re
import logging
from typing import List, Set, Optional, Dict, Any
from .actions import ResponseAction, ResponseActionType

logger = logging.getLogger(__name__)


class SafetyValidator:
    """
    Validates response actions for safety before execution.
    Implements multiple layers of security checks.
    """
    
    # Dangerous patterns to check in text inputs
    DANGEROUS_PATTERNS = [
        r'<script[\s\S]*?>[\s\S]*?</script>',  # XSS scripts
        r'javascript:',  # JavaScript URLs
        r'on\w+\s*=',  # Event handlers
        r'\.\./|\.\.\\',  # Path traversal
        r'DROP\s+TABLE',  # SQL injection (basic)
        r'DELETE\s+FROM',  # SQL injection (basic)
        r';\s*DROP\s+',  # SQL injection
        r'--\s*$',  # SQL comment
        r'eval\s*\(',  # Dangerous eval
        r'exec\s*\(',  # Dangerous exec
    ]
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize safety validator with optional configuration.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.max_payload_size = self.config.get('max_payload_size', 10000)
        self.rate_limit_per_minute = self.config.get('rate_limit_per_minute', 100)
        self.action_history: List[ResponseAction] = []
        self.blocked_patterns = self._compile_patterns()
        
    def _compile_patterns(self) -> List[re.Pattern]:
        """Compile regex patterns for efficiency"""
        return [re.compile(pattern, re.IGNORECASE) for pattern in self.DANGEROUS_PATTERNS]
    
    def validate(self, action: ResponseAction) -> bool:
        """
        Validate a response action for safety.
        
        Args:
            action: The response action to validate
            
        Returns:
            True if action is safe, False otherwise
        """
        # Clear previous validation errors
        action.validation_errors.clear()
        
        # Run all validation checks
        validators = [
            self._validate_action_type,
            self._validate_payload_size,
            self._validate_payload_content,
            self._validate_permissions,
            self._validate_rate_limit,
            self._validate_action_specific,
        ]
        
        for validator in validators:
            if not validator(action):
                logger.warning(f"Validation failed for {action.action_type.value}: {action.validation_errors}")
                return False
        
        # Mark as validated and log
        action.mark_validated()
        self._log_validated_action(action)
        self.action_history.append(action)
        
        return True
    
    def _validate_action_type(self, action: ResponseAction) -> bool:
        """Validate action type is valid"""
        if not isinstance(action.action_type, ResponseActionType):
            action.add_validation_error("Invalid action type")
            return False
        return True
    
    def _validate_payload_size(self, action: ResponseAction) -> bool:
        """Validate payload size is within limits"""
        payload_str = str(action.payload)
        if len(payload_str) > self.max_payload_size:
            action.add_validation_error(
                f"Payload size {len(payload_str)} exceeds maximum {self.max_payload_size}"
            )
            return False
        return True
    
    def _validate_payload_content(self, action: ResponseAction) -> bool:
        """Validate payload content for dangerous patterns"""
        payload_str = str(action.payload)
        
        for pattern in self.blocked_patterns:
            if pattern.search(payload_str):
                action.add_validation_error(
                    f"Payload contains dangerous pattern: {pattern.pattern}"
                )
                return False
        
        return True
    
    def _validate_permissions(self, action: ResponseAction) -> bool:
        """Validate user has permissions for action"""
        if action.action_type.requires_elevated_permission:
            # Check if elevated permission is granted in metadata
            has_permission = action.metadata.get('elevated_permission', False)
            if not has_permission:
                action.add_validation_error(
                    f"Action {action.action_type.value} requires elevated permission"
                )
                return False
        return True
    
    def _validate_rate_limit(self, action: ResponseAction) -> bool:
        """Validate action doesn't exceed rate limits"""
        # Simple rate limiting: count recent actions in last minute
        from datetime import datetime, timedelta, timezone
        
        one_minute_ago = datetime.now(timezone.utc) - timedelta(minutes=1)
        recent_actions = [
            a for a in self.action_history
            if a.created_at > one_minute_ago
        ]
        
        if len(recent_actions) >= self.rate_limit_per_minute:
            action.add_validation_error(
                f"Rate limit exceeded: {len(recent_actions)} actions in last minute"
            )
            return False
        
        return True
    
    def _validate_action_specific(self, action: ResponseAction) -> bool:
        """Perform action-specific validation"""
        validators = {
            ResponseActionType.FIREWALL_BLOCK: self._validate_firewall_block,
            ResponseActionType.FIREWALL_ALLOW: self._validate_firewall_allow,
            ResponseActionType.WEB_SEARCH: self._validate_web_search,
            ResponseActionType.API_CALL: self._validate_api_call,
            ResponseActionType.DATABASE_QUERY: self._validate_database_query,
        }
        
        validator = validators.get(action.action_type)
        if validator:
            return validator(action)
        
        return True
    
    def _validate_firewall_block(self, action: ResponseAction) -> bool:
        """Validate firewall block action"""
        required_fields = ['ip_address', 'reason']
        for field in required_fields:
            if field not in action.payload:
                action.add_validation_error(f"Missing required field: {field}")
                return False
        
        # Validate IP address format
        ip_address = action.payload.get('ip_address', '')
        if not self._is_valid_ip(ip_address):
            action.add_validation_error(f"Invalid IP address: {ip_address}")
            return False
        
        return True
    
    def _validate_firewall_allow(self, action: ResponseAction) -> bool:
        """Validate firewall allow action"""
        required_fields = ['ip_address', 'reason']
        for field in required_fields:
            if field not in action.payload:
                action.add_validation_error(f"Missing required field: {field}")
                return False
        
        # Validate IP address format
        ip_address = action.payload.get('ip_address', '')
        if not self._is_valid_ip(ip_address):
            action.add_validation_error(f"Invalid IP address: {ip_address}")
            return False
        
        return True
    
    def _validate_web_search(self, action: ResponseAction) -> bool:
        """Validate web search action"""
        query = action.payload.get('query', '')
        if not query or len(query) < 1:
            action.add_validation_error("Search query cannot be empty")
            return False
        
        if len(query) > 500:
            action.add_validation_error("Search query too long")
            return False
        
        return True
    
    def _validate_api_call(self, action: ResponseAction) -> bool:
        """Validate API call action"""
        required_fields = ['url', 'method']
        for field in required_fields:
            if field not in action.payload:
                action.add_validation_error(f"Missing required field: {field}")
                return False
        
        # Validate URL is safe
        url = action.payload.get('url', '')
        if not url.startswith(('http://', 'https://')):
            action.add_validation_error("URL must start with http:// or https://")
            return False
        
        # Check for localhost/private IPs to prevent SSRF
        if any(domain in url.lower() for domain in ['localhost', '127.0.0.1', '0.0.0.0', '::1']):
            action.add_validation_error("Cannot make API calls to localhost")
            return False
        
        return True
    
    def _validate_database_query(self, action: ResponseAction) -> bool:
        """Validate database query action"""
        query = action.payload.get('query', '')
        if not query:
            action.add_validation_error("Database query cannot be empty")
            return False
        
        # Only allow SELECT queries (read-only) for safety
        query_upper = query.strip().upper()
        if not query_upper.startswith('SELECT'):
            action.add_validation_error("Only SELECT queries are allowed")
            return False
        
        # Check for dangerous SQL patterns
        dangerous_sql = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'CREATE', 'EXEC', 'EXECUTE']
        for dangerous in dangerous_sql:
            if dangerous in query_upper:
                action.add_validation_error(f"Query contains dangerous keyword: {dangerous}")
                return False
        
        return True
    
    def _is_valid_ip(self, ip_address: str) -> bool:
        """Validate IP address format (simple validation)"""
        import ipaddress
        try:
            ipaddress.ip_address(ip_address)
            return True
        except ValueError:
            return False
    
    def _log_validated_action(self, action: ResponseAction):
        """Log validated action for audit trail"""
        logger.info(
            f"Action validated: {action.action_type.value} | "
            f"Priority: {action.priority} | "
            f"Timestamp: {action.created_at.isoformat()}"
        )
    
    def get_action_history(self, limit: Optional[int] = None) -> List[ResponseAction]:
        """Get action history for auditing"""
        if limit:
            return self.action_history[-limit:]
        return self.action_history.copy()
    
    def clear_history(self):
        """Clear action history"""
        self.action_history.clear()
