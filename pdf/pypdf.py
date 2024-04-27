"""
Estás clases nos permite interactuar con el modulo PyPDF2
Teniendo en cuenta esto, se crearon una serie de clases para cumplir una determinada función, las clases son las siguietes:

	- ExtraerMetadata
	- ExtraerTexto
	- ExtraerImagenes
	- CombinarPDF
	- EncriptarPDF
	- DesencriptarPDF

* Para cada una de estás se creó una clase manejador (Manager*) para instanciar cada clase.
Con el fin de evitar que al momento de modificar o crear una nueva clase, solamente se deba
instanciar la clase en su manejador correspondiente. Así, evitar que cualquier tipo de cambio
afecte ...
"""

import io
import lzma
import base64
import mimetypes
from typing import Union
from typing import List



import PyPDF2
from PIL import Image
from PyPDF2 import PdfReader
from PyPDF2 import PdfWriter

from werkzeug.datastructures import FileStorage

from . import exceptions

class BasePDF:
	def vista(self, *args, **kwargs):
		pass

class ExtraerMetadata(BasePDF):	
	
	def vista(self, archivo_pdf:FileStorage = None) -> dict[str, str]:
		try:
			pdf = PdfReader(archivo_pdf)
			metadata = pdf.metadata
		except PyPDF2.errors.FileNotDecryptedError as e:
			raise exceptions.PDFEncriptado(mensaje = "Este PDF se encuentra encriptado.", archivo = archivo_pdf)
		except:
			raise exceptions.PDFArchivoNoValido(mensaje = "El tipo de dato enviado no es valido", archivo = None)
		else:
			return metadata

class ManagerExtraerMetadata:
	
	@classmethod
	def crear(cls) -> ExtraerMetadata:
		return ExtraerMetadata()


class ExtraerTexto(BasePDF):
	
	def vista(self, archivo_pdf:FileStorage = None):
		try:
			pdf = PdfReader(archivo_pdf)
			
			texto_pdf = [ (i + 1, pag.extract_text()) for i, pag in enumerate(pdf.pages)]

		except PyPDF2.errors.FileNotDecryptedError as e:
			raise exceptions.PDFEncriptado(mensaje = "Este PDF se encuentra encriptado.", archivo = archivo_pdf)
		else:
			return texto_pdf
			

class ManagerExtraerTexto:
	
	@classmethod
	def crear(cls) -> ExtraerTexto:
		return ExtraerTexto()

class ExtraerImagenes(BasePDF):

	def vista(self, archivo_pdf:FileStorage = None) -> List[str]:
		lista_imagenes = list()
		mime = mimetypes.MimeTypes()

		try:
			pdf_imagenes = PdfReader(archivo_pdf).pages[0]
		except PyPDF2.errors.FileNotDecryptedError as e:
			raise exceptions.PDFEncriptado(mensaje = "Este PDF se encuentra encriptado.", archivo = archivo_pdf)
		else:
			for imagen in pdf_imagenes.images:
				image_read_64_encode = base64.b64encode(imagen.data)
				encode_str = image_read_64_encode.decode('utf-8')

				img_type = mime.guess_type(imagen.name)[0]

				formato_imagen = img_type.partition("/")
				
				lista_imagenes += [(f'data:{img_type};base64,{encode_str}', formato_imagen[2])]


			return lista_imagenes

class ManagerExtraerImagenes:
	
	@classmethod
	def crear(cls) -> ExtraerImagenes:
		return ExtraerImagenes()




class CombinarPDF(BasePDF):

	def vista(self, lista_pdf:List[FileStorage]) -> str:
		assert type(lista_pdf) == type([])

		merger = PdfWriter()
		try:
			for pdf in lista_pdf:
				merger.append(pdf)
		except PyPDF2.errors.FileNotDecryptedError as e:
			raise exceptions.PDFEncriptado(mensaje = "Uno de los PDF se encuentra encriptado.", archivo = lista_pdf)
		else:
			with io.BytesIO() as bytes_stream:
				merger.write(bytes_stream)
				merger.close()

				pdf_file64encode = base64.b64encode(bytes_stream.getvalue())
				pdf_str_file64encode = pdf_file64encode.decode('utf-8')
				file_type = mimetypes.types_map['.pdf']
				pdf_file64encode_format = f'data:{file_type};base64, {pdf_str_file64encode}'

			return pdf_file64encode_format

