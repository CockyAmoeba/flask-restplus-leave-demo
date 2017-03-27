import pytest
import os
from app import create_app


@pytest.mark.parametrize('flask_config_name', ['production', 'development', 'testing'])
def test_create_app_passing_flask_config_name(flask_config_name):
    create_app(config_name=flask_config_name)


@pytest.mark.parametrize('flask_config_name', ['production', 'development', 'testing'])
def test_create_app_passing_FLASK_CONFIG_env(monkeypatch, flask_config_name):
    monkeypatch.setenv('FLASK_CONFIG', flask_config_name)
    env_flask_config_name = os.getenv('FLASK_CONFIG')
    create_app(env_flask_config_name)
