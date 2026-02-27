import sys
import os

# aqui me aseguro de que Python encuentre los modulos del proyecto
sys.path.insert(0, os.path.dirname(__file__))

from utils import config
from utils import logger
from db.database import inicializar_base_de_datos
from ui.main_window import VentanaPrincipal

# aqui arranco la aplicacion

def main():
    # primero cargo la configuracion externa
    config.cargar_configuracion()

    # luego inicializo el logger con el nivel configurado
    log = logger.obtener_logger()
    log.info("Iniciando la aplicacion de gestion de activos")

    # creo la base de datos y las tablas si no existen
    inicializar_base_de_datos()

    # creo y arranco la ventana principal
    app = VentanaPrincipal()
    app.mainloop()

    log.info("Aplicacion cerrada")


if __name__ == "__main__":
    main()
