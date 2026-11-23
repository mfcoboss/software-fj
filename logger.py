"""
logger.py
---------
Configuración del archivo de logs. Es el ÚNICO uso de archivos del sistema:
no hay base de datos, solo se escriben eventos y errores en logs/software_fj.log.
"""

import logging  # Módulo estándar de Python para registrar eventos
import os       # Para crear la carpeta de logs si no existe

# Carpeta donde se guardará el archivo de logs (junto al proyecto)
CARPETA_LOGS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
# Ruta completa del archivo de logs
RUTA_LOG = os.path.join(CARPETA_LOGS, "software_fj.log")


def obtener_logger(nombre="SoftwareFJ"):
    """Devuelve un logger configurado que escribe en archivo y en consola."""
    # Creamos la carpeta de logs; exist_ok evita error si ya existe
    os.makedirs(CARPETA_LOGS, exist_ok=True)
    # Obtenemos (o creamos) el logger con ese nombre
    logger = logging.getLogger(nombre)
    # Si ya tiene manejadores, ya fue configurado: lo devolvemos tal cual
    if logger.handlers:
        return logger
    # Nivel mínimo que se registrará (DEBUG captura todo)
    logger.setLevel(logging.DEBUG)
    # Formato: fecha | nivel | mensaje
    formato = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s", "%Y-%m-%d %H:%M:%S")

    # Manejador de archivo: guarda todo (INFO, WARNING, ERROR) en el .log
    archivo = logging.FileHandler(RUTA_LOG, encoding="utf-8")
    archivo.setLevel(logging.DEBUG)
    archivo.setFormatter(formato)
    logger.addHandler(archivo)

    # Evita que los mensajes se dupliquen en el logger raíz
    logger.propagate = False
    return logger
