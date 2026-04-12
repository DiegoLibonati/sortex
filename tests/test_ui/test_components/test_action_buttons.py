import tkinter as tk
from unittest.mock import MagicMock

from src.ui.components.action_buttons import ActionButtons
from src.ui.styles import Styles


class TestActionButtons:
    def test_instantiation(self, root: tk.Tk) -> None:
        widget: ActionButtons = ActionButtons(
            parent=root,
            styles=Styles(),
            on_organize=MagicMock(),
            on_revert=MagicMock(),
        )
        assert widget is not None

    def test_is_frame(self, root: tk.Tk) -> None:
        widget: ActionButtons = ActionButtons(
            parent=root,
            styles=Styles(),
            on_organize=MagicMock(),
            on_revert=MagicMock(),
        )
        assert isinstance(widget, tk.Frame)

    def test_on_organize_stored(self, root: tk.Tk) -> None:
        organize_cb: MagicMock = MagicMock()
        widget: ActionButtons = ActionButtons(
            parent=root,
            styles=Styles(),
            on_organize=organize_cb,
            on_revert=MagicMock(),
        )
        assert widget._on_organize is organize_cb

    def test_on_revert_stored(self, root: tk.Tk) -> None:
        revert_cb: MagicMock = MagicMock()
        widget: ActionButtons = ActionButtons(
            parent=root,
            styles=Styles(),
            on_organize=MagicMock(),
            on_revert=revert_cb,
        )
        assert widget._on_revert is revert_cb

    def test_styles_stored(self, root: tk.Tk) -> None:
        styles: Styles = Styles()
        widget: ActionButtons = ActionButtons(
            parent=root,
            styles=styles,
            on_organize=MagicMock(),
            on_revert=MagicMock(),
        )
        assert widget._styles is styles
