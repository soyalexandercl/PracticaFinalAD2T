import re
from datetime import datetime

# aqui tengo todas las funciones de validacion que uso en la aplicacion

def validar_codigo_activo(codigo):
    # el codigo debe seguir el patron ACT-XXXX donde X son digitos
    patron = r'^ACT-\d{4}$'
    return bool(re.match(patron, codigo))


def validar_fecha(fecha_texto):
    # compruebo que la fecha tenga formato correcto YYYY-MM-DD
    try:
        datetime.strptime(fecha_texto, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validar_no_vacio(texto):
    # compruebo que el campo no este vacio ni sea solo espacios
    return texto is not None and str(texto).strip() != ""


def validar_longitud(texto, minimo=1, maximo=200):
    # compruebo que el texto tenga una longitud razonable
    if texto is None:
        return False
    largo = len(str(texto).strip())
    return minimo <= largo <= maximo


def limpiar_texto(texto):
    # elimino espacios al principio y al final
    if texto is None:
        return ""
    return str(texto).strip()


def validar_activo(datos):
    # aqui valido todos los campos del activo antes de guardarlo
    errores = []

    if not validar_no_vacio(datos.get("codigo")):
        errores.append("El codigo es obligatorio")
    elif not validar_codigo_activo(datos.get("codigo", "")):
        errores.append("El codigo debe tener el formato ACT-XXXX (ejemplo: ACT-0001)")

    campos_obligatorios = ["tipo", "marca", "modelo", "numero_serie", "ubicacion", "fecha_alta", "estado"]
    nombres_legibles = {
        "tipo": "Tipo",
        "marca": "Marca",
        "modelo": "Modelo",
        "numero_serie": "Numero de serie",
        "ubicacion": "Ubicacion",
        "fecha_alta": "Fecha de alta",
        "estado": "Estado"
    }

    for campo in campos_obligatorios:
        if not validar_no_vacio(datos.get(campo)):
            errores.append(f"El campo '{nombres_legibles[campo]}' es obligatorio")

    if validar_no_vacio(datos.get("fecha_alta")):
        if not validar_fecha(datos.get("fecha_alta", "")):
            errores.append("La fecha de alta debe tener el formato YYYY-MM-DD (ejemplo: 2024-01-15)")

    return errores


def validar_incidencia(datos):
    # aqui valido todos los campos de la incidencia antes de guardarla
    errores = []

    if not validar_no_vacio(datos.get("activo_id")):
        errores.append("Debes seleccionar un activo")

    campos_obligatorios = ["fecha_apertura", "prioridad", "categoria", "descripcion", "estado", "tecnico"]
    nombres_legibles = {
        "fecha_apertura": "Fecha de apertura",
        "prioridad": "Prioridad",
        "categoria": "Categoria",
        "descripcion": "Descripcion",
        "estado": "Estado",
        "tecnico": "Tecnico asignado"
    }

    for campo in campos_obligatorios:
        if not validar_no_vacio(datos.get(campo)):
            errores.append(f"El campo '{nombres_legibles[campo]}' es obligatorio")

    if validar_no_vacio(datos.get("fecha_apertura")):
        if not validar_fecha(datos.get("fecha_apertura", "")):
            errores.append("La fecha de apertura debe tener el formato YYYY-MM-DD")

    if validar_no_vacio(datos.get("fecha_cierre")):
        if not validar_fecha(datos.get("fecha_cierre", "")):
            errores.append("La fecha de cierre debe tener el formato YYYY-MM-DD")

    return errores
