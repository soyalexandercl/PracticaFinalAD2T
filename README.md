# SISTEMA DE GESTIÓN DE ACTIVOS INFORMÁTICOS E INCIDENCIAS

Este proyecto es una aplicación de escritorio profesional diseñada para el inventariado y control técnico de activos IT. La herramienta ofrece una interfaz gráfica moderna optimizada en modo oscuro permanente, facilitando la gestión de hardware y el seguimiento de incidencias técnicas en una organización.

## CARACTERÍSTICAS PRINCIPALES

* Gestión de Activos: Permite el registro completo de dispositivos como ordenadores, monitores, servidores y periféricos, incluyendo marca, modelo, número de serie y ubicación.
* Control de Incidencias: Sistema para reportar y gestionar fallos técnicos vinculados a activos específicos, permitiendo definir prioridades, categorías y técnicos asignados.
* Auditoría de Sistema: Módulo que registra de forma automática todas las acciones de inserción, edición y borrado para asegurar la trazabilidad de los datos.
* Dashboard de Estadísticas: Visualización de métricas sobre el estado actual del inventario y la distribución de los activos por tipo.
* Importación e Importación: Herramientas para la exportación de informes en formatos CSV y JSON, además de carga masiva de datos desde archivos CSV.

## TECNOLOGÍAS UTILIZADAS

* Python 3.10+: Lenguaje de programación principal.
* CustomTkinter: Biblioteca para la interfaz gráfica moderna.
* SQLite: Motor de base de datos para almacenamiento local persistente.
* Pillow (PIL): Gestión de imágenes en la interfaz.

## ESTRUCTURA DEL PROYECTO

* datos/: Almacenamiento de la base de datos (.db) y archivos de prueba.
* db/: Lógica de conexión y configuración de la base de datos.
* exports/: Directorio donde se guardan los archivos CSV y JSON generados.
* logs/: Registro persistente de eventos y errores del sistema (app.log).
* models/: Definición de las clases de datos (Activo, Incidencia, Auditoria).
* repositories/: Capa de acceso a datos y consultas SQL.
* services/: Lógica de negocio y procesamiento masivo de datos.
* ui/: Componentes de la interfaz de usuario y frames de navegación.
* utils/: Utilidades para validación, configuración y sistema de logs.
* main.py: Punto de entrada principal de la aplicación.

## INSTALACIÓN Y EJECUCIÓN

1. Requisitos previos:
   * Instalación de Python 3.10 o superior.
   * Instalación de dependencias: pip install customtkinter Pillow

2. Inicio de la aplicación:
   Ejecutar desde la terminal en la raíz del proyecto: python main.py

## FORMATO DE IMPORTACIÓN MASIVA
Para importar activos desde un archivo externo, el CSV debe incluir exactamente los siguientes encabezados:
codigo, tipo, marca, modelo, numero_serie, ubicacion, fecha_alta, estado.