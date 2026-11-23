"""
excepciones.py
--------------
Jerarquía de excepciones personalizadas del sistema Software FJ.

Todas heredan de SoftwareFJError, así el programa principal puede capturar
cualquier error propio del dominio con un solo except, sin atrapar por error
excepciones del lenguaje que indicarían un fallo de programación.
"""


class SoftwareFJError(Exception):
    """Excepción base de todo el sistema."""

    def __init__(self, mensaje, codigo="FJ-000"):
        # Guardamos un código de error para facilitar el rastreo en los logs
        self.codigo = codigo
        # Llamamos al constructor de Exception con el mensaje legible
        super().__init__(f"[{codigo}] {mensaje}")


class DatoInvalidoError(SoftwareFJError):
    """Se lanza cuando un dato no cumple las reglas de validación (formato, rango, tipo)."""

    def __init__(self, campo, valor, motivo):
        # Guardamos el campo y el valor para que el log muestre el detalle exacto
        self.campo = campo
        self.valor = valor
        super().__init__(f"Dato inválido en '{campo}' = {valor!r}: {motivo}", "FJ-100")


class ParametroFaltanteError(SoftwareFJError):
    """Se lanza cuando falta un parámetro obligatorio."""

    def __init__(self, parametro):
        self.parametro = parametro
        super().__init__(f"Falta el parámetro obligatorio '{parametro}'", "FJ-101")


class ClienteDuplicadoError(SoftwareFJError):
    """Se lanza al intentar registrar un cliente con un documento ya existente."""

    def __init__(self, documento):
        super().__init__(f"Ya existe un cliente con documento {documento}", "FJ-200")


class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando el servicio solicitado no está disponible o no existe."""

    def __init__(self, nombre):
        super().__init__(f"El servicio '{nombre}' no está disponible", "FJ-300")


class ReservaInvalidaError(SoftwareFJError):
    """Se lanza cuando los datos de una reserva no son válidos."""

    def __init__(self, motivo):
        super().__init__(f"Reserva inválida: {motivo}", "FJ-400")


class OperacionNoPermitidaError(SoftwareFJError):
    """Se lanza cuando se intenta una transición de estado no permitida (p. ej. cancelar dos veces)."""

    def __init__(self, operacion, estado_actual):
        super().__init__(
            f"No se puede '{operacion}' una reserva en estado '{estado_actual}'", "FJ-401"
        )


class CalculoInconsistenteError(SoftwareFJError):
    """Se lanza cuando un cálculo de costos produce un resultado incoherente."""

    def __init__(self, detalle):
        super().__init__(f"Cálculo inconsistente: {detalle}", "FJ-500")