class ManagerCombinarPDF:
	
	@classmethod
	def crear(cls) -> CombinarPDF:
		return CombinarPDF()

class EncriptarPDF(BasePDF):

	def vista(self, archivo_pdf:FileStorage = None, clave_encriptacion:str = "1234") -> str:
		reader = PdfReader(archivo_pdf)
		writer = PdfWriter()

		try:
			for pag in reader.pages:
				writer.add_page(pag)
		except PyPDF2.errors.FileNotDecryptedError as e:
			raise exceptions.PDFEncriptado(mensaje = "Este PDF ya se encuentra encriptado.", archivo = archivo_pdf)
		else:
			writer.encrypt(clave_encriptacion)

			with io.BytesIO() as bytes_stream:
				writer.write_stream(bytes_stream)
				bytes_stream.seek(0)
				writer.close()

				pdf_file64encode = base64.b64encode(bytes_stream.getvalue())
							
				pdf_str_file64encode = pdf_file64encode.decode('utf-8') # unicode_escape
				file_type = mimetypes.types_map['.pdf']
				pdf_file64encode_format = f'data:{file_type};base64, {pdf_str_file64encode}'

			return pdf_file64encode_format


class ManagerEncriptarPDF:
	
	@classmethod
	def crear(cls) -> EncriptarPDF:
		return EncriptarPDF()

class DesencriptarPDF(BasePDF):

	def vista(self, archivo_pdf:FileStorage, clave_desencriptacion:str = "1234") -> str:
		
		try:
			reader = PdfReader(archivo_pdf, password = clave_desencriptacion)
		except PyPDF2.errors.WrongPasswordError as wpe:
			raise exceptions.PDFClaveAccesoIncorrecta(mensaje = "La contraseña ingresada para abrir este pdf no es valida.", archivo = archivo_pdf)
			
		except PyPDF2.errors.PdfReadError as re:
			raise exceptions.PDFErrorDeLectura(mensaje = "Este pdf no se encuentra encriptado.", archivo = archivo_pdf)
		else:
			reader = PdfReader(archivo_pdf, password = clave_desencriptacion)
			
			writer = PdfWriter()

			for pag in reader.pages:
				writer.insert_page(pag)

			with io.BytesIO() as bytes_stream:
				writer.write_stream(bytes_stream)
				bytes_stream.seek(0)
				writer.close()

				pdf_file64encode = base64.b64encode(bytes_stream.getvalue())
				pdf_str_file64encode = pdf_file64encode.decode('utf-8')
				file_type = mimetypes.types_map['.pdf']
				pdf_file64encode_format = f'data:{file_type};base64, {pdf_str_file64encode}'

			return pdf_file64encode_format

class ManagerDesencriptarPDF:
	@classmethod
	def crear(cls) -> DesencriptarPDF:
		return DesencriptarPDF()


TIPO_METODOS = {
	'texto': ManagerExtraerTexto,
	'metadata': ManagerExtraerMetadata,
	'imagenes': ManagerExtraerImagenes,
	'combinar': ManagerCombinarPDF,
	'encriptar': ManagerEncriptarPDF,
	'desencriptar': ManagerDesencriptarPDF,
}



class PersonalizarPDF:
	@classmethod
	def crear(cls, tipo_metodo:str = "-1") -> BasePDF:
		metodo = TIPO_METODOS.get(tipo_metodo, False)

		if metodo:
			return metodo.crear()
		raise ValueError('Tipo de Metodo Incorrrecto')
		



	






	









