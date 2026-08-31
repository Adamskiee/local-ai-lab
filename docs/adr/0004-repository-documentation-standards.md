# 0004: Repository Documentation Standards

## Status

Accepted

## Context

As the `local-ai-lab` transitions into a more mature, long-term project, it lacks centralized documentation explaining the high-level architecture, component interfaces, prompt engineering strategies, and local execution workflows. Without these, onboarding new contributors and maintaining the system becomes increasingly difficult. Furthermore, maintaining API documentation manually is error-prone when tools like FastAPI can automate it, and starting the various services (UI, API, Ollama) manually is tedious.

## Decision

We will establish a comprehensive documentation standard for the repository, consisting of the following changes:

1. **High-Level Architecture (`docs/architecture.md`)**:
   * **System Overview**: Explain the local-only nature of the lab, utilizing FastAPI, ChromaDB, and Ollama.
   * **Component Diagram**: Add a Mermaid.js diagram showing the React UI, CLI, API, RAG, ChromaDB, and Ollama.
   * **Data Flows**: Detail the Indexing flow and the Chat flow.
   * **Decision Logging**: Explicitly document our use of Architecture Decision Records (ADRs) in `docs/adr/` to track how the architecture evolves.

2. **Interfaces Documentation (`docs/interfaces.md`)**:
   * **API Documentation**: Instead of manually maintaining endpoints, this document will instruct developers on how to access the auto-generated FastAPI OpenAPI specification (Swagger UI) natively at `/docs`.
   * **Integration Concepts**: Provide a high-level overview of how the React UI and CLI clients consume the API.
   * **Error Handling Philosophy**: Specify the standardized approach for surfacing connection failures (e.g., Ollama `503` or `502`).

3. **Prompts Documentation (`docs/prompts.md`)**:
   * **Prompt Strategy & Storage**: We will migrate hardcoded f-strings in the API to dedicated template files in `core/prompts/`. We will adopt **Jinja2** (e.g., `.jinja` files) as the standard technical format to manage complex prompt structures, variable injection, and conditionals cleanly.
   * **Context Injection**: Rules for formatting retrieved RAG chunks before injection.
   * **System Personas**: Establishing default system prompts to enforce concise, accurate AI behavior.

4. **Setup Automation & README**:
   * **Automation**: We will introduce a `Makefile` (or simple bash script) to orchestrate starting the FastAPI server and React UI with a single command. (Note: Ollama is intentionally excluded to avoid lifecycle conflicts with existing system daemons).
   * **README**: Update the `README.md` to reference the automation script rather than listing verbose manual start commands for the API and UI, and explicitly list Ollama as a manual prerequisite.

## Consequences

* **Easier Onboarding**: Developers can understand the system at a glance via `architecture.md` and start it instantly via the `Makefile`.
* **Reduced Documentation Drift**: Relying on FastAPI's native OpenAPI generation ensures the API docs are never out of sync with the code.
* **Better Prompt Management**: Using Jinja2 separates prompt text from Python logic, making it easier to read and tune, though it introduces a new template dependency.
* **Traceability**: Explicitly tying the architecture to the ADR process ensures a clear history of technical decisions.
