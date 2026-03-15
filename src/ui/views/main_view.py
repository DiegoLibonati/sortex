from tkinter import Frame, Tk
from typing import Any

from src.ui.components.action_buttons import ActionButtons
from src.ui.components.extensions_selector import ExtensionsSelector
from src.ui.components.filters_selector import FiltersSelector
from src.ui.components.path_selector import PathSelector
from src.ui.styles import Styles


class MainView(Frame):
    def __init__(
        self,
        root: Tk,
        styles: Styles,
        on_search: callable,
        on_organize: callable,
        on_revert: callable,
    ) -> None:
        super().__init__(root, bg=styles.WHITE_SMOKE_COLOR)
        self._styles = styles
        self._on_search = on_search
        self._on_organize = on_organize
        self._on_revert = on_revert

        self._create_widgets()

    def _create_widgets(self) -> None:
        self.columnconfigure(0, weight=1)

        self._path_selector = PathSelector(
            parent=self,
            styles=self._styles,
            on_search=self._on_search,
        )
        self._path_selector.grid(row=0, column=0, sticky="ew", padx=50, pady=(25, 0))

        self._action_buttons = ActionButtons(
            parent=self,
            styles=self._styles,
            on_organize=self._on_organize,
            on_revert=self._on_revert,
        )
        self._action_buttons.grid(row=1, column=0, sticky="w", padx=50, pady=(15, 0))

        self._extensions_selector = ExtensionsSelector(
            parent=self,
            styles=self._styles,
        )
        self._extensions_selector.grid(row=2, column=0, sticky="w", padx=50, pady=(15, 0))

        self._filters_selector = FiltersSelector(
            parent=self,
            styles=self._styles,
        )
        self._filters_selector.grid(row=3, column=0, sticky="w", padx=50, pady=(10, 0))

    def set_path(self, path: str) -> None:
        self._path_selector.set_path(path)

    def get_selected_extensions(self) -> list[str]:
        return self._extensions_selector.get_selected_extensions()

    def get_filters(self) -> dict[str, Any]:
        return self._filters_selector.get_filters()
