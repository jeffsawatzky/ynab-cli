# YNAB CLI

A command-line interface for interacting with YNAB (You Need A Budget).

## Usage

Full user documentation available [here](http://jeffsawatzky.github.io/ynab-cli)

## Project Structure

- `src/ynab_cli/`: Main source code
- `tests/`: Unit and integration tests
- `docs/`: Documentation (built with MkDocs)

## Getting Started

### Prerequisites
- Python 3.11+
- [uv](https://docs.astral.sh/uv/)

### Installation

Clone the repository:
```sh
$ git clone https://github.com/jeffsawatzky/ynab-cli.git
$ cd ynab-cli
```

Install dependencies with uv:
```sh
$ uv sync
```

### Running the CLI

With uv:
```sh
$ uv run ynab-cli --help
```

## Development

- Source code is in `src/ynab_cli/`.
- Use feature branches for new work.
- Follow PEP8 and use type hints where possible.

### Linting & Formatting

```sh
$ make lint
```

### Running Tests

```sh
$ make test
```
Or directly with pytest:
```sh
uv run pytest
```

## Documentation

- Docs are in `docs/` and built with MkDocs.
- To serve docs locally:
```sh
$ uv run mkdocs serve
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes. Commits should follow conventional commits. The repo is configured with [commitizen](https://commitizen-tools.github.io/commitizen/)
4. Push to your fork and open a pull request

Please include tests for new features and bug fixes.

## License

See [LICENSE.md](LICENSE.md)