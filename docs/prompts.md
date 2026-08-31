# Prompt Strategy & Management

## Prompt Storage

To separate Python logic from prompt engineering, all system and user prompts are stored in the `core/prompts/` directory using **Jinja2** templates (`.jinja` files).

This allows us to cleanly handle variable injection, looping over retrieved chunks, and conditional logic without cluttering API endpoints with complex f-strings.

## Context Injection Rules

When retrieving data from ChromaDB, chunks must be injected into the prompt templates following these rules:
1. **Source Attribution**: Every chunk must be preceded by its relative file path and line numbers to prevent AI hallucination.
2. **Isolation**: Context must be clearly isolated from the user's question using markdown delimiters (e.g., `=== CONTEXT ===`).

## System Personas

The default persona for the `local-ai-lab` is the **Concise Explainer**.
All base templates must instruct the local model to:
- Be concise and direct.
- Never hallucinate file names or code that is not present in the provided context.
- Default to admitting a lack of knowledge if the retrieved context does not answer the user's question.
