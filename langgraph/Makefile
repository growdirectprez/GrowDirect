.PHONY: dev test build lint

dev:
	uv run langgraph dev

test:
	uv run pytest tests/ -v

lint:
	uv run pyright graphs/ tests/

build:
	docker build -t canary-orchestrator .
