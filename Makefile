.PHONY: help api ui all install venv

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
UVICORN := $(VENV)/bin/uvicorn

help:
	@echo "Available commands:"
	@echo "  make api     - Run the FastAPI backend"
	@echo "  make ui      - Run the React frontend"
	@echo "  make all     - Run both API and UI in the background"
	@echo "  make install - Install Python and Node dependencies (uses venv)"

$(VENV)/bin/activate:
	uv venv $(VENV)

venv: $(VENV)/bin/activate

setup:
	@if [ ! -f .env ]; then cp .env.example .env; fi
	$(MAKE) install

install: venv
	uv pip install -e .[api,cli,rag,dev]
	cd interfaces/ui && pnpm install

api: venv
	$(UVICORN) interfaces.api.main:app --reload

ui:
	cd interfaces/ui && pnpm run dev

all: venv
	@echo "Starting API on port 8000 and UI on port 5173..."
	@bash -c "trap 'kill 0' SIGINT; $(UVICORN) interfaces.api.main:app --reload & cd interfaces/ui && pnpm run dev & wait"
