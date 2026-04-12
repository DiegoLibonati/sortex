import tkinter as tk

from src.ui.components.extensions_selector import ExtensionsSelector
from src.ui.styles import Styles


class TestExtensionsSelector:
    def test_instantiation(self, root: tk.Tk) -> None:
        widget: ExtensionsSelector = ExtensionsSelector(parent=root, styles=Styles())
        assert widget is not None

    def test_is_frame(self, root: tk.Tk) -> None:
        widget: ExtensionsSelector = ExtensionsSelector(parent=root, styles=Styles())
        assert isinstance(widget, tk.Frame)

    def test_check_value_all_default_true(self, root: tk.Tk) -> None:
        widget: ExtensionsSelector = ExtensionsSelector(parent=root, styles=Styles())
        assert widget._check_value_all.get() is True

    def test_all_extension_vars_default_true(self, root: tk.Tk) -> None:
        widget: ExtensionsSelector = ExtensionsSelector(parent=root, styles=Styles())
        for var in widget._extensions_options.values():
            assert var.get() is True

    def test_known_extensions_present(self, root: tk.Tk) -> None:
        widget: ExtensionsSelector = ExtensionsSelector(parent=root, styles=Styles())
        expected: list[str] = ["mp4", "pdf", "exe", "png", "jpg", "jpeg", "txt", "json", "mp3", "m3u8", "zip", "gif"]
        for ext in expected:
            assert ext in widget._extensions_options

    def test_extensions_options_count(self, root: tk.Tk) -> None:
        widget: ExtensionsSelector = ExtensionsSelector(parent=root, styles=Styles())
        assert len(widget._extensions_options) == 12

    def test_get_selected_extensions_returns_all_by_default(self, root: tk.Tk) -> None:
        widget: ExtensionsSelector = ExtensionsSelector(parent=root, styles=Styles())
        selected: list[str] = widget.get_selected_extensions()
        assert len(selected) == 12

    def test_get_selected_extensions_empty_when_none_checked(self, root: tk.Tk) -> None:
        widget: ExtensionsSelector = ExtensionsSelector(parent=root, styles=Styles())
        for var in widget._extensions_options.values():
            var.set(False)
        selected: list[str] = widget.get_selected_extensions()
        assert selected == []

    def test_get_selected_extensions_partial(self, root: tk.Tk) -> None:
        widget: ExtensionsSelector = ExtensionsSelector(parent=root, styles=Styles())
        for var in widget._extensions_options.values():
            var.set(False)
        widget._extensions_options["pdf"].set(True)
        widget._extensions_options["mp3"].set(True)
        selected: list[str] = widget.get_selected_extensions()
        assert set(selected) == {"pdf", "mp3"}

    def test_select_all_extensions_unchecks_all(self, root: tk.Tk) -> None:
        widget: ExtensionsSelector = ExtensionsSelector(parent=root, styles=Styles())
        widget._check_value_all.set(False)
        widget._select_all_extensions()
        for var in widget._extensions_options.values():
            assert var.get() is False

    def test_select_all_extensions_checks_all(self, root: tk.Tk) -> None:
        widget: ExtensionsSelector = ExtensionsSelector(parent=root, styles=Styles())
        for var in widget._extensions_options.values():
            var.set(False)
        widget._check_value_all.set(True)
        widget._select_all_extensions()
        for var in widget._extensions_options.values():
            assert var.get() is True

    def test_select_extension_unchecks_all_checkbox(self, root: tk.Tk) -> None:
        widget: ExtensionsSelector = ExtensionsSelector(parent=root, styles=Styles())
        widget._select_extension()
        assert widget._check_value_all.get() is False

    def test_check_value_all_is_boolean_var(self, root: tk.Tk) -> None:
        widget: ExtensionsSelector = ExtensionsSelector(parent=root, styles=Styles())
        assert isinstance(widget._check_value_all, tk.BooleanVar)
