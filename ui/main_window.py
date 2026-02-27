import customtkinter as ctk
from utils import config
from ui.activos_frame import ActivosFrame
from ui.incidencias_frame import IncidenciasFrame
from ui.estadisticas_frame import EstadisticasFrame
from ui.auditoria_frame import AuditoriaFrame


# aqui construyo la ventana principal de la aplicacion


class VentanaPrincipal(ctk.CTk):

    def __init__(self):
        super().__init__()

        # leo el tema de la configuracion y lo aplico
        tema = config.obtener("tema", "dark")
        ctk.set_appearance_mode(tema)
        ctk.set_default_color_theme(config.obtener("color_principal", "blue"))

        self.title("Gestion de Activos Informaticos e Incidencias")
        self.geometry("1100x720")
        self.minsize(900, 600)

        self._frame_actual = None
        self._construir_layout()
        self._mostrar_seccion("activos")

    def _construir_layout(self):
        # aqui construyo el layout con menu lateral y area de contenido

        # menu lateral
        self._sidebar = ctk.CTkFrame(self, width=190, corner_radius=0)
        self._sidebar.pack(side="left", fill="y")
        self._sidebar.pack_propagate(False)

        # titulo del menu
        ctk.CTkLabel(self._sidebar, text="Menu Principal",
                     font=ctk.CTkFont(size=15, weight="bold")).pack(pady=(20, 5), padx=15)

        ctk.CTkFrame(self._sidebar, height=1, fg_color="gray40").pack(fill="x", padx=10, pady=5)

        # botones del menu
        self._btn_activos = ctk.CTkButton(
            self._sidebar, text="Activos",
            command=lambda: self._mostrar_seccion("activos"),
            anchor="w", width=170, height=38,
            fg_color="transparent", hover_color=("gray75", "gray25")
        )
        self._btn_activos.pack(pady=3, padx=10)

        self._btn_incidencias = ctk.CTkButton(
            self._sidebar, text="Incidencias",
            command=lambda: self._mostrar_seccion("incidencias"),
            anchor="w", width=170, height=38,
            fg_color="transparent", hover_color=("gray75", "gray25")
        )
        self._btn_incidencias.pack(pady=3, padx=10)

        self._btn_estadisticas = ctk.CTkButton(
            self._sidebar, text="Estadisticas",
            command=lambda: self._mostrar_seccion("estadisticas"),
            anchor="w", width=170, height=38,
            fg_color="transparent", hover_color=("gray75", "gray25")
        )
        self._btn_estadisticas.pack(pady=3, padx=10)

        self._btn_auditoria = ctk.CTkButton(
            self._sidebar, text="Historial de Cambios",
            command=lambda: self._mostrar_seccion("auditoria"),
            anchor="w", width=170, height=38,
            fg_color="transparent", hover_color=("gray75", "gray25")
        )
        self._btn_auditoria.pack(pady=3, padx=10)

        # cambiador de tema en la parte baja del menu
        ctk.CTkFrame(self._sidebar, height=1, fg_color="gray40").pack(fill="x", padx=10, side="bottom", pady=5)

        frame_tema = ctk.CTkFrame(self._sidebar, fg_color="transparent")
        frame_tema.pack(side="bottom", pady=10, padx=10)

        ctk.CTkLabel(frame_tema, text="Modo:", font=ctk.CTkFont(size=11)).pack()
        self._switch_tema = ctk.CTkSwitch(frame_tema, text="Oscuro",
                                          command=self._cambiar_tema, width=60)
        if ctk.get_appearance_mode() == "Dark":
            self._switch_tema.select()
        self._switch_tema.pack(pady=3)

        ctk.CTkLabel(self._sidebar, text="v1.0",
                     font=ctk.CTkFont(size=10), text_color="gray").pack(side="bottom", pady=2)

        # area de contenido principal
        self._contenido = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self._contenido.pack(side="left", fill="both", expand=True)

        # guardo los botones del menu para poder marcar el activo
        self._botones_menu = {
            "activos": self._btn_activos,
            "incidencias": self._btn_incidencias,
            "estadisticas": self._btn_estadisticas,
            "auditoria": self._btn_auditoria
        }

    def _mostrar_seccion(self, nombre):
        # aqui muestro la seccion seleccionada y destruyo la anterior
        if self._frame_actual:
            self._frame_actual.destroy()

        # marco el boton activo visualmente
        for key, btn in self._botones_menu.items():
            if key == nombre:
                btn.configure(fg_color=("gray80", "gray30"))
            else:
                btn.configure(fg_color="transparent")

        # cargo el frame de la seccion correspondiente
        if nombre == "activos":
            self._frame_actual = ActivosFrame(self._contenido)
        elif nombre == "incidencias":
            self._frame_actual = IncidenciasFrame(self._contenido)
        elif nombre == "estadisticas":
            self._frame_actual = EstadisticasFrame(self._contenido)
        elif nombre == "auditoria":
            self._frame_actual = AuditoriaFrame(self._contenido)

        self._frame_actual.pack(fill="both", expand=True)

    def _cambiar_tema(self):
        # aqui cambio entre modo claro y oscuro
        if self._switch_tema.get():
            ctk.set_appearance_mode("dark")
            self._switch_tema.configure(text="Oscuro")
        else:
            ctk.set_appearance_mode("light")
            self._switch_tema.configure(text="Claro")
