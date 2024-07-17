import uuid

class Integracion:
    """
    Descripción:
    Clase que representa una integración en la aplicación.
    """
    def __init__(self, nombre, nombre_script, script, tipo_dispositivo="s"):
        """
        Descripción:
        Inicializa una instancia de Integracion con un nombre, un nombre de script, un script y un tipo de dispositivo que, por defecto será sensor.

        Retorna:
        No hay retorno explícito.
        """
        self.nombre = nombre
        self.nombre_script = nombre_script
        self.script = script
        self.tipo_dispositivo = tipo_dispositivo