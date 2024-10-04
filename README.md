# Requirements

- Python 3.11+
- Poetry
- Your [YNAB developer access token](https://api.ynab.com/#personal-access-tokens)
- Your YNAB budget ID. You can get this from your browser URL while you have your budget open. For example, if the URL looks like `https://app.ynab.com/aaaaaaaa-1111-bbbb-2222-ddddddd` then the budget ID is `aaaaaaaa-1111-bbbb-2222-ddddddd`.

# Installation
```bash
> git clone https://github.com/jeffsawatzky/ynab-cli.git
> cd ynab-cli
> poetry install --sync
```

# Usage
You need to be in a Poetry shell first.
```bash
$ poetry shell
```
Then you can run the individual commands. Note that for each command you will be asked you enter in your developer access token and the budget id.

> [!WARNING]
> Developer access tokens are rate limited to 200 requests per hour. Some of the commands below will provide you an opportunity to enter a new developer access token when the current one has exceeded it's limit. It also seems like there is a limit to how many developer access tokens you can create from the developer settings UI.

> [!NOTE]
> ynab-cli supports environment variables and dotenv files for specifying options. See the `.env-sample` file for some examples.

## List Unused Payees
```bash
$ ynab payees list-unused
```
You can now go into YNAB and delete the ones you think you don't need.

## List Duplicate Payees
```bash
$ ynab payees list-duplicates
```
You can now go into YNAB and combine the ones you think are duplicates.

## Normalize Payee Names
```bash
$ ynab payees normalize-names
```
This will update the payees in place. You can also specify `--dry-run` to see what changes would be made.

## List Unused Categories
```bash
$ ynab categories list-unused
```
You can now go into YNAB and delete the ones you think you don't need.