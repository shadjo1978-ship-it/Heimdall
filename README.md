# Heimdall
A.I personal assistant with real time thinking and voice also serves as a firewall

## Project Structure

### Gulltoppr Module

The Gulltoppr module handles response actions for the Heimdall AI assistant. Named after Heimdall's golden-maned steed in Norse mythology, this module manages various types of responses and actions.

**Key Features:**
- Voice and text response handling
- Real-time thinking and background processing
- Firewall and security action execution
- Query actions (web search, database, API calls)
- Priority-based action execution
- Extensible architecture for custom actions

**Documentation:** See [gulltoppr/README.md](gulltoppr/README.md) for detailed documentation and usage examples.

**Quick Start:**
```python
from gulltoppr import ResponseAction, ResponseActionType, ResponseHandler

handler = ResponseHandler()
action = ResponseAction(
    action_type=ResponseActionType.TEXT_RESPONSE,
    payload={"text": "Hello, how can I help you?"},
    priority=5
)
result = handler.execute(action)
```

For more examples, see [gulltoppr/examples.py](gulltoppr/examples.py).
