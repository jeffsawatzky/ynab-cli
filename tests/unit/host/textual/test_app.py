from unittest import mock

import pytest
from textual.widgets import Checkbox, Input

from ynab_cli.domain.settings import Settings
from ynab_cli.host.textual.app import SettingsDialogForm, YnabCliApp


def test_settings_dialog_form_initialization() -> None:
    settings = Settings()
    form = SettingsDialogForm(settings)
    assert form._settings == settings


@pytest.mark.anyio
async def test_settings_dialog_form_get_result(monkeypatch: pytest.MonkeyPatch) -> None:
    form = SettingsDialogForm(Settings())

    monkeypatch.setattr(
        form,
        "query_one",
        lambda selector, cls: {
            ("#access_token", Input): mock.Mock(spec=Input, value="newtoken "),
            ("#budget_id", Input): mock.Mock(spec=Input, value=" newbudget"),
            ("#debug", Checkbox): mock.Mock(spec=Checkbox, value=True),
            ("#dry_run", Checkbox): mock.Mock(spec=Checkbox, value=True),
        }[(selector, cls)],
    )

    result = await form.get_result()
    assert isinstance(result, Settings)
    assert result.ynab.access_token == "newtoken"
    assert result.ynab.budget_id == "newbudget"
    assert result.debug is True
    assert result.dry_run is True


def test_ynab_cli_app_initialization() -> None:
    settings = Settings()
    app = YnabCliApp(settings)
    assert app.settings == settings
    assert app.TITLE == "YNAB CLI"
    assert isinstance(app.BINDINGS, list)
