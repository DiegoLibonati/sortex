import pytest

from src.configs.default_config import DefaultConfig


class TestDefaultConfig:
    def test_debug_default(self) -> None:
        config: DefaultConfig = DefaultConfig()
        assert config.DEBUG is False

    def test_testing_default(self) -> None:
        config: DefaultConfig = DefaultConfig()
        assert config.TESTING is False

    def test_tz_default(self) -> None:
        config: DefaultConfig = DefaultConfig()
        assert config.TZ == "America/Argentina/Buenos_Aires"

    def test_env_name_default(self) -> None:
        config: DefaultConfig = DefaultConfig()
        assert config.ENV_NAME == "template tkinter python"

    def test_tz_from_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("TZ", "UTC")
        config: DefaultConfig = DefaultConfig()
        assert config.TZ == "UTC"

    def test_env_name_from_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ENV_NAME", "custom-app")
        config: DefaultConfig = DefaultConfig()
        assert config.ENV_NAME == "custom-app"

    def test_tz_restored_after_monkeypatch(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("TZ", raising=False)
        config: DefaultConfig = DefaultConfig()
        assert config.TZ == "America/Argentina/Buenos_Aires"
