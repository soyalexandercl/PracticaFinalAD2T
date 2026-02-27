import customtkinter as ctk
from tkinter import ttk
from services import incidencia_service, activo_service, export_service
from ui.componentes import crear_tabla, mostrar_mensaje_error, mostrar_mensaje_ok, pedir_confirmacion


# aqui esta la pantalla de gestion de incidencias


PRIORIDADES = ["Baja", "Media", "Alta", "Critica"]
ESTADOS_INC = ["Abierta", "En progreso", "Pendiente", "Resuelta", "Cerrada"]
CATEGORIAS = ["Hardware", "Software", "Red", "Seguridad", "Mantenimiento", "Otro"]


class IncidenciasFrame(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self._pagina_actual = 1
        self._total_paginas = 1
        self._filtros = {}
        self._id_seleccionado = None

        self._construir_interfaz()
        self._cargar_datos()

    def _construir_interfaz(self):
        # aqui construyo toda la pantalla de incidencias

        ctk.CTkLabel(self, text="Gestion de Incidencias",
                     font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(10, 5), anchor="w", padx=15)

        # panel de filtros avanzados
        frame_filtros = ctk.CTkFrame(self)
        frame_filtros.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(frame_filtros, text="Buscar y filtrar:", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, columnspan=8, padx=10, pady=(8, 2), sticky="w")

        ctk.CTkLabel(frame_filtros, text="Estado:").grid(row=1, column=0, padx=(10, 3), pady=5, sticky="w")
        self._filtro_estado = ctk.CTkComboBox(frame_filtros, values=[""] + ESTADOS_INC, width=120)
        self._filtro_estado.set("")
        self._filtro_estado.grid(row=1, column=1, padx=(0, 8), pady=5)

        ctk.CTkLabel(frame_filtros, text="Prioridad:").grid(row=1, column=2, padx=(0, 3), pady=5, sticky="w")
        self._filtro_prioridad = ctk.CTkComboBox(frame_filtros, values=[""] + PRIORIDADES, width=110)
        self._filtro_prioridad.set("")
        self._filtro_prioridad.grid(row=1, column=3, padx=(0, 8), pady=5)

        ctk.CTkLabel(frame_filtros, text="Tecnico:").grid(row=1, column=4, padx=(0, 3), pady=5, sticky="w")
        self._filtro_tecnico = ctk.CTkEntry(frame_filtros, width=120, placeholder_text="Nombre...")
        self._filtro_tecnico.grid(row=1, column=5, padx=(0, 8), pady=5)

        ctk.CTkLabel(frame_filtros, text="Cod. Activo:").grid(row=1, column=6, padx=(0, 3), pady=5, sticky="w")
        self._filtro_activo = ctk.CTkEntry(frame_filtros, width=100, placeholder_text="ACT-...")
        self._filtro_activo.grid(row=1, column=7, padx=(0, 8), pady=5)

        ctk.CTkLabel(frame_filtros, text="Desde:").grid(row=2, column=0, padx=(10, 3), pady=5, sticky="w")
        self._filtro_fecha_desde = ctk.CTkEntry(frame_filtros, width=110, placeholder_text="2024-01-01")
        self._filtro_fecha_desde.grid(row=2, column=1, padx=(0, 8), pady=5)

        ctk.CTkLabel(frame_filtros, text="Hasta:").grid(row=2, column=2, padx=(0, 3), pady=5, sticky="w")
        self._filtro_fecha_hasta = ctk.CTkEntry(frame_filtros, width=110, placeholder_text="2024-12-31")
        self._filtro_fecha_hasta.grid(row=2, column=3, padx=(0, 8), pady=5)

        ctk.CTkButton(frame_filtros, text="Buscar", command=self._buscar, width=90).grid(
            row=2, column=4, padx=5, pady=5)
        ctk.CTkButton(frame_filtros, text="Limpiar", command=self._limpiar_filtros,
                      fg_color="gray40", hover_color="gray30", width=90).grid(row=2, column=5, padx=5, pady=5)

        # tabla de incidencias
        columnas = ["ID", "Activo", "Fecha", "Prioridad", "Categoria", "Estado", "Tecnico", "Descripcion"]
        anchos = [40, 90, 90, 80, 100, 100, 110, 200]
        frame_tabla, self._tabla = crear_tabla(self, columnas, anchos)
        frame_tabla.pack(fill="both", expand=True, padx=15, pady=5)

        self._tabla.bind("<<TreeviewSelect>>", self._al_seleccionar)

        # paginacion
        frame_paginas = ctk.CTkFrame(self, fg_color="transparent")
        frame_paginas.pack(fill="x", padx=15, pady=2)

        ctk.CTkButton(frame_paginas, text="< Anterior", command=self._pagina_anterior, width=90).pack(side="left", padx=3)
        self._label_pagina = ctk.CTkLabel(frame_paginas, text="Pagina 1 de 1")
        self._label_pagina.pack(side="left", padx=10)
        ctk.CTkButton(frame_paginas, text="Siguiente >", command=self._pagina_siguiente, width=90).pack(side="left", padx=3)
        self._label_total = ctk.CTkLabel(frame_paginas, text="")
        self._label_total.pack(side="left", padx=15)

        # botones de accion
        frame_acciones = ctk.CTkFrame(self, fg_color="transparent")
        frame_acciones.pack(fill="x", padx=15, pady=(2, 10))

        ctk.CTkButton(frame_acciones, text="Nueva Incidencia", command=self._abrir_formulario_nuevo,
                      width=140).pack(side="left", padx=3)
        ctk.CTkButton(frame_acciones, text="Modificar", command=self._abrir_formulario_editar,
                      fg_color="#5a9e5a", hover_color="#4a8e4a", width=100).pack(side="left", padx=3)
        ctk.CTkButton(frame_acciones, text="Cambiar Estado", command=self._abrir_cambiar_estado,
                      fg_color="#e69500", hover_color="#c57d00", width=130).pack(side="left", padx=3)
        ctk.CTkButton(frame_acciones, text="Eliminar", command=self._confirmar_eliminar,
                      fg_color="#d9534f", hover_color="#c9302c", width=100).pack(side="left", padx=3)

        ctk.CTkLabel(frame_acciones, text="|", text_color="gray").pack(side="left", padx=5)
        ctk.CTkButton(frame_acciones, text="Exportar JSON", command=self._exportar_json,
                      fg_color="gray40", hover_color="gray30", width=120).pack(side="left", padx=3)

    def _cargar_datos(self):
        # aqui cargo las incidencias en la tabla con filtros y paginacion
        resultado = incidencia_service.listar_incidencias_paginado(self._filtros, self._pagina_actual)

        self._total_paginas = resultado["total_paginas"]
        self._label_pagina.configure(text=f"Pagina {self._pagina_actual} de {self._total_paginas}")
        self._label_total.configure(text=f"Total: {resultado['total_registros']} incidencias")

        for fila in self._tabla.get_children():
            self._tabla.delete(fila)

        for fila in resultado["filas"]:
            activo_codigo = fila[9] if len(fila) > 9 else str(fila[1])
            descripcion_corta = str(fila[5])[:60] + "..." if len(str(fila[5])) > 60 else str(fila[5])
            self._tabla.insert("", "end", values=(
                fila[0], activo_codigo, fila[2], fila[3], fila[4], fila[6], fila[7], descripcion_corta
            ))

    def _al_seleccionar(self, evento):
        seleccion = self._tabla.selection()
        if seleccion:
            valores = self._tabla.item(seleccion[0])["values"]
            self._id_seleccionado = valores[0] if valores else None
        else:
            self._id_seleccionado = None

    def _buscar(self):
        self._filtros = {
            "estado": self._filtro_estado.get().strip(),
            "prioridad": self._filtro_prioridad.get().strip(),
            "tecnico": self._filtro_tecnico.get().strip(),
            "activo_codigo": self._filtro_activo.get().strip(),
            "fecha_desde": self._filtro_fecha_desde.get().strip(),
            "fecha_hasta": self._filtro_fecha_hasta.get().strip()
        }
        self._pagina_actual = 1
        self._cargar_datos()

    def _limpiar_filtros(self):
        self._filtro_estado.set("")
        self._filtro_prioridad.set("")
        self._filtro_tecnico.delete(0, "end")
        self._filtro_activo.delete(0, "end")
        self._filtro_fecha_desde.delete(0, "end")
        self._filtro_fecha_hasta.delete(0, "end")
        self._filtros = {}
        self._pagina_actual = 1
        self._cargar_datos()

    def _pagina_anterior(self):
        if self._pagina_actual > 1:
            self._pagina_actual -= 1
            self._cargar_datos()

    def _pagina_siguiente(self):
        if self._pagina_actual < self._total_paginas:
            self._pagina_actual += 1
            self._cargar_datos()

    def _abrir_formulario_nuevo(self):
        FormularioIncidencia(self, modo="nuevo", callback=self._cargar_datos)

    def _abrir_formulario_editar(self):
        if not self._id_seleccionado:
            mostrar_mensaje_error("Nada seleccionado", "Selecciona una incidencia de la lista para modificarla")
            return
        FormularioIncidencia(self, modo="editar", incidencia_id=self._id_seleccionado, callback=self._cargar_datos)

    def _abrir_cambiar_estado(self):
        if not self._id_seleccionado:
            mostrar_mensaje_error("Nada seleccionado", "Selecciona una incidencia para cambiar su estado")
            return
        CambiarEstadoDialog(self, incidencia_id=self._id_seleccionado, callback=self._cargar_datos)

    def _confirmar_eliminar(self):
        if not self._id_seleccionado:
            mostrar_mensaje_error("Nada seleccionado", "Selecciona una incidencia de la lista para eliminarla")
            return
        pedir_confirmacion(
            "Confirmar eliminacion",
            "Estas seguro de que quieres eliminar esta incidencia?\nEsta accion no se puede deshacer.",
            self._eliminar_incidencia
        )

    def _eliminar_incidencia(self):
        resultado = incidencia_service.eliminar_incidencia(self._id_seleccionado)
        if resultado["exito"]:
            mostrar_mensaje_ok("Eliminado", "La incidencia se ha eliminado correctamente")
            self._id_seleccionado = None
            self._cargar_datos()
        else:
            mostrar_mensaje_error("No se pudo eliminar", "\n".join(resultado["errores"]))

    def _exportar_json(self):
        resultado = export_service.exportar_incidencias_json(self._filtros if self._filtros else None)
        if resultado["exito"]:
            mostrar_mensaje_ok("Exportacion completada",
                               f"Se han exportado {resultado['total']} incidencias.\nArchivo guardado en la carpeta exports/")
        else:
            mostrar_mensaje_error("Error al exportar", "\n".join(resultado["errores"]))


class FormularioIncidencia(ctk.CTkToplevel):
    # aqui esta el formulario para crear o editar una incidencia

    def __init__(self, parent, modo, callback, incidencia_id=None):
        super().__init__(parent)

        self._modo = modo
        self._incidencia_id = incidencia_id
        self._callback = callback

        titulo = "Nueva Incidencia" if modo == "nuevo" else "Modificar Incidencia"
        self.title(titulo)
        self.geometry("560x570")
        self.resizable(False, False)
        self.grab_set()

        # cargo la lista de activos para el desplegable
        self._activos = activo_service.obtener_todos_los_activos()
        self._activos_opciones = [f"{a.id} - {a.codigo} ({a.marca} {a.modelo})" for a in self._activos]

        self._construir_formulario()

        if modo == "editar" and incidencia_id:
            self._cargar_incidencia(incidencia_id)

    def _construir_formulario(self):
        titulo = "Nueva Incidencia" if self._modo == "nuevo" else "Modificar Incidencia"
        ctk.CTkLabel(self, text=titulo, font=ctk.CTkFont(size=16, weight="bold")).grid(
            row=0, column=0, columnspan=2, pady=(15, 10), padx=20, sticky="w")

        ctk.CTkLabel(self, text="Activo:").grid(row=1, column=0, padx=(20, 5), pady=6, sticky="w")
        self._campo_activo = ctk.CTkComboBox(self, values=self._activos_opciones, width=320)
        self._campo_activo.grid(row=1, column=1, padx=(0, 20), pady=6, sticky="w")

        ctk.CTkLabel(self, text="Fecha de apertura:").grid(row=2, column=0, padx=(20, 5), pady=6, sticky="w")
        self._campo_fecha_apertura = ctk.CTkEntry(self, width=200, placeholder_text="2024-01-15")
        self._campo_fecha_apertura.grid(row=2, column=1, padx=(0, 20), pady=6, sticky="w")

        ctk.CTkLabel(self, text="Prioridad:").grid(row=3, column=0, padx=(20, 5), pady=6, sticky="w")
        self._campo_prioridad = ctk.CTkComboBox(self, values=PRIORIDADES, width=200)
        self._campo_prioridad.grid(row=3, column=1, padx=(0, 20), pady=6, sticky="w")

        ctk.CTkLabel(self, text="Categoria:").grid(row=4, column=0, padx=(20, 5), pady=6, sticky="w")
        self._campo_categoria = ctk.CTkComboBox(self, values=CATEGORIAS, width=200)
        self._campo_categoria.grid(row=4, column=1, padx=(0, 20), pady=6, sticky="w")

        ctk.CTkLabel(self, text="Estado:").grid(row=5, column=0, padx=(20, 5), pady=6, sticky="w")
        self._campo_estado = ctk.CTkComboBox(self, values=ESTADOS_INC, width=200)
        self._campo_estado.grid(row=5, column=1, padx=(0, 20), pady=6, sticky="w")

        ctk.CTkLabel(self, text="Tecnico asignado:").grid(row=6, column=0, padx=(20, 5), pady=6, sticky="w")
        self._campo_tecnico = ctk.CTkEntry(self, width=200, placeholder_text="Nombre del tecnico")
        self._campo_tecnico.grid(row=6, column=1, padx=(0, 20), pady=6, sticky="w")

        ctk.CTkLabel(self, text="Fecha de cierre:").grid(row=7, column=0, padx=(20, 5), pady=6, sticky="w")
        self._campo_fecha_cierre = ctk.CTkEntry(self, width=200, placeholder_text="Opcional: 2024-12-01")
        self._campo_fecha_cierre.grid(row=7, column=1, padx=(0, 20), pady=6, sticky="w")

        ctk.CTkLabel(self, text="Descripcion:").grid(row=8, column=0, padx=(20, 5), pady=6, sticky="nw")
        self._campo_descripcion = ctk.CTkTextbox(self, width=320, height=80)
        self._campo_descripcion.grid(row=8, column=1, padx=(0, 20), pady=6, sticky="w")

        self._label_error = ctk.CTkLabel(self, text="", text_color="#ff6b6b", wraplength=480)
        self._label_error.grid(row=9, column=0, columnspan=2, padx=20, pady=5)

        frame_btn = ctk.CTkFrame(self, fg_color="transparent")
        frame_btn.grid(row=10, column=0, columnspan=2, pady=10)

        ctk.CTkButton(frame_btn, text="Guardar", command=self._guardar, width=130).pack(side="left", padx=8)
        ctk.CTkButton(frame_btn, text="Cancelar", command=self.destroy,
                      fg_color="gray40", hover_color="gray30", width=130).pack(side="left", padx=8)

    def _obtener_activo_id_seleccionado(self):
        # aqui extraigo el id del activo del texto del desplegable
        texto = self._campo_activo.get()
        if texto and " - " in texto:
            try:
                return int(texto.split(" - ")[0])
            except ValueError:
                pass
        return None

    def _cargar_incidencia(self, incidencia_id):
        # aqui cargo los datos de la incidencia en el formulario
        incidencia = incidencia_service.obtener_incidencia(incidencia_id)
        if incidencia:
            # busco la opcion del activo correspondiente
            for opcion in self._activos_opciones:
                if opcion.startswith(str(incidencia.activo_id) + " - "):
                    self._campo_activo.set(opcion)

            self._campo_fecha_apertura.insert(0, incidencia.fecha_apertura)
            self._campo_prioridad.set(incidencia.prioridad)
            self._campo_categoria.set(incidencia.categoria)
            self._campo_estado.set(incidencia.estado)
            self._campo_tecnico.insert(0, incidencia.tecnico)
            if incidencia.fecha_cierre:
                self._campo_fecha_cierre.insert(0, incidencia.fecha_cierre)
            self._campo_descripcion.insert("1.0", incidencia.descripcion)

    def _guardar(self):
        # aqui recojo los datos y llamo al servicio para guardar
        activo_id = self._obtener_activo_id_seleccionado()

        datos = {
            "activo_id": activo_id,
            "fecha_apertura": self._campo_fecha_apertura.get(),
            "prioridad": self._campo_prioridad.get(),
            "categoria": self._campo_categoria.get(),
            "descripcion": self._campo_descripcion.get("1.0", "end").strip(),
            "estado": self._campo_estado.get(),
            "tecnico": self._campo_tecnico.get(),
            "fecha_cierre": self._campo_fecha_cierre.get()
        }

        if self._modo == "nuevo":
            resultado = incidencia_service.crear_incidencia(datos)
        else:
            resultado = incidencia_service.modificar_incidencia(self._incidencia_id, datos)

        if resultado["exito"]:
            self._callback()
            self.destroy()
        else:
            self._label_error.configure(text="\n".join(resultado["errores"]))


class CambiarEstadoDialog(ctk.CTkToplevel):
    # aqui esta el dialogo para cambiar solo el estado de una incidencia

    def __init__(self, parent, incidencia_id, callback):
        super().__init__(parent)

        self._incidencia_id = incidencia_id
        self._callback = callback

        self.title("Cambiar Estado de la Incidencia")
        self.geometry("380x260")
        self.resizable(False, False)
        self.grab_set()

        incidencia = incidencia_service.obtener_incidencia(incidencia_id)
        estado_actual = incidencia.estado if incidencia else "Abierta"

        ctk.CTkLabel(self, text="Cambiar Estado", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(15, 5), padx=20)
        ctk.CTkLabel(self, text=f"Estado actual: {estado_actual}").pack(pady=5)

        ctk.CTkLabel(self, text="Nuevo estado:").pack(pady=(10, 2))
        self._nuevo_estado = ctk.CTkComboBox(self, values=ESTADOS_INC, width=200)
        self._nuevo_estado.set(estado_actual)
        self._nuevo_estado.pack(pady=5)

        ctk.CTkLabel(self, text="Fecha de cierre (si aplica):").pack(pady=(10, 2))
        self._fecha_cierre = ctk.CTkEntry(self, width=200, placeholder_text="2024-12-01")
        self._fecha_cierre.pack(pady=5)

        frame_btn = ctk.CTkFrame(self, fg_color="transparent")
        frame_btn.pack(pady=15)

        ctk.CTkButton(frame_btn, text="Guardar", command=self._guardar, width=110).pack(side="left", padx=8)
        ctk.CTkButton(frame_btn, text="Cancelar", command=self.destroy,
                      fg_color="gray40", hover_color="gray30", width=110).pack(side="left", padx=8)

    def _guardar(self):
        nuevo = self._nuevo_estado.get()
        fecha = self._fecha_cierre.get().strip() or None
        resultado = incidencia_service.cambiar_estado(self._incidencia_id, nuevo, fecha)
        if resultado["exito"]:
            self._callback()
            self.destroy()
        else:
            mostrar_mensaje_error("Error", "\n".join(resultado["errores"]))
