.PHONY: lint test clean ynab-sdk release

.venv: pyproject.toml # the python virtual environment
	uv sync
	touch .venv

lint: .venv # run linters and type checkers
	uv run ruff format .
	uv run ruff check .
	uv run mypy .

test: .venv lint # run tests with coverage
	uv run pytest --cov-report term-missing:skip-covered --cov=src tests

clean: # clean up build artifacts and caches
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

ynab-sdk: # regenerate the YNAB SDK from the OpenAPI spec
	rm -rf ./src/ynab_cli/adapters/ynab
	mkdir -p ./src/ynab_cli/adapters/ynab
	uvx openapi-python-client generate --meta none --url https://api.ynab.com/papi/open_api_spec.yaml --output-path ./src/ynab_cli/adapters/ynab --overwrite

dist: clean # build the distribution package
	uv build

site: clean # serve the documentation site locally
	uv run mkdocs serve

release: clean # release the package and deploy documentation
	uv run cz bump
	git push --follow-tags
	uv run mkdocs gh-deploy
