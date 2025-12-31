# Gulltoppr Response Actions

Gulltoppr is the response action module for the Heimdall AI Assistant, named after Heimdall's golden-maned steed in Norse mythology. Just as Gulltoppr carried Heimdall swiftly to fulfill his duties as the guardian of the gods, this module handles the execution of various response actions for the AI assistant.

## Overview

The Gulltoppr module provides a structured way to define and execute response actions for the Heimdall AI assistant. It supports various types of responses including voice, text, real-time thinking, firewall/security actions, and more.

## Components

### ResponseActionType (Enum)

Defines the types of actions that can be executed:

#### Voice Responses
- `VOICE_RESPONSE`: Generate a voice response
- `TEXT_TO_SPEECH`: Convert text to speech

#### Text Responses
- `TEXT_RESPONSE`: Generate a plain text response
- `FORMATTED_RESPONSE`: Generate a formatted text response (markdown, HTML, etc.)

#### Thinking/Processing
- `REAL_TIME_THINKING`: Initiate real-time thinking process
- `BACKGROUND_PROCESSING`: Start background processing task

#### Firewall/Security Actions
- `FIREWALL_BLOCK`: Block a connection or resource
- `FIREWALL_ALLOW`: Allow a connection or resource
- `SECURITY_ALERT`: Trigger a security alert

#### Query Actions
- `WEB_SEARCH`: Perform a web search
- `DATABASE_QUERY`: Execute a database query
- `API_CALL`: Make an API call

#### Control Actions
- `NO_ACTION`: No action required
- `ERROR_RESPONSE`: Handle an error
- `REDIRECT`: Redirect to another handler or resource

### ResponseAction (Dataclass)

Represents a single response action with:
- `action_type`: The type of action to execute (ResponseActionType)
- `payload`: Dictionary containing action-specific data
- `priority`: Priority level (0-10, where 10 is highest priority)
- `metadata`: Optional metadata for the action

### ResponseHandler (Class)

Handles the execution of response actions:
- `execute(action)`: Execute a single response action
- `execute_batch(actions)`: Execute multiple actions in priority order

## Usage Examples

### Basic Usage

```python
from gulltoppr import ResponseAction, ResponseActionType, ResponseHandler

# Create a response handler
handler = ResponseHandler()

# Create a text response action
action = ResponseAction(
    action_type=ResponseActionType.TEXT_RESPONSE,
    payload={"text": "Hello, how can I help you today?"},
    priority=5
)

# Execute the action
result = handler.execute(action)
print(result)
```

### Voice Response

```python
voice_action = ResponseAction(
    action_type=ResponseActionType.VOICE_RESPONSE,
    payload={
        "text": "The weather today is sunny with a high of 72 degrees.",
        "voice": "neural",
        "speed": 1.0
    },
    priority=7
)

result = handler.execute(voice_action)
```

### Firewall Block Action

```python
block_action = ResponseAction(
    action_type=ResponseActionType.FIREWALL_BLOCK,
    payload={
        "ip_address": "192.168.1.100",
        "reason": "Suspicious activity detected",
        "duration": "1h"
    },
    priority=10,
    metadata={"threat_level": "high"}
)

result = handler.execute(block_action)
```

### Real-Time Thinking

```python
thinking_action = ResponseAction(
    action_type=ResponseActionType.REAL_TIME_THINKING,
    payload={
        "prompt": "Analyze the current market trends",
        "stream": True,
        "model": "gpt-4"
    },
    priority=6
)

result = handler.execute(thinking_action)
```

### Batch Execution

```python
actions = [
    ResponseAction(
        action_type=ResponseActionType.WEB_SEARCH,
        payload={"query": "latest AI developments"},
        priority=3
    ),
    ResponseAction(
        action_type=ResponseActionType.TEXT_RESPONSE,
        payload={"text": "Searching for information..."},
        priority=8
    ),
    ResponseAction(
        action_type=ResponseActionType.BACKGROUND_PROCESSING,
        payload={"task": "index_new_documents"},
        priority=2
    )
]

# Actions will be executed in priority order (8, 3, 2)
results = handler.execute_batch(actions)
```

### Serialization

```python
# Convert to dictionary
action_dict = action.to_dict()

# Create from dictionary
restored_action = ResponseAction.from_dict(action_dict)
```

## Integration with Heimdall

The Gulltoppr module is designed to integrate seamlessly with the Heimdall AI Assistant. Response actions can be generated based on user queries and executed to provide appropriate responses through voice, text, or other modalities.

### Typical Flow

1. User provides input (voice or text)
2. Heimdall processes the input
3. Response actions are generated based on the query
4. Gulltoppr executes the actions in priority order
5. Results are returned to the user

## Extension

To add new response action types:

1. Add the new type to the `ResponseActionType` enum in `actions.py`
2. Add a corresponding handler method in the `ResponseHandler` class in `handlers.py`
3. Register the handler in the `__init__` method of `ResponseHandler`

Example:

```python
# In actions.py
class ResponseActionType(Enum):
    # ... existing types ...
    CUSTOM_ACTION = "custom_action"

# In handlers.py
class ResponseHandler:
    def __init__(self):
        self._handlers = {
            # ... existing handlers ...
            ResponseActionType.CUSTOM_ACTION: self._handle_custom_action,
        }
    
    def _handle_custom_action(self, action: ResponseAction) -> Dict[str, Any]:
        """Handle custom action."""
        return {
            "status": "success",
            "action_type": action.action_type.value,
            "message": "Custom action executed",
            "data": action.payload
        }
```

## Security Considerations

- Firewall actions should be validated before execution
- Priority levels should be respected to ensure critical security actions are executed first
- Action payloads should be sanitized to prevent injection attacks
- Metadata should not contain sensitive information unless encrypted

## License

Part of the Heimdall AI Assistant project.
