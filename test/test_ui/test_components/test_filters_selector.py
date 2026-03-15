from tkinter import BooleanVar, IntVar
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from src.ui.components.filters_selector import FiltersSelector


@pytest.fixture
def filters_selector(mock_styles: MagicMock) -> FiltersSelector:
    with (
        patch("src.ui.components.filters_selector.Frame.__init__", return_value=None),
        patch("src.ui.components.filters_selector.LabelFrame"),
        patch("src.ui.components.filters_selector.Checkbutton"),
        patch("src.ui.components.filters_selector.Label"),
        patch("src.ui.components.filters_selector.Entry"),
        patch("src.ui.components.filters_selector.BooleanVar"),
        patch("src.ui.components.filters_selector.IntVar"),
    ):
        instance: FiltersSelector = FiltersSelector.__new__(FiltersSelector)
        instance._styles = mock_styles
        instance._check_value_filters = MagicMock(spec=BooleanVar)
        instance._filter_min_size = MagicMock(spec=IntVar)
        instance._filter_max_size = MagicMock(spec=IntVar)
        instance._entry_min_size = MagicMock()
        instance._entry_max_size = MagicMock()
        return instance


class TestFiltersSelectorInit:
    def test_stores_styles(self, mock_styles: MagicMock) -> None:
        with (
            patch("src.ui.components.filters_selector.Frame.__init__", return_value=None),
            patch("src.ui.components.filters_selector.LabelFrame") as mock_lf,
            patch("src.ui.components.filters_selector.Checkbutton") as mock_cb,
            patch("src.ui.components.filters_selector.Label") as mock_label,
            patch("src.ui.components.filters_selector.Entry") as mock_entry,
            patch("src.ui.components.filters_selector.BooleanVar"),
            patch("src.ui.components.filters_selector.IntVar"),
        ):
            mock_lf.return_value.grid = MagicMock()
            mock_cb.return_value.grid = MagicMock()
            mock_label.return_value.grid = MagicMock()
            mock_entry.return_value.grid = MagicMock()
            instance: FiltersSelector = FiltersSelector.__new__(FiltersSelector)
            FiltersSelector.__init__(instance, parent=MagicMock(), styles=mock_styles)
        assert instance._styles is mock_styles

    def test_check_value_filters_initial_is_false(self, mock_styles: MagicMock) -> None:
        captured: list[bool] = []

        def capture_bv(value: bool = False) -> MagicMock:
            captured.append(value)
            return MagicMock(spec=BooleanVar)

        with (
            patch("src.ui.components.filters_selector.Frame.__init__", return_value=None),
            patch("src.ui.components.filters_selector.LabelFrame") as mock_lf,
            patch("src.ui.components.filters_selector.Checkbutton") as mock_cb,
            patch("src.ui.components.filters_selector.Label") as mock_label,
            patch("src.ui.components.filters_selector.Entry") as mock_entry,
            patch("src.ui.components.filters_selector.BooleanVar", side_effect=capture_bv),
            patch("src.ui.components.filters_selector.IntVar"),
        ):
            mock_lf.return_value.grid = MagicMock()
            mock_cb.return_value.grid = MagicMock()
            mock_label.return_value.grid = MagicMock()
            mock_entry.return_value.grid = MagicMock()
            instance: FiltersSelector = FiltersSelector.__new__(FiltersSelector)
            FiltersSelector.__init__(instance, parent=MagicMock(), styles=mock_styles)
        assert False in captured


class TestFiltersSelectorHandleFilters:
    def test_entries_enabled_when_filter_checked(self, filters_selector: FiltersSelector) -> None:
        filters_selector._check_value_filters.get.return_value = True
        filters_selector._handle_filters()
        filters_selector._entry_min_size.config.assert_called_once_with(state=mock_styles_normal(filters_selector))
        filters_selector._entry_max_size.config.assert_called_once_with(state=mock_styles_normal(filters_selector))

    def test_entries_disabled_when_filter_unchecked(self, filters_selector: FiltersSelector) -> None:
        filters_selector._check_value_filters.get.return_value = False
        filters_selector._handle_filters()
        filters_selector._entry_min_size.config.assert_called_once_with(state=filters_selector._styles.STATE_DISABLED)
        filters_selector._entry_max_size.config.assert_called_once_with(state=filters_selector._styles.STATE_DISABLED)


def mock_styles_normal(instance: FiltersSelector) -> str:
    return instance._styles.STATE_NORMAL


class TestFiltersSelectorGetFilters:
    def test_returns_empty_dict_when_filter_unchecked(self, filters_selector: FiltersSelector) -> None:
        filters_selector._check_value_filters.get.return_value = False
        result: dict[str, Any] = filters_selector.get_filters()
        assert result == {}

    def test_returns_dict_with_min_and_max_when_checked(self, filters_selector: FiltersSelector) -> None:
        filters_selector._check_value_filters.get.return_value = True
        filters_selector._filter_min_size.get.return_value = 5
        filters_selector._filter_max_size.get.return_value = 50
        result: dict[str, Any] = filters_selector.get_filters()
        assert result == {"min_size": 5, "max_size": 50}

    def test_returns_correct_min_size(self, filters_selector: FiltersSelector) -> None:
        filters_selector._check_value_filters.get.return_value = True
        filters_selector._filter_min_size.get.return_value = 3
        filters_selector._filter_max_size.get.return_value = 20
        assert filters_selector.get_filters()["min_size"] == 3

    def test_returns_correct_max_size(self, filters_selector: FiltersSelector) -> None:
        filters_selector._check_value_filters.get.return_value = True
        filters_selector._filter_min_size.get.return_value = 1
        filters_selector._filter_max_size.get.return_value = 100
        assert filters_selector.get_filters()["max_size"] == 100
