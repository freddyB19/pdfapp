import settings
from factory_app import create_app

app = create_app(settings.config['production'])
