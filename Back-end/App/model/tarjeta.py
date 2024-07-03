class Tarjeta:
    def __init__(self, tipo, posicion, id_seccion, contenido=None, imagen=None, tipo_grafico=None, tiempo_grafico=None, id_dispositivo=None, id_atributo=None, nombre_atributo=None, unidades=None, valor=None, nombre_dispositivo=None, icono=None, id_grupo=None, grupo=None, icono_grupo=None):
        self.tipo = tipo
        self.posicion = posicion
        self.id_seccion = id_seccion
        self.contenido = contenido
        self.imagen = imagen
        self.id_dispositivo = id_dispositivo
        self.id_atributo = id_atributo
        self.tipo_grafico = tipo_grafico
        self.tiempo_grafico = tiempo_grafico
        self.nombre_atributo = nombre_atributo
        self.unidades = unidades
        self.valor = valor
        self.nombre_dispositivo = nombre_dispositivo
        self.icono = icono
        self.grupo = grupo
        self.id_grupo = id_grupo
        self.icono_grupo = icono_grupo