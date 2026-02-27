from models.activo import Activo
from repositories import activo_repository, auditoria_repository
from utils import validaciones, logger
from utils import config


# aqui esta toda la logica de negocio para los activos


def crear_activo(datos):
    # aqui valido y creo un activo nuevo
    log = logger.obtener_logger()

    errores = validaciones.validar_activo(datos)
    if errores:
        return {"exito": False, "errores": errores}

    codigo = validaciones.limpiar_texto(datos["codigo"])

    # compruebo que no exista ya un activo con ese codigo
    if activo_repository.existe_codigo(codigo):
        return {"exito": False, "errores": ["Ya existe un activo con ese codigo"]}

    activo = Activo(
        codigo=codigo,
        tipo=validaciones.limpiar_texto(datos["tipo"]),
        marca=validaciones.limpiar_texto(datos["marca"]),
        modelo=validaciones.limpiar_texto(datos["modelo"]),
        numero_serie=validaciones.limpiar_texto(datos["numero_serie"]),
        ubicacion=validaciones.limpiar_texto(datos["ubicacion"]),
        fecha_alta=validaciones.limpiar_texto(datos["fecha_alta"]),
        estado=validaciones.limpiar_texto(datos["estado"])
    )

    try:
        nuevo_id = activo_repository.insertar(activo)
        activo.id = nuevo_id

        # registro la operacion en auditoria
        auditoria_repository.registrar("INSERT", "activos", codigo, f"Activo creado: {codigo} - {activo.marca} {activo.modelo}")
        log.info(f"Activo creado: {codigo}")

        return {"exito": True, "activo": activo}

    except Exception as e:
        log.error(f"Error al crear activo {codigo}: {e}")
        return {"exito": False, "errores": ["No se pudo guardar el activo. Revisa los datos e intentalo de nuevo"]}


def modificar_activo(activo_id, datos):
    # aqui valido y actualizo un activo existente
    log = logger.obtener_logger()

    errores = validaciones.validar_activo(datos)
    if errores:
        return {"exito": False, "errores": errores}

    codigo = validaciones.limpiar_texto(datos["codigo"])

    # compruebo que el codigo no lo use otro activo diferente
    if activo_repository.existe_codigo(codigo, excluir_id=activo_id):
        return {"exito": False, "errores": ["Ya existe otro activo con ese codigo"]}

    activo = Activo(
        id=activo_id,
        codigo=codigo,
        tipo=validaciones.limpiar_texto(datos["tipo"]),
        marca=validaciones.limpiar_texto(datos["marca"]),
        modelo=validaciones.limpiar_texto(datos["modelo"]),
        numero_serie=validaciones.limpiar_texto(datos["numero_serie"]),
        ubicacion=validaciones.limpiar_texto(datos["ubicacion"]),
        fecha_alta=validaciones.limpiar_texto(datos["fecha_alta"]),
        estado=validaciones.limpiar_texto(datos["estado"])
    )

    try:
        activo_repository.actualizar(activo)
        auditoria_repository.registrar("UPDATE", "activos", codigo, f"Activo modificado: {codigo}")
        log.info(f"Activo modificado: {codigo}")

        return {"exito": True, "activo": activo}

    except Exception as e:
        log.error(f"Error al modificar activo {activo_id}: {e}")
        return {"exito": False, "errores": ["No se pudo guardar los cambios. Intentalo de nuevo"]}


def eliminar_activo(activo_id):
    # aqui elimino un activo comprobando que no tenga incidencias
    log = logger.obtener_logger()

    activo = activo_repository.obtener_por_id(activo_id)
    if not activo:
        return {"exito": False, "errores": ["El activo no existe"]}

    from repositories import incidencia_repository
    num_incidencias = incidencia_repository.contar_por_activo(activo_id)
    if num_incidencias > 0:
        return {
            "exito": False,
            "errores": [f"No se puede eliminar porque tiene {num_incidencias} incidencia(s) asociada(s). Elimina primero las incidencias"]
        }

    try:
        activo_repository.eliminar(activo_id)
        auditoria_repository.registrar("DELETE", "activos", activo.codigo, f"Activo eliminado: {activo.codigo}")
        log.info(f"Activo eliminado: {activo.codigo}")

        return {"exito": True}

    except Exception as e:
        log.error(f"Error al eliminar activo {activo_id}: {e}")
        return {"exito": False, "errores": ["No se pudo eliminar el activo. Intentalo de nuevo"]}


def obtener_activo(activo_id):
    # aqui obtengo un activo por su id
    return activo_repository.obtener_por_id(activo_id)


def listar_activos_paginado(filtros, pagina):
    # aqui listo los activos con paginacion y filtros
    limite = config.obtener("registros_por_pagina", 15)
    offset = (pagina - 1) * limite
    activos = activo_repository.listar_paginado(filtros, offset, limite)
    total = activo_repository.contar_con_filtros(filtros)
    total_paginas = max(1, -(-total // limite))  # division redondeada hacia arriba
    return {
        "activos": activos,
        "pagina": pagina,
        "total_paginas": total_paginas,
        "total_registros": total
    }


def obtener_todos_los_activos():
    # aqui traigo todos los activos sin filtros (para usar en desplegables)
    return activo_repository.listar_todos()


def obtener_estadisticas_activos():
    # aqui obtengo las estadisticas de activos
    return activo_repository.obtener_estadisticas()
