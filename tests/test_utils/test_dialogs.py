from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from src.constants.messages import MESSAGE_ERROR_APP
from src.utils.dialogs import (
    AuthenticationDialogError,
    BaseDialog,
    BaseDialogError,
    BusinessDialogError,
    ConflictDialogError,
    DeprecatedDialogWarning,
    InternalDialogError,
    NotFoundDialogError,
    SuccessDialogInformation,
    ValidationDialogError,
)


class TestBaseDialog:
    def test_default_dialog_type_is_error(self) -> None:
        dialog: BaseDialog = BaseDialog()
        assert dialog.dialog_type == BaseDialog.ERROR

    def test_default_message(self) -> None:
        dialog: BaseDialog = BaseDialog()
        assert dialog.message == MESSAGE_ERROR_APP

    def test_custom_message_overrides_default(self) -> None:
        dialog: BaseDialog = BaseDialog(message="Custom message")
        assert dialog.message == "Custom message"

    def test_none_message_keeps_class_default(self) -> None:
        dialog: BaseDialog = BaseDialog(message=None)
        assert dialog.message == MESSAGE_ERROR_APP

    def test_title_for_error_type(self) -> None:
        dialog: BaseDialog = BaseDialog()
        assert dialog.title == "Error"

    def test_error_constant_value(self) -> None:
        assert BaseDialog.ERROR == "Error"

    def test_warning_constant_value(self) -> None:
        assert BaseDialog.WARNING == "Warning"

    def test_info_constant_value(self) -> None:
        assert BaseDialog.INFO == "Info"

    def test_to_dict_contains_required_keys(self) -> None:
        dialog: BaseDialog = BaseDialog()
        result: dict[str, Any] = dialog.to_dict()
        assert "dialog_type" in result
        assert "title" in result
        assert "message" in result

    def test_to_dict_values_match_attributes(self) -> None:
        dialog: BaseDialog = BaseDialog(message="test msg")
        result: dict[str, Any] = dialog.to_dict()
        assert result["dialog_type"] == BaseDialog.ERROR
        assert result["title"] == "Error"
        assert result["message"] == "test msg"

    def test_open_calls_showerror(self) -> None:
        dialog: BaseDialog = BaseDialog()
        mock_handler: MagicMock = MagicMock()
        with patch.dict(BaseDialog._HANDLERS, {BaseDialog.ERROR: mock_handler}):
            dialog.open()
            mock_handler.assert_called_once_with("Error", MESSAGE_ERROR_APP)


class TestBaseDialogError:
    def test_is_exception(self) -> None:
        error: BaseDialogError = BaseDialogError()
        assert isinstance(error, Exception)

    def test_is_base_dialog(self) -> None:
        error: BaseDialogError = BaseDialogError()
        assert isinstance(error, BaseDialog)

    def test_dialog_type_is_error(self) -> None:
        error: BaseDialogError = BaseDialogError()
        assert error.dialog_type == BaseDialog.ERROR

    def test_can_be_raised_and_caught(self) -> None:
        with pytest.raises(BaseDialogError):
            raise BaseDialogError()


class TestValidationDialogError:
    def test_default_message(self) -> None:
        error: ValidationDialogError = ValidationDialogError()
        assert error.message == "Validation error"

    def test_custom_message(self) -> None:
        error: ValidationDialogError = ValidationDialogError(message="Field required")
        assert error.message == "Field required"

    def test_is_exception(self) -> None:
        assert isinstance(ValidationDialogError(), Exception)

    def test_is_base_dialog_error(self) -> None:
        assert isinstance(ValidationDialogError(), BaseDialogError)

    def test_can_be_raised(self) -> None:
        with pytest.raises(ValidationDialogError):
            raise ValidationDialogError()


class TestAuthenticationDialogError:
    def test_default_message(self) -> None:
        error: AuthenticationDialogError = AuthenticationDialogError()
        assert error.message == "Authentication error"

    def test_is_exception(self) -> None:
        assert isinstance(AuthenticationDialogError(), Exception)


class TestNotFoundDialogError:
    def test_default_message(self) -> None:
        error: NotFoundDialogError = NotFoundDialogError()
        assert error.message == "Resource not found"

    def test_custom_message(self) -> None:
        error: NotFoundDialogError = NotFoundDialogError(message="Item missing")
        assert error.message == "Item missing"

    def test_is_exception(self) -> None:
        assert isinstance(NotFoundDialogError(), Exception)


class TestConflictDialogError:
    def test_default_message(self) -> None:
        error: ConflictDialogError = ConflictDialogError()
        assert error.message == "Conflict error"

    def test_is_exception(self) -> None:
        assert isinstance(ConflictDialogError(), Exception)


class TestBusinessDialogError:
    def test_default_message(self) -> None:
        error: BusinessDialogError = BusinessDialogError()
        assert error.message == "Business rule violated"

    def test_is_exception(self) -> None:
        assert isinstance(BusinessDialogError(), Exception)


class TestInternalDialogError:
    def test_default_message(self) -> None:
        error: InternalDialogError = InternalDialogError()
        assert error.message == "Internal error"

    def test_is_exception(self) -> None:
        assert isinstance(InternalDialogError(), Exception)


class TestDeprecatedDialogWarning:
    def test_dialog_type_is_warning(self) -> None:
        warning: DeprecatedDialogWarning = DeprecatedDialogWarning()
        assert warning.dialog_type == BaseDialog.WARNING

    def test_default_message(self) -> None:
        warning: DeprecatedDialogWarning = DeprecatedDialogWarning()
        assert warning.message == "This feature is deprecated"

    def test_title_is_warning(self) -> None:
        warning: DeprecatedDialogWarning = DeprecatedDialogWarning()
        assert warning.title == "Warning"

    def test_is_not_exception(self) -> None:
        assert not isinstance(DeprecatedDialogWarning(), Exception)

    def test_open_calls_showwarning(self) -> None:
        warning: DeprecatedDialogWarning = DeprecatedDialogWarning()
        mock_handler: MagicMock = MagicMock()
        with patch.dict(BaseDialog._HANDLERS, {BaseDialog.WARNING: mock_handler}):
            warning.open()
            mock_handler.assert_called_once_with("Warning", "This feature is deprecated")


class TestSuccessDialogInformation:
    def test_dialog_type_is_info(self) -> None:
        info: SuccessDialogInformation = SuccessDialogInformation()
        assert info.dialog_type == BaseDialog.INFO

    def test_default_message(self) -> None:
        info: SuccessDialogInformation = SuccessDialogInformation()
        assert info.message == "Operation completed successfully"

    def test_title_is_information(self) -> None:
        info: SuccessDialogInformation = SuccessDialogInformation()
        assert info.title == "Information"

    def test_is_not_exception(self) -> None:
        assert not isinstance(SuccessDialogInformation(), Exception)

    def test_open_calls_showinfo(self) -> None:
        info: SuccessDialogInformation = SuccessDialogInformation()
        mock_handler: MagicMock = MagicMock()
        with patch.dict(BaseDialog._HANDLERS, {BaseDialog.INFO: mock_handler}):
            info.open()
            mock_handler.assert_called_once_with("Information", "Operation completed successfully")

    def test_custom_message(self) -> None:
        info: SuccessDialogInformation = SuccessDialogInformation(message="Done!")
        assert info.message == "Done!"
