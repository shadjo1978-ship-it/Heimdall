"""
Security/firewall layer for request validation and filtering
"""

from typing import Any, Dict, Optional, List
from heimdall.layers.base import BaseLayer


class SecurityLayer(BaseLayer):
    """Layer for security checks and firewall functionality"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.blocked_patterns = self.config.get('blocked_patterns', [])
        self.rate_limit = self.config.get('rate_limit', 100)
        self.sanitize_input = self.config.get('sanitize_input', True)
    
    async def process(self, input_data: Any) -> Dict[str, Any]:
        """
        Validate and secure input data
        
        Args:
            input_data: Input to validate
            
        Returns:
            Validated and sanitized data
        """
        result = {
            'data': input_data,
            'passed': True,
            'threats': []
        }
        
        # Extract text for validation
        text = self._extract_text(input_data)
        
        # Check for blocked patterns
        threats = self._check_patterns(text)
        if threats:
            result['passed'] = False
            result['threats'] = threats
            return result
        
        # Sanitize input if enabled
        if self.sanitize_input:
            result['data'] = self._sanitize(input_data)
        
        return result
    
    def _extract_text(self, data: Any) -> str:
        """Extract text from various input formats"""
        if isinstance(data, str):
            return data
        elif isinstance(data, dict):
            return data.get('text', '')
        return str(data)
    
    def _check_patterns(self, text: str) -> List[str]:
        """Check for blocked patterns"""
        threats = []
        for pattern in self.blocked_patterns:
            if pattern.lower() in text.lower():
                threats.append(f"Blocked pattern detected: {pattern}")
        return threats
    
    def _sanitize(self, data: Any) -> Any:
        """
        Sanitize input data
        
        Note: This provides basic HTML entity encoding for display purposes.
        For production use, integrate a comprehensive sanitization library
        for protection against SQL injection, XSS, and other attack vectors.
        """
        if isinstance(data, str):
            # Basic HTML entity encoding
            sanitized = data.replace('&', '&amp;')
            sanitized = sanitized.replace('<', '&lt;')
            sanitized = sanitized.replace('>', '&gt;')
            sanitized = sanitized.replace('"', '&quot;')
            sanitized = sanitized.replace("'", '&#x27;')
            return sanitized
        elif isinstance(data, dict):
            return {k: self._sanitize(v) for k, v in data.items()}
        return data
