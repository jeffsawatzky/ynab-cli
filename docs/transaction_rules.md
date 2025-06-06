!!! note
    Amounts are in milliunits and can be either positive or negative depending on if they are inflow or outflow.

!!! note
    To get the category IDs you can use the `ynab run categories list-all` command.

The rules use the [rule-engine](https://zerosteiner.github.io/rule-engine/getting_started.html) library, so read that documentation to figure out how to write the rules. If ANY of the rules in the `rules` list match a transaction then it will be updated with the `patch` details.
The rules are supplied an instance of a `TransactionDetail`, and the `patch` needs to be an instance of a `SaveTransactionWithIdOrImportId`. Read the [YNAB API documention](https://api.ynab.com/v1) to see what properties are available to base your rules on and update.

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