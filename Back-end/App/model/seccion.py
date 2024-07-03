import uuid
from App.exceptions.wrongLayout import wrongLayoutException

class Seccion:
    def __init__(self, nombre, icono, layout):
        self.nombre = nombre
        self.icono = icono
        if layout != "g" and layout != "c" and layout != "s":
            raise wrongLayoutException()
        self.layout = layout