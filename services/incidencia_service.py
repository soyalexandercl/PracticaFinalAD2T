from models.incidencia import Incidencia
from repositories import incidencia_repository, auditoria_repository
from utils import validaciones, logger
from utils import config


# aqui esta toda la logica de negocio para las incidencias


def crear_incidencia(datos):
    # aqui valido y creo una incidencia nueva
    log = logger.obtener_logger()

    errores = validaciones.validar_incidencia(datos)
    if errores:
        return {"exito": False, "errores": errores}

    incidencia = Incidencia(
        activo_id=int(datos["activo_id"]),
        fecha_apertura=validaciones.limpiar_texto(datos["fecha_apertura"]),
        prioridad=validaciones.limpiar_texto(datos["prioridad"]),
        categoria=validaciones.limpiar_texto(datos["categoria"]),
        descripcion=validaciones.limpiar_texto(datos["descripcion"]),
        estado=validaciones.limpiar_texto(datos["estado"]),
        tecnico=validaciones.limpiar_texto(datos["tecnico"]),
        fecha_cierre=validaciones.limpiar_texto(datos.get("fecha_cierre", "")) or None
    )

    try:
        nuevo_id = incidencia_repository.insertar(incidencia)
        incidencia.id = nuevo_id

        auditoria_repository.registrar("INSERT", "incidencias", nuevo_id, f"Incidencia creada para activo {datos['activo_id']}")
        log.info(f"Incidencia creada: id={nuevo_id} para activo {datos['activo_id']}")

        return {"exito": True, "incidencia": incidencia}

    except Exception as e:
        log.error(f"Error al crear incidencia: {e}")
        return {"exito": False, "errores": ["No se pudo guardar la incidencia. Intentalo de nuevo"]}


def modificar_incidencia(incidencia_id, datos):
    # aqui valido y actualizo una incidencia existente
    log = logger.obtener_logger()

    errores = validaciones.validar_incidencia(datos)
    if errores:
        return {"exito": False, "errores": errores}

    incidencia = Incidencia(
        id=incidencia_id,
        activo_id=int(datos["activo_id"]),
        fecha_apertura=validaciones.limpiar_texto(datos["fecha_apertura"]),
        prioridad=validaciones.limpiar_texto(datos["prioridad"]),
        categoria=validaciones.limpiar_texto(datos["categoria"]),
        descripcion=validaciones.limpiar_texto(datos["descripcion"]),
        estado=validaciones.limpiar_texto(datos["estado"]),
        tecnico=validaciones.limpiar_texto(datos["tecnico"]),
        fecha_cierre=validaciones.limpiar_texto(datos.get("fecha_cierre", "")) or None
    )

    try:
        incidencia_repository.actualizar(incidencia)
        auditoria_repository.registrar("UPDATE", "incidencias", incidencia_id, f"Incidencia {incidencia_id} modificada")
        log.info(f"Incidencia modificada: id={incidencia_id}")

        return {"exito": True, "incidencia": incidencia}

    except Exception as e:
        log.error(f"Error al modificar incidencia {incidencia_id}: {e}")
        return {"exito": False, "errores": ["No se pudo guardar los cambios. Intentalo de nuevo"]}


def cambiar_estado(incidencia_id, nuevo_estado, fecha_cierre=None):
    # aqui cambio solo el estado de una incidencia
    log = logger.obtener_logger()

    incidencia = incidencia_repository.obtener_por_id(incidencia_id)
    if not incidencia:
        return {"exito": False, "errores": ["La incidencia no existe"]}

    estado_anterior = incidencia.estado
    incidencia.estado = nuevo_estado

    if nuevo_estado == "Cerrada" and fecha_cierre:
        incidencia.fecha_cierre = fecha_cierre
    elif nuevo_estado == "Cerrada" and not incidencia.fecha_cierre:
        from datetime import datetime
        incidencia.fecha_cierre = datetime.now().strftime("%Y-%m-%d")

    try:
        incidencia_repository.actualizar(incidencia)
        auditoria_repository.registrar("UPDATE", "incidencias", incidencia_id,
                                       f"Estado cambiado de '{estado_anterior}' a '{nuevo_estado}'")
        log.info(f"Incidencia {incidencia_id}: estado cambiado a {nuevo_estado}")

        return {"exito": True}

    except Exception as e:
        log.error(f"Error al cambiar estado de incidencia {incidencia_id}: {e}")
        return {"exito": False, "errores": ["No se pudo cambiar el estado. Intentalo de nuevo"]}


def eliminar_incidencia(incidencia_id):
    # aqui elimino una incidencia
    log = logger.obtener_logger()

    incidencia = incidencia_repository.obtener_por_id(incidencia_id)
    if not incidencia:
        return {"exito": False, "errores": ["La incidencia no existe"]}

    try:
        incidencia_repository.eliminar(incidencia_id)
        auditoria_repository.registrar("DELETE", "incidencias", incidencia_id, f"Incidencia {incidencia_id} eliminada")
        log.info(f"Incidencia eliminada: id={incidencia_id}")

        return {"exito": True}

    except Exception as e:
        log.error(f"Error al eliminar incidencia {incidencia_id}: {e}")
        return {"exito": False, "errores": ["No se pudo eliminar la incidencia. Intentalo de nuevo"]}


def obtener_incidencia(incidencia_id):
    # aqui obtengo una incidencia por su id
    return incidencia_repository.obtener_por_id(incidencia_id)


def listar_incidencias_paginado(filtros, pagina):
    # aqui listo las incidencias con paginacion y filtros combinados
    limite = config.obtener("registros_por_pagina", 15)
    offset = (pagina - 1) * limite
    filas = incidencia_repository.listar_paginado_con_activo(filtros, offset, limite)
    total = incidencia_repository.contar_con_filtros(filtros)
    total_paginas = max(1, -(-total // limite))
    return {
        "filas": filas,
        "pagina": pagina,
        "total_paginas": total_paginas,
        "total_registros": total
    }


def obtener_estadisticas_incidencias():
    # aqui obtengo las estadisticas de incidencias
    return incidencia_repository.obtener_estadisticas()
