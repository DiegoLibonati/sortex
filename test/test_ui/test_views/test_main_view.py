from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from src.ui.views.main_view import MainView


@pytest.fixture
def main_view(mock_root: MagicMock, mock_styles: MagicMock, mock_on_search: MagicMock, mock_on_organize: MagicMock, mock_on_revert: MagicMock) -> MainView:
    with (
        patch("src.ui.views.main_view.Frame.__init__", return_value=None),
        patch("src.ui.views.main_view.PathSelector"),
        patch("src.ui.views.main_view.ActionButtons"),
        patch("src.ui.views.main_view.ExtensionsSelector"),
        patch("src.ui.views.main_view.FiltersSelector"),
        patch.object(MainView, "columnconfigure"),
    ):
        instance: MainView = MainView.__new__(MainView)
        instance._styles = mock_styles
        instance._on_search = mock_on_search
        instance._on_organize = mock_on_organize
        instance._on_revert = mock_on_revert
        instance._path_selector = MagicMock()
        instance._extensions_selector = MagicMock()
        instance._filters_selector = MagicMock()
        return instance


class TestMainViewInit:
    def test_stores_styles(
        self, mock_root: MagicMock, mock_styles: MagicMock, mock_on_search: MagicMock, mock_on_organize: MagicMock, mock_on_revert: MagicMock
    ) -> None:
        with (
            patch("src.ui.views.main_view.Frame.__init__", return_value=None),
            patch("src.ui.views.main_view.PathSelector") as mock_ps,
            patch("src.ui.views.main_view.ActionButtons") as mock_ab,
            patch("src.ui.views.main_view.ExtensionsSelector") as mock_es,
            patch("src.ui.views.main_view.FiltersSelector") as mock_fs,
            patch.object(MainView, "columnconfigure"),
        ):
            for m in [mock_ps, mock_ab, mock_es, mock_fs]:
                m.return_value.grid = MagicMock()
            instance: MainView = MainView.__new__(MainView)
            MainView.__init__(instance, root=mock_root, styles=mock_styles, on_search=mock_on_search, on_organize=mock_on_organize, on_revert=mock_on_revert)
        assert instance._styles is mock_styles

    def test_stores_on_search(
        self, mock_root: MagicMock, mock_styles: MagicMock, mock_on_search: MagicMock, mock_on_organize: MagicMock, mock_on_revert: MagicMock
    ) -> None:
        with (
            patch("src.ui.views.main_view.Frame.__init__", return_value=None),
            patch("src.ui.views.main_view.PathSelector") as mock_ps,
            patch("src.ui.views.main_view.ActionButtons") as mock_ab,
            patch("src.ui.views.main_view.ExtensionsSelector") as mock_es,
            patch("src.ui.views.main_view.FiltersSelector") as mock_fs,
            patch.object(MainView, "columnconfigure"),
        ):
            for m in [mock_ps, mock_ab, mock_es, mock_fs]:
                m.return_value.grid = MagicMock()
            instance: MainView = MainView.__new__(MainView)
            MainView.__init__(instance, root=mock_root, styles=mock_styles, on_search=mock_on_search, on_organize=mock_on_organize, on_revert=mock_on_revert)
        assert instance._on_search is mock_on_search

    def test_path_selector_receives_on_search(
        self, mock_root: MagicMock, mock_styles: MagicMock, mock_on_search: MagicMock, mock_on_organize: MagicMock, mock_on_revert: MagicMock
    ) -> None:
        with (
            patch("src.ui.views.main_view.Frame.__init__", return_value=None),
            patch("src.ui.views.main_view.PathSelector") as mock_ps,
            patch("src.ui.views.main_view.ActionButtons") as mock_ab,
            patch("src.ui.views.main_view.ExtensionsSelector") as mock_es,
            patch("src.ui.views.main_view.FiltersSelector") as mock_fs,
            patch.object(MainView, "columnconfigure"),
        ):
            for m in [mock_ps, mock_ab, mock_es, mock_fs]:
                m.return_value.grid = MagicMock()
            instance: MainView = MainView.__new__(MainView)
            MainView.__init__(instance, root=mock_root, styles=mock_styles, on_search=mock_on_search, on_organize=mock_on_organize, on_revert=mock_on_revert)
        _, kwargs = mock_ps.call_args
        assert kwargs.get("on_search") is mock_on_search

    def test_action_buttons_receives_on_organize_and_on_revert(
        self, mock_root: MagicMock, mock_styles: MagicMock, mock_on_search: MagicMock, mock_on_organize: MagicMock, mock_on_revert: MagicMock
    ) -> None:
        with (
            patch("src.ui.views.main_view.Frame.__init__", return_value=None),
            patch("src.ui.views.main_view.PathSelector") as mock_ps,
            patch("src.ui.views.main_view.ActionButtons") as mock_ab,
            patch("src.ui.views.main_view.ExtensionsSelector") as mock_es,
            patch("src.ui.views.main_view.FiltersSelector") as mock_fs,
            patch.object(MainView, "columnconfigure"),
        ):
            for m in [mock_ps, mock_ab, mock_es, mock_fs]:
                m.return_value.grid = MagicMock()
            instance: MainView = MainView.__new__(MainView)
            MainView.__init__(instance, root=mock_root, styles=mock_styles, on_search=mock_on_search, on_organize=mock_on_organize, on_revert=mock_on_revert)
        _, kwargs = mock_ab.call_args
        assert kwargs.get("on_organize") is mock_on_organize
        assert kwargs.get("on_revert") is mock_on_revert


class TestMainViewSetPath:
    def test_delegates_to_path_selector(self, main_view: MainView) -> None:
        main_view.set_path("/some/path")
        main_view._path_selector.set_path.assert_called_once_with("/some/path")


class TestMainViewGetSelectedExtensions:
    def test_delegates_to_extensions_selector(self, main_view: MainView) -> None:
        main_view._extensions_selector.get_selected_extensions.return_value = ["txt", "pdf"]
        result: list[str] = main_view.get_selected_extensions()
        assert result == ["txt", "pdf"]
        main_view._extensions_selector.get_selected_extensions.assert_called_once()


class TestMainViewGetFilters:
    def test_delegates_to_filters_selector(self, main_view: MainView) -> None:
        main_view._filters_selector.get_filters.return_value = {"min_size": 1, "max_size": 10}
        result: dict[str, Any] = main_view.get_filters()
        assert result == {"min_size": 1, "max_size": 10}
        main_view._filters_selector.get_filters.assert_called_once()
