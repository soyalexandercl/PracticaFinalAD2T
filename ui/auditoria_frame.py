import customtkinter as ctk
from repositories import auditoria_repository
from ui.componentes import crear_tabla

# aqui esta la pantalla del historial de auditoria

class AuditoriaFrame(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self._construir_interfaz()
        self._cargar_datos()

    def _construir_interfaz(self):
        # aqui construyo la pantalla de auditoria
        cabecera = ctk.CTkFrame(self, fg_color="transparent")
        cabecera.pack(fill="x", padx=15, pady=(10, 5))

        ctk.CTkLabel(cabecera, text="Historial de Cambios",
                     font=ctk.CTkFont(size=20, weight="bold")).pack(side="left")
        ctk.CTkButton(cabecera, text="Actualizar", command=self._cargar_datos, width=100).pack(side="right")

        ctk.CTkLabel(self,
                     text="Aqui puedes ver todos los cambios realizados en la aplicacion (inserciones, modificaciones y eliminaciones).",
                     wraplength=700, justify="left").pack(anchor="w", padx=15, pady=(0, 5))

        columnas = ["Fecha y Hora", "Operacion", "Tabla", "Identificador", "Descripcion"]
        anchos = [150, 90, 100, 120, 350]
        frame_tabla, self._tabla = crear_tabla(self, columnas, anchos)
        frame_tabla.pack(fill="both", expand=True, padx=15, pady=5)

    def _cargar_datos(self):
        # aqui cargo los registros de auditoria en la tabla
        for fila in self._tabla.get_children():
            self._tabla.delete(fila)

        registros = auditoria_repository.listar_recientes(100)
        for reg in registros:
            self._tabla.insert("", "end", values=(
                reg.fecha_hora, reg.operacion, reg.tabla, reg.registro_id, reg.descripcion
            ))
