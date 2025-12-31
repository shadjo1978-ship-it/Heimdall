"""
Tests for Gulltoppr Response Actions
Comprehensive test suite for safe-first response action system
"""

import unittest
from gulltoppr.actions import ResponseAction, ResponseActionType
from gulltoppr.safety import SafetyValidator
from gulltoppr.handler import ActionHandler


class TestResponseActionType(unittest.TestCase):
    """Test ResponseActionType enum"""
    
    def test_security_actions_identified(self):
        """Test that security actions are properly identified"""
        self.assertTrue(ResponseActionType.FIREWALL_BLOCK.is_security_action)
        self.assertTrue(ResponseActionType.FIREWALL_ALLOW.is_security_action)
        self.assertTrue(ResponseActionType.SECURITY_ALERT.is_security_action)
        self.assertFalse(ResponseActionType.TEXT_RESPONSE.is_security_action)
    
    def test_elevated_permissions_required(self):
        """Test that elevated permissions are required for sensitive actions"""
        self.assertTrue(ResponseActionType.FIREWALL_BLOCK.requires_elevated_permission)
        self.assertTrue(ResponseActionType.FIREWALL_ALLOW.requires_elevated_permission)
        self.assertTrue(ResponseActionType.DATABASE_QUERY.requires_elevated_permission)
        self.assertFalse(ResponseActionType.TEXT_RESPONSE.requires_elevated_permission)


class TestResponseAction(unittest.TestCase):
    """Test ResponseAction model"""
    
    def test_create_action(self):
        """Test creating a basic response action"""
        action = ResponseAction(
            action_type=ResponseActionType.TEXT_RESPONSE,
            payload={'text': 'Hello, world!'}
        )
        self.assertEqual(action.action_type, ResponseActionType.TEXT_RESPONSE)
        self.assertEqual(action.payload['text'], 'Hello, world!')
        self.assertFalse(action.validated)
    
    def test_priority_auto_assignment(self):
        """Test that priorities are automatically assigned based on action type"""
        security_action = ResponseAction(
            action_type=ResponseActionType.FIREWALL_BLOCK,
            payload={'ip_address': '192.168.1.1', 'reason': 'Test'}
        )
        self.assertEqual(security_action.priority, 10)
        
        normal_action = ResponseAction(
            action_type=ResponseActionType.TEXT_RESPONSE,
            payload={'text': 'Test'}
        )
        self.assertEqual(normal_action.priority, 5)
    
    def test_validation_marking(self):
        """Test validation marking"""
        action = ResponseAction(
            action_type=ResponseActionType.TEXT_RESPONSE,
            payload={'text': 'Test'}
        )
        self.assertFalse(action.validated)
        
        action.mark_validated()
        self.assertTrue(action.validated)
        
        action.add_validation_error("Test error")
        self.assertFalse(action.validated)
        self.assertIn("Test error", action.validation_errors)
    
    def test_to_dict(self):
        """Test conversion to dictionary"""
        action = ResponseAction(
            action_type=ResponseActionType.TEXT_RESPONSE,
            payload={'text': 'Test'}
        )
        d = action.to_dict()
        self.assertEqual(d['action_type'], 'text_response')
        self.assertEqual(d['payload']['text'], 'Test')
        self.assertIn('created_at', d)


