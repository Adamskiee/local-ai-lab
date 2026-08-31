# Use uv for package management

## Status

Accepted

## Context

The repository originally used standard `pip` and `python3 -m venv` for dependency management and virtual environment creation. As we encourage developers and AI agents to heavily utilize `git worktrees` for task isolation, the primary friction point is recreating the Python virtual environment and reinstalling dependencies for every new worktree. Standard `pip` and `venv` can take a significant amount of time, delaying the start of development and automated tasks.

## Decision

We will adopt `uv` as the primary Python package manager and virtual environment creator for this project. We have updated the `Makefile` to use `uv venv` and `uv pip install`, and consolidated initialization into a new `make setup` command to streamline the bootstrapping of new worktrees.

## Consequences

* **Positive:** Creating virtual environments and installing dependencies in new worktrees is now nearly instantaneous.
* **Positive:** Reduced friction for both developers and AI agents when using isolated git worktrees.
* **Negative:** Requires contributors to install a new tool (`uv`) if they haven't already, although its adoption is increasingly standard in the Python ecosystem.
