from typing import Union

from werkzeug.datastructures import FileStorage


"""
PDFEncriptado
PDFClaveAccesoIncorrecta
PDFErrorDeLectura
"""

class PDFError(Exception):
    """
    Excepción general por intetar abrir el archivo PDF

    Atributos:
        mensaje
        archivo
    """

    def __init__(self, mensaje:str = "Ha ocurrido un error al intentar acceder al archivo", archivo:Union[FileStorage, list[FileStorage]] = None) -> None:
        self.mensaje = mensaje
        self.archivo = archivo

        super().__init__(self.mensaje)

    def __str__(self) -> str:
        return f"{self.mensaje} -->'{self.archivo}'"


class PDFArchivoNoValido(PDFError):
    """
    Excepción al intetar pasar un tipo de dato novalido

    Atributos:
        mensaje
        archivo
    """
    def __str__(self) -> str:
        return f"Error de PDFArchivoNoValido{self.mensaje} -->'{self.archivo}'"

class PDFEncriptado(PDFError):
    """
    Excepción por acceder a un archivo PDF con cencriptación

    Atributos:
        mensaje
        archivo
    """

    def __str__(self) -> str:
        return f"Error de PDFEncriptado: {self.mensaje} --> {self.archivo}"

class PDFClaveAccesoIncorrecta(PDFError):
    """
    Excepción por ingresar clave de encriptación o contraseña erronea del PDF

    Atributos:
        mensaje
        archivo
    """

    def __str__(self) -> str:
        return f"Error de PDFClaveAccesoIncorrecta: {self.mensaje} --> {self.archivo}"

class PDFErrorDeLectura(PDFError):
    """
    Excepción al intentar leer un archivo PDF

    Atributos:
        mensaje
        archivo
    """

    def __str__(self) -> str:
        return f"Error de PDFErrorDeLectura: {self.mensaje} --> {self.archivo}"
