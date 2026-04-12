import os
from pathlib import Path

import pytest

from src.constants.messages import (
    MESSAGE_NOT_FOUND_FOLDERS,
    MESSAGE_NOT_FOUND_PATH_OR_EXTENSIONS,
    MESSAGE_SUCCESS_ORGANIZED,
    MESSAGE_SUCCESS_REVERTED,
)
from src.models.file_organizer_model import FileOrganizerModel


class TestFileOrganizerModelInit:
    def test_sets_path(self, tmp_path: Path) -> None:
        model: FileOrganizerModel = FileOrganizerModel(path=str(tmp_path))
        assert model.path == str(tmp_path)

    def test_default_folder_name(self, tmp_path: Path) -> None:
        model: FileOrganizerModel = FileOrganizerModel(path=str(tmp_path))
        assert model.folder_name == "ORGANIZER"

    def test_custom_folder_name(self, tmp_path: Path) -> None:
        model: FileOrganizerModel = FileOrganizerModel(path=str(tmp_path), folder_name="CUSTOM")
        assert model.folder_name == "CUSTOM"

    def test_default_extensions_allowed_empty(self, tmp_path: Path) -> None:
        model: FileOrganizerModel = FileOrganizerModel(path=str(tmp_path))
        assert model.extensions_allowed == []

    def test_custom_extensions_allowed(self, tmp_path: Path) -> None:
        model: FileOrganizerModel = FileOrganizerModel(path=str(tmp_path), extensions_allowed=["pdf", "txt"])
        assert model.extensions_allowed == ["pdf", "txt"]

    def test_filters_initially_empty(self, tmp_path: Path) -> None:
        model: FileOrganizerModel = FileOrganizerModel(path=str(tmp_path))
        assert model.filters == {}

    def test_all_path_extensions_empty_dir(self, tmp_path: Path) -> None:
        model: FileOrganizerModel = FileOrganizerModel(path=str(tmp_path))
        assert model.all_path_extensions == []

    def test_all_path_extensions_with_files(self, tmp_path: Path) -> None:
        (tmp_path / "doc.pdf").write_text("content")
        (tmp_path / "image.png").write_text("content")
        model: FileOrganizerModel = FileOrganizerModel(path=str(tmp_path))
        assert set(model.all_path_extensions) == {"pdf", "png"}

    def test_all_path_extensions_no_duplicates(self, tmp_path: Path) -> None:
        (tmp_path / "a.pdf").write_text("content")
        (tmp_path / "b.pdf").write_text("content")
        model: FileOrganizerModel = FileOrganizerModel(path=str(tmp_path))
        assert model.all_path_extensions.count("pdf") == 1


