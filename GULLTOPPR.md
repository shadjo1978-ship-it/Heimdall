# Gulltoppr Response Actions

## Overview

Gulltoppr is the response action system for Heimdall AI Assistant. It implements a **safe-first** approach to executing actions, with comprehensive security validation and audit logging.

## Features

### Safety-First Design
- **Input validation** - All actions validated before execution
- **Permission system** - Elevated permissions required for sensitive actions
- **Rate limiting** - Protection against abuse
- **Audit logging** - Complete history of all actions
- **Attack prevention** - Protection against XSS, SQL injection, SSRF, and more

### Action Types

#### Security Actions (Highest Priority)
- `FIREWALL_BLOCK` - Block an IP address
- `FIREWALL_ALLOW` - Allow an IP address
- `SECURITY_ALERT` - Trigger security alert

#### Communication Actions
- `VOICE_RESPONSE` - Generate voice response
- `TEXT_TO_SPEECH` - Convert text to speech
- `TEXT_RESPONSE` - Send text response

#### Processing Actions
- `REAL_TIME_THINKING` - Real-time thought processing
- `BACKGROUND_PROCESSING` - Queue background task

#### Query Actions
- `WEB_SEARCH` - Execute web search
- `DATABASE_QUERY` - Execute database query (read-only)
- `API_CALL` - Make external API call

#### Control Actions
- `NO_ACTION` - No operation
- `ERROR_RESPONSE` - Return error
- `REDIRECT` - Redirect to target

## Usage

### Basic Example

```python
from gulltoppr import ResponseAction, ResponseActionType, ActionHandler

# Create action handler
handler = ActionHandler()

# Create a simple text response action
action = ResponseAction(
    action_type=ResponseActionType.TEXT_RESPONSE,
    payload={'text': 'Hello, how can I help you?'}
)

# Submit and execute
if handler.submit_action(action):
    result = handler.execute_next()
    print(result)
```

### Security Action Example

```python
from gulltoppr import ResponseAction, ResponseActionType, ActionHandler

handler = ActionHandler()

# Block an IP address (requires elevated permission)
action = ResponseAction(
    action_type=ResponseActionType.FIREWALL_BLOCK,
    payload={
        'ip_address': '203.0.113.42',
        'reason': 'Multiple failed login attempts detected'
    },
    metadata={'elevated_permission': True}  # Required!
)

if handler.submit_action(action):
    result = handler.execute_next()
    print(f"Blocked IP: {result['message']}")
```

### Priority-Based Execution

```python
from gulltoppr import ResponseAction, ResponseActionType, ActionHandler

handler = ActionHandler()

# Security actions automatically get highest priority
security_action = ResponseAction(
    action_type=ResponseActionType.SECURITY_ALERT,
    payload={'message': 'Potential threat detected', 'severity': 'high'},
    # priority=10 is set automatically for security actions
)

# Normal actions get lower priority
normal_action = ResponseAction(
    action_type=ResponseActionType.TEXT_RESPONSE,
    payload={'text': 'Regular message'},
    # priority=5 is set automatically
)

# Submit in any order - security actions execute first
handler.submit_action(normal_action)
handler.submit_action(security_action)

# Security action executes first despite being submitted second
results = handler.execute_all()
```

### Custom Safety Configuration

```python
from gulltoppr import SafetyValidator, ActionHandler

# Create validator with custom configuration
validator = SafetyValidator({
    'max_payload_size': 5000,  # Smaller payload limit
    'rate_limit_per_minute': 50  # Lower rate limit
})

# Use custom validator with handler
handler = ActionHandler(validator=validator)
```

### Web Search with Validation

```python
from gulltoppr import ResponseAction, ResponseActionType, ActionHandler

handler = ActionHandler()

# Safe web search
action = ResponseAction(
    action_type=ResponseActionType.WEB_SEARCH,
    payload={'query': 'python programming tutorials'}
)

if handler.submit_action(action):
    result = handler.execute_next()
    print(f"Search initiated: {result['query']}")

# This would be rejected (empty query)
invalid_action = ResponseAction(
    action_type=ResponseActionType.WEB_SEARCH,
    payload={'query': ''}
)

if not handler.submit_action(invalid_action):
    print("Invalid search query rejected")
```

