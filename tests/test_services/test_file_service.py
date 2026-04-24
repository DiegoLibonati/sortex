from pathlib import Path

import pytest

from src.constants.messages import (
    MESSAGE_NOT_FOUND_PATH,
    MESSAGE_NOT_VALID_PATH,
    MESSAGE_SUCCESS_ORGANIZED,
    MESSAGE_SUCCESS_PATH_LOADED,
    MESSAGE_SUCCESS_REVERTED,
)
from src.models.file_organizer_model import FileOrganizerModel
from src.services.file_service import FileService


class TestFileServiceInit:
    def test_file_organizer_initially_none(self) -> None:
        service: FileService = FileService()
        assert service._file_organizer is None


class TestFileServiceSetPath:
    def test_valid_path_returns_true(self, tmp_path: Path) -> None:
        service: FileService = FileService()
        message, success = service.set_path(str(tmp_path))
        assert success is True
        assert message == MESSAGE_SUCCESS_PATH_LOADED

    def test_nonexistent_path_returns_false(self) -> None:
        service: FileService = FileService()
        message, success = service.set_path("/nonexistent/path/abc123")
        assert success is False
        assert message == MESSAGE_NOT_VALID_PATH

    def test_empty_string_returns_false(self) -> None:
        service: FileService = FileService()
        message, success = service.set_path("")
        assert success is False
        assert message == MESSAGE_NOT_VALID_PATH

    def test_valid_path_creates_organizer(self, tmp_path: Path) -> None:
        service: FileService = FileService()
        service.set_path(str(tmp_path))
        assert service._file_organizer is not None

    def test_second_set_path_replaces_organizer(self, tmp_path: Path, tmp_path_factory: pytest.TempPathFactory) -> None:
        second_path: Path = tmp_path_factory.mktemp("second")
        service: FileService = FileService()
        service.set_path(str(tmp_path))
        first_organizer: FileOrganizerModel | None = service._file_organizer
        service.set_path(str(second_path))
        assert service._file_organizer is not first_organizer


class TestFileServiceOrganize:
    def test_without_path_returns_false(self) -> None:
        service: FileService = FileService()
        message, success = service.organize([], {})
        assert success is False
        assert message == MESSAGE_NOT_FOUND_PATH

    def test_empty_dir_returns_false(self, tmp_path: Path) -> None:
        service: FileService = FileService()
        service.set_path(str(tmp_path))
        message, success = service.organize([], {})
        assert success is False

    def test_with_files_returns_true(self, tmp_path: Path) -> None:
        (tmp_path / "doc.pdf").write_text("content")
        service: FileService = FileService()
        service.set_path(str(tmp_path))
        message, success = service.organize([], {})
        assert success is True
        assert message == MESSAGE_SUCCESS_ORGANIZED

    def test_sets_extensions_on_model(self, tmp_path: Path) -> None:
        (tmp_path / "doc.pdf").write_text("content")
        service: FileService = FileService()
        service.set_path(str(tmp_path))
        service.organize(["pdf"], {})
        assert service._file_organizer.extensions_allowed == ["pdf"]

    def test_sets_filters_on_model(self, tmp_path: Path) -> None:
        service: FileService = FileService()
        service.set_path(str(tmp_path))
        filters: dict[str, int] = {"min_size": 1, "max_size": 10}
        service.organize([], filters)
        assert service._file_organizer.filters == filters

    def test_organize_with_extension_filter(self, tmp_path: Path) -> None:
        (tmp_path / "doc.pdf").write_text("content")
        (tmp_path / "image.png").write_text("content")
        service: FileService = FileService()
        service.set_path(str(tmp_path))
        message, success = service.organize(["pdf"], {})
        assert success is True


class TestFileServiceRevert:
    def test_without_path_returns_false(self) -> None:
        service: FileService = FileService()
        message, success = service.revert()
        assert success is False
        assert message == MESSAGE_NOT_FOUND_PATH

    def test_without_organizer_folders_returns_false(self, tmp_path: Path) -> None:
        service: FileService = FileService()
        service.set_path(str(tmp_path))
        message, success = service.revert()
        assert success is False

    def test_after_organize_returns_true(self, tmp_path: Path) -> None:
        (tmp_path / "doc.pdf").write_text("content")
        service: FileService = FileService()
        service.set_path(str(tmp_path))
        service.organize([], {})
        message, success = service.revert()
        assert success is True
        assert message == MESSAGE_SUCCESS_REVERTED

    def test_revert_restores_original_state(self, tmp_path: Path) -> None:
        (tmp_path / "doc.pdf").write_text("content")
        service: FileService = FileService()
        service.set_path(str(tmp_path))
        service.organize([], {})
        service.revert()
        assert (tmp_path / "doc.pdf").is_file()
        assert not (tmp_path / "PDF_ORGANIZER").is_dir()
