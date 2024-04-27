import secrets
from datetime import timedelta

from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from flask_wtf.file import FileAllowed
from flask_wtf.file import FileRequired
from flask_wtf.file import FileSize

from flask_wtf.file import MultipleFileField

from wtforms.fields import PasswordField
from wtforms.validators import EqualTo
from wtforms.validators import InputRequired
from wtforms.validators import ValidationError


class PDF_Form(FlaskForm):
	upload_pdf = FileField(
		"Archivo PDF", 
		validators = [
			FileRequired(),
			FileSize(max_size = 1800000, message = "El archivo es muy grande"),
			FileAllowed(['pdf'], 'Solo puede subir archivos pdf')
		]
	)

	class Meta:
		csrf = True
		csrf_time_limit = timedelta(minutes=20)


def validacion_combinarPDF(form, field):
	if len(field.data) == 1:
		raise ValidationError('Como minimo debe subir dos archivos.')


class MultipleFilePDFForm(FlaskForm):
	archivos = MultipleFileField(
		"Archivos PDF", 
		validators = [
			FileRequired(),
			FileSize(max_size = 1800000, message = "El archivo es muy grande"),
			FileAllowed(['pdf'], 'Solo puede subir archivos pdf'),
		]
	)

	class Meta:
		csrf = True
		csrf_time_limit = timedelta(minutes=20)

	def validate_archivos(form, field):
		if len(form.archivos.data) == 1:
			raise ValidationError(message = "Como minimo debe subir dos archivos.")




class PDFPasswordForm(PDF_Form):
	password = PasswordField("Contraseña", validators = [InputRequired(), EqualTo('confirm', message='Ambas contraseñas deben ser iguales')])
	confirm = PasswordField("Confirmar Contraseña")


class PDFRemovePasswordForm(PDF_Form):
	password = PasswordField("Contraseña", validators = [InputRequired()])