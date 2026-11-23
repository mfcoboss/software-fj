"""
cliente.py
----------
Clase Cliente con encapsulación de datos personales y validaciones estrictas.
"""

import re                                   # Expresiones regulares para validar formatos
from sistema.entidad import Entidad         # Clase abstracta base
from sistema.excepciones import DatoInvalidoError, ParametroFaltanteError

# Patrón de correo: texto@texto.dominio
PATRON_EMAIL = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")
# Patrón de documento: solo dígitos, entre 6 y 10
PATRON_DOCUMENTO = re.compile(r"^\d{6,10}$")
# Patrón de teléfono: 10 dígitos (celular colombiano)
PATRON_TELEFONO = re.compile(r"^\d{10}$")


class Cliente(Entidad):
    """Cliente de Software FJ. Los atributos son privados y se validan en los setters."""

    def __init__(self, nombre, documento, email, telefono):
        # Inicializamos la parte común (id y fecha) de la clase padre
        super().__init__()
        # Asignamos usando las propiedades, así cada dato pasa por su validación
        self.nombre = nombre
        self.documento = documento
        self.email = email
        self.telefono = telefono

    # ---------------- nombre ----------------
    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        # Parámetro obligatorio: no puede ser None ni vacío
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("nombre")
        # Solo letras y espacios (se admiten tildes y ñ)
        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]{3,60}", str(valor).strip()):
            raise DatoInvalidoError("nombre", valor, "solo letras, entre 3 y 60 caracteres")
        self.__nombre = str(valor).strip().title()

    # ---------------- documento ----------------
    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("documento")
        if not PATRON_DOCUMENTO.fullmatch(str(valor)):
            raise DatoInvalidoError("documento", valor, "debe tener entre 6 y 10 dígitos")
        self.__documento = str(valor)

    # ---------------- email ----------------
    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("email")
        if not PATRON_EMAIL.fullmatch(str(valor).strip()):
            raise DatoInvalidoError("email", valor, "formato de correo no válido")
        self.__email = str(valor).strip().lower()

    # ---------------- teléfono ----------------
    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("telefono")
        if not PATRON_TELEFONO.fullmatch(str(valor)):
            raise DatoInvalidoError("telefono", valor, "debe tener exactamente 10 dígitos")
        self.__telefono = str(valor)

    # ------------- métodos abstractos implementados -------------
    def validar(self):
        """Revalida todo el objeto reasignando cada campo (útil tras cambios)."""
        self.nombre, self.documento = self.nombre, self.documento
        self.email, self.telefono = self.email, self.telefono
        return True

    def describir(self):
        # Por privacidad mostramos solo los últimos 4 dígitos del documento
        doc_oculto = "*" * (len(self.documento) - 4) + self.documento[-4:]
        return f"Cliente #{self.id}: {self.nombre} (doc {doc_oculto}, {self.email})"
