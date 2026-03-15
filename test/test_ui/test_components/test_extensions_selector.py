from tkinter import BooleanVar
from unittest.mock import MagicMock, patch

import pytest

from src.ui.components.extensions_selector import ExtensionsSelector


@pytest.fixture
def extensions_selector(mock_styles: MagicMock) -> ExtensionsSelector:
    with (
        patch("src.ui.components.extensions_selector.Frame.__init__", return_value=None),
        patch("src.ui.components.extensions_selector.LabelFrame"),
        patch("src.ui.components.extensions_selector.Checkbutton"),
        patch("src.ui.components.extensions_selector.BooleanVar") as mock_bv,
    ):
        mock_bv.return_value = MagicMock(spec=BooleanVar)
        instance: ExtensionsSelector = ExtensionsSelector.__new__(ExtensionsSelector)
        instance._styles = mock_styles
        instance._check_value_all = MagicMock(spec=BooleanVar)
        instance._extensions_options = {ext: MagicMock(spec=BooleanVar) for ext in ["mp4", "pdf", "txt", "jpg"]}
        return instance


class TestExtensionsSelectorInit:
    def test_stores_styles(self, mock_styles: MagicMock) -> None:
        with (
            patch("src.ui.components.extensions_selector.Frame.__init__", return_value=None),
            patch("src.ui.components.extensions_selector.LabelFrame") as mock_lf,
            patch("src.ui.components.extensions_selector.Checkbutton") as mock_cb,
            patch("src.ui.components.extensions_selector.BooleanVar"),
        ):
            mock_lf.return_value.grid = MagicMock()
            mock_cb.return_value.grid = MagicMock()
            instance: ExtensionsSelector = ExtensionsSelector.__new__(ExtensionsSelector)
            ExtensionsSelector.__init__(instance, parent=MagicMock(), styles=mock_styles)
        assert instance._styles is mock_styles

    def test_check_value_all_initial_value_is_true(self, mock_styles: MagicMock) -> None:
        captured: list[bool] = []

        def capture_bv(value: bool = False) -> MagicMock:
            captured.append(value)
            return MagicMock(spec=BooleanVar)

        with (
            patch("src.ui.components.extensions_selector.Frame.__init__", return_value=None),
            patch("src.ui.components.extensions_selector.LabelFrame") as mock_lf,
            patch("src.ui.components.extensions_selector.Checkbutton") as mock_cb,
            patch("src.ui.components.extensions_selector.BooleanVar", side_effect=capture_bv),
        ):
            mock_lf.return_value.grid = MagicMock()
            mock_cb.return_value.grid = MagicMock()
            instance: ExtensionsSelector = ExtensionsSelector.__new__(ExtensionsSelector)
            ExtensionsSelector.__init__(instance, parent=MagicMock(), styles=mock_styles)
        assert True in captured

    def test_extensions_options_has_12_entries(self, mock_styles: MagicMock) -> None:
        with (
            patch("src.ui.components.extensions_selector.Frame.__init__", return_value=None),
            patch("src.ui.components.extensions_selector.LabelFrame") as mock_lf,
            patch("src.ui.components.extensions_selector.Checkbutton") as mock_cb,
            patch("src.ui.components.extensions_selector.BooleanVar"),
        ):
            mock_lf.return_value.grid = MagicMock()
            mock_cb.return_value.grid = MagicMock()
            instance: ExtensionsSelector = ExtensionsSelector.__new__(ExtensionsSelector)
            ExtensionsSelector.__init__(instance, parent=MagicMock(), styles=mock_styles)
        assert len(instance._extensions_options) == 12


class TestExtensionsSelectorSelectAll:
    def test_select_all_sets_all_extensions_to_true(self, extensions_selector: ExtensionsSelector) -> None:
        extensions_selector._check_value_all.get.return_value = True
        extensions_selector._select_all_extensions()
        for var in extensions_selector._extensions_options.values():
            var.set.assert_called_with(True)

    def test_deselect_all_sets_all_extensions_to_false(self, extensions_selector: ExtensionsSelector) -> None:
        extensions_selector._check_value_all.get.return_value = False
        extensions_selector._select_all_extensions()
        for var in extensions_selector._extensions_options.values():
            var.set.assert_called_with(False)


class TestExtensionsSelectorSelectExtension:
    def test_select_extension_sets_check_all_to_false(self, extensions_selector: ExtensionsSelector) -> None:
        extensions_selector._select_extension()
        extensions_selector._check_value_all.set.assert_called_once_with(False)


class TestExtensionsSelectorGetSelectedExtensions:
    def test_returns_only_checked_extensions(self, extensions_selector: ExtensionsSelector) -> None:
        extensions_selector._extensions_options["txt"].get.return_value = True
        extensions_selector._extensions_options["jpg"].get.return_value = False
        extensions_selector._extensions_options["mp4"].get.return_value = True
        extensions_selector._extensions_options["pdf"].get.return_value = False

        result: list[str] = extensions_selector.get_selected_extensions()
        assert set(result) == {"txt", "mp4"}

    def test_returns_all_when_all_checked(self, extensions_selector: ExtensionsSelector) -> None:
        for var in extensions_selector._extensions_options.values():
            var.get.return_value = True
        result: list[str] = extensions_selector.get_selected_extensions()
        assert len(result) == len(extensions_selector._extensions_options)

    def test_returns_empty_when_none_checked(self, extensions_selector: ExtensionsSelector) -> None:
        for var in extensions_selector._extensions_options.values():
            var.get.return_value = False
        result: list[str] = extensions_selector.get_selected_extensions()
        assert result == []
