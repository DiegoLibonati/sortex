from unittest.mock import MagicMock, patch

import pytest

from src.utils.dialogs import InternalDialogError, ValidationDialogError
from src.utils.tkinter_exception_hook import tkinter_exception_hook


class TestTkinterExceptionHook:
    @pytest.mark.unit
    def test_base_dialog_subclass_calls_open(self) -> None:
        error: ValidationDialogError = ValidationDialogError(message="test error")

        with patch.object(error, "open") as mock_open:
            tkinter_exception_hook(type(error), error, None)

        mock_open.assert_called_once()

    @pytest.mark.unit
    def test_non_dialog_exception_creates_internal_error(self) -> None:
        exc: ValueError = ValueError("something went wrong")
        mock_internal: MagicMock = MagicMock()

        with patch("src.utils.tkinter_exception_hook.InternalDialogError", mock_internal):
            mock_instance: MagicMock = MagicMock()
            mock_internal.return_value = mock_instance

            tkinter_exception_hook(ValueError, exc, None)

        mock_internal.assert_called_once_with(message="something went wrong")
        mock_instance.open.assert_called_once()

    @pytest.mark.unit
    def test_non_dialog_exception_uses_str_representation(self) -> None:
        exc: RuntimeError = RuntimeError("runtime failure")
        mock_internal: MagicMock = MagicMock()

        with patch("src.utils.tkinter_exception_hook.InternalDialogError", mock_internal):
            mock_internal.return_value = MagicMock()

            tkinter_exception_hook(RuntimeError, exc, None)

        mock_internal.assert_called_once_with(message="runtime failure")

    @pytest.mark.unit
    def test_accepts_none_traceback(self) -> None:
        error: ValidationDialogError = ValidationDialogError()

        with patch.object(error, "open"):
            tkinter_exception_hook(type(error), error, None)

    @pytest.mark.unit
    def test_internal_dialog_error_itself_calls_open(self) -> None:
        error: InternalDialogError = InternalDialogError(message="internal")

        with patch.object(error, "open") as mock_open:
            tkinter_exception_hook(type(error), error, None)

        mock_open.assert_called_once()

    @pytest.mark.unit
    def test_logs_traceback_on_unhandled_exception(self) -> None:
        exc: RuntimeError = RuntimeError("logged error")

        with (
            patch("src.utils.tkinter_exception_hook.logger") as mock_logger,
            patch("src.utils.tkinter_exception_hook.InternalDialogError"),
        ):
            tkinter_exception_hook(RuntimeError, exc, None)

        mock_logger.error.assert_called_once()

    @pytest.mark.unit
    def test_logs_traceback_on_dialog_exception(self) -> None:
        error: ValidationDialogError = ValidationDialogError(message="val err")

        with (
            patch("src.utils.tkinter_exception_hook.logger") as mock_logger,
            patch.object(error, "open"),
        ):
            tkinter_exception_hook(type(error), error, None)

        mock_logger.error.assert_called_once()
