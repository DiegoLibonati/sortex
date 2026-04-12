import logging

from src.configs.logger_config import setup_logger


class TestSetupLogger:
    def test_returns_logger_instance(self) -> None:
        logger: logging.Logger = setup_logger()
        assert isinstance(logger, logging.Logger)

    def test_default_name(self) -> None:
        logger: logging.Logger = setup_logger()
        assert logger.name == "tkinter-app"

    def test_custom_name(self) -> None:
        logger: logging.Logger = setup_logger("custom-logger")
        assert logger.name == "custom-logger"

    def test_has_handlers(self) -> None:
        logger: logging.Logger = setup_logger("test-has-handlers")
        assert len(logger.handlers) > 0

    def test_debug_level(self) -> None:
        logger: logging.Logger = setup_logger("test-debug-level")
        assert logger.level == logging.DEBUG

    def test_idempotent_does_not_add_duplicate_handlers(self) -> None:
        logger: logging.Logger = setup_logger("test-idempotent")
        initial_count: int = len(logger.handlers)
        setup_logger("test-idempotent")
        assert len(logger.handlers) == initial_count

    def test_handler_is_stream_handler(self) -> None:
        logger: logging.Logger = setup_logger("test-stream-handler")
        assert any(isinstance(h, logging.StreamHandler) for h in logger.handlers)
