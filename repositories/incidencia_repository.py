from db.database import obtener_conexion
from models.incidencia import Incidencia

# aqui hago todas las consultas a la base de datos para las incidencias

def insertar(incidencia):
    # aqui guardo una incidencia nueva en la base de datos
    con = obtener_conexion()
    try:
        cursor = con.cursor()
        cursor.execute("""
            INSERT INTO incidencias (activo_id, fecha_apertura, prioridad, categoria, descripcion, estado, tecnico, fecha_cierre)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (incidencia.activo_id, incidencia.fecha_apertura, incidencia.prioridad,
              incidencia.categoria, incidencia.descripcion, incidencia.estado,
              incidencia.tecnico, incidencia.fecha_cierre))
        con.commit()
        return cursor.lastrowid
    finally:
        con.close()


def actualizar(incidencia):
    # aqui actualizo los datos de una incidencia existente
    con = obtener_conexion()
    try:
        cursor = con.cursor()
        cursor.execute("""
            UPDATE incidencias
            SET activo_id=?, fecha_apertura=?, prioridad=?, categoria=?, descripcion=?,
                estado=?, tecnico=?, fecha_cierre=?
            WHERE id=?
        """, (incidencia.activo_id, incidencia.fecha_apertura, incidencia.prioridad,
              incidencia.categoria, incidencia.descripcion, incidencia.estado,
              incidencia.tecnico, incidencia.fecha_cierre, incidencia.id))
        con.commit()
    finally:
        con.close()


def eliminar(incidencia_id):
    # aqui elimino una incidencia por su id
    con = obtener_conexion()
    try:
        cursor = con.cursor()
        cursor.execute("DELETE FROM incidencias WHERE id=?", (incidencia_id,))
        con.commit()
    finally:
        con.close()


def obtener_por_id(incidencia_id):
    # aqui busco una incidencia por su id
    con = obtener_conexion()
    try:
        cursor = con.cursor()
        cursor.execute("""
            SELECT i.id, i.activo_id, i.fecha_apertura, i.prioridad, i.categoria,
                   i.descripcion, i.estado, i.tecnico, i.fecha_cierre
            FROM incidencias i
            WHERE i.id=?
        """, (incidencia_id,))
        fila = cursor.fetchone()
        if fila:
            return Incidencia.desde_fila(fila)
        return None
    finally:
        con.close()


def listar_todos():
    # aqui traigo todas las incidencias
    con = obtener_conexion()
    try:
        cursor = con.cursor()
        cursor.execute("""
            SELECT i.id, i.activo_id, i.fecha_apertura, i.prioridad, i.categoria,
                   i.descripcion, i.estado, i.tecnico, i.fecha_cierre
            FROM incidencias i
            ORDER BY i.fecha_apertura DESC
        """)
        filas = cursor.fetchall()
        return [Incidencia.desde_fila(f) for f in filas]
    finally:
        con.close()


def listar_paginado_con_activo(filtros, offset, limite):
    # aqui traigo incidencias con filtros combinados y datos del activo para mostrar en la tabla
    con = obtener_conexion()
    try:
        cursor = con.cursor()

        condiciones = []
        parametros = []

        # aqui construyo los filtros de busqueda de forma segura
        if filtros.get("estado"):
            condiciones.append("i.estado = ?")
            parametros.append(filtros["estado"])

        if filtros.get("prioridad"):
            condiciones.append("i.prioridad = ?")
            parametros.append(filtros["prioridad"])

        if filtros.get("categoria"):
            condiciones.append("i.categoria LIKE ?")
            parametros.append(f"%{filtros['categoria']}%")

        if filtros.get("tecnico"):
            condiciones.append("i.tecnico LIKE ?")
            parametros.append(f"%{filtros['tecnico']}%")

        if filtros.get("activo_codigo"):
            condiciones.append("a.codigo LIKE ?")
            parametros.append(f"%{filtros['activo_codigo']}%")

        if filtros.get("fecha_desde"):
            condiciones.append("i.fecha_apertura >= ?")
            parametros.append(filtros["fecha_desde"])

        if filtros.get("fecha_hasta"):
            condiciones.append("i.fecha_apertura <= ?")
            parametros.append(filtros["fecha_hasta"])

        sql = """
            SELECT i.id, i.activo_id, i.fecha_apertura, i.prioridad, i.categoria,
                   i.descripcion, i.estado, i.tecnico, i.fecha_cierre,
                   a.codigo as activo_codigo
            FROM incidencias i
            LEFT JOIN activos a ON i.activo_id = a.id
        """
        if condiciones:
            sql += " WHERE " + " AND ".join(condiciones)
        sql += " ORDER BY i.fecha_apertura DESC LIMIT ? OFFSET ?"

        parametros.extend([limite, offset])
        cursor.execute(sql, parametros)
        return cursor.fetchall()
    finally:
        con.close()


def contar_con_filtros(filtros):
    # aqui cuento las incidencias que coinciden con los filtros
    con = obtener_conexion()
    try:
        cursor = con.cursor()

        condiciones = []
        parametros = []

        if filtros.get("estado"):
            condiciones.append("i.estado = ?")
            parametros.append(filtros["estado"])

        if filtros.get("prioridad"):
            condiciones.append("i.prioridad = ?")
            parametros.append(filtros["prioridad"])

        if filtros.get("categoria"):
            condiciones.append("i.categoria LIKE ?")
            parametros.append(f"%{filtros['categoria']}%")

        if filtros.get("tecnico"):
            condiciones.append("i.tecnico LIKE ?")
            parametros.append(f"%{filtros['tecnico']}%")

        if filtros.get("activo_codigo"):
            condiciones.append("a.codigo LIKE ?")
            parametros.append(f"%{filtros['activo_codigo']}%")

        if filtros.get("fecha_desde"):
            condiciones.append("i.fecha_apertura >= ?")
            parametros.append(filtros["fecha_desde"])

        if filtros.get("fecha_hasta"):
            condiciones.append("i.fecha_apertura <= ?")
            parametros.append(filtros["fecha_hasta"])

        sql = """
            SELECT COUNT(*)
            FROM incidencias i
            LEFT JOIN activos a ON i.activo_id = a.id
        """
        if condiciones:
            sql += " WHERE " + " AND ".join(condiciones)

        cursor.execute(sql, parametros)
        return cursor.fetchone()[0]
    finally:
        con.close()


def contar_por_activo(activo_id):
    # aqui cuento cuantas incidencias tiene un activo
    con = obtener_conexion()
    try:
        cursor = con.cursor()
        cursor.execute("SELECT COUNT(*) FROM incidencias WHERE activo_id=?", (activo_id,))
        return cursor.fetchone()[0]
    finally:
        con.close()


def obtener_estadisticas():
    # aqui calculo estadisticas de las incidencias
    con = obtener_conexion()
    try:
        cursor = con.cursor()

        cursor.execute("SELECT COUNT(*) FROM incidencias")
        total = cursor.fetchone()[0]

        cursor.execute("SELECT estado, COUNT(*) FROM incidencias GROUP BY estado")
        por_estado = cursor.fetchall()

        cursor.execute("SELECT prioridad, COUNT(*) FROM incidencias GROUP BY prioridad")
        por_prioridad = cursor.fetchall()

        cursor.execute("SELECT categoria, COUNT(*) FROM incidencias GROUP BY categoria ORDER BY COUNT(*) DESC")
        por_categoria = cursor.fetchall()

        # los activos con mas incidencias
        cursor.execute("""
            SELECT a.codigo, a.marca, a.modelo, COUNT(i.id) as num_incidencias
            FROM activos a
            LEFT JOIN incidencias i ON a.id = i.activo_id
            GROUP BY a.id
            ORDER BY num_incidencias DESC
            LIMIT 5
        """)
        top_activos = cursor.fetchall()

        return {
            "total": total,
            "por_estado": por_estado,
            "por_prioridad": por_prioridad,
            "por_categoria": por_categoria,
            "top_activos": top_activos
        }
    finally:
        con.close()
