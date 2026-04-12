from tkinter import Tk, filedialog

from src.configs.default_config import DefaultConfig
from src.constants.messages import MESSAGE_NOT_FOUND_EXTENSIONS
from src.services.file_service import FileService
from src.ui.styles import Styles
from src.ui.views.main_view import MainView
from src.utils.dialogs import NotFoundDialogError, SuccessDialogInformation, ValidationDialogError


class InterfaceApp:
    def __init__(self, root: Tk, config: DefaultConfig, styles: Styles = Styles()) -> None:
        self._styles = styles
        self._config = config
        self._root = root
        self._root.title("Sortex V1.0.0")
        self._root.geometry("400x600")
        self._root.resizable(False, False)
        self._root.config(background=self._styles.WHITE_SMOKE_COLOR)

        self._file_service = FileService()

        self._main_view = MainView(
            root=self._root,
            styles=self._styles,
            on_search=self._set_path,
            on_organize=self._organize,
            on_revert=self._reverse_organize,
        )
        self._main_view.grid(row=0, column=0, sticky="nsew")
        self._root.columnconfigure(0, weight=1)
        self._root.rowconfigure(0, weight=1)

    def _set_path(self) -> None:
        path = filedialog.askdirectory(title="Choose a directory")
        message, status = self._file_service.set_path(path)

        if not status:
            raise ValidationDialogError(message=message)

        self._main_view.set_path(path)
        SuccessDialogInformation(message=message).open()

    def _organize(self) -> None:
        extensions = self._main_view.get_selected_extensions()

        if not extensions:
            raise NotFoundDialogError(message=MESSAGE_NOT_FOUND_EXTENSIONS)

        filters = self._main_view.get_filters()
        message, status = self._file_service.organize(extensions, filters)

        if not status:
            raise ValidationDialogError(message=message)

        SuccessDialogInformation(message=message).open()

    def _reverse_organize(self) -> None:
        message, status = self._file_service.revert()

        if not status:
            raise ValidationDialogError(message=message)

        SuccessDialogInformation(message=message).open()
