from src.constants.messages import (
    MESSAGE_ERROR_APP,
    MESSAGE_NOT_FOUND_DIALOG_TYPE,
    MESSAGE_NOT_FOUND_EXTENSIONS,
    MESSAGE_NOT_FOUND_FILES,
    MESSAGE_NOT_FOUND_FOLDERS,
    MESSAGE_NOT_FOUND_PATH,
    MESSAGE_NOT_FOUND_PATH_OR_EXTENSIONS,
    MESSAGE_NOT_VALID_PATH,
    MESSAGE_SUCCESS_ORGANIZED,
    MESSAGE_SUCCESS_PATH_LOADED,
    MESSAGE_SUCCESS_REVERTED,
)


class TestMessages:
    def test_success_organized_is_string(self) -> None:
        assert isinstance(MESSAGE_SUCCESS_ORGANIZED, str)

    def test_success_organized_is_not_empty(self) -> None:
        assert MESSAGE_SUCCESS_ORGANIZED

    def test_success_reverted_is_string(self) -> None:
        assert isinstance(MESSAGE_SUCCESS_REVERTED, str)

    def test_success_reverted_is_not_empty(self) -> None:
        assert MESSAGE_SUCCESS_REVERTED

    def test_success_path_loaded_is_string(self) -> None:
        assert isinstance(MESSAGE_SUCCESS_PATH_LOADED, str)

    def test_success_path_loaded_is_not_empty(self) -> None:
        assert MESSAGE_SUCCESS_PATH_LOADED

    def test_error_app_is_string(self) -> None:
        assert isinstance(MESSAGE_ERROR_APP, str)

    def test_error_app_is_not_empty(self) -> None:
        assert MESSAGE_ERROR_APP

    def test_not_valid_path_is_string(self) -> None:
        assert isinstance(MESSAGE_NOT_VALID_PATH, str)

    def test_not_valid_path_is_not_empty(self) -> None:
        assert MESSAGE_NOT_VALID_PATH

    def test_not_found_dialog_type_is_string(self) -> None:
        assert isinstance(MESSAGE_NOT_FOUND_DIALOG_TYPE, str)

    def test_not_found_dialog_type_is_not_empty(self) -> None:
        assert MESSAGE_NOT_FOUND_DIALOG_TYPE

    def test_not_found_path_or_extensions_is_string(self) -> None:
        assert isinstance(MESSAGE_NOT_FOUND_PATH_OR_EXTENSIONS, str)

    def test_not_found_path_or_extensions_is_not_empty(self) -> None:
        assert MESSAGE_NOT_FOUND_PATH_OR_EXTENSIONS

    def test_not_found_files_is_string(self) -> None:
        assert isinstance(MESSAGE_NOT_FOUND_FILES, str)

    def test_not_found_files_is_not_empty(self) -> None:
        assert MESSAGE_NOT_FOUND_FILES

    def test_not_found_folders_is_string(self) -> None:
        assert isinstance(MESSAGE_NOT_FOUND_FOLDERS, str)

    def test_not_found_folders_is_not_empty(self) -> None:
        assert MESSAGE_NOT_FOUND_FOLDERS

    def test_not_found_extensions_is_string(self) -> None:
        assert isinstance(MESSAGE_NOT_FOUND_EXTENSIONS, str)

    def test_not_found_extensions_is_not_empty(self) -> None:
        assert MESSAGE_NOT_FOUND_EXTENSIONS

    def test_not_found_path_is_string(self) -> None:
        assert isinstance(MESSAGE_NOT_FOUND_PATH, str)

    def test_not_found_path_is_not_empty(self) -> None:
        assert MESSAGE_NOT_FOUND_PATH

    def test_all_messages_are_unique(self) -> None:
        all_messages: list[str] = [
            MESSAGE_SUCCESS_ORGANIZED,
            MESSAGE_SUCCESS_REVERTED,
            MESSAGE_SUCCESS_PATH_LOADED,
            MESSAGE_ERROR_APP,
            MESSAGE_NOT_VALID_PATH,
            MESSAGE_NOT_FOUND_DIALOG_TYPE,
            MESSAGE_NOT_FOUND_PATH_OR_EXTENSIONS,
            MESSAGE_NOT_FOUND_FILES,
            MESSAGE_NOT_FOUND_FOLDERS,
            MESSAGE_NOT_FOUND_EXTENSIONS,
            MESSAGE_NOT_FOUND_PATH,
        ]
        assert len(all_messages) == len(set(all_messages))
