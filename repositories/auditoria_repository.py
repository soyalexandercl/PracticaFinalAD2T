from db.database import obtener_conexion
from models.auditoria import Auditoria


# aqui guardo y consulto los registros de auditoria


def registrar(operacion, tabla, registro_id, descripcion):
    # aqui guardo un nuevo registro de auditoria con la fecha y hora actual
    from datetime import datetime
    con = obtener_conexion()
    try:
        cursor = con.cursor()
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO auditoria (fecha_hora, operacion, tabla, registro_id, descripcion)
            VALUES (?, ?, ?, ?, ?)
        """, (fecha_hora, operacion, tabla, str(registro_id), descripcion))
        con.commit()
    finally:
        con.close()


def listar_recientes(limite=50):
    # aqui traigo los ultimos registros de auditoria
    con = obtener_conexion()
    try:
        cursor = con.cursor()
        cursor.execute("""
            SELECT * FROM auditoria
            ORDER BY fecha_hora DESC
            LIMIT ?
        """, (limite,))
        filas = cursor.fetchall()
        return [Auditoria.desde_fila(f) for f in filas]
    finally:
        con.close()
