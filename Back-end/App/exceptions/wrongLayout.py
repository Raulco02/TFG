class wrongLayoutException(Exception):
    def __init__(self, mensaje="El layout no es válido, debe ser 'g'(grid), 'c'(card) o 's'(sidebar)."):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