class TestFileOrganizerModelOrganizer:
    def test_empty_dir_returns_false(self, tmp_path: Path) -> None:
        model: FileOrganizerModel = FileOrganizerModel(path=str(tmp_path))
        message, success = model.organizer()
        assert success is False
        assert message == MESSAGE_NOT_FOUND_PATH_OR_EXTENSIONS

    def test_with_files_returns_true(self, tmp_path: Path) -> None:
        (tmp_path / "doc.pdf").write_text("content")
        model: FileOrganizerModel = FileOrganizerModel(path=str(tmp_path))
        message, success = model.organizer()
        assert success is True
        assert message == MESSAGE_SUCCESS_ORGANIZED

    def test_creates_organizer_folder(self, tmp_path: Path) -> None:
        (tmp_path / "doc.pdf").write_text("content")
        model: FileOrganizerModel = FileOrganizerModel(path=str(tmp_path))
        model.organizer()
        assert os.path.isdir(str(tmp_path / "PDF_ORGANIZER"))

    def test_moves_file_to_folder(self, tmp_path: Path) -> None:
        (tmp_path / "doc.pdf").write_text("content")
        model: FileOrganizerModel = FileOrganizerModel(path=str(tmp_path))
        model.organizer()
        assert os.path.isfile(str(tmp_path / "PDF_ORGANIZER" / "doc.pdf"))
        assert not os.path.isfile(str(tmp_path / "doc.pdf"))

    def test_with_extensions_allowed_only_moves_matching(self, tmp_path: Path) -> None:
        (tmp_path / "doc.pdf").write_text("content")
        (tmp_path / "image.png").write_text("content")
        model: FileOrganizerModel = FileOrganizerModel(path=str(tmp_path), extensions_allowed=["pdf"])
        model.organizer()
        assert os.path.isdir(str(tmp_path / "PDF_ORGANIZER"))
        assert not os.path.isdir(str(tmp_path / "PNG_ORGANIZER"))
        assert os.path.isfile(str(tmp_path / "image.png"))

    def test_no_matching_files_returns_false(self, tmp_path: Path) -> None:
        (tmp_path / "doc.pdf").write_text("content")
        model: FileOrganizerModel = FileOrganizerModel(path=str(tmp_path), extensions_allowed=["txt"])
        message, success = model.organizer()
        assert success is False
        assert message == MESSAGE_NOT_FOUND_PATH_OR_EXTENSIONS

    def test_multiple_extensions_organized(self, tmp_path: Path) -> None:
        (tmp_path / "doc.pdf").write_text("content")
        (tmp_path / "track.mp3").write_text("content")
        model: FileOrganizerModel = FileOrganizerModel(path=str(tmp_path))
        model.organizer()
        assert os.path.isdir(str(tmp_path / "PDF_ORGANIZER"))
        assert os.path.isdir(str(tmp_path / "MP3_ORGANIZER"))

    def test_existing_organizer_folder_not_recreated(self, tmp_path: Path) -> None:
        (tmp_path / "doc.pdf").write_text("content")
        os.mkdir(str(tmp_path / "PDF_ORGANIZER"))
        model: FileOrganizerModel = FileOrganizerModel(path=str(tmp_path))
        model.organizer()
        assert os.path.isdir(str(tmp_path / "PDF_ORGANIZER"))


class TestFileOrganizerModelRevert:
    def test_no_organizer_folders_returns_false(self, tmp_path: Path) -> None:
        model: FileOrganizerModel = FileOrganizerModel(path=str(tmp_path))
        message, success = model.revert_organizer()
        assert success is False
        assert message == MESSAGE_NOT_FOUND_FOLDERS

    def test_after_organize_returns_true(self, tmp_path: Path) -> None:
        (tmp_path / "doc.pdf").write_text("content")
        model: FileOrganizerModel = FileOrganizerModel(path=str(tmp_path))
        model.organizer()
        message, success = model.revert_organizer()
        assert success is True
        assert message == MESSAGE_SUCCESS_REVERTED

    def test_restores_file_to_root(self, tmp_path: Path) -> None:
        (tmp_path / "doc.pdf").write_text("content")
        model: FileOrganizerModel = FileOrganizerModel(path=str(tmp_path))
        model.organizer()
        model.revert_organizer()
        assert os.path.isfile(str(tmp_path / "doc.pdf"))

    def test_removes_organizer_folder(self, tmp_path: Path) -> None:
        (tmp_path / "doc.pdf").write_text("content")
        model: FileOrganizerModel = FileOrganizerModel(path=str(tmp_path))
        model.organizer()
        model.revert_organizer()
        assert not os.path.isdir(str(tmp_path / "PDF_ORGANIZER"))

    def test_empty_organizer_folder_is_removed(self, tmp_path: Path) -> None:
        os.mkdir(str(tmp_path / "PDF_ORGANIZER"))
        model: FileOrganizerModel = FileOrganizerModel(path=str(tmp_path))
        message, success = model.revert_organizer()
        assert success is True
        assert not os.path.isdir(str(tmp_path / "PDF_ORGANIZER"))

    def test_revert_resets_filters(self, tmp_path: Path) -> None:
        (tmp_path / "doc.pdf").write_text("content")
        model: FileOrganizerModel = FileOrganizerModel(path=str(tmp_path))
        model.organizer()
        model.filters = {"min_size": 1, "max_size": 10}
        model.revert_organizer()
        assert model.filters == {}


