import tkinter as tk
from unittest.mock import MagicMock

from src.ui.components.path_selector import PathSelector
from src.ui.styles import Styles


class TestPathSelector:
    def test_instantiation(self, root: tk.Tk) -> None:
        widget: PathSelector = PathSelector(
            parent=root,
            styles=Styles(),
            on_search=MagicMock(),
        )
        assert widget is not None

    def test_is_frame(self, root: tk.Tk) -> None:
        widget: PathSelector = PathSelector(
            parent=root,
            styles=Styles(),
            on_search=MagicMock(),
        )
        assert isinstance(widget, tk.Frame)

    def test_default_text_path_value(self, root: tk.Tk) -> None:
        widget: PathSelector = PathSelector(
            parent=root,
            styles=Styles(),
            on_search=MagicMock(),
        )
        assert widget._text_path.get() == "Wait for directory..."

    def test_set_path_updates_string_var(self, root: tk.Tk) -> None:
        widget: PathSelector = PathSelector(
            parent=root,
            styles=Styles(),
            on_search=MagicMock(),
        )
        widget.set_path("/some/directory")
        assert widget._text_path.get() == "/some/directory"

    def test_set_path_replaces_previous_value(self, root: tk.Tk) -> None:
        widget: PathSelector = PathSelector(
            parent=root,
            styles=Styles(),
            on_search=MagicMock(),
        )
        widget.set_path("/first/path")
        widget.set_path("/second/path")
        assert widget._text_path.get() == "/second/path"

    def test_on_search_stored(self, root: tk.Tk) -> None:
        search_cb: MagicMock = MagicMock()
        widget: PathSelector = PathSelector(
            parent=root,
            styles=Styles(),
            on_search=search_cb,
        )
        assert widget._on_search is search_cb

    def test_text_path_is_string_var(self, root: tk.Tk) -> None:
        widget: PathSelector = PathSelector(
            parent=root,
            styles=Styles(),
            on_search=MagicMock(),
        )
        assert isinstance(widget._text_path, tk.StringVar)
