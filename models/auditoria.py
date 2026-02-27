from dataclasses import dataclass
from typing import Optional

# aqui defino la estructura del registro de auditoria
@dataclass
class Auditoria:
    fecha_hora: str
    operacion: str
    tabla: str
    registro_id: str
    descripcion: str
    id: Optional[int] = None

    @staticmethod
    def desde_fila(fila):
        return Auditoria(
            id=fila[0],
            fecha_hora=fila[1],
            operacion=fila[2],
            tabla=fila[3],
            registro_id=fila[4],
            descripcion=fila[5]
        )
