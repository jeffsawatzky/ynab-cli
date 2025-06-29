import click
from click_default_group import DefaultGroup

from ynab_cli.domain.settings import Settings
from ynab_cli.host.click.cli import run
from ynab_cli.host.constants import CONTEXT_KEY_SETTINGS, ENV_PREFIX
from ynab_cli.host.textual.cli import tui


@click.group(cls=DefaultGroup, default="tui", default_if_no_args=True)
@click.option("--dry-run", is_flag=True, default=False, help="Run without making any changes.")
@click.option("--debug", is_flag=True, default=False, help="Enable debug mode for more verbose output.")
@click.version_option()
@click.pass_context
def cli(
    ctx: click.Context,
    dry_run: bool,
    debug: bool,
) -> None:
    """Main entrypoint."""

    ctx.ensure_object(dict)
    ctx.obj[CONTEXT_KEY_SETTINGS] = Settings(dry_run=dry_run, debug=debug)


cli.add_command(run)
cli.add_command(tui)


def main() -> None:
    cli(
        auto_envvar_prefix=ENV_PREFIX,
        obj={},  # click context object
    )


if __name__ == "__main__":
    main()  # pragma: no cover
