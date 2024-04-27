import os
import secrets


#BASE = os.path.dirname(os.path.abspath(__file__))

class BasicConfig:
	SECRET_KEY = secrets.token_hex()

class DevelopmetConfig(BasicConfig):
	DEBUG = True

class ProductionConfig(BasicConfig):
	WTF_CSRF_SECRET_KEY = secrets.token_hex()
	DEBUG = False


class TestingConfig(BasicConfig):
	TESTING =  True

config = {
	'development': DevelopmetConfig,
	'production': ProductionConfig,
	'test': TestingConfig,
}