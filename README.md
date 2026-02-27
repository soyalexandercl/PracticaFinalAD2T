# Gestion de Activos Informaticos e Incidencias

Aplicacion de escritorio desarrollada en Python con SQLite y customtkinter para la gestion de activos informaticos y sus incidencias asociadas.

## Requisitos

- Python 3.9 o superior
- customtkinter

### Instalar dependencias

```bash
pip install customtkinter
```

## Como ejecutar

```bash
python main.py
```

## Estructura del proyecto

```
practica_acceso_datos/
|
+-- ui/                     Pantallas e interfaz de usuario
|   +-- main_window.py      Ventana principal con menu lateral
|   +-- activos_frame.py    Pantalla de gestion de activos
|   +-- incidencias_frame.py  Pantalla de gestion de incidencias
|   +-- estadisticas_frame.py  Pantalla de estadisticas
|   +-- auditoria_frame.py  Pantalla de historial de cambios
|   +-- componentes.py      Componentes reutilizables
|
+-- db/
|   +-- database.py         Conexion y creacion de tablas SQLite
|
+-- models/
|   +-- activo.py           Estructura de datos del activo
|   +-- incidencia.py       Estructura de datos de la incidencia
|   +-- auditoria.py        Estructura del registro de auditoria
|
+-- repositories/
|   +-- activo_repository.py      Consultas SQL de activos
|   +-- incidencia_repository.py  Consultas SQL de incidencias
|   +-- auditoria_repository.py   Consultas SQL de auditoria
|
+-- services/
|   +-- activo_service.py     Logica de negocio de activos
|   +-- incidencia_service.py  Logica de negocio de incidencias
|   +-- export_service.py     Exportacion e importacion de datos
|
+-- utils/
|   +-- config.py        Lee el archivo config.json
|   +-- logger.py        Configuracion del sistema de logs
|   +-- validaciones.py  Funciones de validacion
|
+-- exports/             Archivos exportados (CSV y JSON)
+-- logs/                Archivo app.log con registro de acciones
+-- datos/               Base de datos SQLite (se crea al iniciar)
+-- config.json          Configuracion de la aplicacion
+-- main.py              Punto de entrada
+-- README.md            Este archivo
```

## Funcionalidades

### Activos
- Dar de alta nuevos activos con codigo en formato ACT-XXXX
- Modificar activos existentes
- Eliminar activos (solo si no tienen incidencias asociadas)
- Buscar y filtrar por codigo, tipo, marca, estado y ubicacion
- Paginacion configurable
- Exportar a CSV
- Importar desde CSV

### Incidencias
- Crear incidencias asociadas a un activo
- Modificar incidencias
- Cambiar estado rapidamente
- Eliminar incidencias
- Filtros combinados: estado, prioridad, tecnico, activo, rango de fechas
- Exportar a JSON

### Estadisticas
- Total de activos e incidencias
- Activos por estado y tipo
- Incidencias por estado, prioridad y categoria
- Activos con mas incidencias

### Historial de cambios
- Registro automatico de todas las inserciones, modificaciones y eliminaciones
- Visualizacion de los ultimos 100 cambios

## Configuracion (config.json)

```json
{
    "db_path": "datos/gestion_activos.db",
    "registros_por_pagina": 15,
    "nivel_log": "INFO",
    "tema": "dark",
    "color_principal": "blue"
}
```

- `db_path`: ruta relativa a la base de datos SQLite
- `registros_por_pagina`: cuantos registros se muestran en cada pagina
- `nivel_log`: nivel de detalle del log (DEBUG, INFO, WARNING, ERROR)
- `tema`: modo de color de la interfaz (dark / light)
- `color_principal`: color del tema (blue, green, dark-blue)

## Formato del CSV de importacion

El archivo CSV para importar activos debe tener estas columnas:

```
codigo,tipo,marca,modelo,numero_serie,ubicacion,fecha_alta,estado
```
