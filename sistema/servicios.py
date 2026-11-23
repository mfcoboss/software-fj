"""
servicios.py
------------
Clase abstracta Servicio y tres servicios especializados:
  - ReservaSala       (cobro por hora, recargo por aforo)
  - AlquilerEquipo    (cobro por día y por unidad)
  - Asesoria          (cobro por hora, recargo por nivel experto)

Cada subclase sobrescribe: _costo_base(), validar_parametros() y describir()
(polimorfismo). El método calcular_costo() está "sobrecargado" mediante
parámetros opcionales: se puede llamar con 1, 2 o 3 argumentos.
"""

from abc import abstractmethod
from sistema.entidad import Entidad
from sistema.excepciones import (
    DatoInvalidoError,
    ParametroFaltanteError,
    CalculoInconsistenteError,
)


class Servicio(Entidad):
    """Servicio genérico que ofrece Software FJ (clase abstracta)."""

    def __init__(self, nombre, tarifa_base, disponible=True):
        super().__init__()
        # Validamos el nombre: obligatorio
        if not nombre or not str(nombre).strip():
            raise ParametroFaltanteError("nombre del servicio")
        # La tarifa debe ser número positivo
        if not isinstance(tarifa_base, (int, float)) or tarifa_base <= 0:
            raise DatoInvalidoError("tarifa_base", tarifa_base, "debe ser un número mayor que 0")
        self._nombre = str(nombre).strip()      # Protegido: lo usan las subclases
        self._tarifa_base = float(tarifa_base)  # Tarifa por unidad de tiempo
        self._disponible = bool(disponible)     # Indica si se puede reservar

    # Propiedades de solo lectura
    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa_base(self):
        return self._tarifa_base

    @property
    def disponible(self):
        return self._disponible

    def cambiar_disponibilidad(self, estado):
        """Permite activar/desactivar el servicio."""
        self._disponible = bool(estado)

    # --------- métodos que DEBEN implementar las subclases ---------
    @abstractmethod
    def _costo_base(self, duracion):
        """Costo sin impuestos ni descuentos (depende del tipo de servicio)."""

    @abstractmethod
    def validar_parametros(self, duracion):
        """Valida que la duración tenga sentido para este servicio."""

    # --------- método "sobrecargado" ---------
    def calcular_costo(self, duracion, impuesto=None, descuento=None):
        """
        Variantes de uso (sobrecarga por parámetros opcionales):
          calcular_costo(d)            -> costo base
          calcular_costo(d, 0.19)      -> costo base + IVA
          calcular_costo(d, 0.19, 0.1) -> costo base + IVA - descuento
        """
        # 1) La duración debe ser válida para el tipo de servicio
        self.validar_parametros(duracion)
        # 2) Costo propio de cada subclase (polimorfismo)
        costo = self._costo_base(duracion)
        # 3) Aplicamos descuento si se envió
        if descuento is not None:
            if not 0 <= descuento < 1:
                raise DatoInvalidoError("descuento", descuento, "debe estar entre 0 y 0.99")
            costo *= (1 - descuento)
        # 4) Aplicamos impuesto si se envió
        if impuesto is not None:
            if not 0 <= impuesto <= 0.5:
                raise DatoInvalidoError("impuesto", impuesto, "debe estar entre 0 y 0.5")
            costo *= (1 + impuesto)
        # 5) Verificación de consistencia: un costo nunca puede ser negativo ni cero
        if costo <= 0:
            raise CalculoInconsistenteError(f"costo calculado = {costo}")
        # Redondeamos a pesos
        return round(costo, 0)

    def validar(self):
        """Valida el estado general del servicio."""
        return self._tarifa_base > 0 and bool(self._nombre)

    @staticmethod
    def _validar_rango(campo, valor, minimo, maximo):
        """Utilidad común: valida que un valor numérico esté en [minimo, maximo]."""
        if not isinstance(valor, (int, float)) or isinstance(valor, bool):
            raise DatoInvalidoError(campo, valor, "debe ser numérico")
        if not minimo <= valor <= maximo:
            raise DatoInvalidoError(campo, valor, f"debe estar entre {minimo} y {maximo}")


class ReservaSala(Servicio):
    """Reserva de salas de reuniones. Duración en HORAS (1 a 12)."""

    def __init__(self, nombre, tarifa_hora, capacidad, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        # La capacidad es un entero entre 2 y 100 personas
        self._validar_rango("capacidad", capacidad, 2, 100)
        self._capacidad = int(capacidad)

    def validar_parametros(self, duracion):
        self._validar_rango("duración (horas)", duracion, 1, 12)

    def _costo_base(self, duracion):
        # Salas grandes (>20 personas) tienen recargo del 20 %
        recargo = 1.2 if self._capacidad > 20 else 1.0
        return self._tarifa_base * duracion * recargo

    def describir(self):
        return f"Sala '{self.nombre}' ({self._capacidad} personas) - ${self.tarifa_base:,.0f}/hora"


class AlquilerEquipo(Servicio):
    """Alquiler de equipos (portátiles, proyectores...). Duración en DÍAS (1 a 30)."""

    def __init__(self, nombre, tarifa_dia, cantidad, disponible=True):
        super().__init__(nombre, tarifa_dia, disponible)
        self._validar_rango("cantidad", cantidad, 1, 50)
        self._cantidad = int(cantidad)

    def validar_parametros(self, duracion):
        self._validar_rango("duración (días)", duracion, 1, 30)

    def _costo_base(self, duracion):
        # Precio por unidad y por día; desde 7 días se descuenta 10 % por alquiler largo
        costo = self._tarifa_base * self._cantidad * duracion
        return costo * 0.9 if duracion >= 7 else costo

    def describir(self):
        return f"Alquiler '{self.nombre}' x{self._cantidad} - ${self.tarifa_base:,.0f}/día c/u"


class Asesoria(Servicio):
    """Asesoría especializada. Duración en HORAS (1 a 8). Nivel 'basico' o 'experto'."""

    NIVELES = {"basico": 1.0, "experto": 1.5}  # Multiplicador de tarifa por nivel

    def __init__(self, nombre, tarifa_hora, nivel="basico", disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if nivel not in self.NIVELES:
            raise DatoInvalidoError("nivel", nivel, f"debe ser uno de {list(self.NIVELES)}")
        self._nivel = nivel

    def validar_parametros(self, duracion):
        self._validar_rango("duración (horas)", duracion, 1, 8)

    def _costo_base(self, duracion):
        return self._tarifa_base * duracion * self.NIVELES[self._nivel]

    def describir(self):
        return f"Asesoría '{self.nombre}' (nivel {self._nivel}) - ${self.tarifa_base:,.0f}/hora"
