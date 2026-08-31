# Interfaces & API Contracts

## API Documentation

The `local-ai-lab` uses FastAPI, which automatically generates interactive OpenAPI documentation. We rely entirely on this auto-generated documentation to maintain our API endpoint contracts.

To view the endpoints (e.g., `POST /index`, `POST /chat`), request schemas, and try out the API interactively:
1. Start the API server.
2. Navigate to [http://localhost:8000/docs](http://localhost:8000/docs) in your browser.

## Integration Concepts

The backend is completely decoupled from the presentation layer.
- **React UI**: Interacts with the API via standard HTTP POST requests. It handles streaming responses if applicable and presents the retrieved RAG sources alongside the AI response.
- **CLI**: Acts as a thin wrapper over the API, executing identical HTTP calls as the UI but rendering output to standard out.

## Error Handling Philosophy

Clients must be prepared to handle backend connection failures gracefully, particularly regarding the external Ollama service:
- **503 Service Unavailable**: Raised when the Ollama service is down, unreachable, or times out. Clients should prompt the user to ensure Ollama is running (`ollama serve`).
- **502 Bad Gateway**: Raised when Ollama returns an error response indicating model failures or out-of-memory errors.
