# AI Agent Instructions

When working in this repository, please adhere to the following rules:

## Architecture Decision Records (ADRs)

* This repository uses Architecture Decision Records to document significant technical and design choices for reference implementations and prototypes.
* **Whenever you (the AI agent) make or propose a significant architectural, design, or technology decision** (e.g., selecting a framework, designing an API boundary, choosing a data store, etc.), you MUST create a new ADR.
* **Location:** Place new ADRs in the `docs/adr/` directory.
* **Template:** Always copy and use the `docs/adr/template.md` file.
* **Naming:** Number the files sequentially (e.g., `0002-short-description.md`).
* Be sure to fill out the `Status`, `Context`, `Decision`, and `Consequences` sections thoroughly.

## Git Commit Conventions

* **Conventional Commits:** You MUST follow the [Conventional Commits](https://www.conventionalcommits.org/) specification for all commit messages.
* Use appropriate prefixes such as `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:`, etc.
* Keep the subject line concise (under 50 characters) and use the imperative mood (e.g., "add feature" not "added feature").
