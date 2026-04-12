import tkinter as tk
from typing import Any

from src.ui.components.filters_selector import FiltersSelector
from src.ui.styles import Styles


class TestFiltersSelector:
    def test_instantiation(self, root: tk.Tk) -> None:
        widget: FiltersSelector = FiltersSelector(parent=root, styles=Styles())
        assert widget is not None

    def test_is_frame(self, root: tk.Tk) -> None:
        widget: FiltersSelector = FiltersSelector(parent=root, styles=Styles())
        assert isinstance(widget, tk.Frame)

    def test_check_value_filters_default_false(self, root: tk.Tk) -> None:
        widget: FiltersSelector = FiltersSelector(parent=root, styles=Styles())
        assert widget._check_value_filters.get() is False

    def test_filter_min_size_default(self, root: tk.Tk) -> None:
        widget: FiltersSelector = FiltersSelector(parent=root, styles=Styles())
        assert widget._filter_min_size.get() == 1

    def test_filter_max_size_default(self, root: tk.Tk) -> None:
        widget: FiltersSelector = FiltersSelector(parent=root, styles=Styles())
        assert widget._filter_max_size.get() == 10

    def test_get_filters_unchecked_returns_empty_dict(self, root: tk.Tk) -> None:
        widget: FiltersSelector = FiltersSelector(parent=root, styles=Styles())
        result: dict[str, Any] = widget.get_filters()
        assert result == {}

    def test_get_filters_checked_returns_default_values(self, root: tk.Tk) -> None:
        widget: FiltersSelector = FiltersSelector(parent=root, styles=Styles())
        widget._check_value_filters.set(True)
        result: dict[str, Any] = widget.get_filters()
        assert result == {"min_size": 1, "max_size": 10}

    def test_get_filters_checked_with_custom_values(self, root: tk.Tk) -> None:
        widget: FiltersSelector = FiltersSelector(parent=root, styles=Styles())
        widget._check_value_filters.set(True)
        widget._filter_min_size.set(5)
        widget._filter_max_size.set(50)
        result: dict[str, Any] = widget.get_filters()
        assert result == {"min_size": 5, "max_size": 50}

    def test_handle_filters_enables_entries_when_checked(self, root: tk.Tk) -> None:
        widget: FiltersSelector = FiltersSelector(parent=root, styles=Styles())
        widget._check_value_filters.set(True)
        widget._handle_filters()
        assert str(widget._entry_min_size.cget("state")) == "normal"
        assert str(widget._entry_max_size.cget("state")) == "normal"

    def test_handle_filters_disables_entries_when_unchecked(self, root: tk.Tk) -> None:
        widget: FiltersSelector = FiltersSelector(parent=root, styles=Styles())
        widget._check_value_filters.set(False)
        widget._handle_filters()
        assert str(widget._entry_min_size.cget("state")) == "disabled"
        assert str(widget._entry_max_size.cget("state")) == "disabled"

    def test_check_value_filters_is_boolean_var(self, root: tk.Tk) -> None:
        widget: FiltersSelector = FiltersSelector(parent=root, styles=Styles())
        assert isinstance(widget._check_value_filters, tk.BooleanVar)

    def test_filter_min_size_is_int_var(self, root: tk.Tk) -> None:
        widget: FiltersSelector = FiltersSelector(parent=root, styles=Styles())
        assert isinstance(widget._filter_min_size, tk.IntVar)

    def test_filter_max_size_is_int_var(self, root: tk.Tk) -> None:
        widget: FiltersSelector = FiltersSelector(parent=root, styles=Styles())
        assert isinstance(widget._filter_max_size, tk.IntVar)
