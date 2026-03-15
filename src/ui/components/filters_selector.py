from tkinter import BooleanVar, Checkbutton, Entry, Frame, IntVar, Label, LabelFrame, Misc
from typing import Any

from src.ui.styles import Styles


class FiltersSelector(Frame):
    def __init__(self, parent: Misc, styles: Styles) -> None:
        super().__init__(parent, bg=styles.WHITE_SMOKE_COLOR)
        self._styles = styles

        self._check_value_filters = BooleanVar(value=False)
        self._filter_min_size = IntVar(value=1)
        self._filter_max_size = IntVar(value=10)

        self._create_widgets()

    def _create_widgets(self) -> None:
        label_frame = LabelFrame(
            self,
            text="Select filters",
            padx=20,
            pady=20,
        )
        label_frame.grid(row=0, column=0)

        Checkbutton(
            master=label_frame,
            text="Filter by",
            variable=self._check_value_filters,
            command=self._handle_filters,
            width=18,
            anchor=self._styles.ANCHOR_W,
        ).grid(padx=0, pady=5, row=0, column=0)

        Label(
            master=label_frame,
            fg=self._styles.BLACK_COLOR,
            font=self._styles.FONT_ARIAL_BOLD_10,
            text="Min size in MB: ",
            width=15,
            anchor=self._styles.ANCHOR_W,
        ).grid(padx=0, pady=0, row=1, column=0)

        self._entry_min_size = Entry(
            master=label_frame,
            bg=self._styles.WHITE_COLOR,
            font=self._styles.FONT_ARIAL_BOLD_10,
            textvariable=self._filter_min_size,
            state=self._styles.STATE_DISABLED,
            width=5,
        )
        self._entry_min_size.grid(padx=0, pady=0, row=1, column=1)

        Label(
            master=label_frame,
            fg=self._styles.BLACK_COLOR,
            font=self._styles.FONT_ARIAL_BOLD_10,
            text="Max size in MB: ",
            width=15,
            anchor=self._styles.ANCHOR_W,
        ).grid(padx=0, pady=0, row=2, column=0)

        self._entry_max_size = Entry(
            master=label_frame,
            bg=self._styles.WHITE_COLOR,
            font=self._styles.FONT_ARIAL_BOLD_10,
            textvariable=self._filter_max_size,
            state=self._styles.STATE_DISABLED,
            width=5,
        )
        self._entry_max_size.grid(padx=0, pady=0, row=2, column=1)

    def _handle_filters(self) -> None:
        state = self._styles.STATE_NORMAL if self._check_value_filters.get() else self._styles.STATE_DISABLED
        self._entry_min_size.config(state=state)
        self._entry_max_size.config(state=state)

    def get_filters(self) -> dict[str, Any]:
        if not self._check_value_filters.get():
            return {}

        return {
            "min_size": self._filter_min_size.get(),
            "max_size": self._filter_max_size.get(),
        }
