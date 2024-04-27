from typing import Union

from flask import flash
from flask import url_for
from flask import request
from flask import redirect
from flask import Response
from flask import Blueprint
from flask import render_template	

from . import forms
from pdf import pypdf
from pdf import exceptions
from pdf.pypdf import PersonalizarPDF

views = Blueprint("pdf", __name__, template_folder = 'templates')

@views.route("/", methods= ['GET'])
def index() -> Union[str, Response]:
	return render_template("pdf/index.html")


@views.route("/leer-metadata", methods = ['GET', 'POST'])
def metadata() -> Union[str, Response]:
	form = forms.PDF_Form()
	if form.validate_on_submit():		
		try:
			pdf = PersonalizarPDF.crear('metadata')
			
			data = pdf.vista(archivo_pdf = form.upload_pdf.data)

			print(form.upload_pdf.data.__sizeof__())
		except exceptions.PDFEncriptado as e:
			message = f"{e}"
			response =  redirect(url_for('pdf.index'))
		else:
			response = render_template("pdf/meatdata_pdf.html", metadata_pdf = data)
			message = "Metadata extraida"
		
		flash(message)
		return response

	return render_template("pdf/extraer_datos_pdf.html", form = form, titulo = "Extraer Metadata del PDF")


@views.route("/extraer-texto", methods = ['GET', 'POST'])
def extraer_texto() -> Union[str, Response]:
	form = forms.PDF_Form()
	
	if form.validate_on_submit():
		
		try:
			pdf = PersonalizarPDF.crear('texto')

			data = pdf.vista(archivo_pdf = form.upload_pdf.data)
			
		except exceptions.PDFEncriptado as e:
			message = f"{e}"
			response = redirect(url_for('pdf.index'))
		else:
			response = render_template("pdf/texto_pdf.html", lista_texto = data)
			message = "Se ha extraido todo el texto del pdf."
		
		flash(message)
		return response
	
	return render_template("pdf/extraer_datos_pdf.html", form = form, titulo = "Extraer texto de PDF")


@views.route("/extraer-imagenes", methods = ['GET', 'POST'])
def extraer_imagenes() -> Union[str, Response]:
	form = forms.PDF_Form()

	if form.validate_on_submit():
		try:
			pdf = PersonalizarPDF.crear('imagenes')

			data = pdf.vista(archivo_pdf = form.upload_pdf.data)
			
		except exceptions.PDFEncriptado as e:
			message = f"{e}"
			response = redirect(url_for('pdf.index'))
		else:
			if data:
				message = "Se ha extraido todo las imagenes del pdf"
			else:
				message = 'El pdf no contiene imagenes'
			response = render_template("pdf/imagen_pdf.html", lista_imagenes = data)
			
		
		flash(message)
		return response
			
	return render_template("pdf/extraer_datos_pdf.html", form = form, titulo = "Extraer imagenes del PDF")


@views.route("/unir-pdf", methods = ['GET', 'POST'])
def unir_pdf() -> Union[str, Response]:
	form = forms.MultipleFilePDFForm()

	if form.validate_on_submit():
		
		try:			
			pdf = PersonalizarPDF.crear('combinar')

			data = pdf.vista(lista_pdf = form.archivos.data)
			
		except AssertionError as e:
			message = "Ha ocurrido un error al intenrar combinar los pdf"
			response =  redirect(url_for('pdf.index'))
		except exceptions.PDFEncriptado as e:
			message = f"{e}"
			response =  redirect(url_for('pdf.index'))
		else:
			response = render_template("pdf/combinacion_pdf.html", merge = data)
			
			message = "Operación de combinación completada."

		flash(message)
		return response	
								
	return render_template("pdf/extraer_datos_pdf.html", form = form, titulo = "Combinar PDFs")


@views.route("/pdf-encriptado", methods = ['GET', 'POST'])
def set_password_pdf() -> Union[str, Response]:
	form = forms.PDFPasswordForm()

	if form.validate_on_submit():
		
		try:
			pdf = PersonalizarPDF.crear('encriptar')

			data = pdf.vista(archivo_pdf = form.upload_pdf.data, clave_encriptacion = form.password.data)
			
		except exceptions.PDFEncriptado as e:
			message = f"{e}"
			response = redirect(url_for('pdf.index'))
		else:
			response = render_template("pdf/pdf_encriptado.html", pdf_encry = data)
			message = "El PDF ahora posee una contraseña"
		
		flash(message)
		return response	
	
	return render_template("pdf/extraer_datos_pdf.html", form = form, titulo = "Definir una contraseña para el PDF")


@views.route("/pdf-desencriptado", methods = ['GET', 'POST'])
def remove_password_pdf() -> Union[str, Response]:
	form = forms.PDFRemovePasswordForm()

	if form.validate_on_submit():	
		try:
			pdf = PersonalizarPDF.crear('desencriptar')
			
			data = pdf.vista(archivo_pdf = form.upload_pdf.data, clave_desencriptacion = form.password.data)	
			
		except exceptions.PDFClaveAccesoIncorrecta as e:
			message = f"{e}"
			response = redirect(url_for('pdf.index'))
		except exceptions.PDFErrorDeLectura as e:
			message = f"{e}"
			response = redirect(url_for('pdf.index'))
		else:
			response = render_template("pdf/pdf_desencriptado.html", pdf_decrypt = data)
			message = "Se ha removido la contraseña del pdf"
	
		flash(message)
		return response	
	
	return render_template("pdf/extraer_datos_pdf.html", form = form, titulo = "Eliminar la contraseña del PDF")
