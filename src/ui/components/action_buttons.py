from tkinter import Button, Frame, Misc

from src.ui.styles import Styles


class ActionButtons(Frame):
    def __init__(self, parent: Misc, styles: Styles, on_organize: callable, on_revert: callable) -> None:
        super().__init__(parent, bg=styles.WHITE_SMOKE_COLOR)
        self._styles = styles
        self._on_organize = on_organize
        self._on_revert = on_revert

        Button(
            self,
            text="ORGANIZE",
            relief=self._styles.RELIEF_FLAT,
            bg=self._styles.PRIMARY_COLOR,
            fg=self._styles.WHITE_COLOR,
            cursor=self._styles.CURSOR_HAND2,
            command=self._on_organize,
            width=15,
        ).grid(row=0, column=0, pady=5)

        Button(
            self,
            text="Revert ORGANIZE",
            relief=self._styles.RELIEF_FLAT,
            bg=self._styles.PRIMARY_COLOR,
            fg=self._styles.WHITE_COLOR,
            cursor=self._styles.CURSOR_HAND2,
            command=self._on_revert,
            width=15,
        ).grid(row=1, column=0, pady=5)
