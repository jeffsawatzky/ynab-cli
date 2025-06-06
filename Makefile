.PHONY: lint test clean

.venv: pyproject.toml
	uv sync
	touch .venv

lint: .venv
	uv run ruff format .
	uv run ruff check .
	uv run mypy .

test: .venv lint
	uv run pytest --cov=src tests

clean:
	rm -f .coverage
	rm -rf dist
	rm -rf htmlcov
	rm -rf site
	find . -type f -name .DS_Store | xargs rm -rf
	find . -type d -name __pycache__ | xargs rm -rf
	find . -type d -name .mypy_cache | xargs rm -rf
	find . -type d -name .pytest_cache | xargs rm -rf
	find . -type d -name .ruff_cache | xargs rm -rf
	find . -type d -empty -delete

ynab-sdk:
	rm -rf ./src/ynab_cli/adapters/ynab
	mkdir -p ./src/ynab_cli/adapters/ynab
	uvx openapi-python-client generate --meta none --url https://api.ynab.com/papi/open_api_spec.yaml --output-path ./src/ynab_cli/adapters/ynab --overwrite