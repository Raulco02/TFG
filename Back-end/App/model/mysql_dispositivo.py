class mysql_dispositivo:
    """
    Descripción:
    Clase que representa un dispositivo en la aplicación.
    """
    def __init__(self, id, nombre, atributos):#(self, id, nombre, atributos, valores_actuales, icono):
        """
        Descripción:
        Inicializa una instancia de mysql_dispositivo con un id, nombre y atributos.

        Retorna:
        No hay retorno explícito.
        """
        self.id = id
        self.nombre = nombre
        self.atributos = atributos
        #self.valores_actuales = valores_actuales ##Iría aquí?
        #self.icono = icono #Seria en atributos