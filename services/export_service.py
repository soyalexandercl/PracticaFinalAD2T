import csv
import json
import os
from datetime import datetime
from repositories import activo_repository, incidencia_repository
from models.activo import Activo
from utils import logger, validaciones

# aqui gestiono la exportacion e importacion de datos

def _ruta_exports():
    # devuelvo la ruta de la carpeta exports
    ruta_base = os.path.dirname(os.path.dirname(__file__))
    ruta = os.path.join(ruta_base, "exports")
    os.makedirs(ruta, exist_ok=True)
    return ruta


def exportar_activos_csv(filtros=None):
    # aqui exporto los activos a un archivo CSV
    log = logger.obtener_logger()
    try:
        if filtros:
            activos = activo_repository.listar_paginado(filtros, 0, 999999)
        else:
            activos = activo_repository.listar_todos()

        nombre = f"activos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        ruta = os.path.join(_ruta_exports(), nombre)

        with open(ruta, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "codigo", "tipo", "marca", "modelo",
                                                    "numero_serie", "ubicacion", "fecha_alta", "estado"])
            writer.writeheader()
            for activo in activos:
                writer.writerow(activo.a_diccionario())

        log.info(f"Activos exportados a CSV: {nombre} ({len(activos)} registros)")
        return {"exito": True, "ruta": ruta, "total": len(activos)}

    except Exception as e:
        log.error(f"Error al exportar activos a CSV: {e}")
        return {"exito": False, "errores": ["No se pudo exportar. Intentalo de nuevo"]}


def exportar_incidencias_json(filtros=None):
    # aqui exporto las incidencias a un archivo JSON
    log = logger.obtener_logger()
    try:
        if filtros:
            filas = incidencia_repository.listar_paginado_con_activo(filtros, 0, 999999)
        else:
            incidencias = incidencia_repository.listar_todos()
            datos = [i.a_diccionario() for i in incidencias]
            nombre = f"incidencias_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            ruta = os.path.join(_ruta_exports(), nombre)
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
            log.info(f"Incidencias exportadas a JSON: {nombre} ({len(datos)} registros)")
            return {"exito": True, "ruta": ruta, "total": len(datos)}

        # cuando vienen con filtros las filas tienen mas columnas
        datos = []
        for fila in filas:
            datos.append({
                "id": fila[0],
                "activo_id": fila[1],
                "activo_codigo": fila[9] if len(fila) > 9 else "",
                "fecha_apertura": fila[2],
                "prioridad": fila[3],
                "categoria": fila[4],
                "descripcion": fila[5],
                "estado": fila[6],
                "tecnico": fila[7],
                "fecha_cierre": fila[8]
            })

        nombre = f"incidencias_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        ruta = os.path.join(_ruta_exports(), nombre)

        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)

        log.info(f"Incidencias exportadas a JSON: {nombre} ({len(datos)} registros)")
        return {"exito": True, "ruta": ruta, "total": len(datos)}

    except Exception as e:
        log.error(f"Error al exportar incidencias a JSON: {e}")
        return {"exito": False, "errores": ["No se pudo exportar. Intentalo de nuevo"]}


def importar_activos_csv(ruta_archivo):
    # aqui importo activos desde un archivo CSV usando transaccion
    log = logger.obtener_logger()
    from db.database import obtener_conexion
    from repositories import auditoria_repository

    insertados = 0
    errores_filas = []

    con = obtener_conexion()
    try:
        # uso una transaccion para que si algo falla se deshaga todo
        con.execute("BEGIN")

        with open(ruta_archivo, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for numero_fila, fila in enumerate(reader, start=2):
                datos = {
                    "codigo": fila.get("codigo", "").strip(),
                    "tipo": fila.get("tipo", "").strip(),
                    "marca": fila.get("marca", "").strip(),
                    "modelo": fila.get("modelo", "").strip(),
                    "numero_serie": fila.get("numero_serie", "").strip(),
                    "ubicacion": fila.get("ubicacion", "").strip(),
                    "fecha_alta": fila.get("fecha_alta", "").strip(),
                    "estado": fila.get("estado", "").strip()
                }

                errores = validaciones.validar_activo(datos)
                if errores:
                    errores_filas.append(f"Fila {numero_fila}: {', '.join(errores)}")
                    continue

                if activo_repository.existe_codigo(datos["codigo"]):
                    errores_filas.append(f"Fila {numero_fila}: Ya existe el codigo {datos['codigo']}")
                    continue

                activo = Activo(
                    codigo=datos["codigo"],
                    tipo=datos["tipo"],
                    marca=datos["marca"],
                    modelo=datos["modelo"],
                    numero_serie=datos["numero_serie"],
                    ubicacion=datos["ubicacion"],
                    fecha_alta=datos["fecha_alta"],
                    estado=datos["estado"]
                )

                activo_repository.insertar_con_conexion(activo, con)
                insertados += 1

        con.commit()
        log.info(f"Importacion CSV completada: {insertados} activos importados")

        # registro en auditoria
        auditoria_repository.registrar("INSERT", "activos", "importacion", f"Importados {insertados} activos desde CSV")

        return {"exito": True, "insertados": insertados, "errores_filas": errores_filas}

    except Exception as e:
        con.rollback()
        log.error(f"Error en importacion CSV, se deshizo la operacion: {e}")
        return {"exito": False, "errores": ["Error durante la importacion. No se guardo ningun dato"]}
    finally:
        con.close()
