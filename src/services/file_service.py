import os
from typing import Any

from src.constants.messages import MESSAGE_NOT_FOUND_PATH, MESSAGE_NOT_VALID_PATH, MESSAGE_SUCCESS_PATH_LOADED
from src.models.file_organizer_model import FileOrganizerModel


class FileService:
    def __init__(self):
        self._file_organizer: FileOrganizerModel | None = None

    def set_path(self, path: str) -> tuple[str, bool]:
        if not path or not os.path.exists(path):
            return MESSAGE_NOT_VALID_PATH, False

        self._file_organizer = FileOrganizerModel(path=path)
        return MESSAGE_SUCCESS_PATH_LOADED, True

    def organize(self, extensions: list[str], filters: dict[str, Any]) -> tuple[str, bool]:
        if not self._file_organizer:
            return MESSAGE_NOT_FOUND_PATH, False

        self._file_organizer.extensions_allowed = extensions
        self._file_organizer.filters = filters

        return self._file_organizer.organizer()

    def revert(self) -> tuple[str, bool]:
        if not self._file_organizer:
            return (
                MESSAGE_NOT_FOUND_PATH,
                False,
            )
        return self._file_organizer.revert_organizer()
