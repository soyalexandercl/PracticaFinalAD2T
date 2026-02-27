import sqlite3
import os
from utils import config
from utils import logger


# aqui gestiono la conexion con la base de datos SQLite


def obtener_conexion():
    # obtengo la ruta de la base de datos desde la configuracion
    ruta_relativa = config.obtener("db_path", "datos/gestion_activos.db")
    ruta_base = os.path.dirname(os.path.dirname(__file__))
    ruta_db = os.path.join(ruta_base, ruta_relativa)

    # creo la carpeta si no existe
    os.makedirs(os.path.dirname(ruta_db), exist_ok=True)

    conexion = sqlite3.connect(ruta_db)

    # activo las claves foraneas para mantener la integridad referencial
    conexion.execute("PRAGMA foreign_keys = ON")

    return conexion


def inicializar_base_de_datos():
    log = logger.obtener_logger()
    try:
        con = obtener_conexion()
        cursor = con.cursor()

        # creo la tabla de activos si no existe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS activos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT UNIQUE NOT NULL,
                tipo TEXT NOT NULL,
                marca TEXT NOT NULL,
                modelo TEXT NOT NULL,
                numero_serie TEXT NOT NULL,
                ubicacion TEXT NOT NULL,
                fecha_alta TEXT NOT NULL,
                estado TEXT NOT NULL
            )
        """)

        # creo la tabla de incidencias con clave foranea al activo
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS incidencias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                activo_id INTEGER NOT NULL,
                fecha_apertura TEXT NOT NULL,
                prioridad TEXT NOT NULL,
                categoria TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                estado TEXT NOT NULL,
                tecnico TEXT NOT NULL,
                fecha_cierre TEXT,
                FOREIGN KEY (activo_id) REFERENCES activos(id)
            )
        """)

        # creo la tabla de auditoria para registrar todos los cambios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS auditoria (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha_hora TEXT NOT NULL,
                operacion TEXT NOT NULL,
                tabla TEXT NOT NULL,
                registro_id TEXT NOT NULL,
                descripcion TEXT NOT NULL
            )
        """)

        con.commit()
        con.close()
        log.info("Base de datos inicializada correctamente")

    except Exception as e:
        log.error(f"Error al inicializar la base de datos: {e}")
        raise
