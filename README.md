# local-ai-lab

Offline AI-assisted code explainer running on a local Ollama instance.

## Prerequisites
- Python 3.10+
- [Ollama](https://ollama.com/) installed and running locally (`ollama run qwen2.5:3b`)
- Node.js 18+ and `pnpm` (for Web UI)

## Setup & Running

1. Copy `.env.example` to `.env` and adjust if needed.
2. Install dependencies:
   `make install`
3. Start the application stack (API and UI):
   `make all`

   Alternatively, you can run components individually using `make api` or `make ui`.

## Documentation
- [System Architecture](docs/architecture.md)
- [Interfaces & API](docs/interfaces.md)
- [Prompt Strategy](docs/prompts.md)
- [Architecture Decisions](docs/adr/)
