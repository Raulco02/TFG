class duplicateIntegracionException(Exception):
    def __init__(self, mensaje="Ya existe una integración con ese nombre."):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

class duplicateDispositivoException(Exception):
    def __init__(self, mensaje="Ya existe un dispositivo con ese nombre o ID."):
        self.mensaje = mensaje
        super().__init__(self.mensaje)
    
class duplicateAtributoException(Exception):
    def __init__(self, mensaje="Se está intentando crear un atributo que ya existe."):
        self.mensaje = mensaje
        super().__init__(self.mensaje)