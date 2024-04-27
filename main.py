import settings
from factory_app import create_app


if __name__== "__main__":
	app = create_app(settings.config['production'])
	app.run()

