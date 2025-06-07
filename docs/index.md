# Welcome to YNAB CLI

This is a simple cli/tui application written in python to help manage your YNAB data.

## Requirements

- [uv](https://docs.astral.sh/uv/getting-started/installation/) which allows you to easily run python applications.
- Your [YNAB developer access token](https://api.ynab.com/#personal-access-tokens).

!!! warning
    Developer access tokens are rate limited to 200 requests per hour. Some of the commands below will provide you an opportunity to enter a new developer access token when the current one has exceeded it's limit. It also seems like there is a limit to how many developer access tokens you can create from the developer settings UI.

- Your YNAB budget ID. Once you have `uv` and your `access token` you can list your budgets by running:

```sh
$ uvx ynab-cli run --access-token your_access_token budgets list-all
```

## Usage

!!! note
    YNAB CLI supports environment variables and dotenv (`.env`) files for specifying options. See the `.env-sample` file for some examples. YNAB CLI looks for the `.env` file in current working directory. If you create a `.env` file with the following information you won't need to keep entering it on the command line.

    ``` title=".env"
    YNAB_CLI_ACCESS_TOKEN=your_access_token
    YNAB_CLI_BUDGET_ID=your_budget_id
    ```

To run the text ui, execute the following command:

```sh
$ uvx ynab-cli
```

The individual CLI commands can be similarily run using `uvx`. Full command line usage is below.

::: mkdocs-click
    :module: ynab_cli.host.cli
    :command: cli
    :prog_name: ynab-cli
    :style: table
    :list_subcommands: True