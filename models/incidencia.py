from dataclasses import dataclass
from typing import Optional


# aqui defino la estructura de una incidencia
@dataclass
class Incidencia:
    activo_id: int
    fecha_apertura: str
    prioridad: str
    categoria: str
    descripcion: str
    estado: str
    tecnico: str
    fecha_cierre: Optional[str] = None
    id: Optional[int] = None

    def a_diccionario(self):
        # convierto la incidencia a diccionario para facilitar el manejo
        return {
            "id": self.id,
            "activo_id": self.activo_id,
            "fecha_apertura": self.fecha_apertura,
            "prioridad": self.prioridad,
            "categoria": self.categoria,
            "descripcion": self.descripcion,
            "estado": self.estado,
            "tecnico": self.tecnico,
            "fecha_cierre": self.fecha_cierre
        }

    @staticmethod
    def desde_fila(fila):
        # creo una incidencia a partir de una fila de la base de datos
        return Incidencia(
            id=fila[0],
            activo_id=fila[1],
            fecha_apertura=fila[2],
            prioridad=fila[3],
            categoria=fila[4],
            descripcion=fila[5],
            estado=fila[6],
            tecnico=fila[7],
            fecha_cierre=fila[8] if len(fila) > 8 else None
        )