class TestFileOrganizerModelGetFiles:
    def test_empty_dir_returns_empty_list(self, tmp_path: Path) -> None:
        model: FileOrganizerModel = FileOrganizerModel(path=str(tmp_path))
        assert model._get_files() == []

    def test_excludes_subdirectories(self, tmp_path: Path) -> None:
        (tmp_path / "doc.pdf").write_text("content")
        os.mkdir(str(tmp_path / "subdir"))
        model: FileOrganizerModel = FileOrganizerModel(path=str(tmp_path))
        files: list[str] = model._get_files()
        assert "subdir" not in files
        assert "doc.pdf" in files

    def test_filters_by_extension(self, tmp_path: Path) -> None:
        (tmp_path / "doc.pdf").write_text("content")
        (tmp_path / "image.png").write_text("content")
        model: FileOrganizerModel = FileOrganizerModel(path=str(tmp_path), extensions_allowed=["pdf"])
        files: list[str] = model._get_files()
        assert "doc.pdf" in files
        assert "image.png" not in files

    def test_size_filter_excludes_oversized_file(self, tmp_path: Path) -> None:
        large: Path = tmp_path / "big.txt"
        large.write_bytes(b"x" * (2 * 1024 * 1024))
        model: FileOrganizerModel = FileOrganizerModel(path=str(tmp_path))
        model.filters = {"min_size": 0, "max_size": 1}
        files: list[str] = model._get_files()
        assert "big.txt" not in files

    def test_size_filter_includes_file_in_range(self, tmp_path: Path) -> None:
        medium: Path = tmp_path / "medium.txt"
        medium.write_bytes(b"x" * (512 * 1024))
        model: FileOrganizerModel = FileOrganizerModel(path=str(tmp_path))
        model.filters = {"min_size": 0, "max_size": 1}
        files: list[str] = model._get_files()
        assert "medium.txt" in files

    def test_size_filter_with_extension_filter(self, tmp_path: Path) -> None:
        (tmp_path / "doc.pdf").write_bytes(b"x" * (512 * 1024))
        (tmp_path / "image.png").write_bytes(b"x" * (512 * 1024))
        model: FileOrganizerModel = FileOrganizerModel(path=str(tmp_path), extensions_allowed=["pdf"])
        model.filters = {"min_size": 0, "max_size": 1}
        files: list[str] = model._get_files()
        assert "doc.pdf" in files
        assert "image.png" not in files


class TestFileOrganizerModelGetExtensions:
    def test_empty_files_returns_empty(self, tmp_path: Path) -> None:
        model: FileOrganizerModel = FileOrganizerModel(path=str(tmp_path))
        assert model._get_extensions(files=[]) == []

    def test_single_file(self, tmp_path: Path) -> None:
        model: FileOrganizerModel = FileOrganizerModel(path=str(tmp_path))
        result: list[str] = model._get_extensions(files=["doc.pdf"])
        assert result == ["pdf"]

    def test_no_duplicate_extensions(self, tmp_path: Path) -> None:
        model: FileOrganizerModel = FileOrganizerModel(path=str(tmp_path))
        result: list[str] = model._get_extensions(files=["a.pdf", "b.pdf", "c.png"])
        assert set(result) == {"pdf", "png"}
        assert len(result) == 2

    def test_multiple_different_extensions(self, tmp_path: Path) -> None:
        model: FileOrganizerModel = FileOrganizerModel(path=str(tmp_path))
        result: list[str] = model._get_extensions(files=["a.pdf", "b.mp3", "c.txt"])
        assert set(result) == {"pdf", "mp3", "txt"}


class TestFileOrganizerModelStr:
    def test_str_contains_path(self, tmp_path: Path) -> None:
        model: FileOrganizerModel = FileOrganizerModel(path=str(tmp_path))
        assert str(tmp_path) in str(model)

    def test_str_contains_folder_name(self, tmp_path: Path) -> None:
        model: FileOrganizerModel = FileOrganizerModel(path=str(tmp_path))
        assert "ORGANIZER" in str(model)

    def test_print_path_does_not_raise(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        model: FileOrganizerModel = FileOrganizerModel(path=str(tmp_path))
        model.print_path()
        captured = capsys.readouterr()
        assert str(tmp_path) in captured.out
