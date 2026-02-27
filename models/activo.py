from dataclasses import dataclass
from typing import Optional

# aqui defino la estructura de un activo informatico
@dataclass
class Activo:
    codigo: str
    tipo: str
    marca: str
    modelo: str
    numero_serie: str
    ubicacion: str
    fecha_alta: str
    estado: str
    id: Optional[int] = None

    def a_diccionario(self):
        # convierto el activo a un diccionario para facilitar el manejo
        return {
            "id": self.id,
            "codigo": self.codigo,
            "tipo": self.tipo,
            "marca": self.marca,
            "modelo": self.modelo,
            "numero_serie": self.numero_serie,
            "ubicacion": self.ubicacion,
            "fecha_alta": self.fecha_alta,
            "estado": self.estado
        }

    @staticmethod
    def desde_fila(fila):
        # creo un activo a partir de una fila de la base de datos
        return Activo(
            id=fila[0],
            codigo=fila[1],
            tipo=fila[2],
            marca=fila[3],
            modelo=fila[4],
            numero_serie=fila[5],
            ubicacion=fila[6],
            fecha_alta=fila[7],
            estado=fila[8]
        )
