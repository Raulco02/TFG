from App.model.tarjetaDAO import tarjetaDAO
from App.model.mysql_dispositivoDAO import mysql_dispositivoDAO
from App.model.tarjeta import Tarjeta
from App.helpers.tarjetas import tarjetasHelper

class tarjetaService:
    def obtener_tarjetas_seccion(id_seccion): #Comprobar los atributos
        tarjeta_dao = tarjetaDAO()
        tarjeta_data = tarjeta_dao.obtener_tarjetas_seccion(id_seccion)
        tarjetas=[]
        if tarjeta_data is None:
            return None
        tarjetas = tarjetasHelper.generar_lista_tarjetas(tarjeta_data, tarjeta_dao)
        # for tarjeta in tarjeta_data:
        #     tarjeta = Tarjeta(tarjeta[1], tarjeta[2], tarjeta[7], tarjeta[3], tarjeta[4], tarjeta[5], tarjeta[6])
        #     tarjeta_comp = tarjeta_dao.obtener_tarjeta_tipo(tarjeta)
        #     tarjetas.append(tarjeta_comp)#{"id": tarjeta[0], "tipo": tarjeta[1], "posicion": tarjeta[2], "dimensiones": tarjeta[3], "contenido": tarjeta[4], "imagen": tarjeta[5], "id-dispositivo": tarjeta[6], "id-atributo": tarjeta[7], "tipo-grafico": tarjeta[8], "tiempo-grafico": tarjeta[9], "id-seccion": tarjeta[10]})
        return tarjetas
    
    
    def crear_tarjeta(tipo, posicion, contenido, imagen, id_dispositivo, id_atributo, tipo_grafico, tiempo_grafico, id_seccion, grupo = None):
        print('tipo', tipo)	
        print('posicion', posicion)
        print('contenido', contenido)
        print('imagen', imagen)
        print('id_dispositivo', id_dispositivo)
        print('id_atributo', id_atributo)
        print('tipo_grafico', tipo_grafico)
        print('tiempo_grafico', tiempo_grafico)
        print('id_seccion', id_seccion)
        tarjeta_dao = tarjetaDAO()
        if tipo == 'Termostato':
            atributo = tarjeta_dao.obtener_atributo(id_atributo)
            print('El atributo', atributo)
            for i in atributo:
                print(i)
            if atributo is None:
                raise ValueError("El atributo no existe.")
            if atributo[4] != 't':
                raise ValueError("El atributo no es de tipo temperatura.")
        tarjeta = Tarjeta(tipo, posicion, id_seccion, contenido, imagen, tipo_grafico, tiempo_grafico, None, None)
        print('Tarjeta', tarjeta)
        tarjeta_data = tarjeta_dao.crear_tarjeta(tarjeta)
        print('ID de la tarjeta', tarjeta_data, id_atributo, id_dispositivo)
        if id_dispositivo is not None and id_atributo is not None: #Si aqui obtengo error tengo que eliminar la tarjeta que se ha creado
            #id_atributo = tarjeta_dao.obtener_atributo(id_atributo)[0]
            try:
                print('tarjeta',tarjeta)
                print('id_atributo',id_atributo)
                print('id_dispositivo',id_dispositivo)
                print('tarjeta_data',tarjeta_data)
                if isinstance(id_dispositivo, list):
                    if isinstance(id_atributo, list):
                        i = 0
                        for id in id_dispositivo:
                            tarjeta_dao.crear_tarjeta_estado(tarjeta_data['id'], id, id_atributo[i])
                            i += 1
                    else:
                        for id in id_dispositivo:
                            tarjeta_dao.crear_tarjeta_estado(tarjeta_data['id'], id, id_atributo)
                else:
                    tarjeta_dao.crear_tarjeta_estado(tarjeta_data['id'], id_dispositivo, id_atributo) #cambiar nombre de este metodo
            except Exception as e:
                print('Error al crear tarjeta estado', e)
                tarjeta_dao.eliminar_tarjeta(tarjeta_data['id'])
                if 'Incorrect integer value' in str(e):
                    raise ValueError("Atributo debe ser un numero.")
                raise
        elif grupo is not None:
            try:
                tarjeta_dao.crear_tarjeta_grupo(tarjeta_data['id'], grupo)
            except Exception as e:
                print('Error al crear tarjeta grupo', e)
                tarjeta_dao.eliminar_tarjeta(tarjeta_data['id'])
                if 'Incorrect integer value' in str(e):
                    raise ValueError("id_grupo debe ser un numero.")
                raise
        return tarjeta_data

    def setTemperatura(id_dispositivo, id_atributo, valor):
        tarjeta_dao = tarjetaDAO()  # Observa si el dispositivo y el atributo corresponden
        from mqtt_client import mqtt_client
        mqtt_client_instance = mqtt_client(publish=True)  # Renombrado y pasando publish=True
        dispositivo_dao = mysql_dispositivoDAO()
        # temperatura_establecida = tarjeta_dao.setTemperatura(id_dispositivo, id_atributo, valor)  # Quizá esto no va aquí
        datos_actuacion = dispositivo_dao.obtener_datos_actuacion(id_dispositivo, id_atributo)
        print('Datos de actuación', datos_actuacion)
        if datos_actuacion is None or datos_actuacion['topic'] is None or datos_actuacion['plantilla'] is None:
            raise ValueError("No se ha encontrado el dispositivo o el atributo.")
        print('Datos de actuación', datos_actuacion)
        publicado = mqtt_client_instance.publish_message(datos_actuacion['topic'], datos_actuacion['plantilla'], {"valor":valor})
        return publicado
        #return temperatura_establecida