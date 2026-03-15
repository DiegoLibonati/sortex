import os
import time
from shutil import move, rmtree
from typing import Any

from src.constants.messages import (
    MESSAGE_NOT_FOUND_FILES,
    MESSAGE_NOT_FOUND_FOLDERS,
    MESSAGE_NOT_FOUND_PATH_OR_EXTENSIONS,
    MESSAGE_SUCCESS_ORGANIZED,
    MESSAGE_SUCCESS_REVERTED,
)


class FileOrganizerModel:
    def __init__(
        self,
        path: str,
        extensions_allowed: list[str] = [],
        folder_name: str = "ORGANIZER",
    ) -> None:
        self.path: str = path
        self.folder_name = folder_name
        self.extensions_allowed: list[str] = extensions_allowed

        self.filters: dict[str, Any] = {}
        self.all_path_extensions: list[str] = self._get_extensions(files=self._get_files())

    def organizer(self) -> tuple[str, bool]:
        if not self.all_path_extensions or not self.path:
            return (
                MESSAGE_NOT_FOUND_PATH_OR_EXTENSIONS,
                False,
            )

        files = self._get_files()

        if not files:
            return (
                MESSAGE_NOT_FOUND_FILES,
                False,
            )

        files_extensions = self._get_extensions(files=self._get_files())

        extensions = self.extensions_allowed if self.extensions_allowed else self.all_path_extensions

        for extension in extensions:
            folder_name = f"{extension.upper()}_{self.folder_name}"
            dir_path = os.path.join(self.path, folder_name)

            if os.path.exists(dir_path) or extension not in files_extensions:
                continue

            os.mkdir(dir_path)

        for file in files:
            extension = file.rsplit(".", 1).pop().upper()
            last_path = f"{self.path}/{file}"
            new_path = f"{self.path}/{extension}_ORGANIZER/{file}"

            move(last_path, new_path)

        return MESSAGE_SUCCESS_ORGANIZED, True

    def revert_organizer(self) -> tuple[str, bool]:
        folder_names = [name for name in os.listdir(self.path) if os.path.isdir(f"{self.path}/{name}") and self.folder_name in name]

        if not folder_names:
            return MESSAGE_NOT_FOUND_FOLDERS, False

        for folder_name in folder_names:
            dir_path = f"{self.path}/{folder_name}"
            dir_files = os.listdir(dir_path)

            if not dir_files:
                rmtree(dir_path)
                continue

            for file in dir_files:
                last_path = f"{dir_path}/{file}"
                new_path = f"{self.path}/{file}"

                move(last_path, new_path)

            rmtree(dir_path)

        self._reset_state()
        return MESSAGE_SUCCESS_REVERTED, True

    def _get_files(self) -> list[str]:
        try:
            files_in_path = os.listdir(self.path)

            if not self.filters and not self.extensions_allowed:
                return [file for file in files_in_path if os.path.isfile(f"{self.path}/{file}")]

            if not self.filters and self.extensions_allowed:
                return [file for file in files_in_path if os.path.isfile(f"{self.path}/{file}") and file.rsplit(".", 1).pop() in self.extensions_allowed]

            files = []
            byte = 1024 * 1024

            filter_min_size = self.filters["min_size"] * byte
            filter_max_size = self.filters["max_size"] * byte

            for file in files_in_path:
                is_file = os.path.isfile(f"{self.path}/{file}")

                if not is_file:
                    continue

                file_size = os.stat(f"{self.path}/{file}").st_size
                file_extension = file.rsplit(".", 1).pop()

                if (not self.extensions_allowed or file_extension in self.extensions_allowed) and file_size >= filter_min_size and file_size <= filter_max_size:
                    files.append(file)

            return files
        except Exception as ex:
            raise ValueError(str(ex))

    def _get_extensions(self, files: list[str]) -> list[str]:
        if not files:
            return []

        extensions: list[str] = []

        for file in files:
            extension = file.rsplit(".", 1).pop()

            if extension not in extensions:
                extensions.append(extension)

        return extensions

    def _reset_state(self) -> None:
        self.filters = {}
        self.all_path_extensions = self._get_extensions(files=self._get_files())

    def print_path(self) -> None:
        print(f"The chosen path is: {self.path}")

    def __str__(self) -> str:
        return (
            f"----- FileOrganizer -----\n"
            f"----- Path: {self.path} -----\n"
            f"----- Folder Name: {self.folder_name} -----\n"
            f"----- Extensions: {self.all_path_extensions} -----\n"
            f"----- Extensions Allowed: {self.extensions_allowed} -----\n"
            f"----- Filters: {self.filters} -----\n"
        )


if __name__ == "__main__":
    path = "D:/a"

    file_organizer = FileOrganizerModel(path=path)

    message, success = file_organizer.organizer()

    time.sleep(5)

    file_organizer.revert_organizer()
