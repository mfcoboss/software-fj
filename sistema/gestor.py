"""
gestor.py
---------
GestorSoftwareFJ: administra en memoria (listas internas, SIN base de datos)
los clientes, servicios y reservas.
"""

from sistema.cliente import Cliente
from sistema.reserva import Reserva
from sistema.excepciones import ClienteDuplicadoError, ServicioNoDisponibleError, SoftwareFJError
from sistema.logger import obtener_logger

log = obtener_logger()


class GestorSoftwareFJ:
    """Fachada del sistema: punto único para registrar y consultar información."""

    def __init__(self):
        # Listas internas: toda la información vive en memoria
        self._clientes = []
        self._servicios = []
        self._reservas = []

    # ---------------- clientes ----------------
    def registrar_cliente(self, nombre, documento, email, telefono):
        """Crea y guarda un cliente; lanza error si el documento ya existe."""
        if any(c.documento == str(documento) for c in self._clientes):
            raise ClienteDuplicadoError(documento)
        cliente = Cliente(nombre, documento, email, telefono)  # Puede lanzar DatoInvalidoError
        self._clientes.append(cliente)
        log.info(f"Cliente registrado: {cliente.describir()}")
        return cliente

    # ---------------- servicios ----------------
    def agregar_servicio(self, servicio):
        """Agrega un servicio ya construido al catálogo."""
        self._servicios.append(servicio)
        log.info(f"Servicio agregado: {servicio.describir()}")
        return servicio

    def buscar_servicio(self, nombre):
        """Devuelve el servicio por nombre o lanza ServicioNoDisponibleError."""
        for s in self._servicios:
            if s.nombre.lower() == nombre.lower():
                return s
        raise ServicioNoDisponibleError(nombre)

    # ---------------- reservas ----------------
    def crear_reserva(self, cliente, nombre_servicio, duracion):
        """Busca el servicio y crea la reserva (estado PENDIENTE)."""
        servicio = self.buscar_servicio(nombre_servicio)
        reserva = Reserva(cliente, servicio, duracion)
        self._reservas.append(reserva)
        log.info(f"Reserva creada: {reserva.describir()}")
        return reserva

    # ---------------- reportes ----------------
    def resumen(self):
        """Texto con el estado actual de las listas internas."""
        lineas = [f"Clientes: {len(self._clientes)} | Servicios: {len(self._servicios)} | "
                  f"Reservas: {len(self._reservas)}"]
        lineas += [f"  - {c}" for c in self._clientes]
        lineas += [f"  - {s}" for s in self._servicios]
        lineas += [f"  - {r}" for r in self._reservas]
        ingresos = sum(r.costo_final or 0 for r in self._reservas if r.estado == Reserva.PROCESADA)
        lineas.append(f"Ingresos procesados: ${ingresos:,.0f}")
        return "\n".join(lineas)
