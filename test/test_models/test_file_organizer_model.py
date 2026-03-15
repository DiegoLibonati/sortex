from unittest.mock import MagicMock, patch

import pytest

from src.constants.messages import (
    MESSAGE_NOT_FOUND_FILES,
    MESSAGE_NOT_FOUND_FOLDERS,
    MESSAGE_NOT_FOUND_PATH_OR_EXTENSIONS,
    MESSAGE_SUCCESS_ORGANIZED,
    MESSAGE_SUCCESS_REVERTED,
)
from src.models.file_organizer_model import FileOrganizerModel


@pytest.fixture
def model_no_files() -> FileOrganizerModel:
    with patch("src.models.file_organizer_model.os.listdir", return_value=[]):
        return FileOrganizerModel(path="/fake/path")


@pytest.fixture
def model_with_files() -> FileOrganizerModel:
    files: list[str] = ["doc.txt", "photo.jpg", "video.mp4"]
    with (
        patch("src.models.file_organizer_model.os.listdir", return_value=files),
        patch("src.models.file_organizer_model.os.path.isfile", return_value=True),
    ):
        return FileOrganizerModel(path="/fake/path")


class TestFileOrganizerModelInit:
    def test_stores_path(self, model_no_files: FileOrganizerModel) -> None:
        assert model_no_files.path == "/fake/path"

    def test_default_folder_name(self, model_no_files: FileOrganizerModel) -> None:
        assert model_no_files.folder_name == "ORGANIZER"

    def test_custom_folder_name(self) -> None:
        with patch("src.models.file_organizer_model.os.listdir", return_value=[]):
            model: FileOrganizerModel = FileOrganizerModel(path="/fake/path", folder_name="CUSTOM")
        assert model.folder_name == "CUSTOM"

    def test_default_extensions_allowed_is_empty(self, model_no_files: FileOrganizerModel) -> None:
        assert model_no_files.extensions_allowed == []

    def test_filters_initial_value_is_empty_dict(self, model_no_files: FileOrganizerModel) -> None:
        assert model_no_files.filters == {}

    def test_all_path_extensions_populated_from_files(self, model_with_files: FileOrganizerModel) -> None:
        assert set(model_with_files.all_path_extensions) == {"txt", "jpg", "mp4"}

    def test_all_path_extensions_empty_when_no_files(self, model_no_files: FileOrganizerModel) -> None:
        assert model_no_files.all_path_extensions == []


class TestFileOrganizerModelGetExtensions:
    def test_returns_empty_list_for_empty_files(self, model_no_files: FileOrganizerModel) -> None:
        assert model_no_files._get_extensions(files=[]) == []

    def test_returns_unique_extensions(self, model_no_files: FileOrganizerModel) -> None:
        files: list[str] = ["a.txt", "b.txt", "c.jpg"]
        result: list[str] = model_no_files._get_extensions(files=files)
        assert result == ["txt", "jpg"]

    def test_does_not_duplicate_extensions(self, model_no_files: FileOrganizerModel) -> None:
        files: list[str] = ["a.txt", "b.txt", "c.txt"]
        result: list[str] = model_no_files._get_extensions(files=files)
        assert len(result) == 1

    def test_extracts_correct_extension(self, model_no_files: FileOrganizerModel) -> None:
        result: list[str] = model_no_files._get_extensions(files=["document.pdf"])
        assert result == ["pdf"]


