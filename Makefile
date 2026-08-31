.PHONY: help api ui all install

help:
	@echo "Available commands:"
	@echo "  make api     - Run the FastAPI backend"
	@echo "  make ui      - Run the React frontend"
	@echo "  make all     - Run both API and UI in the background"
	@echo "  make install - Install Python and Node dependencies"

install:
	pip install -e .[api,cli,rag,dev]
	cd interfaces/ui && pnpm install

api:
	uvicorn interfaces.api.main:app --reload

ui:
	cd interfaces/ui && pnpm run dev

all:
	@echo "Starting API on port 8000 and UI on port 5173..."
	@bash -c "trap 'kill 0' SIGINT; uvicorn interfaces.api.main:app --reload & cd interfaces/ui && pnpm run dev & wait"
