import tkinter as tk

import pytest

from src.configs.testing_config import TestingConfig
from src.services.file_service import FileService
from src.ui.interface_app import InterfaceApp
from src.ui.styles import Styles
from src.ui.views.main_view import MainView
from src.utils.dialogs import NotFoundDialogError, ValidationDialogError


class TestInterfaceApp:
    def test_instantiation(self, root: tk.Tk) -> None:
        config: TestingConfig = TestingConfig()
        app: InterfaceApp = InterfaceApp(root=root, config=config)
        assert app is not None

    def test_title_is_set(self, root: tk.Tk) -> None:
        config: TestingConfig = TestingConfig()
        InterfaceApp(root=root, config=config)
        assert root.title() == "Sortex V1.0.0"

    def test_file_service_initialized(self, root: tk.Tk) -> None:
        config: TestingConfig = TestingConfig()
        app: InterfaceApp = InterfaceApp(root=root, config=config)
        assert app._file_service is not None
        assert isinstance(app._file_service, FileService)

    def test_main_view_initialized(self, root: tk.Tk) -> None:
        config: TestingConfig = TestingConfig()
        app: InterfaceApp = InterfaceApp(root=root, config=config)
        assert app._main_view is not None
        assert isinstance(app._main_view, MainView)

    def test_config_stored(self, root: tk.Tk) -> None:
        config: TestingConfig = TestingConfig()
        app: InterfaceApp = InterfaceApp(root=root, config=config)
        assert app._config is config

    def test_styles_stored(self, root: tk.Tk) -> None:
        config: TestingConfig = TestingConfig()
        styles: Styles = Styles()
        app: InterfaceApp = InterfaceApp(root=root, config=config, styles=styles)
        assert app._styles is styles

    def test_organize_raises_not_found_when_no_extensions(self, root: tk.Tk) -> None:
        config: TestingConfig = TestingConfig()
        app: InterfaceApp = InterfaceApp(root=root, config=config)
        for var in app._main_view._extensions_selector._extensions_options.values():
            var.set(False)
        with pytest.raises(NotFoundDialogError):
            app._organize()

    def test_reverse_organize_raises_validation_when_no_path(self, root: tk.Tk) -> None:
        config: TestingConfig = TestingConfig()
        app: InterfaceApp = InterfaceApp(root=root, config=config)
        with pytest.raises(ValidationDialogError):
            app._reverse_organize()
