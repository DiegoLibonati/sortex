from unittest.mock import MagicMock, patch

from src.utils.dialogs import InternalDialogError, ValidationDialogError
from src.utils.error_handler import error_handler


class TestErrorHandler:
    def test_base_dialog_subclass_calls_open(self) -> None:
        error: ValidationDialogError = ValidationDialogError(message="test error")
        mock_open: MagicMock
        with patch.object(error, "open") as mock_open:
            error_handler(type(error), error, None)
            mock_open.assert_called_once()

    def test_non_dialog_exception_creates_internal_error(self) -> None:
        exc: ValueError = ValueError("something went wrong")
        mock_internal: MagicMock
        with patch("src.utils.error_handler.InternalDialogError") as mock_internal:
            mock_instance: MagicMock = MagicMock()
            mock_internal.return_value = mock_instance
            error_handler(ValueError, exc, None)
            mock_internal.assert_called_once_with(message="something went wrong")
            mock_instance.open.assert_called_once()

    def test_non_dialog_exception_uses_str_representation(self) -> None:
        exc: RuntimeError = RuntimeError("runtime failure")
        mock_internal: MagicMock
        with patch("src.utils.error_handler.InternalDialogError") as mock_internal:
            mock_instance: MagicMock = MagicMock()
            mock_internal.return_value = mock_instance
            error_handler(RuntimeError, exc, None)
            mock_internal.assert_called_once_with(message="runtime failure")

    def test_accepts_none_traceback(self) -> None:
        error: ValidationDialogError = ValidationDialogError()
        with patch.object(error, "open"):
            error_handler(type(error), error, None)

    def test_internal_dialog_error_itself_calls_open(self) -> None:
        error: InternalDialogError = InternalDialogError(message="internal")
        mock_open: MagicMock
        with patch.object(error, "open") as mock_open:
            error_handler(type(error), error, None)
            mock_open.assert_called_once()
