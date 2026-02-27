from db.database import obtener_conexion
from models.activo import Activo

# aqui hago todas las consultas a la base de datos para los activos

def insertar(activo):
    # aqui guardo un activo nuevo en la base de datos
    con = obtener_conexion()
    try:
        cursor = con.cursor()
        cursor.execute("""
            INSERT INTO activos (codigo, tipo, marca, modelo, numero_serie, ubicacion, fecha_alta, estado)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (activo.codigo, activo.tipo, activo.marca, activo.modelo,
              activo.numero_serie, activo.ubicacion, activo.fecha_alta, activo.estado))
        con.commit()
        return cursor.lastrowid
    finally:
        con.close()


def actualizar(activo):
    # aqui actualizo los datos de un activo existente
    con = obtener_conexion()
    try:
        cursor = con.cursor()
        cursor.execute("""
            UPDATE activos
            SET codigo=?, tipo=?, marca=?, modelo=?, numero_serie=?, ubicacion=?, fecha_alta=?, estado=?
            WHERE id=?
        """, (activo.codigo, activo.tipo, activo.marca, activo.modelo,
              activo.numero_serie, activo.ubicacion, activo.fecha_alta, activo.estado, activo.id))
        con.commit()
    finally:
        con.close()


def eliminar(activo_id):
    # aqui elimino un activo por su id
    con = obtener_conexion()
    try:
        cursor = con.cursor()
        cursor.execute("DELETE FROM activos WHERE id=?", (activo_id,))
        con.commit()
    finally:
        con.close()


def obtener_por_id(activo_id):
    # aqui busco un activo por su id
    con = obtener_conexion()
    try:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM activos WHERE id=?", (activo_id,))
        fila = cursor.fetchone()
        if fila:
            return Activo.desde_fila(fila)
        return None
    finally:
        con.close()


def obtener_por_codigo(codigo):
    # aqui busco un activo por su codigo unico
    con = obtener_conexion()
    try:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM activos WHERE codigo=?", (codigo,))
        fila = cursor.fetchone()
        if fila:
            return Activo.desde_fila(fila)
        return None
    finally:
        con.close()


def listar_todos():
    # aqui traigo todos los activos de la base de datos
    con = obtener_conexion()
    try:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM activos ORDER BY codigo")
        filas = cursor.fetchall()
        return [Activo.desde_fila(f) for f in filas]
    finally:
        con.close()


def listar_paginado(filtros, offset, limite):
    # aqui traigo activos con filtros y paginacion usando LIMIT y OFFSET
    con = obtener_conexion()
    try:
        cursor = con.cursor()

        condiciones = []
        parametros = []

        # aqui construyo los filtros de busqueda de forma segura
        if filtros.get("codigo"):
            condiciones.append("codigo LIKE ?")
            parametros.append(f"%{filtros['codigo']}%")

        if filtros.get("tipo"):
            condiciones.append("tipo LIKE ?")
            parametros.append(f"%{filtros['tipo']}%")

        if filtros.get("marca"):
            condiciones.append("marca LIKE ?")
            parametros.append(f"%{filtros['marca']}%")

        if filtros.get("ubicacion"):
            condiciones.append("ubicacion LIKE ?")
            parametros.append(f"%{filtros['ubicacion']}%")

        if filtros.get("estado"):
            condiciones.append("estado = ?")
            parametros.append(filtros["estado"])

        sql = "SELECT * FROM activos"
        if condiciones:
            sql += " WHERE " + " AND ".join(condiciones)
        sql += " ORDER BY codigo LIMIT ? OFFSET ?"

        parametros.extend([limite, offset])
        cursor.execute(sql, parametros)
        filas = cursor.fetchall()
        return [Activo.desde_fila(f) for f in filas]
    finally:
        con.close()


def contar_con_filtros(filtros):
    # aqui cuento los registros que coinciden con los filtros para la paginacion
    con = obtener_conexion()
    try:
        cursor = con.cursor()

        condiciones = []
        parametros = []

        if filtros.get("codigo"):
            condiciones.append("codigo LIKE ?")
            parametros.append(f"%{filtros['codigo']}%")

        if filtros.get("tipo"):
            condiciones.append("tipo LIKE ?")
            parametros.append(f"%{filtros['tipo']}%")

        if filtros.get("marca"):
            condiciones.append("marca LIKE ?")
            parametros.append(f"%{filtros['marca']}%")

        if filtros.get("ubicacion"):
            condiciones.append("ubicacion LIKE ?")
            parametros.append(f"%{filtros['ubicacion']}%")

        if filtros.get("estado"):
            condiciones.append("estado = ?")
            parametros.append(filtros["estado"])

        sql = "SELECT COUNT(*) FROM activos"
        if condiciones:
            sql += " WHERE " + " AND ".join(condiciones)

        cursor.execute(sql, parametros)
        return cursor.fetchone()[0]
    finally:
        con.close()


def existe_codigo(codigo, excluir_id=None):
    # aqui compruebo si ya existe un activo con ese codigo
    con = obtener_conexion()
    try:
        cursor = con.cursor()
        if excluir_id:
            cursor.execute("SELECT id FROM activos WHERE codigo=? AND id!=?", (codigo, excluir_id))
        else:
            cursor.execute("SELECT id FROM activos WHERE codigo=?", (codigo,))
        return cursor.fetchone() is not None
    finally:
        con.close()


def obtener_estadisticas():
    # aqui calculo estadisticas simples de los activos
    con = obtener_conexion()
    try:
        cursor = con.cursor()

        cursor.execute("SELECT COUNT(*) FROM activos")
        total = cursor.fetchone()[0]

        cursor.execute("SELECT estado, COUNT(*) FROM activos GROUP BY estado")
        por_estado = cursor.fetchall()

        cursor.execute("SELECT tipo, COUNT(*) FROM activos GROUP BY tipo ORDER BY COUNT(*) DESC")
        por_tipo = cursor.fetchall()

        return {
            "total": total,
            "por_estado": por_estado,
            "por_tipo": por_tipo
        }
    finally:
        con.close()


def insertar_con_conexion(activo, con):
    # aqui inserto un activo usando una conexion existente (para transacciones)
    cursor = con.cursor()
    cursor.execute("""
        INSERT INTO activos (codigo, tipo, marca, modelo, numero_serie, ubicacion, fecha_alta, estado)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (activo.codigo, activo.tipo, activo.marca, activo.modelo,
          activo.numero_serie, activo.ubicacion, activo.fecha_alta, activo.estado))
    return cursor.lastrowid
