.PHONY: clean lint test

clean:
	rm -f .coverage
	rm -rf htmlcov
	find . -type f -name .DS_Store | xargs rm -rf
	find . -type d -name __pycache__ | xargs rm -rf
	find . -type d -name .mypy_cache | xargs rm -rf
	find . -type d -name .ruff_cache | xargs rm -rf
	find . -type d -name .pytest_cache | xargs rm -rf

.venv: pyproject.toml
	uv sync
	touch .venv

lint: .venv
	uv run ruff format .
	uv run ruff check .
	uv run mypy .

test: .venv
	uv run pytest --cov=src tests