class TestSafetyValidator(unittest.TestCase):
    """Test SafetyValidator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.validator = SafetyValidator()
    
    def test_validate_safe_action(self):
        """Test validating a safe action"""
        action = ResponseAction(
            action_type=ResponseActionType.TEXT_RESPONSE,
            payload={'text': 'Hello, world!'}
        )
        self.assertTrue(self.validator.validate(action))
        self.assertTrue(action.validated)
    
    def test_reject_xss_attack(self):
        """Test that XSS attacks are rejected"""
        action = ResponseAction(
            action_type=ResponseActionType.TEXT_RESPONSE,
            payload={'text': '<script>alert("XSS")</script>'}
        )
        self.assertFalse(self.validator.validate(action))
        self.assertFalse(action.validated)
    
    def test_reject_sql_injection(self):
        """Test that SQL injection attempts are rejected"""
        action = ResponseAction(
            action_type=ResponseActionType.DATABASE_QUERY,
            payload={'query': 'SELECT * FROM users; DROP TABLE users;'},
            metadata={'elevated_permission': True}
        )
        self.assertFalse(self.validator.validate(action))
    
    def test_reject_oversized_payload(self):
        """Test that oversized payloads are rejected"""
        large_text = 'A' * 20000
        action = ResponseAction(
            action_type=ResponseActionType.TEXT_RESPONSE,
            payload={'text': large_text}
        )
        self.assertFalse(self.validator.validate(action))
    
    def test_reject_action_without_permission(self):
        """Test that elevated actions without permission are rejected"""
        action = ResponseAction(
            action_type=ResponseActionType.FIREWALL_BLOCK,
            payload={'ip_address': '192.168.1.1', 'reason': 'Test'}
        )
        self.assertFalse(self.validator.validate(action))
    
    def test_accept_action_with_permission(self):
        """Test that elevated actions with permission are accepted"""
        action = ResponseAction(
            action_type=ResponseActionType.FIREWALL_BLOCK,
            payload={'ip_address': '192.168.1.1', 'reason': 'Test'},
            metadata={'elevated_permission': True}
        )
        self.assertTrue(self.validator.validate(action))
    
    def test_firewall_block_validation(self):
        """Test firewall block action validation"""
        # Valid action
        valid_action = ResponseAction(
            action_type=ResponseActionType.FIREWALL_BLOCK,
            payload={'ip_address': '192.168.1.1', 'reason': 'Suspicious activity'},
            metadata={'elevated_permission': True}
        )
        self.assertTrue(self.validator.validate(valid_action))
        
        # Missing IP address
        invalid_action = ResponseAction(
            action_type=ResponseActionType.FIREWALL_BLOCK,
            payload={'reason': 'Test'},
            metadata={'elevated_permission': True}
        )
        self.assertFalse(self.validator.validate(invalid_action))
        
        # Invalid IP address
        invalid_ip_action = ResponseAction(
            action_type=ResponseActionType.FIREWALL_BLOCK,
            payload={'ip_address': 'not-an-ip', 'reason': 'Test'},
            metadata={'elevated_permission': True}
        )
        self.assertFalse(self.validator.validate(invalid_ip_action))
    
    def test_web_search_validation(self):
        """Test web search action validation"""
        # Valid search
        valid_action = ResponseAction(
            action_type=ResponseActionType.WEB_SEARCH,
            payload={'query': 'python programming'}
        )
        self.assertTrue(self.validator.validate(valid_action))
        
        # Empty query
        empty_query = ResponseAction(
            action_type=ResponseActionType.WEB_SEARCH,
            payload={'query': ''}
        )
        self.assertFalse(self.validator.validate(empty_query))
        
        # Query too long
        long_query = ResponseAction(
            action_type=ResponseActionType.WEB_SEARCH,
            payload={'query': 'A' * 1000}
        )
        self.assertFalse(self.validator.validate(long_query))
    
    def test_api_call_validation(self):
        """Test API call action validation"""
        # Valid API call
        valid_action = ResponseAction(
            action_type=ResponseActionType.API_CALL,
            payload={'url': 'https://api.example.com/data', 'method': 'GET'}
        )
        self.assertTrue(self.validator.validate(valid_action))
        
        # SSRF attempt (localhost)
        ssrf_action = ResponseAction(
            action_type=ResponseActionType.API_CALL,
            payload={'url': 'http://localhost:8080/admin', 'method': 'GET'}
        )
        self.assertFalse(self.validator.validate(ssrf_action))
        
        # Invalid URL scheme
        invalid_url = ResponseAction(
            action_type=ResponseActionType.API_CALL,
            payload={'url': 'ftp://example.com', 'method': 'GET'}
        )
        self.assertFalse(self.validator.validate(invalid_url))
    
    def test_database_query_validation(self):
        """Test database query validation (read-only)"""
        # Valid SELECT query
        valid_query = ResponseAction(
            action_type=ResponseActionType.DATABASE_QUERY,
            payload={'query': 'SELECT * FROM users WHERE id = 1'},
            metadata={'elevated_permission': True}
        )
        self.assertTrue(self.validator.validate(valid_query))
        
        # Invalid: DELETE query
        delete_query = ResponseAction(
            action_type=ResponseActionType.DATABASE_QUERY,
            payload={'query': 'DELETE FROM users WHERE id = 1'},
            metadata={'elevated_permission': True}
        )
        self.assertFalse(self.validator.validate(delete_query))
        
        # Invalid: DROP query
        drop_query = ResponseAction(
            action_type=ResponseActionType.DATABASE_QUERY,
            payload={'query': 'DROP TABLE users'},
            metadata={'elevated_permission': True}
        )
        self.assertFalse(self.validator.validate(drop_query))
    
    def test_rate_limiting(self):
        """Test rate limiting"""
        validator = SafetyValidator({'rate_limit_per_minute': 3})
        
        # First 3 actions should succeed
        for i in range(3):
            action = ResponseAction(
                action_type=ResponseActionType.TEXT_RESPONSE,
                payload={'text': f'Message {i}'}
            )
            self.assertTrue(validator.validate(action))
        
        # 4th action should be rate limited
        action = ResponseAction(
            action_type=ResponseActionType.TEXT_RESPONSE,
            payload={'text': 'Message 4'}
        )
        self.assertFalse(validator.validate(action))
    
    def test_action_history(self):
        """Test action history tracking"""
        action1 = ResponseAction(
            action_type=ResponseActionType.TEXT_RESPONSE,
            payload={'text': 'Test 1'}
        )
        action2 = ResponseAction(
            action_type=ResponseActionType.TEXT_RESPONSE,
            payload={'text': 'Test 2'}
        )
        
        self.validator.validate(action1)
        self.validator.validate(action2)
        
        history = self.validator.get_action_history()
        self.assertEqual(len(history), 2)
        
        # Test with limit
        limited_history = self.validator.get_action_history(limit=1)
        self.assertEqual(len(limited_history), 1)


class TestActionHandler(unittest.TestCase):
    """Test ActionHandler"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.handler = ActionHandler()
    
    def test_submit_valid_action(self):
        """Test submitting a valid action"""
        action = ResponseAction(
            action_type=ResponseActionType.TEXT_RESPONSE,
            payload={'text': 'Hello'}
        )
        self.assertTrue(self.handler.submit_action(action))
    
    def test_reject_invalid_action(self):
        """Test that invalid actions are rejected"""
        action = ResponseAction(
            action_type=ResponseActionType.TEXT_RESPONSE,
            payload={'text': '<script>alert("XSS")</script>'}
        )
        self.assertFalse(self.handler.submit_action(action))
    
    def test_execute_action(self):
        """Test executing an action"""
        action = ResponseAction(
            action_type=ResponseActionType.TEXT_RESPONSE,
            payload={'text': 'Hello'}
        )
        self.handler.submit_action(action)
        
        result = self.handler.execute_next()
        self.assertIsNotNone(result)
        self.assertTrue(result['success'])
    
    def test_priority_ordering(self):
        """Test that actions are executed in priority order"""
        low_priority = ResponseAction(
            action_type=ResponseActionType.TEXT_RESPONSE,
            payload={'text': 'Low'},
            priority=1
        )
        high_priority = ResponseAction(
            action_type=ResponseActionType.SECURITY_ALERT,
            payload={'message': 'High'},
            priority=10
        )
        
        # Submit in reverse order
        self.handler.submit_action(low_priority)
        self.handler.submit_action(high_priority)
        
        # High priority should execute first
        result1 = self.handler.execute_next()
        self.assertEqual(result1['action_type'], 'security_alert')
        
        result2 = self.handler.execute_next()
        self.assertEqual(result2['action_type'], 'text_response')
    
    def test_execute_all(self):
        """Test executing all queued actions"""
        actions = [
            ResponseAction(
                action_type=ResponseActionType.TEXT_RESPONSE,
                payload={'text': f'Message {i}'}
            )
            for i in range(3)
        ]
        
        for action in actions:
            self.handler.submit_action(action)
        
        results = self.handler.execute_all()
        self.assertEqual(len(results), 3)
        self.assertTrue(all(r['success'] for r in results))
    
    def test_execution_history(self):
        """Test execution history tracking"""
        action = ResponseAction(
            action_type=ResponseActionType.TEXT_RESPONSE,
            payload={'text': 'Test'}
        )
        self.handler.submit_action(action)
        self.handler.execute_next()
        
        history = self.handler.get_execution_history()
        self.assertEqual(len(history), 1)
    
    def test_custom_executor(self):
        """Test registering a custom executor"""
        custom_result = {'custom': True}
        
        def custom_executor(action):
            return custom_result
        
        self.handler.register_executor(ResponseActionType.TEXT_RESPONSE, custom_executor)
        
        action = ResponseAction(
            action_type=ResponseActionType.TEXT_RESPONSE,
            payload={'text': 'Test'}
        )
        self.handler.submit_action(action)
        result = self.handler.execute_next()
        
        self.assertEqual(result, custom_result)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system"""
    
    def test_safe_firewall_workflow(self):
        """Test a complete safe firewall workflow"""
        handler = ActionHandler()
        
        # Create a firewall block action with proper permissions
        action = ResponseAction(
            action_type=ResponseActionType.FIREWALL_BLOCK,
            payload={
                'ip_address': '203.0.113.42',
                'reason': 'Multiple failed login attempts'
            },
            metadata={'elevated_permission': True}
        )
        
        # Submit and execute
        self.assertTrue(handler.submit_action(action))
        result = handler.execute_next()
        
        self.assertTrue(result['success'])
        self.assertIn('203.0.113.42', result['message'])
    
    def test_unsafe_firewall_rejected(self):
        """Test that unsafe firewall actions are rejected"""
        handler = ActionHandler()
        
        # Create a firewall block action without permissions
        action = ResponseAction(
            action_type=ResponseActionType.FIREWALL_BLOCK,
            payload={
                'ip_address': '203.0.113.42',
                'reason': 'Test'
            }
        )
        
        # Should be rejected
        self.assertFalse(handler.submit_action(action))
    
    def test_multiple_action_types(self):
        """Test handling multiple different action types"""
        handler = ActionHandler()
        
        actions = [
            ResponseAction(
                action_type=ResponseActionType.TEXT_RESPONSE,
                payload={'text': 'Processing your request...'}
            ),
            ResponseAction(
                action_type=ResponseActionType.WEB_SEARCH,
                payload={'query': 'python programming'}
            ),
            ResponseAction(
                action_type=ResponseActionType.TEXT_RESPONSE,
                payload={'text': 'Search completed'}
            ),
        ]
        
        for action in actions:
            self.assertTrue(handler.submit_action(action))
        
        results = handler.execute_all()
        self.assertEqual(len(results), 3)
        self.assertTrue(all(r['success'] for r in results))


if __name__ == '__main__':
    unittest.main()
