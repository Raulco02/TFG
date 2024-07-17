import uuid
from App.exceptions.wrongLayout import wrongLayoutException

class Seccion:
    """
    Descripción:
    Clase que representa una sección en la aplicación.
    """
    def __init__(self, nombre, icono, layout):
        """
        Descripción:
        Inicializa una instancia de Sección con un nombre, icono y layout que debe ser "c" "g" o "s".

        Retorna:
        No hay retorno explícito.
        """
        self.nombre = nombre
        self.icono = icono
        if layout != "g" and layout != "c" and layout != "s":
            raise wrongLayoutException()
        self.layout = layout