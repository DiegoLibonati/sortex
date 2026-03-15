from tkinter import BooleanVar, Checkbutton, Frame, LabelFrame, Misc

from src.ui.styles import Styles


class ExtensionsSelector(Frame):
    def __init__(self, parent: Misc, styles: Styles) -> None:
        super().__init__(parent, bg=styles.WHITE_SMOKE_COLOR)
        self._styles = styles

        self._check_value_all = BooleanVar(value=True)
        self._extensions_options: dict[str, BooleanVar] = {
            ext: BooleanVar(value=True) for ext in ["mp4", "pdf", "exe", "png", "jpg", "jpeg", "txt", "json", "mp3", "m3u8", "zip", "gif"]
        }

        self._create_widgets()

    def _create_widgets(self) -> None:
        label_frame = LabelFrame(
            self,
            text="Select extensions",
            padx=20,
            pady=20,
        )
        label_frame.grid(row=0, column=0)

        Checkbutton(
            master=label_frame,
            text="ALL",
            variable=self._check_value_all,
            command=self._select_all_extensions,
            width=5,
            anchor=self._styles.ANCHOR_W,
        ).grid(padx=1, pady=5, row=0, column=0)

        positions = [
            ("mp4", 1, 0),
            ("pdf", 2, 0),
            ("exe", 3, 0),
            ("jpg", 4, 0),
            ("jpeg", 0, 1),
            ("png", 1, 1),
            ("txt", 2, 1),
            ("json", 3, 1),
            ("mp3", 4, 1),
            ("m3u8", 0, 2),
            ("zip", 1, 2),
            ("gif", 2, 2),
        ]

        for ext, row, col in positions:
            Checkbutton(
                master=label_frame,
                text=ext.upper(),
                variable=self._extensions_options[ext],
                command=self._select_extension,
                width=5,
                anchor=self._styles.ANCHOR_W,
            ).grid(padx=1, pady=5, row=row, column=col)

    def _select_all_extensions(self) -> None:
        check_all = self._check_value_all.get()
        for var in self._extensions_options.values():
            var.set(check_all)

    def _select_extension(self) -> None:
        self._check_value_all.set(False)

    def get_selected_extensions(self) -> list[str]:
        return [ext for ext, var in self._extensions_options.items() if var.get()]
