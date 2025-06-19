from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from typing_extensions import override

from ynab_cli.domain.ports.io import IO, Progress, StdIO, StdProgress


class TestProgress:
    """Test the Progress protocol interface."""

    @pytest.mark.anyio
    async def test_progress_update_signature(self) -> None:
        """Test that Progress.update has the correct signature."""

        # This test ensures the protocol signature is correct
        class MockProgress(Progress):
            @override
            async def update(
                self, *, total: float | None = None, completed: float | None = None, advance: float | None = None
            ) -> None:
                pass

        progress = MockProgress()
        await progress.update()
        await progress.update(total=100.0)
        await progress.update(completed=50.0)
        await progress.update(advance=10.0)
        await progress.update(total=100.0, completed=50.0, advance=10.0)


class TestIO:
    """Test the IO protocol interface."""

    def test_io_has_progress_attribute(self) -> None:
        """Test that IO protocol has progress attribute."""

        class MockIO(IO):
            def __init__(self) -> None:
                self.progress = MagicMock(spec=Progress)

            @override
            async def prompt(self, prompt: str, password: bool = False) -> str:
                return "test"

            @override
            async def print(self, message: str) -> None:
                pass

        io = MockIO()
        assert hasattr(io, "progress")

    @pytest.mark.anyio
    async def test_io_prompt_signature(self) -> None:
        """Test that IO.prompt has the correct signature."""

        class MockIO(IO):
            def __init__(self) -> None:
                self.progress = MagicMock(spec=Progress)

            @override
            async def prompt(self, prompt: str, password: bool = False) -> str:
                return f"mock_response_to_{prompt}"

            @override
            async def print(self, message: str) -> None:
                pass

        io = MockIO()
        result1 = await io.prompt("test")
        result2 = await io.prompt("test", password=True)
        result3 = await io.prompt("test", password=False)

        assert result1 == "mock_response_to_test"
        assert result2 == "mock_response_to_test"
        assert result3 == "mock_response_to_test"

    @pytest.mark.anyio
    async def test_io_print_signature(self) -> None:
        """Test that IO.print has the correct signature."""

        class MockIO(IO):
            def __init__(self) -> None:
                self.progress = MagicMock(spec=Progress)

            @override
            async def prompt(self, prompt: str, password: bool = False) -> str:
                return "test"

            @override
            async def print(self, message: str) -> None:
                pass

        io = MockIO()
        await io.print("test message")


