import logging
import os
from utils import config

# aqui configuro el sistema de logs de la aplicacion
_logger = None


def obtener_logger():
    global _logger
    if _logger is not None:
        return _logger

    nivel_texto = config.obtener("nivel_log", "INFO")
    nivel = getattr(logging, nivel_texto.upper(), logging.INFO)

    # creo la carpeta de logs si no existe
    ruta_logs = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    os.makedirs(ruta_logs, exist_ok=True)

    ruta_archivo = os.path.join(ruta_logs, "app.log")

    _logger = logging.getLogger("gestion_activos")
    _logger.setLevel(nivel)

    # evito duplicar handlers si se llama varias veces
    if not _logger.handlers:
        formato = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s",
                                    datefmt="%Y-%m-%d %H:%M:%S")

        # handler para archivo
        handler_archivo = logging.FileHandler(ruta_archivo, encoding="utf-8")
        handler_archivo.setFormatter(formato)
        _logger.addHandler(handler_archivo)

        # handler para consola
        handler_consola = logging.StreamHandler()
        handler_consola.setFormatter(formato)
        _logger.addHandler(handler_consola)

    return _logger
