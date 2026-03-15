from unittest.mock import MagicMock, patch

import pytest

from src.ui.components.action_buttons import ActionButtons


@pytest.fixture
def action_buttons(mock_styles: MagicMock, mock_on_organize: MagicMock, mock_on_revert: MagicMock) -> ActionButtons:
    with (
        patch("src.ui.components.action_buttons.Frame.__init__", return_value=None),
        patch("src.ui.components.action_buttons.Button") as mock_button,
    ):
        mock_button.return_value.grid = MagicMock()
        instance: ActionButtons = ActionButtons.__new__(ActionButtons)
        instance._styles = mock_styles
        instance._on_organize = mock_on_organize
        instance._on_revert = mock_on_revert
        return instance


class TestActionButtonsInit:
    def test_stores_styles(self, mock_styles: MagicMock, mock_on_organize: MagicMock, mock_on_revert: MagicMock) -> None:
        with (
            patch("src.ui.components.action_buttons.Frame.__init__", return_value=None),
            patch("src.ui.components.action_buttons.Button") as mock_button,
        ):
            mock_button.return_value.grid = MagicMock()
            instance: ActionButtons = ActionButtons.__new__(ActionButtons)
            ActionButtons.__init__(instance, parent=MagicMock(), styles=mock_styles, on_organize=mock_on_organize, on_revert=mock_on_revert)
        assert instance._styles is mock_styles

    def test_stores_on_organize(self, mock_styles: MagicMock, mock_on_organize: MagicMock, mock_on_revert: MagicMock) -> None:
        with (
            patch("src.ui.components.action_buttons.Frame.__init__", return_value=None),
            patch("src.ui.components.action_buttons.Button") as mock_button,
        ):
            mock_button.return_value.grid = MagicMock()
            instance: ActionButtons = ActionButtons.__new__(ActionButtons)
            ActionButtons.__init__(instance, parent=MagicMock(), styles=mock_styles, on_organize=mock_on_organize, on_revert=mock_on_revert)
        assert instance._on_organize is mock_on_organize

    def test_stores_on_revert(self, mock_styles: MagicMock, mock_on_organize: MagicMock, mock_on_revert: MagicMock) -> None:
        with (
            patch("src.ui.components.action_buttons.Frame.__init__", return_value=None),
            patch("src.ui.components.action_buttons.Button") as mock_button,
        ):
            mock_button.return_value.grid = MagicMock()
            instance: ActionButtons = ActionButtons.__new__(ActionButtons)
            ActionButtons.__init__(instance, parent=MagicMock(), styles=mock_styles, on_organize=mock_on_organize, on_revert=mock_on_revert)
        assert instance._on_revert is mock_on_revert

    def test_two_buttons_created(self, mock_styles: MagicMock, mock_on_organize: MagicMock, mock_on_revert: MagicMock) -> None:
        with (
            patch("src.ui.components.action_buttons.Frame.__init__", return_value=None),
            patch("src.ui.components.action_buttons.Button") as mock_button,
        ):
            mock_button.return_value.grid = MagicMock()
            instance: ActionButtons = ActionButtons.__new__(ActionButtons)
            ActionButtons.__init__(instance, parent=MagicMock(), styles=mock_styles, on_organize=mock_on_organize, on_revert=mock_on_revert)
        assert mock_button.call_count == 2

    def test_organize_button_command_is_on_organize(self, mock_styles: MagicMock, mock_on_organize: MagicMock, mock_on_revert: MagicMock) -> None:
        with (
            patch("src.ui.components.action_buttons.Frame.__init__", return_value=None),
            patch("src.ui.components.action_buttons.Button") as mock_button,
        ):
            mock_button.return_value.grid = MagicMock()
            instance: ActionButtons = ActionButtons.__new__(ActionButtons)
            ActionButtons.__init__(instance, parent=MagicMock(), styles=mock_styles, on_organize=mock_on_organize, on_revert=mock_on_revert)
        organize_call = next(c for c in mock_button.call_args_list if c[1].get("text") == "ORGANIZE")
        assert organize_call[1].get("command") is mock_on_organize

    def test_revert_button_command_is_on_revert(self, mock_styles: MagicMock, mock_on_organize: MagicMock, mock_on_revert: MagicMock) -> None:
        with (
            patch("src.ui.components.action_buttons.Frame.__init__", return_value=None),
            patch("src.ui.components.action_buttons.Button") as mock_button,
        ):
            mock_button.return_value.grid = MagicMock()
            instance: ActionButtons = ActionButtons.__new__(ActionButtons)
            ActionButtons.__init__(instance, parent=MagicMock(), styles=mock_styles, on_organize=mock_on_organize, on_revert=mock_on_revert)
        revert_call = next(c for c in mock_button.call_args_list if "Revert" in c[1].get("text", ""))
        assert revert_call[1].get("command") is mock_on_revert
