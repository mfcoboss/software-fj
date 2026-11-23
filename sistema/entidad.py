"""
entidad.py
----------
Clase abstracta que representa cualquier entidad general del sistema
(clientes, servicios y reservas heredan de ella).
"""

from abc import ABC, abstractmethod  # ABC permite definir clases abstractas
import itertools                     # Para generar identificadores consecutivos
from datetime import datetime        # Para la fecha de creación de cada entidad


class Entidad(ABC):
    """Entidad general: tiene un id único y una fecha de creación."""

    # Contador compartido por todas las entidades para asignar ids únicos
    _contador = itertools.count(1)

    def __init__(self):
        # Id único e inmutable (encapsulado con doble guion bajo)
        self.__id = next(Entidad._contador)
        # Momento en que se creó el objeto
        self.__creado_en = datetime.now()

    @property
    def id(self):
        """Solo lectura: el id no se puede modificar desde afuera."""
        return self.__id

    @property
    def creado_en(self):
        """Solo lectura: fecha de creación."""
        return self.__creado_en

    @abstractmethod
    def describir(self):
        """Cada entidad concreta debe saber describirse (polimorfismo)."""

    @abstractmethod
    def validar(self):
        """Cada entidad concreta debe validar su propio estado."""

    def __str__(self):
        # Todas las entidades se imprimen usando su propia descripción
        return self.describir()
