"""
reserva.py
----------
Clase Reserva: integra cliente, servicio, duración y estado.
Implementa confirmar(), cancelar() y procesar() con manejo de excepciones
(try/except/else/finally y encadenamiento con 'raise ... from ...').
"""

from sistema.entidad import Entidad
from sistema.cliente import Cliente
from sistema.servicios import Servicio
from sistema.excepciones import (
    SoftwareFJError,
    ReservaInvalidaError,
    ServicioNoDisponibleError,
    OperacionNoPermitidaError,
)
from sistema.logger import obtener_logger

log = obtener_logger()  # Logger compartido


class Reserva(Entidad):
    """Reserva de un servicio por parte de un cliente."""

    # Estados posibles de una reserva
    PENDIENTE, CONFIRMADA, CANCELADA, PROCESADA = "PENDIENTE", "CONFIRMADA", "CANCELADA", "PROCESADA"

    def __init__(self, cliente, servicio, duracion):
        super().__init__()
        # Validamos tipos: deben ser objetos del dominio, no textos sueltos
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("el cliente no es un objeto Cliente válido")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("el servicio no es un objeto Servicio válido")
        # No se puede reservar un servicio deshabilitado
        if not servicio.disponible:
            raise ServicioNoDisponibleError(servicio.nombre)
        # La duración se valida con las reglas propias del servicio (polimorfismo)
        try:
            servicio.validar_parametros(duracion)
        except SoftwareFJError as e:
            # Encadenamiento: el error original queda en __cause__
            raise ReservaInvalidaError(f"duración no válida para {servicio.nombre}") from e

        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__estado = Reserva.PENDIENTE
        self.__costo_final = None

    # Propiedades de solo lectura
    @property
    def estado(self):
        return self.__estado

    @property
    def costo_final(self):
        return self.__costo_final

    @property
    def cliente(self):
        return self.__cliente

    @property
    def servicio(self):
        return self.__servicio

    # ---------------- operaciones ----------------
    def confirmar(self):
        """PENDIENTE -> CONFIRMADA."""
        if self.__estado != Reserva.PENDIENTE:
            raise OperacionNoPermitidaError("confirmar", self.__estado)
        self.__estado = Reserva.CONFIRMADA
        log.info(f"Reserva #{self.id} confirmada")

    def cancelar(self):
        """PENDIENTE o CONFIRMADA -> CANCELADA. No se cancela algo ya procesado o cancelado."""
        if self.__estado in (Reserva.CANCELADA, Reserva.PROCESADA):
            raise OperacionNoPermitidaError("cancelar", self.__estado)
        self.__estado = Reserva.CANCELADA
        log.info(f"Reserva #{self.id} cancelada")

    def procesar(self, impuesto=0.19, descuento=None):
        """
        Calcula el costo final y marca la reserva como PROCESADA.
        Usa try/except/else/finally:
          - try:     intenta calcular el costo
          - except:  si falla, registra y encadena el error
          - else:    solo si no hubo error, cambia el estado
          - finally: siempre deja constancia del intento en el log
        """
        if self.__estado != Reserva.CONFIRMADA:
            raise OperacionNoPermitidaError("procesar", self.__estado)
        try:
            costo = self.__servicio.calcular_costo(self.__duracion, impuesto, descuento)
        except SoftwareFJError as e:
            log.error(f"Fallo al procesar reserva #{self.id}: {e}")
            # Encadenamos para no perder la causa original
            raise ReservaInvalidaError(f"no se pudo procesar la reserva #{self.id}") from e
        else:
            self.__costo_final = costo
            self.__estado = Reserva.PROCESADA
            log.info(f"Reserva #{self.id} procesada. Total: ${costo:,.0f}")
        finally:
            log.debug(f"Intento de procesamiento de reserva #{self.id} finalizado")
        return self.__costo_final

    # ------------- métodos abstractos implementados -------------
    def validar(self):
        return self.__estado in (Reserva.PENDIENTE, Reserva.CONFIRMADA, Reserva.CANCELADA, Reserva.PROCESADA)

    def describir(self):
        total = f" | Total ${self.__costo_final:,.0f}" if self.__costo_final else ""
        return (f"Reserva #{self.id}: {self.__cliente.nombre} -> {self.__servicio.nombre} "
                f"({self.__duracion}) [{self.__estado}]{total}")