class TestFileOrganizerModelGetFiles:
    def test_returns_only_files_not_dirs(self, model_no_files: FileOrganizerModel) -> None:
        with (
            patch("src.models.file_organizer_model.os.listdir", return_value=["file.txt", "folder"]),
            patch("src.models.file_organizer_model.os.path.isfile", side_effect=lambda p: p.endswith(".txt")),
        ):
            result: list[str] = model_no_files._get_files()
        assert result == ["file.txt"]

    def test_filters_by_extensions_allowed(self) -> None:
        files: list[str] = ["doc.txt", "photo.jpg"]
        with (
            patch("src.models.file_organizer_model.os.listdir", return_value=files),
            patch("src.models.file_organizer_model.os.path.isfile", return_value=True),
        ):
            model: FileOrganizerModel = FileOrganizerModel(path="/fake/path", extensions_allowed=["txt"])
            result: list[str] = model._get_files()
        assert result == ["doc.txt"]

    def test_raises_value_error_on_os_exception(self, model_no_files: FileOrganizerModel) -> None:
        with (
            patch("src.models.file_organizer_model.os.listdir", side_effect=OSError("no access")),
            pytest.raises(ValueError, match="no access"),
        ):
            model_no_files._get_files()

    def test_filters_by_size_when_filters_set(self) -> None:
        files: list[str] = ["small.txt", "large.txt"]
        byte: int = 1024 * 1024
        with (
            patch("src.models.file_organizer_model.os.listdir", return_value=files),
            patch("src.models.file_organizer_model.os.path.isfile", return_value=True),
            patch("src.models.file_organizer_model.os.stat") as mock_stat,
        ):
            mock_stat.side_effect = lambda p: MagicMock(st_size=5 * byte if "small" in p else 50 * byte)
            model: FileOrganizerModel = FileOrganizerModel.__new__(FileOrganizerModel)
            model.path = "/fake/path"
            model.extensions_allowed = []
            model.filters = {"min_size": 1, "max_size": 10}
            result: list[str] = model._get_files()
        assert result == ["small.txt"]


class TestFileOrganizerModelOrganizer:
    def test_returns_error_when_no_path(self) -> None:
        with patch("src.models.file_organizer_model.os.listdir", return_value=[]):
            model: FileOrganizerModel = FileOrganizerModel(path="")
        message, status = model.organizer()
        assert status is False
        assert message == MESSAGE_NOT_FOUND_PATH_OR_EXTENSIONS

    def test_returns_error_when_no_extensions(self, model_no_files: FileOrganizerModel) -> None:
        message, status = model_no_files.organizer()
        assert status is False
        assert message == MESSAGE_NOT_FOUND_PATH_OR_EXTENSIONS

    def test_returns_error_when_no_files(self) -> None:
        with (
            patch("src.models.file_organizer_model.os.listdir", return_value=["doc.txt"]),
            patch("src.models.file_organizer_model.os.path.isfile", return_value=True),
        ):
            model: FileOrganizerModel = FileOrganizerModel(path="/fake/path")

        with patch.object(model, "_get_files", return_value=[]):
            message, status = model.organizer()

        assert status is False
        assert message == MESSAGE_NOT_FOUND_FILES

    def test_returns_success_and_creates_dirs(self) -> None:
        files: list[str] = ["doc.txt"]
        with (
            patch("src.models.file_organizer_model.os.listdir", return_value=files),
            patch("src.models.file_organizer_model.os.path.isfile", return_value=True),
        ):
            model: FileOrganizerModel = FileOrganizerModel(path="/fake/path")

        with (
            patch.object(model, "_get_files", return_value=files),
            patch("src.models.file_organizer_model.os.path.exists", return_value=False),
            patch("src.models.file_organizer_model.os.mkdir") as mock_mkdir,
            patch("src.models.file_organizer_model.move"),
        ):
            message, status = model.organizer()

        assert status is True
        assert message == MESSAGE_SUCCESS_ORGANIZED
        mock_mkdir.assert_called_once()

    def test_moves_files_to_correct_folders(self) -> None:
        files: list[str] = ["doc.txt"]
        with (
            patch("src.models.file_organizer_model.os.listdir", return_value=files),
            patch("src.models.file_organizer_model.os.path.isfile", return_value=True),
        ):
            model: FileOrganizerModel = FileOrganizerModel(path="/fake/path")

        with (
            patch.object(model, "_get_files", return_value=files),
            patch("src.models.file_organizer_model.os.path.exists", return_value=False),
            patch("src.models.file_organizer_model.os.mkdir"),
            patch("src.models.file_organizer_model.move") as mock_move,
        ):
            model.organizer()

        mock_move.assert_called_once_with(
            "/fake/path/doc.txt",
            "/fake/path/TXT_ORGANIZER/doc.txt",
        )

    def test_skips_existing_directories(self) -> None:
        files: list[str] = ["doc.txt"]
        with (
            patch("src.models.file_organizer_model.os.listdir", return_value=files),
            patch("src.models.file_organizer_model.os.path.isfile", return_value=True),
        ):
            model: FileOrganizerModel = FileOrganizerModel(path="/fake/path")

        with (
            patch.object(model, "_get_files", return_value=files),
            patch("src.models.file_organizer_model.os.path.exists", return_value=True),
            patch("src.models.file_organizer_model.os.mkdir") as mock_mkdir,
            patch("src.models.file_organizer_model.move"),
        ):
            model.organizer()

        mock_mkdir.assert_not_called()


