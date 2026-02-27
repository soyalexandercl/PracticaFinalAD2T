import json
import os

# aqui cargo la configuracion desde el archivo config.json
_config = {}


def cargar_configuracion():
    ruta = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            global _config
            _config = json.load(f)
    except Exception:
        _config = {
            "db_path": "datos/gestion_activos.db",
            "registros_por_pagina": 15,
            "nivel_log": "INFO",
            "tema": "dark",
            "color_principal": "blue"
        }


def obtener(clave, valor_defecto=None):
    # aqui devuelvo el valor de la configuracion pedida
    return _config.get(clave, valor_defecto)
