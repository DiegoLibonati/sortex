from tkinter import Button, Entry, Frame, Misc, StringVar

from src.ui.styles import Styles


class PathSelector(Frame):
    def __init__(self, parent: Misc, styles: Styles, on_search: callable) -> None:
        super().__init__(parent, bg=styles.WHITE_SMOKE_COLOR)
        self._styles = styles
        self._on_search = on_search

        self._text_path = StringVar(value="Wait for directory...")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)

        Entry(
            self,
            bg=self._styles.WHITE_COLOR,
            fg=self._styles.BLACK_COLOR,
            font=self._styles.FONT_ARIAL_BOLD_10,
            textvariable=self._text_path,
            state=self._styles.STATE_DISABLED,
        ).grid(row=0, column=0, sticky="ew", ipady=3)

        Button(
            self,
            text="Search",
            relief=self._styles.RELIEF_FLAT,
            bg=self._styles.PRIMARY_COLOR,
            fg=self._styles.WHITE_COLOR,
            cursor=self._styles.CURSOR_HAND2,
            command=self._on_search,
        ).grid(row=0, column=1, sticky="e", padx=(5, 0), ipady=3)

    def set_path(self, path: str) -> None:
        self._text_path.set(path)