class TestStdProgress:
    """Test the StdProgress implementation."""

    @pytest.fixture
    def mock_io(self) -> MagicMock:
        """Create a mock StdIO instance."""
        mock = MagicMock(spec=StdIO)
        mock.print = AsyncMock(return_value=None)
        return mock

    @pytest.fixture
    def std_progress(self, mock_io: MagicMock) -> StdProgress:
        """Create a StdProgress instance with mock IO."""
        return StdProgress(mock_io)

    def test_init_sets_io_reference(self, mock_io: MagicMock) -> None:
        """Test that StdProgress stores the IO reference correctly."""
        progress = StdProgress(mock_io)

        assert progress._io == mock_io
        assert progress._total is None
        assert progress._completed is None

    def test_init_initializes_state(self, mock_io: MagicMock) -> None:
        """Test that StdProgress initializes with correct default state."""
        progress = StdProgress(mock_io)

        assert progress._total is None
        assert progress._completed is None

    @pytest.mark.anyio
    async def test_update_with_total_only(self, std_progress: StdProgress, mock_io: MagicMock) -> None:
        """Test update with only total parameter."""
        await std_progress.update(total=100.0)

        assert std_progress._total == 100.0
        assert std_progress._completed is None
        mock_io.print.assert_called_once_with("Progress: 100.0 to go")

    @pytest.mark.anyio
    async def test_update_with_completed_only(self, std_progress: StdProgress, mock_io: MagicMock) -> None:
        """Test update with only completed parameter."""
        await std_progress.update(completed=50.0)

        assert std_progress._total is None
        assert std_progress._completed == 50.0
        mock_io.print.assert_called_once_with("Progress: 50.0 completed")

    @pytest.mark.anyio
    async def test_update_with_advance_only(self, std_progress: StdProgress, mock_io: MagicMock) -> None:
        """Test update with only advance parameter."""
        await std_progress.update(advance=25.0)

        assert std_progress._total is None
        assert std_progress._completed == 25.0
        mock_io.print.assert_called_once_with("Progress: 25.0 completed")

    @pytest.mark.anyio
    async def test_update_with_advance_adds_to_existing_completed(
        self, std_progress: StdProgress, mock_io: MagicMock
    ) -> None:
        """Test that advance adds to existing completed value."""
        std_progress._completed = 10.0

        await std_progress.update(advance=15.0)

        assert std_progress._completed == 25.0
        mock_io.print.assert_called_once_with("Progress: 25.0 completed")

    @pytest.mark.anyio
    async def test_update_with_total_and_completed(self, std_progress: StdProgress, mock_io: MagicMock) -> None:
        """Test update with both total and completed parameters."""
        await std_progress.update(total=100.0, completed=75.0)

        assert std_progress._total == 100.0
        assert std_progress._completed == 75.0
        mock_io.print.assert_called_once_with("Progress: 75.0/100.0")

    @pytest.mark.anyio
    async def test_update_with_all_parameters(self, std_progress: StdProgress, mock_io: MagicMock) -> None:
        """Test update with all parameters."""
        await std_progress.update(total=100.0, completed=50.0, advance=25.0)

        assert std_progress._total == 100.0
        assert std_progress._completed == 75.0  # 50.0 + 25.0
        mock_io.print.assert_called_once_with("Progress: 75.0/100.0")

    @pytest.mark.anyio
    async def test_update_with_no_parameters(self, std_progress: StdProgress, mock_io: MagicMock) -> None:
        """Test update with no parameters."""
        await std_progress.update()

        assert std_progress._total is None
        assert std_progress._completed is None
        mock_io.print.assert_called_once_with("No progress information available")

    @pytest.mark.anyio
    async def test_update_priority_total_and_completed_over_others(
        self, std_progress: StdProgress, mock_io: MagicMock
    ) -> None:
        """Test that when both total and completed are set, they take priority in display."""
        std_progress._total = 50.0
        std_progress._completed = 25.0

        await std_progress.update()

        mock_io.print.assert_called_once_with("Progress: 25.0/50.0")

    @pytest.mark.anyio
    async def test_update_overwrites_existing_total(self, std_progress: StdProgress, mock_io: MagicMock) -> None:
        """Test that setting total overwrites existing value."""
        std_progress._total = 50.0

        await std_progress.update(total=100.0)

        assert std_progress._total == 100.0
        mock_io.print.assert_called_once_with("Progress: 100.0 to go")

    @pytest.mark.anyio
    async def test_update_overwrites_existing_completed(self, std_progress: StdProgress, mock_io: MagicMock) -> None:
        """Test that setting completed overwrites existing value."""
        std_progress._completed = 25.0

        await std_progress.update(completed=50.0)

        assert std_progress._completed == 50.0
        mock_io.print.assert_called_once_with("Progress: 50.0 completed")

    @pytest.mark.anyio
    async def test_update_with_zero_values(self, std_progress: StdProgress, mock_io: MagicMock) -> None:
        """Test update with zero values."""
        await std_progress.update(total=0.0, completed=0.0, advance=0.0)

        assert std_progress._total == 0.0
        assert std_progress._completed == 0.0
        mock_io.print.assert_called_once_with("Progress: 0.0/0.0")

    @pytest.mark.anyio
    async def test_update_with_negative_values(self, std_progress: StdProgress, mock_io: MagicMock) -> None:
        """Test update with negative values."""
        await std_progress.update(total=-10.0, completed=-5.0, advance=-2.0)

        assert std_progress._total == -10.0
        assert std_progress._completed == -7.0  # -5.0 + (-2.0)
        mock_io.print.assert_called_once_with("Progress: -7.0/-10.0")

    @pytest.mark.anyio
    async def test_update_with_float_values(self, std_progress: StdProgress, mock_io: MagicMock) -> None:
        """Test update with precise float values."""
        await std_progress.update(total=99.99, completed=33.33, advance=11.11)

        assert std_progress._total == 99.99
        assert std_progress._completed == 44.44  # 33.33 + 11.11
        mock_io.print.assert_called_once_with("Progress: 44.44/99.99")

    @pytest.mark.anyio
    async def test_update_calls_io_print_exactly_once(self, std_progress: StdProgress, mock_io: MagicMock) -> None:
        """Test that update calls io.print exactly once per call."""
        await std_progress.update(total=100.0)

        mock_io.print.assert_called_once()
        mock_io.print.reset_mock()

        await std_progress.update(completed=50.0)

        mock_io.print.assert_called_once()

    @pytest.mark.anyio
    async def test_update_message_formats(self, std_progress: StdProgress, mock_io: MagicMock) -> None:
        """Test different message formats based on available data."""
        # Test total and completed
        await std_progress.update(total=100.0, completed=50.0)
        mock_io.print.assert_called_with("Progress: 50.0/100.0")
        mock_io.print.reset_mock()

        # Reset state and test total only
        std_progress._total = None
        std_progress._completed = None
        await std_progress.update(total=100.0)
        mock_io.print.assert_called_with("Progress: 100.0 to go")
        mock_io.print.reset_mock()

        # Reset state and test completed only
        std_progress._total = None
        std_progress._completed = None
        await std_progress.update(completed=50.0)
        mock_io.print.assert_called_with("Progress: 50.0 completed")
        mock_io.print.reset_mock()

        # Reset state and test no information
        std_progress._total = None
        std_progress._completed = None
        await std_progress.update()
        mock_io.print.assert_called_with("No progress information available")


