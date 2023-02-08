from dataclasses import dataclass
from psycopg2._psycopg import connection

@dataclass
class Cliente:
    nombre_completo: str
    dni: str
    fecha_nacimiento: str
    telefono: str
    deportes: list

    def __datos__(self):
        # La 'f' es una fuzzy string, es decir, una cadena de texto que permite meter variables dentro de ella.
        # Interpola los valores dentro de las llaves.
        return f'Nombre: {self.nombre_completo}, DNI: {self.dni}, Fecha de nacimiento: {self.fecha_nacimiento}, Teléfono: {self.telefono}'

    def __deportes__(self):
        return f'Deportes: {self.deportes}'
