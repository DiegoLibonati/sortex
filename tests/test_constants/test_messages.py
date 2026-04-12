from src.constants import messages


class TestMessages:
    def test_message_success_organized(self) -> None:
        assert messages.MESSAGE_SUCCESS_ORGANIZED == "Successfully organized."

    def test_message_success_reverted(self) -> None:
        assert messages.MESSAGE_SUCCESS_REVERTED == "Successfully reverted."

    def test_message_success_path_loaded(self) -> None:
        assert messages.MESSAGE_SUCCESS_PATH_LOADED == "Path loaded successfully."

    def test_message_error_app(self) -> None:
        assert messages.MESSAGE_ERROR_APP == "Internal error. Contact a developer."

    def test_message_not_valid_path(self) -> None:
        assert messages.MESSAGE_NOT_VALID_PATH == "Invalid path."

    def test_message_not_found_dialog_type(self) -> None:
        assert messages.MESSAGE_NOT_FOUND_DIALOG_TYPE == "The type of dialog to display is not found."

    def test_message_not_found_path_or_extensions(self) -> None:
        assert messages.MESSAGE_NOT_FOUND_PATH_OR_EXTENSIONS == "There is no path or there are no extensions."

    def test_message_not_found_files(self) -> None:
        assert messages.MESSAGE_NOT_FOUND_FILES == "There are no files."

    def test_message_not_found_folders(self) -> None:
        assert messages.MESSAGE_NOT_FOUND_FOLDERS == "There are no folders."

    def test_message_not_found_extensions(self) -> None:
        assert messages.MESSAGE_NOT_FOUND_EXTENSIONS == "There are no extensions."

    def test_message_not_found_path(self) -> None:
        assert messages.MESSAGE_NOT_FOUND_PATH == "There is no path."

    def test_all_messages_are_strings(self) -> None:
        string_attrs: list[str] = [attr for attr in dir(messages) if attr.startswith("MESSAGE_")]
        for attr in string_attrs:
            assert isinstance(getattr(messages, attr), str)