class TestStdIO:
    """Test the StdIO implementation."""

    @pytest.fixture
    def std_io(self) -> StdIO:
        """Create a StdIO instance."""
        return StdIO()

    def test_init_creates_std_progress(self, std_io: StdIO) -> None:
        """Test that StdIO creates a StdProgress instance."""
        assert isinstance(std_io.progress, StdProgress)
        assert std_io.progress._io == std_io

    def test_init_progress_circular_reference(self, std_io: StdIO) -> None:
        """Test that progress has reference back to the IO instance."""
        assert std_io.progress._io is std_io

    @pytest.mark.anyio
    async def test_prompt_with_input(self, std_io: StdIO) -> None:
        """Test prompt method with regular input."""
        with patch("builtins.input", return_value="test_input") as mock_input:
            result = await std_io.prompt("Enter value: ")

            assert result == "test_input"
            mock_input.assert_called_once_with("Enter value: ")

    @pytest.mark.anyio
    async def test_prompt_with_password(self, std_io: StdIO) -> None:
        """Test prompt method with password flag."""
        with patch("ynab_cli.domain.ports.io.getpass", return_value="secret") as mock_getpass:
            result = await std_io.prompt("Enter password: ", password=True)

            assert result == "secret"
            mock_getpass.assert_called_once_with("Enter password: ")

    @pytest.mark.anyio
    async def test_prompt_without_password_flag(self, std_io: StdIO) -> None:
        """Test prompt method with explicit password=False."""
        with patch("builtins.input", return_value="regular_input") as mock_input:
            result = await std_io.prompt("Enter value: ", password=False)

            assert result == "regular_input"
            mock_input.assert_called_once_with("Enter value: ")

    @pytest.mark.anyio
    async def test_prompt_with_empty_string(self, std_io: StdIO) -> None:
        """Test prompt method with empty string input."""
        with patch("builtins.input", return_value="") as mock_input:
            result = await std_io.prompt("Enter value: ")

            assert result == ""
            mock_input.assert_called_once_with("Enter value: ")

    @pytest.mark.anyio
    async def test_prompt_with_empty_prompt(self, std_io: StdIO) -> None:
        """Test prompt method with empty prompt string."""
        with patch("builtins.input", return_value="response") as mock_input:
            result = await std_io.prompt("")

            assert result == "response"
            mock_input.assert_called_once_with("")

    @pytest.mark.anyio
    async def test_prompt_with_special_characters(self, std_io: StdIO) -> None:
        """Test prompt method with special characters."""
        special_input = "Test with 特殊字符 and émojis 🚀"
        with patch("builtins.input", return_value=special_input) as mock_input:
            result = await std_io.prompt("Enter value: ")

            assert result == special_input
            mock_input.assert_called_once_with("Enter value: ")

    @pytest.mark.anyio
    async def test_prompt_with_multiline_input(self, std_io: StdIO) -> None:
        """Test prompt method with multiline input."""
        multiline_input = "Line 1\nLine 2\nLine 3"
        with patch("builtins.input", return_value=multiline_input) as mock_input:
            result = await std_io.prompt("Enter value: ")

            assert result == multiline_input
            mock_input.assert_called_once_with("Enter value: ")

    @pytest.mark.anyio
    async def test_prompt_password_with_empty_input(self, std_io: StdIO) -> None:
        """Test password prompt with empty input."""
        with patch("ynab_cli.domain.ports.io.getpass", return_value="") as mock_getpass:
            result = await std_io.prompt("Enter password: ", password=True)

            assert result == ""
            mock_getpass.assert_called_once_with("Enter password: ")

    @pytest.mark.anyio
    async def test_prompt_keyboard_interrupt(self, std_io: StdIO) -> None:
        """Test prompt method handling KeyboardInterrupt."""
        with patch("builtins.input", side_effect=KeyboardInterrupt()) as mock_input:
            with pytest.raises(KeyboardInterrupt):
                await std_io.prompt("Enter value: ")

            mock_input.assert_called_once_with("Enter value: ")

    @pytest.mark.anyio
    async def test_prompt_eof_error(self, std_io: StdIO) -> None:
        """Test prompt method handling EOFError."""
        with patch("builtins.input", side_effect=EOFError()) as mock_input:
            with pytest.raises(EOFError):
                await std_io.prompt("Enter value: ")

            mock_input.assert_called_once_with("Enter value: ")

    @pytest.mark.anyio
    async def test_print_with_message(self, std_io: StdIO) -> None:
        """Test print method with regular message."""
        with patch("builtins.print") as mock_print:
            await std_io.print("Hello, World!")

            mock_print.assert_called_once_with("Hello, World!")

    @pytest.mark.anyio
    async def test_print_with_empty_message(self, std_io: StdIO) -> None:
        """Test print method with empty message."""
        with patch("builtins.print") as mock_print:
            await std_io.print("")

            mock_print.assert_called_once_with("")

    @pytest.mark.anyio
    async def test_print_with_multiline_message(self, std_io: StdIO) -> None:
        """Test print method with multiline message."""
        multiline_message = "Line 1\nLine 2\nLine 3"
        with patch("builtins.print") as mock_print:
            await std_io.print(multiline_message)

            mock_print.assert_called_once_with(multiline_message)

    @pytest.mark.anyio
    async def test_print_with_special_characters(self, std_io: StdIO) -> None:
        """Test print method with special characters."""
        special_message = "Message with 特殊字符 and émojis 🚀"
        with patch("builtins.print") as mock_print:
            await std_io.print(special_message)

            mock_print.assert_called_once_with(special_message)

    @pytest.mark.anyio
    async def test_print_returns_none(self, std_io: StdIO) -> None:
        """Test that print method returns None."""
        with patch("builtins.print") as mock_print:
            await std_io.print("test message")

            mock_print.assert_called_once_with("test message")

    @pytest.mark.anyio
    async def test_print_multiple_calls(self, std_io: StdIO) -> None:
        """Test multiple calls to print method."""
        with patch("builtins.print") as mock_print:
            await std_io.print("Message 1")
            await std_io.print("Message 2")
            await std_io.print("Message 3")

            assert mock_print.call_count == 3
            mock_print.assert_any_call("Message 1")
            mock_print.assert_any_call("Message 2")
            mock_print.assert_any_call("Message 3")

    @pytest.mark.anyio
    async def test_progress_integration(self, std_io: StdIO) -> None:
        """Test that progress updates work through the IO instance."""
        with patch("builtins.print") as mock_print:
            await std_io.progress.update(total=100.0, completed=50.0)

            mock_print.assert_called_once_with("Progress: 50.0/100.0")

    def test_implements_io_protocol(self, std_io: StdIO) -> None:
        """Test that StdIO properly implements the IO protocol."""
        assert hasattr(std_io, "progress")
        assert hasattr(std_io, "prompt")
        assert hasattr(std_io, "print")

    def test_progress_implements_progress_protocol(self, std_io: StdIO) -> None:
        """Test that StdProgress properly implements the Progress protocol."""
        assert hasattr(std_io.progress, "update")

    @pytest.mark.anyio
    async def test_prompt_return_type_is_string(self, std_io: StdIO) -> None:
        """Test that prompt always returns a string."""
        with patch("builtins.input", return_value="test"):
            result = await std_io.prompt("Test: ")
            assert isinstance(result, str)

        with patch("ynab_cli.domain.ports.io.getpass", return_value="secret"):
            result = await std_io.prompt("Password: ", password=True)
            assert isinstance(result, str)

    @pytest.mark.anyio
    async def test_print_parameter_types(self, std_io: StdIO) -> None:
        """Test that print accepts correct parameter types."""
        with patch("builtins.print"):
            await std_io.print("string message")

    @pytest.mark.anyio
    async def test_progress_update_parameter_types(self, std_io: StdIO) -> None:
        """Test that progress.update accepts correct parameter types."""
        with patch("builtins.print"):
            await std_io.progress.update(total=100.0)
            await std_io.progress.update(completed=50.0)
            await std_io.progress.update(advance=25.0)
            await std_io.progress.update(total=None)
            await std_io.progress.update(completed=None)
            await std_io.progress.update(advance=None)