### Database Query (Read-Only)

```python
from gulltoppr import ResponseAction, ResponseActionType, ActionHandler

handler = ActionHandler()

# Safe SELECT query (requires elevated permission)
action = ResponseAction(
    action_type=ResponseActionType.DATABASE_QUERY,
    payload={'query': 'SELECT * FROM users WHERE active = true'},
    metadata={'elevated_permission': True}
)

if handler.submit_action(action):
    result = handler.execute_next()
    print("Query executed")

# This would be rejected (write operation)
unsafe_action = ResponseAction(
    action_type=ResponseActionType.DATABASE_QUERY,
    payload={'query': 'DELETE FROM users'},
    metadata={'elevated_permission': True}
)

if not handler.submit_action(unsafe_action):
    print("Unsafe query rejected - only SELECT allowed")
```

### Audit Trail

```python
from gulltoppr import ActionHandler

handler = ActionHandler()

# Execute several actions...
# (actions omitted for brevity)

# Get execution history
history = handler.get_execution_history(limit=10)
for record in history:
    action_data = record['action']
    result_data = record['result']
    print(f"Action: {action_data['action_type']}")
    print(f"Success: {result_data['success']}")
    print(f"Timestamp: {action_data['created_at']}")
    print("---")

# Get validation history
validator_history = handler.validator.get_action_history(limit=10)
for action in validator_history:
    print(f"Validated: {action.action_type.value}")
```

## Security Features

### Attack Prevention

The system prevents:

1. **XSS (Cross-Site Scripting)**
   - Detects and blocks script tags and JavaScript URLs
   - Validates all text inputs

2. **SQL Injection**
   - Only allows SELECT queries
   - Blocks dangerous SQL keywords (DROP, DELETE, etc.)
   - Pattern matching for SQL injection attempts

3. **SSRF (Server-Side Request Forgery)**
   - Blocks API calls to localhost and private IPs
   - Validates URL schemes

4. **Path Traversal**
   - Detects `../` patterns in inputs

5. **Code Injection**
   - Blocks `eval()` and `exec()` patterns

### Permission System

Actions requiring elevated permissions:
- `FIREWALL_BLOCK`
- `FIREWALL_ALLOW`
- `DATABASE_QUERY`

These actions will be rejected unless `metadata['elevated_permission'] = True`.

### Rate Limiting

Default: 100 actions per minute per handler instance.
Configurable via `SafetyValidator` configuration.

### Payload Size Limits

Default: 10,000 characters.
Configurable via `SafetyValidator` configuration.

## Testing

Run the test suite:

```bash
python -m pytest tests/test_gulltoppr.py -v
```

Or with unittest:

```bash
python -m unittest tests.test_gulltoppr -v
```

## Architecture

```
gulltoppr/
├── __init__.py         # Package initialization
├── actions.py          # Action types and models
├── safety.py           # Safety validation layer
└── handler.py          # Action execution handler
```

### Key Components

1. **ResponseActionType** - Enum defining all action types
2. **ResponseAction** - Data model for actions with validation metadata
3. **SafetyValidator** - Validates actions against security rules
4. **ActionHandler** - Executes validated actions in priority order

## Best Practices

1. **Always use SafetyValidator** - Never execute actions without validation
2. **Set appropriate priorities** - Use priorities to ensure critical actions execute first
3. **Require permissions for sensitive actions** - Use elevated_permission metadata
4. **Monitor execution history** - Regularly review audit logs
5. **Configure rate limits** - Adjust based on your use case
6. **Custom executors** - Implement actual integrations (firewall, TTS, etc.)

## Extending the System

### Custom Action Executor

```python
from gulltoppr import ActionHandler, ResponseAction, ResponseActionType

def my_custom_executor(action: ResponseAction) -> dict:
    """Custom executor for text responses"""
    text = action.payload.get('text', '')
    # Your custom logic here
    return {
        'action_type': action.action_type.value,
        'success': True,
        'custom_field': 'custom_value'
    }

# Register custom executor
handler = ActionHandler()
handler.register_executor(ResponseActionType.TEXT_RESPONSE, my_custom_executor)
```

## License

Part of the Heimdall AI Assistant project.
