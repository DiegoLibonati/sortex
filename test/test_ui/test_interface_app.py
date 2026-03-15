from unittest.mock import MagicMock, patch

import pytest

from src.constants.messages import MESSAGE_NOT_FOUND_EXTENSIONS
from src.ui.interface_app import InterfaceApp
from src.ui.styles import Styles
from src.utils.dialogs import NotFoundDialogError, ValidationDialogError


@pytest.fixture
def interface_app(mock_root: MagicMock, mock_styles: MagicMock) -> InterfaceApp:
    with (
        patch("src.ui.interface_app.MainView") as mock_main_view_class,
        patch("src.ui.interface_app.FileService"),
    ):
        mock_main_view_class.return_value = MagicMock()
        instance: InterfaceApp = InterfaceApp.__new__(InterfaceApp)
        instance._styles = mock_styles
        instance._config = MagicMock()
        instance._root = mock_root
        instance._main_view = mock_main_view_class.return_value
        instance._file_service = MagicMock()
        return instance


class TestInterfaceAppInit:
    def test_stores_styles(self, mock_root: MagicMock, mock_styles: MagicMock) -> None:
        with (
            patch("src.ui.interface_app.MainView") as mock_main_view_class,
            patch("src.ui.interface_app.FileService"),
        ):
            mock_main_view_class.return_value.grid = MagicMock()
            app: InterfaceApp = InterfaceApp(root=mock_root, config=MagicMock(), styles=mock_styles)
        assert app._styles is mock_styles

    def test_stores_root(self, mock_root: MagicMock, mock_styles: MagicMock) -> None:
        with (
            patch("src.ui.interface_app.MainView") as mock_main_view_class,
            patch("src.ui.interface_app.FileService"),
        ):
            mock_main_view_class.return_value.grid = MagicMock()
            app: InterfaceApp = InterfaceApp(root=mock_root, config=MagicMock(), styles=mock_styles)
        assert app._root is mock_root

    def test_title_is_set(self, mock_root: MagicMock, mock_styles: MagicMock) -> None:
        with (
            patch("src.ui.interface_app.MainView") as mock_main_view_class,
            patch("src.ui.interface_app.FileService"),
        ):
            mock_main_view_class.return_value.grid = MagicMock()
            InterfaceApp(root=mock_root, config=MagicMock(), styles=mock_styles)
        mock_root.title.assert_called_once_with("File Organizer V1.0.0")

    def test_geometry_is_set(self, mock_root: MagicMock, mock_styles: MagicMock) -> None:
        with (
            patch("src.ui.interface_app.MainView") as mock_main_view_class,
            patch("src.ui.interface_app.FileService"),
        ):
            mock_main_view_class.return_value.grid = MagicMock()
            InterfaceApp(root=mock_root, config=MagicMock(), styles=mock_styles)
        mock_root.geometry.assert_called_once_with("400x600")

    def test_is_not_resizable(self, mock_root: MagicMock, mock_styles: MagicMock) -> None:
        with (
            patch("src.ui.interface_app.MainView") as mock_main_view_class,
            patch("src.ui.interface_app.FileService"),
        ):
            mock_main_view_class.return_value.grid = MagicMock()
            InterfaceApp(root=mock_root, config=MagicMock(), styles=mock_styles)
        mock_root.resizable.assert_called_once_with(False, False)

    def test_background_uses_white_smoke_color(self, mock_root: MagicMock, mock_styles: MagicMock) -> None:
        with (
            patch("src.ui.interface_app.MainView") as mock_main_view_class,
            patch("src.ui.interface_app.FileService"),
        ):
            mock_main_view_class.return_value.grid = MagicMock()
            InterfaceApp(root=mock_root, config=MagicMock(), styles=mock_styles)
        mock_root.config.assert_called_once_with(background=mock_styles.WHITE_SMOKE_COLOR)

    def test_default_styles_is_styles_instance(self, mock_root: MagicMock) -> None:
        with (
            patch("src.ui.interface_app.MainView") as mock_main_view_class,
            patch("src.ui.interface_app.FileService"),
        ):
            mock_main_view_class.return_value.grid = MagicMock()
            app: InterfaceApp = InterfaceApp(root=mock_root, config=MagicMock())
        assert isinstance(app._styles, Styles)

    def test_file_service_is_instantiated(self, mock_root: MagicMock, mock_styles: MagicMock) -> None:
        with (
            patch("src.ui.interface_app.MainView") as mock_main_view_class,
            patch("src.ui.interface_app.FileService") as mock_fs_class,
        ):
            mock_main_view_class.return_value.grid = MagicMock()
            InterfaceApp(root=mock_root, config=MagicMock(), styles=mock_styles)
        mock_fs_class.assert_called_once()

    def test_main_view_receives_callbacks(self, mock_root: MagicMock, mock_styles: MagicMock) -> None:
        with (
            patch("src.ui.interface_app.MainView") as mock_main_view_class,
            patch("src.ui.interface_app.FileService"),
        ):
            mock_main_view_class.return_value.grid = MagicMock()
            InterfaceApp(root=mock_root, config=MagicMock(), styles=mock_styles)
        _, kwargs = mock_main_view_class.call_args
        assert callable(kwargs.get("on_search"))
        assert callable(kwargs.get("on_organize"))
        assert callable(kwargs.get("on_revert"))

    def test_main_view_grid_called(self, mock_root: MagicMock, mock_styles: MagicMock) -> None:
        with (
            patch("src.ui.interface_app.MainView") as mock_main_view_class,
            patch("src.ui.interface_app.FileService"),
        ):
            mock_main_view: MagicMock = MagicMock()
            mock_main_view_class.return_value = mock_main_view
            InterfaceApp(root=mock_root, config=MagicMock(), styles=mock_styles)
        mock_main_view.grid.assert_called_once_with(row=0, column=0, sticky="nsew")

    def test_columnconfigure_called_on_root(self, mock_root: MagicMock, mock_styles: MagicMock) -> None:
        with (
            patch("src.ui.interface_app.MainView") as mock_main_view_class,
            patch("src.ui.interface_app.FileService"),
        ):
            mock_main_view_class.return_value.grid = MagicMock()
            InterfaceApp(root=mock_root, config=MagicMock(), styles=mock_styles)
        mock_root.columnconfigure.assert_called_once_with(0, weight=1)

    def test_rowconfigure_called_on_root(self, mock_root: MagicMock, mock_styles: MagicMock) -> None:
        with (
            patch("src.ui.interface_app.MainView") as mock_main_view_class,
            patch("src.ui.interface_app.FileService"),
        ):
            mock_main_view_class.return_value.grid = MagicMock()
            InterfaceApp(root=mock_root, config=MagicMock(), styles=mock_styles)
        mock_root.rowconfigure.assert_called_once_with(0, weight=1)


