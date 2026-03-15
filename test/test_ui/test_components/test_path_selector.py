from tkinter import StringVar
from unittest.mock import MagicMock, patch

import pytest

from src.ui.components.path_selector import PathSelector


@pytest.fixture
def path_selector(mock_styles: MagicMock, mock_on_search: MagicMock) -> PathSelector:
    with (
        patch("src.ui.components.path_selector.Frame.__init__", return_value=None),
        patch("src.ui.components.path_selector.Entry"),
        patch("src.ui.components.path_selector.Button"),
        patch("src.ui.components.path_selector.StringVar") as mock_sv,
        patch.object(PathSelector, "columnconfigure"),
    ):
        mock_sv.return_value = MagicMock(spec=StringVar)
        instance: PathSelector = PathSelector.__new__(PathSelector)
        instance._styles = mock_styles
        instance._on_search = mock_on_search
        instance._text_path = mock_sv.return_value
        return instance


class TestPathSelectorInit:
    def test_stores_styles(self, mock_styles: MagicMock, mock_on_search: MagicMock) -> None:
        with (
            patch("src.ui.components.path_selector.Frame.__init__", return_value=None),
            patch("src.ui.components.path_selector.Entry") as mock_entry,
            patch("src.ui.components.path_selector.Button") as mock_button,
            patch("src.ui.components.path_selector.StringVar"),
            patch.object(PathSelector, "columnconfigure"),
        ):
            mock_entry.return_value.grid = MagicMock()
            mock_button.return_value.grid = MagicMock()
            instance: PathSelector = PathSelector.__new__(PathSelector)
            PathSelector.__init__(instance, parent=MagicMock(), styles=mock_styles, on_search=mock_on_search)
        assert instance._styles is mock_styles

    def test_stores_on_search(self, mock_styles: MagicMock, mock_on_search: MagicMock) -> None:
        with (
            patch("src.ui.components.path_selector.Frame.__init__", return_value=None),
            patch("src.ui.components.path_selector.Entry") as mock_entry,
            patch("src.ui.components.path_selector.Button") as mock_button,
            patch("src.ui.components.path_selector.StringVar"),
            patch.object(PathSelector, "columnconfigure"),
        ):
            mock_entry.return_value.grid = MagicMock()
            mock_button.return_value.grid = MagicMock()
            instance: PathSelector = PathSelector.__new__(PathSelector)
            PathSelector.__init__(instance, parent=MagicMock(), styles=mock_styles, on_search=mock_on_search)
        assert instance._on_search is mock_on_search

    def test_entry_initial_value_is_wait_for_directory(self, mock_styles: MagicMock, mock_on_search: MagicMock) -> None:
        captured: list[str] = []

        def capture_sv(value: str = "") -> MagicMock:
            captured.append(value)
            return MagicMock(spec=StringVar)

        with (
            patch("src.ui.components.path_selector.Frame.__init__", return_value=None),
            patch("src.ui.components.path_selector.Entry") as mock_entry,
            patch("src.ui.components.path_selector.Button") as mock_button,
            patch("src.ui.components.path_selector.StringVar", side_effect=capture_sv),
            patch.object(PathSelector, "columnconfigure"),
        ):
            mock_entry.return_value.grid = MagicMock()
            mock_button.return_value.grid = MagicMock()
            instance: PathSelector = PathSelector.__new__(PathSelector)
            PathSelector.__init__(instance, parent=MagicMock(), styles=mock_styles, on_search=mock_on_search)
        assert "Wait for directory..." in captured

    def test_search_button_command_is_on_search(self, mock_styles: MagicMock, mock_on_search: MagicMock) -> None:
        with (
            patch("src.ui.components.path_selector.Frame.__init__", return_value=None),
            patch("src.ui.components.path_selector.Entry") as mock_entry,
            patch("src.ui.components.path_selector.Button") as mock_button,
            patch("src.ui.components.path_selector.StringVar"),
            patch.object(PathSelector, "columnconfigure"),
        ):
            mock_entry.return_value.grid = MagicMock()
            mock_button.return_value.grid = MagicMock()
            instance: PathSelector = PathSelector.__new__(PathSelector)
            PathSelector.__init__(instance, parent=MagicMock(), styles=mock_styles, on_search=mock_on_search)
        _, kwargs = mock_button.call_args
        assert kwargs.get("command") is mock_on_search

    def test_entry_state_is_disabled(self, mock_styles: MagicMock, mock_on_search: MagicMock) -> None:
        with (
            patch("src.ui.components.path_selector.Frame.__init__", return_value=None),
            patch("src.ui.components.path_selector.Entry") as mock_entry,
            patch("src.ui.components.path_selector.Button") as mock_button,
            patch("src.ui.components.path_selector.StringVar"),
            patch.object(PathSelector, "columnconfigure"),
        ):
            mock_entry.return_value.grid = MagicMock()
            mock_button.return_value.grid = MagicMock()
            instance: PathSelector = PathSelector.__new__(PathSelector)
            PathSelector.__init__(instance, parent=MagicMock(), styles=mock_styles, on_search=mock_on_search)
        _, kwargs = mock_entry.call_args
        assert kwargs.get("state") == mock_styles.STATE_DISABLED

    def test_columnconfigure_called_twice(self, mock_styles: MagicMock, mock_on_search: MagicMock) -> None:
        with (
            patch("src.ui.components.path_selector.Frame.__init__", return_value=None),
            patch("src.ui.components.path_selector.Entry") as mock_entry,
            patch("src.ui.components.path_selector.Button") as mock_button,
            patch("src.ui.components.path_selector.StringVar"),
            patch.object(PathSelector, "columnconfigure") as mock_col,
        ):
            mock_entry.return_value.grid = MagicMock()
            mock_button.return_value.grid = MagicMock()
            instance: PathSelector = PathSelector.__new__(PathSelector)
            PathSelector.__init__(instance, parent=MagicMock(), styles=mock_styles, on_search=mock_on_search)
        assert mock_col.call_count == 2


class TestPathSelectorSetPath:
    def test_set_path_updates_text_path(self, path_selector: PathSelector) -> None:
        path_selector.set_path("/new/path")
        path_selector._text_path.set.assert_called_once_with("/new/path")

    def test_set_path_with_empty_string(self, path_selector: PathSelector) -> None:
        path_selector.set_path("")
        path_selector._text_path.set.assert_called_once_with("")
