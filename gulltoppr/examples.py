"""
Example usage of the Gulltoppr response action module.
This file demonstrates how to use the various response actions.
"""

from gulltoppr import ResponseAction, ResponseActionType, ResponseHandler


def example_basic_usage():
    """Demonstrate basic usage of response actions."""
    print("=== Basic Usage Example ===")
    
    handler = ResponseHandler()
    
    # Simple text response
    action = ResponseAction(
        action_type=ResponseActionType.TEXT_RESPONSE,
        payload={"text": "Hello, I am Heimdall, your AI assistant."},
        priority=5
    )
    
    result = handler.execute(action)
    print(f"Result: {result}")
    print()


def example_voice_response():
    """Demonstrate voice response actions."""
    print("=== Voice Response Example ===")
    
    handler = ResponseHandler()
    
    action = ResponseAction(
        action_type=ResponseActionType.VOICE_RESPONSE,
        payload={
            "text": "The current temperature is 72 degrees Fahrenheit.",
            "voice": "neural",
            "speed": 1.0,
            "pitch": 1.0
        },
        priority=7
    )
    
    result = handler.execute(action)
    print(f"Result: {result}")
    print()


def example_firewall_actions():
    """Demonstrate firewall security actions."""
    print("=== Firewall Actions Example ===")
    
    handler = ResponseHandler()
    
    # Block action
    block_action = ResponseAction(
        action_type=ResponseActionType.FIREWALL_BLOCK,
        payload={
            "ip_address": "192.168.1.100",
            "reason": "Multiple failed login attempts",
            "duration": "1h"
        },
        priority=10,
        metadata={"threat_level": "high", "auto_block": True}
    )
    
    # Security alert
    alert_action = ResponseAction(
        action_type=ResponseActionType.SECURITY_ALERT,
        payload={
            "message": "Suspicious activity detected from IP 192.168.1.100",
            "severity": "high",
            "timestamp": "2025-12-31T04:37:44Z"
        },
        priority=9
    )
    
    results = handler.execute_batch([block_action, alert_action])
    for result in results:
        print(f"Result: {result}")
    print()


def example_thinking_actions():
    """Demonstrate real-time thinking actions."""
    print("=== Real-Time Thinking Example ===")
    
    handler = ResponseHandler()
    
    action = ResponseAction(
        action_type=ResponseActionType.REAL_TIME_THINKING,
        payload={
            "prompt": "Analyze the provided code for potential security vulnerabilities",
            "stream": True,
            "model": "gpt-4",
            "context": {"code": "def process_input(user_input): exec(user_input)"}
        },
        priority=6
    )
    
    result = handler.execute(action)
    print(f"Result: {result}")
    print()


def example_query_actions():
    """Demonstrate query actions (web search, API calls, etc.)."""
    print("=== Query Actions Example ===")
    
    handler = ResponseHandler()
    
    actions = [
        ResponseAction(
            action_type=ResponseActionType.WEB_SEARCH,
            payload={
                "query": "latest developments in artificial intelligence",
                "max_results": 10
            },
            priority=5
        ),
        ResponseAction(
            action_type=ResponseActionType.API_CALL,
            payload={
                "endpoint": "https://api.example.com/data",
                "method": "GET",
                "headers": {"Authorization": "Bearer token"}
            },
            priority=6
        ),
        ResponseAction(
            action_type=ResponseActionType.DATABASE_QUERY,
            payload={
                "query": "SELECT * FROM users WHERE active = true",
                "database": "heimdall_db"
            },
            priority=4
        )
    ]
    
    results = handler.execute_batch(actions)
    for result in results:
        print(f"Result: {result}")
    print()


def example_batch_processing():
    """Demonstrate batch processing with priority ordering."""
    print("=== Batch Processing Example ===")
    
    handler = ResponseHandler()
    
    actions = [
        ResponseAction(
            action_type=ResponseActionType.BACKGROUND_PROCESSING,
            payload={"task": "index_documents", "count": 1000},
            priority=2
        ),
        ResponseAction(
            action_type=ResponseActionType.TEXT_RESPONSE,
            payload={"text": "Processing your request..."},
            priority=8
        ),
        ResponseAction(
            action_type=ResponseActionType.REAL_TIME_THINKING,
            payload={"prompt": "Generate summary of findings"},
            priority=5
        ),
        ResponseAction(
            action_type=ResponseActionType.FORMATTED_RESPONSE,
            payload={"format": "markdown", "content": "# Results\n\nProcessing complete."},
            priority=3
        )
    ]
    
    print("Actions will be executed in priority order (8, 5, 3, 2):")
    results = handler.execute_batch(actions)
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['action_type']}: {result['message']}")
    print()


def example_serialization():
    """Demonstrate serialization and deserialization of actions."""
    print("=== Serialization Example ===")
    
    # Create an action
    original_action = ResponseAction(
        action_type=ResponseActionType.VOICE_RESPONSE,
        payload={"text": "Hello, world!", "voice": "neural"},
        priority=7,
        metadata={"language": "en-US"}
    )
    
    # Serialize to dictionary
    action_dict = original_action.to_dict()
    print(f"Serialized: {action_dict}")
    
    # Deserialize from dictionary
    restored_action = ResponseAction.from_dict(action_dict)
    print(f"Deserialized: {restored_action}")
    print()


def example_error_handling():
    """Demonstrate error handling."""
    print("=== Error Handling Example ===")
    
    handler = ResponseHandler()
    
    # Error response action
    error_action = ResponseAction(
        action_type=ResponseActionType.ERROR_RESPONSE,
        payload={
            "error_code": "ERR_001",
            "message": "Failed to process request",
            "details": "Invalid input parameter"
        },
        priority=10
    )
    
    result = handler.execute(error_action)
    print(f"Result: {result}")
    print()


def main():
    """Run all examples."""
    print("Gulltoppr Response Actions - Usage Examples\n")
    print("=" * 60)
    print()
    
    example_basic_usage()
    example_voice_response()
    example_firewall_actions()
    example_thinking_actions()
    example_query_actions()
    example_batch_processing()
    example_serialization()
    example_error_handling()
    
    print("=" * 60)
    print("\nAll examples completed!")


if __name__ == "__main__":
    main()
