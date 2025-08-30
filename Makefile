.PHONY: up, test, build 

run:
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	uv run pytest --cov=app --cov-report=term-missing

build:
	uv sync
