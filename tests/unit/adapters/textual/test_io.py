from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest
from textual.app import App
from textual.widgets import Input, Label, Log, ProgressBar

from ynab_cli.adapters.textual.io import IODialogForm, TextualIO, TextualProgress
from ynab_cli.host.textual.widgets.common.dialogs import CANCELLED, SaveCancelDialogScreen


class TestTextualProgress:
    @pytest.fixture
    def mock_progress_bar(self) -> MagicMock:
        return MagicMock(spec=ProgressBar)

    @pytest.fixture
    def textual_progress_instance(self, mock_progress_bar: MagicMock) -> TextualProgress:
        return TextualProgress(mock_progress_bar)

    @pytest.mark.anyio
    async def test_update_with_total_only(
        self, textual_progress_instance: TextualProgress, mock_progress_bar: MagicMock
    ) -> None:
        await textual_progress_instance.update(total=100.0)

        mock_progress_bar.update.assert_called_once_with(total=100.0)

    @pytest.mark.anyio
    async def test_update_with_completed_only(
        self, textual_progress_instance: TextualProgress, mock_progress_bar: MagicMock
    ) -> None:
        await textual_progress_instance.update(completed=50.0)

        mock_progress_bar.update.assert_called_once_with(progress=50.0)

    @pytest.mark.anyio
    async def test_update_with_advance_only(
        self, textual_progress_instance: TextualProgress, mock_progress_bar: MagicMock
    ) -> None:
        await textual_progress_instance.update(advance=10.0)

        mock_progress_bar.update.assert_called_once_with(advance=10.0)

    @pytest.mark.anyio
    async def test_update_with_all_parameters(
        self, textual_progress_instance: TextualProgress, mock_progress_bar: MagicMock
    ) -> None:
        await textual_progress_instance.update(total=100.0, completed=75.0, advance=25.0)

        mock_progress_bar.update.assert_called_once_with(total=100.0, progress=75.0, advance=25.0)

    @pytest.mark.anyio
    async def test_update_with_no_parameters(
        self, textual_progress_instance: TextualProgress, mock_progress_bar: MagicMock
    ) -> None:
        await textual_progress_instance.update()

        mock_progress_bar.update.assert_called_once_with()

    @pytest.mark.anyio
    async def test_update_with_zero_values(
        self, textual_progress_instance: TextualProgress, mock_progress_bar: MagicMock
    ) -> None:
        await textual_progress_instance.update(total=0.0, completed=0.0, advance=0.0)

        mock_progress_bar.update.assert_called_once_with(total=0.0, progress=0.0, advance=0.0)

    @pytest.mark.anyio
    async def test_update_with_negative_values(
        self, textual_progress_instance: TextualProgress, mock_progress_bar: MagicMock
    ) -> None:
        await textual_progress_instance.update(total=-1.0, completed=-5.0, advance=-2.0)

        mock_progress_bar.update.assert_called_once_with(total=-1.0, progress=-5.0, advance=-2.0)

    def test_init_stores_progress_bar(self, mock_progress_bar: MagicMock) -> None:
        textual_progress = TextualProgress(mock_progress_bar)

        assert textual_progress._progress_bar == mock_progress_bar


