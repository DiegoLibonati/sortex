import tkinter as tk
from typing import Any
from unittest.mock import MagicMock

from src.ui.styles import Styles
from src.ui.views.main_view import MainView


class TestMainView:
    def test_instantiation(self, root: tk.Tk) -> None:
        widget: MainView = MainView(
            root=root,
            styles=Styles(),
            on_search=MagicMock(),
            on_organize=MagicMock(),
            on_revert=MagicMock(),
        )
        assert widget is not None

    def test_is_frame(self, root: tk.Tk) -> None:
        widget: MainView = MainView(
            root=root,
            styles=Styles(),
            on_search=MagicMock(),
            on_organize=MagicMock(),
            on_revert=MagicMock(),
        )
        assert isinstance(widget, tk.Frame)

    def test_callbacks_stored(self, root: tk.Tk) -> None:
        search_cb: MagicMock = MagicMock()
        organize_cb: MagicMock = MagicMock()
        revert_cb: MagicMock = MagicMock()
        widget: MainView = MainView(
            root=root,
            styles=Styles(),
            on_search=search_cb,
            on_organize=organize_cb,
            on_revert=revert_cb,
        )
        assert widget._on_search is search_cb
        assert widget._on_organize is organize_cb
        assert widget._on_revert is revert_cb

    def test_set_path_updates_path_selector(self, root: tk.Tk) -> None:
        widget: MainView = MainView(
            root=root,
            styles=Styles(),
            on_search=MagicMock(),
            on_organize=MagicMock(),
            on_revert=MagicMock(),
        )
        widget.set_path("/test/path")
        assert widget._path_selector._text_path.get() == "/test/path"

    def test_get_selected_extensions_returns_all_by_default(self, root: tk.Tk) -> None:
        widget: MainView = MainView(
            root=root,
            styles=Styles(),
            on_search=MagicMock(),
            on_organize=MagicMock(),
            on_revert=MagicMock(),
        )
        extensions: list[str] = widget.get_selected_extensions()
        assert len(extensions) == 12

    def test_get_filters_default_returns_empty(self, root: tk.Tk) -> None:
        widget: MainView = MainView(
            root=root,
            styles=Styles(),
            on_search=MagicMock(),
            on_organize=MagicMock(),
            on_revert=MagicMock(),
        )
        filters: dict[str, Any] = widget.get_filters()
        assert filters == {}

    def test_get_filters_when_enabled(self, root: tk.Tk) -> None:
        widget: MainView = MainView(
            root=root,
            styles=Styles(),
            on_search=MagicMock(),
            on_organize=MagicMock(),
            on_revert=MagicMock(),
        )
        widget._filters_selector._check_value_filters.set(True)
        filters: dict[str, Any] = widget.get_filters()
        assert "min_size" in filters
        assert "max_size" in filters

    def test_sub_components_initialized(self, root: tk.Tk) -> None:
        widget: MainView = MainView(
            root=root,
            styles=Styles(),
            on_search=MagicMock(),
            on_organize=MagicMock(),
            on_revert=MagicMock(),
        )
        assert widget._path_selector is not None
        assert widget._action_buttons is not None
        assert widget._extensions_selector is not None
        assert widget._filters_selector is not None
