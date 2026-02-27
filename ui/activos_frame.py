import customtkinter as ctk
from tkinter import filedialog
from services import activo_service, export_service
from ui.componentes import crear_tabla, mostrar_mensaje_error, mostrar_mensaje_ok, pedir_confirmacion

# aqui esta la pantalla de gestion de activos

TIPOS = ["Ordenador", "Portatil", "Monitor", "Impresora", "Servidor", "Router", "Switch", "Tablet", "Otro"]
ESTADOS = ["Activo", "En reparacion", "Baja", "Almacenado"]


class ActivosFrame(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self._pagina_actual = 1
        self._total_paginas = 1
        self._filtros = {}
        self._id_seleccionado = None

        self._construir_interfaz()
        self._cargar_datos()

    def _construir_interfaz(self):
        # aqui construyo toda la pantalla de activos

        # titulo de la seccion
        ctk.CTkLabel(self, text="Gestion de Activos Informaticos",
                     font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(10, 5), anchor="w", padx=15)

        # panel de filtros de busqueda
        frame_filtros = ctk.CTkFrame(self)
        frame_filtros.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(frame_filtros, text="Buscar y filtrar:", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, columnspan=8, padx=10, pady=(8, 2), sticky="w")

        ctk.CTkLabel(frame_filtros, text="Codigo:").grid(row=1, column=0, padx=(10, 3), pady=5, sticky="w")
        self._filtro_codigo = ctk.CTkEntry(frame_filtros, width=100, placeholder_text="ACT-0001")
        self._filtro_codigo.grid(row=1, column=1, padx=(0, 8), pady=5)

        ctk.CTkLabel(frame_filtros, text="Tipo:").grid(row=1, column=2, padx=(0, 3), pady=5, sticky="w")
        self._filtro_tipo = ctk.CTkComboBox(frame_filtros, values=[""] + TIPOS, width=130)
        self._filtro_tipo.set("")
        self._filtro_tipo.grid(row=1, column=3, padx=(0, 8), pady=5)

        ctk.CTkLabel(frame_filtros, text="Marca:").grid(row=1, column=4, padx=(0, 3), pady=5, sticky="w")
        self._filtro_marca = ctk.CTkEntry(frame_filtros, width=100, placeholder_text="Dell, HP...")
        self._filtro_marca.grid(row=1, column=5, padx=(0, 8), pady=5)

        ctk.CTkLabel(frame_filtros, text="Estado:").grid(row=1, column=6, padx=(0, 3), pady=5, sticky="w")
        self._filtro_estado = ctk.CTkComboBox(frame_filtros, values=[""] + ESTADOS, width=130)
        self._filtro_estado.set("")
        self._filtro_estado.grid(row=1, column=7, padx=(0, 8), pady=5)

        ctk.CTkLabel(frame_filtros, text="Ubicacion:").grid(row=2, column=0, padx=(10, 3), pady=5, sticky="w")
        self._filtro_ubicacion = ctk.CTkEntry(frame_filtros, width=150, placeholder_text="Aula, Sala...")
        self._filtro_ubicacion.grid(row=2, column=1, columnspan=2, padx=(0, 8), pady=5, sticky="w")

        ctk.CTkButton(frame_filtros, text="Buscar", command=self._buscar, width=90).grid(
            row=2, column=3, padx=5, pady=5)
        ctk.CTkButton(frame_filtros, text="Limpiar filtros", command=self._limpiar_filtros,
                      fg_color="gray40", hover_color="gray30", width=110).grid(row=2, column=4, padx=5, pady=5)

        # tabla de activos
        columnas = ["ID", "Codigo", "Tipo", "Marca", "Modelo", "N. Serie", "Ubicacion", "Fecha Alta", "Estado"]
        anchos = [40, 90, 100, 100, 110, 120, 120, 90, 100]
        frame_tabla, self._tabla = crear_tabla(self, columnas, anchos)
        frame_tabla.pack(fill="both", expand=True, padx=15, pady=5)

        # aqui escucho cuando el usuario selecciona una fila
        self._tabla.bind("<<TreeviewSelect>>", self._al_seleccionar)

        # panel de paginacion
        frame_paginas = ctk.CTkFrame(self, fg_color="transparent")
        frame_paginas.pack(fill="x", padx=15, pady=2)

        ctk.CTkButton(frame_paginas, text="< Anterior", command=self._pagina_anterior, width=90).pack(side="left", padx=3)
        self._label_pagina = ctk.CTkLabel(frame_paginas, text="Pagina 1 de 1")
        self._label_pagina.pack(side="left", padx=10)
        ctk.CTkButton(frame_paginas, text="Siguiente >", command=self._pagina_siguiente, width=90).pack(side="left", padx=3)
        self._label_total = ctk.CTkLabel(frame_paginas, text="")
        self._label_total.pack(side="left", padx=15)

        # panel de botones de accion
        frame_acciones = ctk.CTkFrame(self, fg_color="transparent")
        frame_acciones.pack(fill="x", padx=15, pady=(2, 10))

        ctk.CTkButton(frame_acciones, text="Nuevo Activo", command=self._abrir_formulario_nuevo,
                      width=130).pack(side="left", padx=3)
        ctk.CTkButton(frame_acciones, text="Modificar", command=self._abrir_formulario_editar,
                      fg_color="#5a9e5a", hover_color="#4a8e4a", width=100).pack(side="left", padx=3)
        ctk.CTkButton(frame_acciones, text="Eliminar", command=self._confirmar_eliminar,
                      fg_color="#d9534f", hover_color="#c9302c", width=100).pack(side="left", padx=3)

        # separador
        ctk.CTkLabel(frame_acciones, text="|", text_color="gray").pack(side="left", padx=5)

        ctk.CTkButton(frame_acciones, text="Exportar CSV", command=self._exportar_csv,
                      fg_color="gray40", hover_color="gray30", width=110).pack(side="left", padx=3)
        ctk.CTkButton(frame_acciones, text="Importar CSV", command=self._importar_csv,
                      fg_color="gray40", hover_color="gray30", width=110).pack(side="left", padx=3)

    def _cargar_datos(self):
        # aqui cargo los datos en la tabla segun los filtros y la pagina actual
        resultado = activo_service.listar_activos_paginado(self._filtros, self._pagina_actual)

        self._total_paginas = resultado["total_paginas"]
        self._label_pagina.configure(text=f"Pagina {self._pagina_actual} de {self._total_paginas}")
        self._label_total.configure(text=f"Total: {resultado['total_registros']} activos")

        # limpio la tabla antes de cargar nuevos datos
        for fila in self._tabla.get_children():
            self._tabla.delete(fila)

        for activo in resultado["activos"]:
            self._tabla.insert("", "end", values=(
                activo.id, activo.codigo, activo.tipo, activo.marca, activo.modelo,
                activo.numero_serie, activo.ubicacion, activo.fecha_alta, activo.estado
            ))

    def _al_seleccionar(self, evento):
        # aqui guardo el id del activo seleccionado
        seleccion = self._tabla.selection()
        if seleccion:
            valores = self._tabla.item(seleccion[0])["values"]
            self._id_seleccionado = valores[0] if valores else None
        else:
            self._id_seleccionado = None

    def _buscar(self):
        # aqui recojo los filtros y recargo la tabla desde la primera pagina
        self._filtros = {
            "codigo": self._filtro_codigo.get().strip(),
            "tipo": self._filtro_tipo.get().strip(),
            "marca": self._filtro_marca.get().strip(),
            "estado": self._filtro_estado.get().strip(),
            "ubicacion": self._filtro_ubicacion.get().strip()
        }
        self._pagina_actual = 1
        self._cargar_datos()

    def _limpiar_filtros(self):
        # aqui limpio todos los campos de busqueda
        self._filtro_codigo.delete(0, "end")
        self._filtro_tipo.set("")
        self._filtro_marca.delete(0, "end")
        self._filtro_estado.set("")
        self._filtro_ubicacion.delete(0, "end")
        self._filtros = {}
        self._pagina_actual = 1
        self._cargar_datos()

    def _pagina_anterior(self):
        # aqui voy a la pagina anterior si existe
        if self._pagina_actual > 1:
            self._pagina_actual -= 1
            self._cargar_datos()

    def _pagina_siguiente(self):
        # aqui voy a la pagina siguiente si existe
        if self._pagina_actual < self._total_paginas:
            self._pagina_actual += 1
            self._cargar_datos()

    def _abrir_formulario_nuevo(self):
        # aqui abro el formulario para crear un activo nuevo
        FormularioActivo(self, modo="nuevo", callback=self._cargar_datos)

    def _abrir_formulario_editar(self):
        # aqui abro el formulario para editar el activo seleccionado
        if not self._id_seleccionado:
            mostrar_mensaje_error("Nada seleccionado", "Selecciona un activo de la lista para modificarlo")
            return
        FormularioActivo(self, modo="editar", activo_id=self._id_seleccionado, callback=self._cargar_datos)

    def _confirmar_eliminar(self):
        # aqui pido confirmacion antes de eliminar el activo
        if not self._id_seleccionado:
            mostrar_mensaje_error("Nada seleccionado", "Selecciona un activo de la lista para eliminarlo")
            return
        pedir_confirmacion(
            "Confirmar eliminacion",
            "Estas seguro de que quieres eliminar este activo?\nEsta accion no se puede deshacer.",
            self._eliminar_activo
        )

    def _eliminar_activo(self):
        # aqui ejecuto la eliminacion del activo
        resultado = activo_service.eliminar_activo(self._id_seleccionado)
        if resultado["exito"]:
            mostrar_mensaje_ok("Eliminado", "El activo se ha eliminado correctamente")
            self._id_seleccionado = None
            self._cargar_datos()
        else:
            mostrar_mensaje_error("No se pudo eliminar", "\n".join(resultado["errores"]))

    def _exportar_csv(self):
        # aqui exporto los activos a un archivo CSV
        resultado = export_service.exportar_activos_csv(self._filtros if self._filtros else None)
        if resultado["exito"]:
            mostrar_mensaje_ok("Exportacion completada",
                               f"Se han exportado {resultado['total']} activos.\nArchivo guardado en la carpeta exports/")
        else:
            mostrar_mensaje_error("Error al exportar", "\n".join(resultado["errores"]))

    def _importar_csv(self):
        # aqui dejo al usuario elegir un archivo CSV para importar activos
        ruta = filedialog.askopenfilename(
            title="Selecciona el archivo CSV",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
        )
        if not ruta:
            return

        resultado = export_service.importar_activos_csv(ruta)
        if resultado["exito"]:
            msg = f"Se han importado {resultado['insertados']} activos correctamente."
            if resultado["errores_filas"]:
                msg += f"\n\nFilas con problemas ({len(resultado['errores_filas'])}):\n" + "\n".join(resultado["errores_filas"][:5])
                if len(resultado["errores_filas"]) > 5:
                    msg += f"\n...y {len(resultado['errores_filas']) - 5} mas"
            mostrar_mensaje_ok("Importacion completada", msg)
            self._cargar_datos()
        else:
            mostrar_mensaje_error("Error al importar", "\n".join(resultado["errores"]))


class FormularioActivo(ctk.CTkToplevel):
    # aqui esta el formulario para crear o editar un activo

    def __init__(self, parent, modo, callback, activo_id=None):
        super().__init__(parent)

        self._modo = modo
        self._activo_id = activo_id
        self._callback = callback

        titulo = "Nuevo Activo" if modo == "nuevo" else "Modificar Activo"
        self.title(titulo)
        self.geometry("520x500")
        self.resizable(False, False)
        self.grab_set()

        self._construir_formulario()

        if modo == "editar" and activo_id:
            self._cargar_activo(activo_id)

    def _construir_formulario(self):
        # aqui construyo el formulario con todos los campos del activo
        titulo = "Nuevo Activo" if self._modo == "nuevo" else "Modificar Activo"
        ctk.CTkLabel(self, text=titulo, font=ctk.CTkFont(size=16, weight="bold")).grid(
            row=0, column=0, columnspan=2, pady=(15, 10), padx=20, sticky="w")

        # campos del formulario
        ctk.CTkLabel(self, text="Codigo (ACT-XXXX):").grid(row=1, column=0, padx=(20, 5), pady=6, sticky="w")
        self._campo_codigo = ctk.CTkEntry(self, width=200, placeholder_text="ACT-0001")
        self._campo_codigo.grid(row=1, column=1, padx=(0, 20), pady=6, sticky="w")

        ctk.CTkLabel(self, text="Tipo:").grid(row=2, column=0, padx=(20, 5), pady=6, sticky="w")
        self._campo_tipo = ctk.CTkComboBox(self, values=TIPOS, width=200)
        self._campo_tipo.grid(row=2, column=1, padx=(0, 20), pady=6, sticky="w")

        ctk.CTkLabel(self, text="Marca:").grid(row=3, column=0, padx=(20, 5), pady=6, sticky="w")
        self._campo_marca = ctk.CTkEntry(self, width=200, placeholder_text="Dell, HP, Lenovo...")
        self._campo_marca.grid(row=3, column=1, padx=(0, 20), pady=6, sticky="w")

        ctk.CTkLabel(self, text="Modelo:").grid(row=4, column=0, padx=(20, 5), pady=6, sticky="w")
        self._campo_modelo = ctk.CTkEntry(self, width=200, placeholder_text="Inspiron 15, ThinkPad...")
        self._campo_modelo.grid(row=4, column=1, padx=(0, 20), pady=6, sticky="w")

        ctk.CTkLabel(self, text="Numero de serie:").grid(row=5, column=0, padx=(20, 5), pady=6, sticky="w")
        self._campo_serie = ctk.CTkEntry(self, width=200, placeholder_text="SN123456")
        self._campo_serie.grid(row=5, column=1, padx=(0, 20), pady=6, sticky="w")

        ctk.CTkLabel(self, text="Ubicacion:").grid(row=6, column=0, padx=(20, 5), pady=6, sticky="w")
        self._campo_ubicacion = ctk.CTkEntry(self, width=200, placeholder_text="Aula 101, Sala servidores...")
        self._campo_ubicacion.grid(row=6, column=1, padx=(0, 20), pady=6, sticky="w")

        ctk.CTkLabel(self, text="Fecha de alta (AAAA-MM-DD):").grid(row=7, column=0, padx=(20, 5), pady=6, sticky="w")
        self._campo_fecha = ctk.CTkEntry(self, width=200, placeholder_text="2026-02-28")
        self._campo_fecha.grid(row=7, column=1, padx=(0, 20), pady=6, sticky="w")

        ctk.CTkLabel(self, text="Estado:").grid(row=8, column=0, padx=(20, 5), pady=6, sticky="w")
        self._campo_estado = ctk.CTkComboBox(self, values=ESTADOS, width=200)
        self._campo_estado.grid(row=8, column=1, padx=(0, 20), pady=6, sticky="w")

        # mensaje de error en el formulario
        self._label_error = ctk.CTkLabel(self, text="", text_color="#ff6b6b", wraplength=450)
        self._label_error.grid(row=9, column=0, columnspan=2, padx=20, pady=5)

        # botones
        frame_btn = ctk.CTkFrame(self, fg_color="transparent")
        frame_btn.grid(row=10, column=0, columnspan=2, pady=10)

        ctk.CTkButton(frame_btn, text="Guardar", command=self._guardar, width=130).pack(side="left", padx=8)
        ctk.CTkButton(frame_btn, text="Cancelar", command=self.destroy,
                      fg_color="gray40", hover_color="gray30", width=130).pack(side="left", padx=8)

    def _cargar_activo(self, activo_id):
        # aqui cargo los datos del activo en el formulario para editar
        activo = activo_service.obtener_activo(activo_id)
        if activo:
            self._campo_codigo.insert(0, activo.codigo)
            self._campo_tipo.set(activo.tipo)
            self._campo_marca.insert(0, activo.marca)
            self._campo_modelo.insert(0, activo.modelo)
            self._campo_serie.insert(0, activo.numero_serie)
            self._campo_ubicacion.insert(0, activo.ubicacion)
            self._campo_fecha.insert(0, activo.fecha_alta)
            self._campo_estado.set(activo.estado)

    def _guardar(self):
        # aqui recojo los datos del formulario y llamo al servicio para guardar
        datos = {
            "codigo": self._campo_codigo.get(),
            "tipo": self._campo_tipo.get(),
            "marca": self._campo_marca.get(),
            "modelo": self._campo_modelo.get(),
            "numero_serie": self._campo_serie.get(),
            "ubicacion": self._campo_ubicacion.get(),
            "fecha_alta": self._campo_fecha.get(),
            "estado": self._campo_estado.get()
        }

        if self._modo == "nuevo":
            resultado = activo_service.crear_activo(datos)
        else:
            resultado = activo_service.modificar_activo(self._activo_id, datos)

        if resultado["exito"]:
            self._callback()
            self.destroy()
        else:
            self._label_error.configure(text="\n".join(resultado["errores"]))
