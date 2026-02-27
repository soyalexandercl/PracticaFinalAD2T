import customtkinter as ctk
from services import activo_service, incidencia_service


# aqui esta la pantalla de estadisticas e informes


class EstadisticasFrame(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self._construir_interfaz()
        self._cargar_estadisticas()

    def _construir_interfaz(self):
        # aqui construyo la pantalla de estadisticas
        cabecera = ctk.CTkFrame(self, fg_color="transparent")
        cabecera.pack(fill="x", padx=15, pady=(10, 5))

        ctk.CTkLabel(cabecera, text="Estadisticas e Informes",
                     font=ctk.CTkFont(size=20, weight="bold")).pack(side="left")
        ctk.CTkButton(cabecera, text="Actualizar datos", command=self._cargar_estadisticas,
                      width=140).pack(side="right")

        # contenedor scrollable para las estadisticas
        self._scroll = ctk.CTkScrollableFrame(self)
        self._scroll.pack(fill="both", expand=True, padx=15, pady=5)

    def _limpiar(self):
        # aqui borro los widgets del scroll antes de recargar
        for widget in self._scroll.winfo_children():
            widget.destroy()

    def _cargar_estadisticas(self):
        # aqui cargo y muestro todas las estadisticas
        self._limpiar()

        stats_activos = activo_service.obtener_estadisticas_activos()
        stats_incidencias = incidencia_service.obtener_estadisticas_incidencias()

        # seccion de activos
        self._seccion("Activos")

        self._tarjeta_numero("Total de activos registrados", stats_activos.get("total", 0))

        if stats_activos.get("por_estado"):
            self._tabla_estadistica("Activos por estado", ["Estado", "Cantidad"], stats_activos["por_estado"])

        if stats_activos.get("por_tipo"):
            self._tabla_estadistica("Activos por tipo", ["Tipo", "Cantidad"], stats_activos["por_tipo"])

        # separador
        ctk.CTkFrame(self._scroll, height=2, fg_color="gray40").pack(fill="x", pady=15)

        # seccion de incidencias
        self._seccion("Incidencias")

        self._tarjeta_numero("Total de incidencias registradas", stats_incidencias.get("total", 0))

        if stats_incidencias.get("por_estado"):
            self._tabla_estadistica("Incidencias por estado", ["Estado", "Cantidad"], stats_incidencias["por_estado"])

        if stats_incidencias.get("por_prioridad"):
            self._tabla_estadistica("Incidencias por prioridad", ["Prioridad", "Cantidad"], stats_incidencias["por_prioridad"])

        if stats_incidencias.get("por_categoria"):
            self._tabla_estadistica("Incidencias por categoria", ["Categoria", "Cantidad"], stats_incidencias["por_categoria"])

        if stats_incidencias.get("top_activos"):
            columnas_top = ["Codigo", "Marca", "Modelo", "Num. Incidencias"]
            self._tabla_estadistica("Activos con mas incidencias", columnas_top, stats_incidencias["top_activos"])

    def _seccion(self, titulo):
        # aqui creo un titulo de seccion
        ctk.CTkLabel(self._scroll, text=titulo,
                     font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=(5, 3))

    def _tarjeta_numero(self, etiqueta, valor):
        # aqui creo una tarjeta con un numero destacado
        frame = ctk.CTkFrame(self._scroll)
        frame.pack(fill="x", pady=4)

        ctk.CTkLabel(frame, text=etiqueta, anchor="w").pack(side="left", padx=15, pady=10)
        ctk.CTkLabel(frame, text=str(valor),
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color="#1f9ed9").pack(side="right", padx=15, pady=10)

    def _tabla_estadistica(self, titulo, columnas, datos):
        # aqui creo una tabla pequena para mostrar estadisticas
        frame = ctk.CTkFrame(self._scroll)
        frame.pack(fill="x", pady=4, padx=5)

        ctk.CTkLabel(frame, text=titulo,
                     font=ctk.CTkFont(weight="bold"), anchor="w").pack(anchor="w", padx=10, pady=(8, 3))

        # cabecera de la tabla
        frame_cab = ctk.CTkFrame(frame, fg_color="gray25")
        frame_cab.pack(fill="x", padx=10, pady=(0, 2))

        for col in columnas:
            ctk.CTkLabel(frame_cab, text=col, font=ctk.CTkFont(weight="bold"),
                         width=150, anchor="w").pack(side="left", padx=5, pady=4)

        # filas de datos
        for i, fila in enumerate(datos):
            color = "gray17" if i % 2 == 0 else "gray20"
            frame_fila = ctk.CTkFrame(frame, fg_color=color)
            frame_fila.pack(fill="x", padx=10)
            for valor in fila:
                ctk.CTkLabel(frame_fila, text=str(valor) if valor is not None else "-",
                             width=150, anchor="w").pack(side="left", padx=5, pady=3)

        ctk.CTkFrame(frame, height=5, fg_color="transparent").pack()
