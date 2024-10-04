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
	poetry install --sync
	touch .venv

lint: .venv
	poetry run ruff format .
	poetry run ruff check .
	poetry run mypy .

test: .venv # lint
	poetry run pytest --cov=src tests