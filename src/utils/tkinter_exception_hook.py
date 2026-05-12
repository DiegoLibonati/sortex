import traceback
import types

from src.configs.logger_config import setup_logger
from src.utils.dialogs import BaseDialog, InternalDialogError

logger = setup_logger("tkinter-app - tkinter_exception_hook")


def tkinter_exception_hook(
    _exc_type: type[BaseException],
    exc_value: BaseException,
    _exc_tb: types.TracebackType,
) -> None:
    error_detail = "".join(traceback.format_exception(_exc_type, exc_value, _exc_tb))
    logger.error("Unhandled exception:\n%s", error_detail)

    if isinstance(exc_value, BaseDialog):
        exc_value.open()
    else:
        InternalDialogError(message=str(exc_value)).open()
