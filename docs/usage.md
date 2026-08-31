# Usage Guide

The `local-ai-lab` provides two primary ways to interact with the system: a Web UI and a Command Line Interface (CLI). Both interfaces communicate with the same FastAPI backend to index codebases and answer queries.

## Prerequisites

Before using either interface, you **must** ensure the backend services are running.

1. **Start the Ollama Service:**
   The AI model runs via a local Ollama instance. You must have this running in a separate terminal:
   ```bash
   ollama run qwen2.5:3b
   ```
2. **Start the Application Stack (API + UI):**
   Run the following from the root of the repository:
   ```bash
   make all
   ```
   *This starts the FastAPI backend (required for both UI and CLI) and the Vite frontend.*

---

## Web UI Workflow

The Web UI provides a clean, split-pane interface for reading AI explanations alongside the referenced code.

1. **Access the UI:**
   Open your browser to [http://localhost:5173](http://localhost:5173).

2. **Step 1: Index a Project:**
   Enter the absolute path of the codebase you want to analyze and click **Index**.
   > **Note:** If you skip this step and try to chat immediately, the system will not have any context and the AI will likely respond that it doesn't know the answer based on the current context.

3. **Step 2: Ask Questions:**
   Once indexed, use the chat box to ask questions about the code. The UI will display the AI's response and dynamically render the exact source files and line numbers it cited for its explanation.

---

## CLI Workflow

The CLI acts as a thin wrapper over the API, bringing the same RAG capabilities directly to your terminal. 

*(Assuming you have installed the project with `make install` or `pip install -e .[cli]`)*

### 1. Indexing a Project

Use the `index` command to ingest a directory:

```bash
local-ai-lab index /absolute/path/to/project
```

### 2. Chatting with the Project

Use the `chat` command to ask a question. The CLI will return the AI's response followed by a list of cited sources.

```bash
local-ai-lab chat /absolute/path/to/project "How does the router work?"
```

**Example Output:**
```text
Response:
The router works by mapping incoming HTTP requests to specific handler functions based on the URL path and HTTP method...

Sources:
  - core/router.py:45
  - core/router.py:112
```