class TestFileOrganizerModelRevertOrganizer:
    def test_returns_error_when_no_organizer_folders(self) -> None:
        with patch("src.models.file_organizer_model.os.listdir", return_value=[]):
            model: FileOrganizerModel = FileOrganizerModel(path="/fake/path")

        with patch("src.models.file_organizer_model.os.listdir", return_value=["some_folder"]):
            with patch("src.models.file_organizer_model.os.path.isdir", return_value=False):
                message, status = model.revert_organizer()

        assert status is False
        assert message == MESSAGE_NOT_FOUND_FOLDERS

    def test_returns_success_when_folders_reverted(self) -> None:
        with patch("src.models.file_organizer_model.os.listdir", return_value=[]):
            model: FileOrganizerModel = FileOrganizerModel(path="/fake/path")

        def listdir_side_effect(path: str) -> list[str]:
            if path == "/fake/path":
                return ["TXT_ORGANIZER"]
            return ["doc.txt"]

        with (
            patch("src.models.file_organizer_model.os.listdir", side_effect=listdir_side_effect),
            patch("src.models.file_organizer_model.os.path.isdir", return_value=True),
            patch("src.models.file_organizer_model.move"),
            patch("src.models.file_organizer_model.rmtree"),
            patch.object(model, "_reset_state"),
        ):
            message, status = model.revert_organizer()

        assert status is True
        assert message == MESSAGE_SUCCESS_REVERTED

    def test_removes_empty_folder_with_rmtree(self) -> None:
        with patch("src.models.file_organizer_model.os.listdir", return_value=[]):
            model: FileOrganizerModel = FileOrganizerModel(path="/fake/path")

        def listdir_side_effect(path: str) -> list[str]:
            if path == "/fake/path":
                return ["TXT_ORGANIZER"]
            return []

        with (
            patch("src.models.file_organizer_model.os.listdir", side_effect=listdir_side_effect),
            patch("src.models.file_organizer_model.os.path.isdir", return_value=True),
            patch("src.models.file_organizer_model.rmtree") as mock_rmtree,
            patch.object(model, "_reset_state"),
        ):
            model.revert_organizer()

        mock_rmtree.assert_called_once_with("/fake/path/TXT_ORGANIZER")

    def test_moves_files_back_to_root(self) -> None:
        with patch("src.models.file_organizer_model.os.listdir", return_value=[]):
            model: FileOrganizerModel = FileOrganizerModel(path="/fake/path")

        def listdir_side_effect(path: str) -> list[str]:
            if path == "/fake/path":
                return ["TXT_ORGANIZER"]
            return ["doc.txt"]

        with (
            patch("src.models.file_organizer_model.os.listdir", side_effect=listdir_side_effect),
            patch("src.models.file_organizer_model.os.path.isdir", return_value=True),
            patch("src.models.file_organizer_model.move") as mock_move,
            patch("src.models.file_organizer_model.rmtree"),
            patch.object(model, "_reset_state"),
        ):
            model.revert_organizer()

        mock_move.assert_called_once_with(
            "/fake/path/TXT_ORGANIZER/doc.txt",
            "/fake/path/doc.txt",
        )

    def test_reset_state_called_after_revert(self) -> None:
        with patch("src.models.file_organizer_model.os.listdir", return_value=[]):
            model: FileOrganizerModel = FileOrganizerModel(path="/fake/path")

        def listdir_side_effect(path: str) -> list[str]:
            if path == "/fake/path":
                return ["TXT_ORGANIZER"]
            return []

        with (
            patch("src.models.file_organizer_model.os.listdir", side_effect=listdir_side_effect),
            patch("src.models.file_organizer_model.os.path.isdir", return_value=True),
            patch("src.models.file_organizer_model.rmtree"),
            patch.object(model, "_reset_state") as mock_reset,
        ):
            model.revert_organizer()

        mock_reset.assert_called_once()
