from src.configs.default_config import DefaultConfig
from src.configs.production_config import ProductionConfig


class TestProductionConfig:
    def test_debug_is_false(self) -> None:
        config: ProductionConfig = ProductionConfig()
        assert config.DEBUG is False

    def test_env_is_production(self) -> None:
        config: ProductionConfig = ProductionConfig()
        assert config.ENV == "production"

    def test_testing_inherited_false(self) -> None:
        config: ProductionConfig = ProductionConfig()
        assert config.TESTING is False

    def test_inherits_from_default(self) -> None:
        config: ProductionConfig = ProductionConfig()
        assert isinstance(config, DefaultConfig)

    def test_tz_inherited(self) -> None:
        config: ProductionConfig = ProductionConfig()
        assert config.TZ == "America/Argentina/Buenos_Aires"
