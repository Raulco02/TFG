class mysql_dispositivo:
    def __init__(self, id, nombre, atributos):#(self, id, nombre, atributos, valores_actuales, icono):
        self.id = id
        self.nombre = nombre
        self.atributos = atributos
        #self.valores_actuales = valores_actuales ##Iría aquí?
        #self.icono = icono #Seria en atributos