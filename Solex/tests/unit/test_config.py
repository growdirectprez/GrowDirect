from solex.config import resolve_config, DevConfig, TestConfig, ProdConfig


def test_dev_env_returns_dev_config(monkeypatch):
    monkeypatch.setenv("SOLEX_ENV", "development")
    assert resolve_config() is DevConfig


def test_test_env_returns_test_config(monkeypatch):
    monkeypatch.setenv("SOLEX_ENV", "testing")
    assert resolve_config() is TestConfig


def test_invalid_env_raises(monkeypatch):
    monkeypatch.setenv("SOLEX_ENV", "bogus")
    import pytest
    with pytest.raises(ValueError):
        resolve_config()
