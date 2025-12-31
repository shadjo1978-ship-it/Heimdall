# Heimdall

A.I personal assistant with real time thinking and voice also serves as a firewall

## Features

- **Gulltoppr Response Actions** - Safe-first response action system with comprehensive security validation
- Real-time thinking and processing capabilities
- Voice-based interaction support
- Integrated firewall protection

## Components

### Gulltoppr Response Action System

Gulltoppr is the response action framework for Heimdall, implementing a **safety-first** approach to executing AI assistant actions.

**Key Features:**
- 15 action types (security, communication, processing, query, and control)
- Multi-layered security validation (XSS, SQL injection, SSRF protection)
- Permission-based access control
- Rate limiting and audit logging
- Priority-based execution queue

See [GULLTOPPR.md](GULLTOPPR.md) for detailed documentation.

## Quick Start

```python
from gulltoppr import ResponseAction, ResponseActionType, ActionHandler

# Create action handler
handler = ActionHandler()

# Create and execute a simple action
action = ResponseAction(
    action_type=ResponseActionType.TEXT_RESPONSE,
    payload={'text': 'Hello from Heimdall!'}
)

if handler.submit_action(action):
    result = handler.execute_next()
    print(result)
```

## Testing

Run the test suite:

```bash
python -m unittest tests.test_gulltoppr -v
```

Run the example:

```bash
python example.py
```

## Architecture

```
Heimdall/
├── gulltoppr/              # Response action system
│   ├── __init__.py
│   ├── actions.py         # Action types and models
│   ├── safety.py          # Security validation
│   └── handler.py         # Action execution
├── tests/
│   └── test_gulltoppr.py  # Comprehensive test suite
├── example.py             # Usage examples
├── GULLTOPPR.md          # Detailed documentation
└── README.md             # This file
```

## Security

Heimdall implements multiple layers of security:

1. **Input Validation** - All inputs sanitized and validated
2. **Permission System** - Elevated permissions required for sensitive operations
3. **Attack Prevention** - Protection against XSS, SQL injection, SSRF, and more
4. **Rate Limiting** - Configurable action rate limits
5. **Audit Logging** - Complete history of all actions

## License

MIT License