class TestInterfaceAppSetPath:
    def test_raises_validation_error_when_set_path_fails(self, interface_app: InterfaceApp) -> None:
        interface_app._file_service.set_path.return_value = ("Invalid path.", False)
        with (
            patch("src.ui.interface_app.filedialog.askdirectory", return_value="/bad/path"),
            pytest.raises(ValidationDialogError) as exc_info,
        ):
            interface_app._set_path()
        assert exc_info.value.message == "Invalid path."

    def test_main_view_set_path_called_on_success(self, interface_app: InterfaceApp) -> None:
        interface_app._file_service.set_path.return_value = ("ok", True)
        with (
            patch("src.ui.interface_app.filedialog.askdirectory", return_value="/valid/path"),
            patch("src.ui.interface_app.SuccessDialogInformation") as mock_dialog_class,
        ):
            mock_dialog_class.return_value = MagicMock()
            interface_app._set_path()
        interface_app._main_view.set_path.assert_called_once_with("/valid/path")

    def test_success_dialog_opened_on_set_path(self, interface_app: InterfaceApp) -> None:
        interface_app._file_service.set_path.return_value = ("Path loaded.", True)
        with (
            patch("src.ui.interface_app.filedialog.askdirectory", return_value="/valid/path"),
            patch("src.ui.interface_app.SuccessDialogInformation") as mock_dialog_class,
        ):
            mock_dialog: MagicMock = MagicMock()
            mock_dialog_class.return_value = mock_dialog
            interface_app._set_path()
        mock_dialog.open.assert_called_once()

    def test_file_service_set_path_called_with_directory(self, interface_app: InterfaceApp) -> None:
        interface_app._file_service.set_path.return_value = ("ok", True)
        with (
            patch("src.ui.interface_app.filedialog.askdirectory", return_value="/valid/path"),
            patch("src.ui.interface_app.SuccessDialogInformation") as mock_dialog_class,
        ):
            mock_dialog_class.return_value = MagicMock()
            interface_app._set_path()
        interface_app._file_service.set_path.assert_called_once_with("/valid/path")

    def test_main_view_set_path_not_called_when_fails(self, interface_app: InterfaceApp) -> None:
        interface_app._file_service.set_path.return_value = ("error", False)
        with (
            patch("src.ui.interface_app.filedialog.askdirectory", return_value="/bad/path"),
            pytest.raises(ValidationDialogError),
        ):
            interface_app._set_path()
        interface_app._main_view.set_path.assert_not_called()


