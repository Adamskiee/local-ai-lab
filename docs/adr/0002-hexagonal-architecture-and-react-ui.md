# 2. Hexagonal Architecture and React UI

Date: 2026-08-31

## Status

Accepted

## Context

The initial design for the Local Code Explainer used a flat directory structure (`indexer/`, `rag/`, `api/`, `cli/`) and a single-file HTML frontend served directly by FastAPI. However, as the project evolved into an "AI lab", a more structured approach was needed to cleanly separate domain logic from interface adapters, and a more robust frontend ecosystem was desired.

## Decision

We have adopted a modular architecture separating core logic from interfaces:
- `core/`: Contains all domain logic, including config, RAG (indexer, retriever), LLM interactions, and agents.
- `interfaces/`: Contains all driving adapters, including the FastAPI server (`interfaces/api`), the CLI (`interfaces/cli`), and the web UI (`interfaces/ui`).

Additionally, the Web UI has been upgraded from a static HTML file to a React application powered by Vite.

## Consequences

- **Pros**: Clearer separation of concerns. The `core` can be tested independently of FastAPI or Click. The Vite/React frontend provides a better developer experience and component reusability for future AI tools.
- **Cons**: Increased setup complexity. The frontend must now be run separately (e.g., `npm run dev`) or built and served statically. FastAPI must configure CORS to allow requests from the React dev server.
