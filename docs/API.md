# API Documentation

## Base URL
```
http://localhost:3000
```

## Endpoints

### Health Check
Check if the service is running.

**GET** `/health`

**Response:**
```json
{
  "status": "healthy",
  "timestamp": 1234567890
}
```

---

### Process Message
Send a text message to the AI assistant.

**POST** `/api/message`

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "userId": "user123",
  "message": "Hello, Heimdall!"
}
```

**Response:**
```json
{
  "response": "Hello! How can I assist you today?"
}
```

**Error Responses:**

- `400 Bad Request` - Missing required fields
- `403 Forbidden` - Request blocked by firewall
- `503 Service Unavailable` - AI module not available

---

### Voice Processing
Process voice input (to be implemented).

**POST** `/api/voice`

**Headers:**
```
Content-Type: multipart/form-data
```

**Request Body:**
```
audio: [audio file]
userId: user123
```

**Response:**
```json
{
  "transcription": "Hello, Heimdall",
  "response": "Hello! How can I assist you?"
}
```

---

## WebSocket API

### Connection
Connect to the WebSocket server:

```javascript
const socket = io('http://localhost:3000');
```

### Events

#### Client → Server

**message**
Send a message to the AI assistant.

```javascript
socket.emit('message', {
  userId: 'user123',
  message: 'Hello, Heimdall!'
});
```

#### Server → Client

**response**
Receive AI response.

```javascript
socket.on('response', (data) => {
  console.log(data.content);
});
```

**error**
Receive error messages.

```javascript
socket.on('error', (error) => {
  console.error(error.message);
});
```

---

## Example Usage

### cURL

```bash
# Health check
curl http://localhost:3000/health

# Send message
curl -X POST http://localhost:3000/api/message \
  -H "Content-Type: application/json" \
  -d '{"userId": "user123", "message": "Hello!"}'
```

### JavaScript (fetch)

```javascript
// Send message
async function sendMessage(message) {
  const response = await fetch('http://localhost:3000/api/message', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      userId: 'user123',
      message: message
    })
  });
  
  const data = await response.json();
  return data.response;
}
```

### JavaScript (WebSocket)

```javascript
const io = require('socket.io-client');
const socket = io('http://localhost:3000');

socket.on('connect', () => {
  console.log('Connected to Heimdall');
  
  // Send message
  socket.emit('message', {
    userId: 'user123',
    message: 'Hello, Heimdall!'
  });
});

socket.on('response', (data) => {
  console.log('AI:', data.content);
});

socket.on('error', (error) => {
  console.error('Error:', error.message);
});
```

---

## Rate Limiting

The API implements rate limiting to prevent abuse. Default limits:
- 100 requests per minute per user/IP

If you exceed the rate limit, you'll receive a `403 Forbidden` response with:
```json
{
  "error": "Request blocked",
  "reason": "rate_limited"
}
```

---

## Security

All requests are processed through the firewall module which:
- Validates input for malicious content
- Applies rate limiting
- Checks blocklist/allowlist
- Applies custom security rules

Configure firewall settings in `config/config.yaml`.
