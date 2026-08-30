# 3. Local Code Explainer Tech Stack and Offline Architecture

Date: 2026-08-31

## Status

Accepted

## Context

Developers need a tool to explore, understand, and ask natural-language questions about codebases without sending proprietary code, intellectual property, or sensitive data to third-party cloud AI APIs. To fulfill this need, the Local Code Explainer must run fully locally, offering fast semantic code indexing, retrieval-augmented generation (RAG), and an intuitive interface while maintaining strict data privacy and zero cloud dependencies after initial setup.

## Decision

We have chosen a fully local, privacy-first tech stack for the Local Code Explainer:

1. **Embeddings (`sentence-transformers/all-MiniLM-L6-v2`)**: Runs offline locally using CPU or GPU to generate 384-dimensional vector embeddings for code chunks quickly and accurately.
2. **Vector Store (`ChromaDB`)**: Provides an embedded, zero-configuration, persistent vector database stored directly on the local filesystem (`~/.cache/local-code-explainer/chromadb`).
3. **Local LLM Inference (`Ollama` with `qwen2.5:3b`)**: Serves local open-weight language models via Ollama's local HTTP API, ensuring all prompt generation and completions happen on-device without external telemetry or API calls.
4. **Interface Layer (`FastAPI` + `React/Vite` + `Click CLI`)**:
   - **FastAPI**: Provides an asynchronous backend API with non-blocking calls (`httpx`) to Ollama and CORS configuration for frontend interaction.
   - **React / Vite**: Provides a modern, responsive single-page web UI for interactive chat sessions.
   - **Click + Rich**: Provides a terminal CLI client for indexing repositories and interactive command-line chat.

This setup ensures 100% offline capability and complete data privacy after initial model downloads.

## Consequences

- **Pros**:
  - **Zero Data Leakage / Full Privacy**: Source code, vector embeddings, queries, and generated explanations never leave the local machine.
  - **100% Offline Capability**: The application functions without an active internet connection once weights and dependencies are downloaded.
  - **No API Costs**: Eliminates recurring API subscription or per-token usage fees.
  - **Lightweight & Portable**: `all-MiniLM-L6-v2` and `qwen2.5:3b` run efficiently on standard consumer hardware.
  - **Multi-Modal Interfaces**: Users can interact via both terminal CLI and a browser-based React UI.

- **Cons**:
  - **Local Hardware Requirements**: System must meet minimum RAM and compute requirements to run Ollama models smoothly.
  - **Model Download Requirement**: Initial setup requires downloading model weights for Ollama and SentenceTransformers.
  - **Local Inference Latency**: Inference speed is dependent on local hardware (CPU/GPU) capabilities rather than scaled cloud infrastructure.
