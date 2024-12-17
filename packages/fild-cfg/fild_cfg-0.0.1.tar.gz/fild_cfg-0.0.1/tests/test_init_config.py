import pytest

from fild_cfg.config import Cfg


@pytest.fixture(scope='function', autouse=True)
def reset_config():
    Cfg.initial_dict = None
    yield
    Cfg.initialize()


def test_config_initialized():
    assert Cfg.App is not None


def test_config_initialized_on_contains():
    assert 'test' not in Cfg
