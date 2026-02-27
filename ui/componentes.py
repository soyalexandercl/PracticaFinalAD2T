import customtkinter as ctk
from tkinter import ttk

# aqui tengo componentes reutilizables para no repetir codigo en la interfaz

def crear_tabla(parent, columnas, anchos):
    # aqui creo una tabla visual con tkinter Treeview dentro de un frame customtkinter
    frame = ctk.CTkFrame(parent)

    # configuro el estilo de la tabla para que se vea bien
    estilo = ttk.Style()
    estilo.theme_use("default")
    estilo.configure("Treeview",
                     background="#2b2b2b",
                     foreground="white",
                     rowheight=28,
                     fieldbackground="#2b2b2b",
                     borderwidth=0,
                     font=("Segoe UI", 11))
    estilo.configure("Treeview.Heading",
                     background="#1f538d",
                     foreground="white",
                     font=("Segoe UI", 11, "bold"),
                     relief="flat")
    estilo.map("Treeview",
               background=[("selected", "#1f538d")],
               foreground=[("selected", "white")])

    tabla = ttk.Treeview(frame, columns=columnas, show="headings", selectmode="browse")

    # configuro cada columna con su ancho y titulo
    for col, ancho in zip(columnas, anchos):
        tabla.heading(col, text=col)
        tabla.column(col, width=ancho, minwidth=50)

    # barra de desplazamiento vertical
    scrollbar_v = ttk.Scrollbar(frame, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=scrollbar_v.set)

    # barra de desplazamiento horizontal
    scrollbar_h = ttk.Scrollbar(frame, orient="horizontal", command=tabla.xview)
    tabla.configure(xscrollcommand=scrollbar_h.set)

    tabla.grid(row=0, column=0, sticky="nsew")
    scrollbar_v.grid(row=0, column=1, sticky="ns")
    scrollbar_h.grid(row=1, column=0, sticky="ew")

    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    return frame, tabla


def crear_campo_formulario(parent, etiqueta, fila, columna=0, ancho=200, opciones=None):
    # aqui creo un campo de formulario con su etiqueta
    ctk.CTkLabel(parent, text=etiqueta, anchor="w").grid(
        row=fila, column=columna, padx=(10, 5), pady=5, sticky="w"
    )

    if opciones:
        widget = ctk.CTkComboBox(parent, values=opciones, width=ancho)
    else:
        widget = ctk.CTkEntry(parent, width=ancho, placeholder_text=etiqueta)

    widget.grid(row=fila, column=columna + 1, padx=(0, 10), pady=5, sticky="w")
    return widget


def mostrar_mensaje_error(titulo, mensaje):
    # aqui muestro un mensaje de error al usuario
    ventana = ctk.CTkToplevel()
    ventana.title(titulo)
    ventana.geometry("400x180")
    ventana.resizable(False, False)
    ventana.grab_set()

    ctk.CTkLabel(ventana, text=titulo, font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(20, 5))
    ctk.CTkLabel(ventana, text=mensaje, wraplength=360, justify="center").pack(pady=5, padx=20)
    ctk.CTkButton(ventana, text="Aceptar", command=ventana.destroy, width=100).pack(pady=15)


def mostrar_mensaje_ok(titulo, mensaje):
    # aqui muestro un mensaje de confirmacion al usuario
    ventana = ctk.CTkToplevel()
    ventana.title(titulo)
    ventana.geometry("400x180")
    ventana.resizable(False, False)
    ventana.grab_set()

    ctk.CTkLabel(ventana, text=titulo, font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(20, 5))
    ctk.CTkLabel(ventana, text=mensaje, wraplength=360, justify="center").pack(pady=5, padx=20)
    ctk.CTkButton(ventana, text="Aceptar", command=ventana.destroy, width=100).pack(pady=15)


def pedir_confirmacion(titulo, mensaje, callback_si):
    # aqui pido confirmacion antes de hacer algo importante
    ventana = ctk.CTkToplevel()
    ventana.title(titulo)
    ventana.geometry("420x180")
    ventana.resizable(False, False)
    ventana.grab_set()

    ctk.CTkLabel(ventana, text=titulo, font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(20, 5))
    ctk.CTkLabel(ventana, text=mensaje, wraplength=380, justify="center").pack(pady=5, padx=20)

    frame_botones = ctk.CTkFrame(ventana, fg_color="transparent")
    frame_botones.pack(pady=15)

    def confirmar():
        ventana.destroy()
        callback_si()

    ctk.CTkButton(frame_botones, text="Si, continuar", command=confirmar,
                  fg_color="#d9534f", hover_color="#c9302c", width=130).pack(side="left", padx=10)
    ctk.CTkButton(frame_botones, text="Cancelar", command=ventana.destroy,
                  fg_color="gray40", hover_color="gray30", width=130).pack(side="left", padx=10)
