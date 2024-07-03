import uuid

class Integracion:
    def __init__(self, nombre, nombre_script, script, tipo_dispositivo="s"):
        self.nombre = nombre
        self.nombre_script = nombre_script
        self.script = script
        self.tipo_dispositivo = tipo_dispositivo