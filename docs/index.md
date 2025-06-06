# Welcome to YNAB CLI

This is a simple cli/tui application written in python to help manage your YNAB data.

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)
- Your [YNAB developer access token](https://api.ynab.com/#personal-access-tokens)
- Your YNAB budget ID. You can get this from your browser URL while you have your budget open. For example, if the URL looks like `https://app.ynab.com/aaaaaaaa-1111-bbbb-2222-ddddddd` then the budget ID is `aaaaaaaa-1111-bbbb-2222-ddddddd`.

## Installation
```bash
$ git clone https://github.com/jeffsawatzky/ynab-cli.git
$ cd ynab-cli
$ uv sync
```

## Usage

!!! warning
    Developer access tokens are rate limited to 200 requests per hour. Some of the commands below will provide you an opportunity to enter a new developer access token when the current one has exceeded it's limit. It also seems like there is a limit to how many developer access tokens you can create from the developer settings UI.

!!! note
    YNAB CLI supports environment variables and dotenv (`.env`) files for specifying options. See the `.env-sample` file for some examples. It looks for the `.env` file in current working directory.

To run the text ui, execute the following command:

```bash
$ uv run ynab
```

Full command line usage is below.

::: mkdocs-click
    :module: ynab_cli.host.cli
    :command: cli
    :prog_name: ynab
    :style: table
    :list_subcommands: True