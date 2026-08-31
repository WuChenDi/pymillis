.PHONY: install lock lint fmt fmt-check typecheck test build clean

install:
	uv sync

lock:
	uv lock --upgrade

lint:
	uv run ruff check .

fmt:
	uv run ruff format .
	uv run ruff check . --fix

fmt-check:
	uv run ruff format --check .

typecheck:
	uv run mypy

test:
	uv run pytest --cov=pymillis --cov-report=term-missing --cov-report=html --durations=3

build:
	uv build

clean:
	rm -rf dist htmlcov .pytest_cache .mypy_cache .ruff_cache .coverage coverage.xml
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
