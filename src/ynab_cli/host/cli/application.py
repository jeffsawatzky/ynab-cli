import click

from ynab_cli.host.cli.commands import categories, payees, transactions
from ynab_cli.host.cli.constants import CONTEXT_KEY_ACCESS_TOKEN, CONTEXT_KEY_BUDGET_ID, CONTEXT_KEY_DRY_RUN, ENV_PREFIX


@click.group()
@click.option("--access-token", prompt=True, hide_input=True, show_envvar=True)
@click.option("--budget-id", prompt=True, show_envvar=True)
@click.option("--dry-run", is_flag=True, default=False)
@click.pass_context
def cli(ctx: click.Context, access_token: str, budget_id: str, dry_run: bool) -> None:
    ctx.ensure_object(dict)

    ctx.obj[CONTEXT_KEY_ACCESS_TOKEN] = access_token
    ctx.obj[CONTEXT_KEY_BUDGET_ID] = budget_id
    ctx.obj[CONTEXT_KEY_DRY_RUN] = dry_run


cli.add_command(payees.payees)
cli.add_command(categories.categories)
cli.add_command(transactions.transactions)


def main() -> None:
    cli(
        auto_envvar_prefix=ENV_PREFIX,
        obj={},  # click context object
    )


if __name__ == "__main__":
    main()