class TestIODialogForm:
    @pytest.fixture
    def io_dialog_form(self) -> IODialogForm:
        return IODialogForm("Enter username:", False)

    @pytest.fixture
    def password_dialog_form(self) -> IODialogForm:
        return IODialogForm("Enter password:", True)

    def test_init_stores_prompt_and_password_flag(self) -> None:
        form = IODialogForm("Test prompt", True)

        assert form._prompt == "Test prompt"
        assert form._password is True

    def test_compose_yields_label_and_input(self, io_dialog_form: IODialogForm) -> None:
        compose_result = list(io_dialog_form.compose())

        assert len(compose_result) == 2
        assert isinstance(compose_result[0], Label)
        assert isinstance(compose_result[1], Input)
        assert compose_result[0].renderable == "Enter username:"
        assert compose_result[1].password is False

    def test_compose_with_password_input(self, password_dialog_form: IODialogForm) -> None:
        compose_result = list(password_dialog_form.compose())

        assert len(compose_result) == 2
        assert isinstance(compose_result[1], Input)
        assert compose_result[1].password is True

    @pytest.mark.anyio
    async def test_get_result_returns_stripped_input_value(
        self, monkeypatch: pytest.MonkeyPatch, io_dialog_form: IODialogForm
    ) -> None:
        mock_input = MagicMock(spec=Input)
        mock_input.value = "  test_value  "
        monkeypatch.setattr(io_dialog_form, "query_one", MagicMock(return_value=mock_input))

        result = await io_dialog_form.get_result()

        assert result == "test_value"

    @pytest.mark.anyio
    async def test_get_result_with_empty_input(
        self, monkeypatch: pytest.MonkeyPatch, io_dialog_form: IODialogForm
    ) -> None:
        mock_input = MagicMock(spec=Input)
        mock_input.value = "   "
        monkeypatch.setattr(io_dialog_form, "query_one", MagicMock(return_value=mock_input))

        result = await io_dialog_form.get_result()

        assert result == ""

    @pytest.mark.anyio
    async def test_get_result_with_no_whitespace(
        self, monkeypatch: pytest.MonkeyPatch, io_dialog_form: IODialogForm
    ) -> None:
        mock_input = MagicMock(spec=Input)
        mock_input.value = "no_whitespace"
        monkeypatch.setattr(io_dialog_form, "query_one", MagicMock(return_value=mock_input))

        result = await io_dialog_form.get_result()

        assert result == "no_whitespace"


