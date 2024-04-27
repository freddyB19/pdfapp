from flask import Flask
from flask_wtf.csrf import CSRFProtect


from app.pdf.views import views as views_pdf

import settings

def create_app(config_object):
	app = Flask(__name__)
	app.config.from_object(config_object) # Configuracion

	# Registro de las vistas
	app.register_blueprint(views_pdf)

	# Token CSRF para los forms
	csrf = CSRFProtect(app)

	return app