class TestInterfaceAppOrganize:
    def test_raises_not_found_error_when_no_extensions(self, interface_app: InterfaceApp) -> None:
        interface_app._main_view.get_selected_extensions.return_value = []
        with pytest.raises(NotFoundDialogError) as exc_info:
            interface_app._organize()
        assert exc_info.value.message == MESSAGE_NOT_FOUND_EXTENSIONS

    def test_raises_validation_error_when_organize_fails(self, interface_app: InterfaceApp) -> None:
        interface_app._main_view.get_selected_extensions.return_value = ["txt"]
        interface_app._main_view.get_filters.return_value = {}
        interface_app._file_service.organize.return_value = ("error msg", False)
        with pytest.raises(ValidationDialogError) as exc_info:
            interface_app._organize()
        assert exc_info.value.message == "error msg"

    def test_success_dialog_opened_on_organize(self, interface_app: InterfaceApp) -> None:
        interface_app._main_view.get_selected_extensions.return_value = ["txt"]
        interface_app._main_view.get_filters.return_value = {}
        interface_app._file_service.organize.return_value = ("ok", True)
        with patch("src.ui.interface_app.SuccessDialogInformation") as mock_dialog_class:
            mock_dialog: MagicMock = MagicMock()
            mock_dialog_class.return_value = mock_dialog
            interface_app._organize()
        mock_dialog.open.assert_called_once()

    def test_organize_called_with_extensions_and_filters(self, interface_app: InterfaceApp) -> None:
        interface_app._main_view.get_selected_extensions.return_value = ["txt", "pdf"]
        interface_app._main_view.get_filters.return_value = {"min_size": 1, "max_size": 10}
        interface_app._file_service.organize.return_value = ("ok", True)
        with patch("src.ui.interface_app.SuccessDialogInformation") as mock_dialog_class:
            mock_dialog_class.return_value = MagicMock()
            interface_app._organize()
        interface_app._file_service.organize.assert_called_once_with(["txt", "pdf"], {"min_size": 1, "max_size": 10})

    def test_get_filters_not_called_when_no_extensions(self, interface_app: InterfaceApp) -> None:
        interface_app._main_view.get_selected_extensions.return_value = []
        with pytest.raises(NotFoundDialogError):
            interface_app._organize()
        interface_app._main_view.get_filters.assert_not_called()


class TestInterfaceAppReverseOrganize:
    def test_raises_validation_error_when_revert_fails(self, interface_app: InterfaceApp) -> None:
        interface_app._file_service.revert.return_value = ("error msg", False)
        with pytest.raises(ValidationDialogError) as exc_info:
            interface_app._reverse_organize()
        assert exc_info.value.message == "error msg"

    def test_success_dialog_opened_on_revert(self, interface_app: InterfaceApp) -> None:
        interface_app._file_service.revert.return_value = ("reverted", True)
        with patch("src.ui.interface_app.SuccessDialogInformation") as mock_dialog_class:
            mock_dialog: MagicMock = MagicMock()
            mock_dialog_class.return_value = mock_dialog
            interface_app._reverse_organize()
        mock_dialog.open.assert_called_once()

    def test_revert_called_on_file_service(self, interface_app: InterfaceApp) -> None:
        interface_app._file_service.revert.return_value = ("reverted", True)
        with patch("src.ui.interface_app.SuccessDialogInformation") as mock_dialog_class:
            mock_dialog_class.return_value = MagicMock()
            interface_app._reverse_organize()
        interface_app._file_service.revert.assert_called_once()

    def test_success_dialog_message_matches_revert_message(self, interface_app: InterfaceApp) -> None:
        interface_app._file_service.revert.return_value = ("Successfully reverted.", True)
        with patch("src.ui.interface_app.SuccessDialogInformation") as mock_dialog_class:
            mock_dialog_class.return_value = MagicMock()
            interface_app._reverse_organize()
        mock_dialog_class.assert_called_once_with(message="Successfully reverted.")