class TestTextualIO:
    @pytest.fixture
    def mock_app(self) -> MagicMock:
        return MagicMock(spec=App)

    @pytest.fixture
    def mock_log(self) -> MagicMock:
        return MagicMock(spec=Log)

    @pytest.fixture
    def mock_progress_bar(self) -> MagicMock:
        return MagicMock(spec=ProgressBar)

    @pytest.fixture
    def textual_io_instance(self, mock_app: MagicMock, mock_log: MagicMock, mock_progress_bar: MagicMock) -> TextualIO:
        return TextualIO(mock_app, mock_log, mock_progress_bar)

    def test_init_creates_textual_progress(
        self, mock_app: MagicMock, mock_log: MagicMock, mock_progress_bar: MagicMock
    ) -> None:
        textual_io = TextualIO(mock_app, mock_log, mock_progress_bar)

        assert isinstance(textual_io.progress, TextualProgress)
        assert textual_io._app == mock_app
        assert textual_io._log == mock_log
        assert textual_io.progress._progress_bar == mock_progress_bar

    @pytest.mark.anyio
    async def test_prompt_returns_user_input(self, textual_io_instance: TextualIO, mock_app: MagicMock) -> None:
        mock_app.push_screen_wait = AsyncMock(return_value="user_input")

        result = await textual_io_instance.prompt("Enter value:")

        assert result == "user_input"
        mock_app.push_screen_wait.assert_called_once()
        args, kwargs = mock_app.push_screen_wait.call_args
        screen = args[0]
        assert isinstance(screen, SaveCancelDialogScreen)
        assert isinstance(screen._dialog._form, IODialogForm)
        assert screen._dialog._form._prompt == "Enter value:"

    @pytest.mark.anyio
    async def test_prompt_with_password(self, textual_io_instance: TextualIO, mock_app: MagicMock) -> None:
        mock_app.push_screen_wait = AsyncMock(return_value="secret")

        result = await textual_io_instance.prompt("Enter password:", password=True)

        assert result == "secret"
        mock_app.push_screen_wait.assert_called_once()
        args, kwargs = mock_app.push_screen_wait.call_args
        screen = args[0]
        assert isinstance(screen, SaveCancelDialogScreen)
        assert isinstance(screen._dialog._form, IODialogForm)
        assert screen._dialog._form._prompt == "Enter password:"

    @pytest.mark.anyio
    async def test_prompt_returns_empty_string_when_cancelled(
        self, textual_io_instance: TextualIO, mock_app: MagicMock
    ) -> None:
        mock_app.push_screen_wait = AsyncMock(return_value=CANCELLED)

        result = await textual_io_instance.prompt("Enter value:")

        assert result == ""
        mock_app.push_screen_wait.assert_called_once()
        args, kwargs = mock_app.push_screen_wait.call_args
        screen = args[0]
        assert isinstance(screen, SaveCancelDialogScreen)
        assert isinstance(screen._dialog._form, IODialogForm)
        assert screen._dialog._form._prompt == "Enter value:"

    @pytest.mark.anyio
    async def test_prompt_with_empty_prompt(self, textual_io_instance: TextualIO, mock_app: MagicMock) -> None:
        mock_app.push_screen_wait = AsyncMock(return_value="response")

        result = await textual_io_instance.prompt("")

        assert result == "response"
        mock_app.push_screen_wait.assert_called_once()
        args, kwargs = mock_app.push_screen_wait.call_args
        screen = args[0]
        assert isinstance(screen, SaveCancelDialogScreen)
        assert isinstance(screen._dialog._form, IODialogForm)
        assert screen._dialog._form._prompt == ""

    @pytest.mark.anyio
    async def test_prompt_with_special_characters(self, textual_io_instance: TextualIO, mock_app: MagicMock) -> None:
        special_prompt = "Enter value with 特殊字符 and émojis 🚀:"
        mock_app.push_screen_wait = AsyncMock(return_value="response")

        result = await textual_io_instance.prompt(special_prompt)

        assert result == "response"
        args, kwargs = mock_app.push_screen_wait.call_args
        screen = args[0]
        assert screen._dialog._form._prompt == special_prompt

    @pytest.mark.anyio
    async def test_print_writes_to_log(self, textual_io_instance: TextualIO, mock_log: MagicMock) -> None:
        await textual_io_instance.print("Hello, World!")

        mock_log.write_line.assert_called_once_with("Hello, World!")

    @pytest.mark.anyio
    async def test_print_with_empty_message(self, textual_io_instance: TextualIO, mock_log: MagicMock) -> None:
        await textual_io_instance.print("")

        mock_log.write_line.assert_called_once_with("")

    @pytest.mark.anyio
    async def test_print_with_multiline_message(self, textual_io_instance: TextualIO, mock_log: MagicMock) -> None:
        multiline_message = "Line 1\nLine 2\nLine 3"

        await textual_io_instance.print(multiline_message)

        mock_log.write_line.assert_called_once_with(multiline_message)

    @pytest.mark.anyio
    async def test_print_with_special_characters(self, textual_io_instance: TextualIO, mock_log: MagicMock) -> None:
        special_message = "Message with 特殊字符 and émojis 🚀"

        await textual_io_instance.print(special_message)

        mock_log.write_line.assert_called_once_with(special_message)

    @pytest.mark.anyio
    async def test_print_returns_none(self, textual_io_instance: TextualIO, mock_log: MagicMock) -> None:
        await textual_io_instance.print("test message")
        mock_log.write_line.assert_called_once_with("test message")

    def test_progress_property_returns_textual_progress_instance(self, textual_io_instance: TextualIO) -> None:
        assert isinstance(textual_io_instance.progress, TextualProgress)

    @pytest.mark.anyio
    async def test_prompt_exception_handling(self, textual_io_instance: TextualIO, mock_app: MagicMock) -> None:
        mock_app.push_screen_wait = AsyncMock(side_effect=Exception("Screen error"))

        with pytest.raises(Exception, match="Screen error"):
            await textual_io_instance.prompt("Enter value:")

    @pytest.mark.anyio
    async def test_prompt_with_none_result(self, textual_io_instance: TextualIO, mock_app: MagicMock) -> None:
        mock_app.push_screen_wait = AsyncMock(return_value=None)

        result = await textual_io_instance.prompt("Enter value:")

        assert result is None

    def test_init_with_typed_app(self) -> None:
        mock_app: App[Any] = MagicMock(spec=App)
        mock_log = MagicMock(spec=Log)
        mock_progress_bar = MagicMock(spec=ProgressBar)

        textual_io = TextualIO(mock_app, mock_log, mock_progress_bar)

        assert textual_io._app == mock_app
        assert textual_io._log == mock_log
        assert isinstance(textual_io.progress, TextualProgress)
