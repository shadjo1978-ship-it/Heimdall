#!/usr/bin/env python3
"""
Example usage of Gulltoppr Response Actions
Demonstrates safe-first approach to action handling
"""

import logging
from gulltoppr import ResponseAction, ResponseActionType, ActionHandler, SafetyValidator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Main example function"""
    print("=" * 60)
    print("Gulltoppr Response Actions - Safe First Example")
    print("=" * 60)
    print()
    
    # Create action handler
    handler = ActionHandler()
    
    # Example 1: Simple text response
    print("Example 1: Simple Text Response")
    print("-" * 60)
    action1 = ResponseAction(
        action_type=ResponseActionType.TEXT_RESPONSE,
        payload={'text': 'Hello! I am Heimdall, your AI assistant.'}
    )
    if handler.submit_action(action1):
        result = handler.execute_next()
        print(f"✓ Success: {result['message']}")
    print()
    
    # Example 2: Security alert (high priority)
    print("Example 2: Security Alert (High Priority)")
    print("-" * 60)
    action2 = ResponseAction(
        action_type=ResponseActionType.SECURITY_ALERT,
        payload={
            'message': 'Unusual activity detected from IP 203.0.113.42',
            'severity': 'high'
        }
    )
    if handler.submit_action(action2):
        result = handler.execute_next()
        print(f"✓ Alert triggered: {result['message']} [Severity: {result['severity']}]")
    print()
    
    # Example 3: Firewall block (requires elevated permission)
    print("Example 3: Firewall Block (With Permission)")
    print("-" * 60)
    action3 = ResponseAction(
        action_type=ResponseActionType.FIREWALL_BLOCK,
        payload={
            'ip_address': '203.0.113.42',
            'reason': 'Multiple failed authentication attempts'
        },
        metadata={'elevated_permission': True}
    )
    if handler.submit_action(action3):
        result = handler.execute_next()
        print(f"✓ {result['message']}")
    print()
    
    # Example 4: Firewall block WITHOUT permission (should fail)
    print("Example 4: Firewall Block (Without Permission - Should Fail)")
    print("-" * 60)
    action4 = ResponseAction(
        action_type=ResponseActionType.FIREWALL_BLOCK,
        payload={
            'ip_address': '198.51.100.10',
            'reason': 'Test'
        }
        # Note: No elevated_permission in metadata
    )
    if not handler.submit_action(action4):
        print("✗ Action rejected: Missing elevated permission (as expected)")
    print()
    
    # Example 5: XSS attempt (should fail)
    print("Example 5: XSS Attack Attempt (Should Fail)")
    print("-" * 60)
    action5 = ResponseAction(
        action_type=ResponseActionType.TEXT_RESPONSE,
        payload={'text': '<script>alert("XSS")</script>'}
    )
    if not handler.submit_action(action5):
        print("✗ Action rejected: XSS pattern detected (as expected)")
    print()
    
    # Example 6: Safe web search
    print("Example 6: Safe Web Search")
    print("-" * 60)
    action6 = ResponseAction(
        action_type=ResponseActionType.WEB_SEARCH,
        payload={'query': 'best practices for AI security'}
    )
    if handler.submit_action(action6):
        result = handler.execute_next()
        print(f"✓ Search initiated: '{result['query']}'")
    print()
    
    # Example 7: Database query (read-only)
    print("Example 7: Database Query (Read-Only)")
    print("-" * 60)
    action7 = ResponseAction(
        action_type=ResponseActionType.DATABASE_QUERY,
        payload={'query': 'SELECT username, last_login FROM users WHERE active = true'},
        metadata={'elevated_permission': True}
    )
    if handler.submit_action(action7):
        result = handler.execute_next()
        print(f"✓ Query executed successfully")
    print()
    
    # Example 8: Unsafe database query (should fail)
    print("Example 8: Unsafe Database Query (Should Fail)")
    print("-" * 60)
    action8 = ResponseAction(
        action_type=ResponseActionType.DATABASE_QUERY,
        payload={'query': 'DROP TABLE users'},
        metadata={'elevated_permission': True}
    )
    if not handler.submit_action(action8):
        print("✗ Action rejected: Dangerous SQL operation detected (as expected)")
    print()
    
    # Example 9: Priority ordering
    print("Example 9: Priority-Based Execution")
    print("-" * 60)
    print("Submitting actions in this order: Low, Medium, High priority")
    
    low_priority = ResponseAction(
        action_type=ResponseActionType.TEXT_RESPONSE,
        payload={'text': 'Low priority message'},
        priority=1
    )
    medium_priority = ResponseAction(
        action_type=ResponseActionType.TEXT_RESPONSE,
        payload={'text': 'Medium priority message'},
        priority=5
    )
    high_priority = ResponseAction(
        action_type=ResponseActionType.SECURITY_ALERT,
        payload={'message': 'High priority alert', 'severity': 'critical'},
        priority=10
    )
    
    handler.submit_action(low_priority)
    handler.submit_action(medium_priority)
    handler.submit_action(high_priority)
    
    print("Executing in priority order (highest first):")
    result1 = handler.execute_next()
    print(f"  1. {result1['action_type']} (priority 10)")
    result2 = handler.execute_next()
    print(f"  2. {result2['action_type']} (priority 5)")
    result3 = handler.execute_next()
    print(f"  3. {result3['action_type']} (priority 1)")
    print()
    
    # Example 10: API call with SSRF protection
    print("Example 10: API Call (SSRF Protection)")
    print("-" * 60)
    
    # Safe API call
    safe_api = ResponseAction(
        action_type=ResponseActionType.API_CALL,
        payload={'url': 'https://api.github.com/repos/heimdall', 'method': 'GET'}
    )
    if handler.submit_action(safe_api):
        result = handler.execute_next()
        print(f"✓ Safe API call accepted: GET {safe_api.payload['url']}")
    
    # SSRF attempt
    ssrf_api = ResponseAction(
        action_type=ResponseActionType.API_CALL,
        payload={'url': 'http://localhost:8080/admin', 'method': 'GET'}
    )
    if not handler.submit_action(ssrf_api):
        print("✗ SSRF attempt rejected: localhost access blocked (as expected)")
    print()
    
    # Show execution history
    print("=" * 60)
    print("Execution History Summary")
    print("=" * 60)
    history = handler.get_execution_history()
    print(f"Total actions executed: {len(history)}")
    
    success_count = sum(1 for h in history if h['result']['success'])
    print(f"Successful actions: {success_count}")
    print()
    
    # Show validation history
    validation_history = handler.validator.get_action_history()
    print(f"Total actions validated: {len(validation_history)}")
    
    security_actions = sum(
        1 for a in validation_history 
        if a.action_type.is_security_action
    )
    print(f"Security actions validated: {security_actions}")
    print()
    
    print("=" * 60)
    print("Safe-First Response Actions: Complete!")
    print("=" * 60)


if __name__ == '__main__':
    main()
