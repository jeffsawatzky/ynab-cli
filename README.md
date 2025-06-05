# Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)
- Your [YNAB developer access token](https://api.ynab.com/#personal-access-tokens)
- Your YNAB budget ID. You can get this from your browser URL while you have your budget open. For example, if the URL looks like `https://app.ynab.com/aaaaaaaa-1111-bbbb-2222-ddddddd` then the budget ID is `aaaaaaaa-1111-bbbb-2222-ddddddd`.

# Installation
```bash
$ git clone https://github.com/jeffsawatzky/ynab-cli.git
$ cd ynab-cli
$ uv sync
```

# Usage
> [!WARNING]
> Developer access tokens are rate limited to 200 requests per hour. Some of the commands below will provide you an opportunity to enter a new developer access token when the current one has exceeded it's limit. It also seems like there is a limit to how many developer access tokens you can create from the developer settings UI.

> [!NOTE]
> ynab-cli supports environment variables and dotenv (`.env`) files for specifying options. See the `.env-sample` file for some examples. It looks for the `.env` file in current working directory.


## Text UI
```bash
$ uv run ynab
```

This will present a text ui which will let you run the below commands.


## List Unused Payees
```bash
$ uv run ynab run payees list-unused
```
> [!NOTE]
> This will make 1 API call to get the list of payees, and then 1 API call *for each* payee to get the list of transactions. If you have more than 200 payees then you will hit your rate limit for the access token and will be asked to enter in a new one when this happens.

You can now go into YNAB and delete the ones you think you don't need.


## List Duplicate Payees
```bash
$ uv run ynab run payees list-duplicates
```
> [!NOTE]
> This will make 1 API call to get the list of payees, and then go through them all, comparing them to eachother with a fuzzy match to see which ones *might* be duplicates. You will probably get some false positives, but I prefer this over missing some.

You can now go into YNAB and combine the ones you think are duplicates.

## Normalize Payee Names
```bash
$ uv run ynab run payees normalize-names
```
> [!WARNING]
> This will update the payees in place. You can also specify `--dry-run` to see what changes would be made.

```bash
$ uv run ynab --dry-run run payees normalize-names
```

> [!NOTE]
> This will make 1 API call to get the list of payees, and then 1 API call *for each* payee to update the name. If you have more than 200 payees then you will hit your rate limit for the access token and will be asked to enter in a new one when this happens.

To normalize a payee name, it converts the name to Title Case and applies some extra tweaks for possesive names and domain names.

## List Unused Categories
```bash
$ uv run ynab run categories list-unused
```
> [!NOTE]
> This will make 1 API call to get the list of categories, and then 1 API call *for each* category to get the list of transactions. If you have more than 200 categories then you will hit your rate limit for the access token and will be asked to enter in a new one when this happens.

You can now go into YNAB and delete the ones you think you don't need.

## List All Categories
```bash
$ uv run ynab run categories list-all
```

You can use this to list the IDs for all your categories which you can then use in your transaction rules.

## Apply Transaction Rules
```bash
$ uv run ynab run transactions apply-rules rules.json
```
> [!WARNING]
> This will update the transactions in place. You can also specify `--dry-run` to see what changes would be made.

```bash
$ uv run ynab run --dry-run transactions apply-rules rules.json
```
This assumes you have a `rules.json` file with your rules to apply. It could look something like this:
```json
{
    "transaction_rules": [
        {
            "rules": [
                "payee_name == 'My Payee' and amount == -213490"
            ],
            "patch": {
                "category_id": "insert the category id you want to assign it to here"
            }
        },
        {
            "rules": [
                "payee_name == 'My Split Transaction Payee' and amount == -346500"
            ],
            "patch": {
                "category_id": null,
                "subtransactions": [
                    {
                        "category_id": "insert the first category id you want to assign it to here",
                        "amount": -51980
                    },
                    {
                        "category_id": "insert the other category id you want to assign it to here",
                        "amount": -294520
                    }
                ]
            }
        }
    ]
}
```
> [!NOTE]
> Amounts are in milliunits and can be either positive or negative depending on if they are inflow or outflow.

> [!NOTE]
> To get the category IDs you can use the `uv run ynab run categories list-all` command listed above.

The rules use the [rule-engine](https://zerosteiner.github.io/rule-engine/getting_started.html) library, so read that documentation to figure out how to write the rules. If ANY of the rules in the `rules` list match a transaction then it will be updated with the `patch` details.
The rules are supplied an instance of a `TransactionDetail`, and the `patch` needs to be an instance of a `SaveTransactionWithIdOrImportId`. Read the [YNAB API documention](https://api.ynab.com/v1) to see what properties are available to base your rules on and update.