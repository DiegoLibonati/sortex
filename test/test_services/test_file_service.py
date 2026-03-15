from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from src.constants.messages import (
    MESSAGE_NOT_FOUND_PATH,
    MESSAGE_NOT_VALID_PATH,
    MESSAGE_SUCCESS_PATH_LOADED,
)
from src.services.file_service import FileService


@pytest.fixture
def file_service() -> FileService:
    return FileService()


@pytest.fixture
def file_service_with_organizer(file_service: FileService, mock_file_organizer: MagicMock) -> FileService:
    file_service._file_organizer = mock_file_organizer
    return file_service


class TestFileServiceInit:
    def test_file_organizer_initial_value_is_none(self, file_service: FileService) -> None:
        assert file_service._file_organizer is None


class TestFileServiceSetPath:
    def test_returns_error_when_path_is_empty(self, file_service: FileService) -> None:
        message, status = file_service.set_path(path="")
        assert status is False
        assert message == MESSAGE_NOT_VALID_PATH

    def test_returns_error_when_path_does_not_exist(self, file_service: FileService) -> None:
        with patch("src.services.file_service.os.path.exists", return_value=False):
            message, status = file_service.set_path(path="/nonexistent/path")
        assert status is False
        assert message == MESSAGE_NOT_VALID_PATH

    def test_returns_success_when_path_is_valid(self, file_service: FileService) -> None:
        with (
            patch("src.services.file_service.os.path.exists", return_value=True),
            patch("src.services.file_service.FileOrganizerModel"),
        ):
            message, status = file_service.set_path(path="/valid/path")
        assert status is True
        assert message == MESSAGE_SUCCESS_PATH_LOADED

    def test_file_organizer_is_set_when_path_is_valid(self, file_service: FileService) -> None:
        with (
            patch("src.services.file_service.os.path.exists", return_value=True),
            patch("src.services.file_service.FileOrganizerModel") as mock_organizer_class,
        ):
            mock_organizer_class.return_value = MagicMock()
            file_service.set_path(path="/valid/path")
        assert file_service._file_organizer is not None

    def test_file_organizer_created_with_correct_path(self, file_service: FileService) -> None:
        with (
            patch("src.services.file_service.os.path.exists", return_value=True),
            patch("src.services.file_service.FileOrganizerModel") as mock_organizer_class,
        ):
            mock_organizer_class.return_value = MagicMock()
            file_service.set_path(path="/valid/path")
        mock_organizer_class.assert_called_once_with(path="/valid/path")

    def test_file_organizer_not_set_when_path_is_invalid(self, file_service: FileService) -> None:
        with patch("src.services.file_service.os.path.exists", return_value=False):
            file_service.set_path(path="/bad/path")
        assert file_service._file_organizer is None


class TestFileServiceOrganize:
    def test_returns_error_when_organizer_is_none(self, file_service: FileService) -> None:
        message, status = file_service.organize(extensions=["txt"], filters={})
        assert status is False
        assert message == MESSAGE_NOT_FOUND_PATH

    def test_sets_extensions_allowed_on_organizer(self, file_service_with_organizer: FileService, mock_file_organizer: MagicMock) -> None:
        mock_file_organizer.organizer.return_value = ("ok", True)
        file_service_with_organizer.organize(extensions=["txt", "pdf"], filters={})
        assert mock_file_organizer.extensions_allowed == ["txt", "pdf"]

    def test_sets_filters_on_organizer(self, file_service_with_organizer: FileService, mock_file_organizer: MagicMock) -> None:
        filters: dict[str, Any] = {"min_size": 1, "max_size": 10}
        mock_file_organizer.organizer.return_value = ("ok", True)
        file_service_with_organizer.organize(extensions=["txt"], filters=filters)
        assert mock_file_organizer.filters == filters

    def test_delegates_to_organizer(self, file_service_with_organizer: FileService, mock_file_organizer: MagicMock) -> None:
        mock_file_organizer.organizer.return_value = ("ok", True)
        result = file_service_with_organizer.organize(extensions=["txt"], filters={})
        assert result == ("ok", True)
        mock_file_organizer.organizer.assert_called_once()


class TestFileServiceRevert:
    def test_returns_error_when_organizer_is_none(self, file_service: FileService) -> None:
        message, status = file_service.revert()
        assert status is False
        assert message == MESSAGE_NOT_FOUND_PATH

    def test_delegates_to_revert_organizer(self, file_service_with_organizer: FileService, mock_file_organizer: MagicMock) -> None:
        mock_file_organizer.revert_organizer.return_value = ("reverted", True)
        result = file_service_with_organizer.revert()
        assert result == ("reverted", True)
        mock_file_organizer.revert_organizer.assert_called_once()
