from src.configs.default_config import DefaultConfig
from src.configs.development_config import DevelopmentConfig


class TestDevelopmentConfig:
    def test_debug_is_true(self) -> None:
        config: DevelopmentConfig = DevelopmentConfig()
        assert config.DEBUG is True

    def test_env_is_development(self) -> None:
        config: DevelopmentConfig = DevelopmentConfig()
        assert config.ENV == "development"

    def test_testing_inherited_false(self) -> None:
        config: DevelopmentConfig = DevelopmentConfig()
        assert config.TESTING is False

    def test_inherits_from_default(self) -> None:
        config: DevelopmentConfig = DevelopmentConfig()
        assert isinstance(config, DefaultConfig)

    def test_tz_inherited(self) -> None:
        config: DevelopmentConfig = DevelopmentConfig()
        assert config.TZ == "America/Argentina/Buenos_Aires"

    def test_env_name_inherited(self) -> None:
        config: DevelopmentConfig = DevelopmentConfig()
        assert config.ENV_NAME == "template tkinter python"
