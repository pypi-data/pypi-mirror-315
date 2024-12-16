<div style="text-align: left; margin-bottom: 20px;">
  <img src="https://kiss-ai-stack.github.io/kissaistack.svg" alt="KISS AI Stack Banner" style="max-width: auto; height: 250px">
</div>



# KISS AI Stack - Client

The KISS AI Stack Client provides an easy-to-use interface for interacting with the KISS AI Stack Server, 
supporting RESTful and WebSocket APIs to manage AI-agent session lifecycle and execute tasks.

---

## Features

- REST client for session management, query execution, and document storage.
- WebSocket client for real-time interactions with the AI agent.

---

## Getting Started

### Requirements

- Python 3.12

### Installation

1. Install the `kiss-ai-stack-client` package:
```bash
pip install kiss-ai-stack-client
```

2. Initialize the REST client:
```python
from kiss_ai_stack_client import RestEvent

client = RestEvent(hostname="your-server-hostname", secure_protocol=True)
```

---

## Usage

### 1. Authorize an Agent Session
Create or refresh an agent session:
```python
session = await client.authorize_agent(scope="temporary")
# or
session = await client.authorize_agent(client_id="your-client-id", client_secret="your-client-secret")
```

### 2. Bootstrap the Agent
Initialize the agent session for task execution:
```python
response = await client.bootstrap_agent(data="Hello, Agent!")
```

### 3. Generate an Answer
Send a query and receive the agent's response:
```python
response = await client.generate_answer(data="What is the weather today?")
```

### 4. Store Documents
Upload files with optional metadata for storage:
```python
files = ["path/to/document1.txt", "path/to/document2.pdf"]
metadata = {"category": "example"}
response = await client.store_data(files=files, metadata=metadata)
```

### 5. Destroy the Agent Session
Close the current session and clean up resources:
```python
response = await client.destroy_agent(data="Goodbye!")
```

---

## License

This project is licensed under the MIT License.
