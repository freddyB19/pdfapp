from settings import config
from factory_app import create_app

import pytest
import warnings

@pytest.fixture()
def app():
	app = create_app(config['test'])

	yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test_config():
	assert create_app(config['test']).testing

# pytest ./tests/test.py -W ignore::DeprecationWarning