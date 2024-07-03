from App.model.agente_mysql import agente_mysql

class tarjetaDAO:
    def __init__(self):
        self.agent = agente_mysql()

    def conectar(self):
        try:
            self.agent.connect()
        except Exception as ex:
            print(f"Error al conectar con la base de datos: {ex}")

    def desconectar(self):
        try:
            print('Desconectando', self.agent.connection.is_connected())
            self.agent.disconnect()
        except Exception as ex:
            print('Desconectando', self.agent.connection.is_connected())
            print(f"Error al desconectar de la base de datos: {ex}")

    def obtener_tarjetas_seccion(self, id_seccion):
        try:
            self.conectar()
            condition = f"`id-seccion` = '{id_seccion}'"
            tarjetas = self.agent.read_records('tarjetas', condition)
            tarjetas_lists = []
            if tarjetas:
                for tarjeta in tarjetas:
                    tarjeta = list(tarjeta)
                    print(tarjeta[1])
                    if tarjeta[1] == 'Estado' or tarjeta[1] == 'Grafico' or tarjeta[1] == 'Termostato':
                        print('AAAAA')
                        id_tarjeta = tarjeta[0]
                        query = '''
                                SELECT ta.`id-atributo`, a.nombre AS nombre_atributo, a.unidades, d.id AS id_dispositivo, d.nombre AS nombre_dispositivo, d.icono, v.valor
                                FROM `tarjetas-atributos` ta
                                JOIN atributos a ON ta.`id-atributo` = a.id
                                JOIN dispositivos d ON ta.`id-dispositivo` = d.id
                                JOIN valores_actuales v ON v.`id-atributo` = a.id AND v.`id-dispositivo` = d.id
                                WHERE ta.`id-tarjeta` = %s;
                                '''
                        atributos = self.agent.read_records_by_query(query, (id_tarjeta,))#self.agent.read_records('tarjetas-atributos', f"`id-tarjeta` = '{id_tarjeta}'")
                        
                        print('atributoss',atributos)
                        if atributos:
                            if len(atributos) > 1:
                                id_atributos = [item[0] for item in atributos]
                                nombres_atributos = [item[1] for item in atributos]
                                unidades = [item[2] for item in atributos]
                                id_dispositivos = [item[3] for item in atributos]
                                nombres_dispositivos = [item[4] for item in atributos]
                                iconos_dispositivos = [item[5] for item in atributos]
                                valores_dispositivos = [item[6] for item in atributos]
                                tarjeta.append(id_atributos)
                                tarjeta.append(nombres_atributos)
                                tarjeta.append(unidades)
                                tarjeta.append(id_dispositivos)
                                tarjeta.append(nombres_dispositivos)
                                tarjeta.append(iconos_dispositivos)
                                tarjeta.append(valores_dispositivos)
                            else:
                                for i in range(len(atributos[0])):
                                    tarjeta.append(atributos[0][i])
                            # tarjeta.append(atributos[0][1])
                            # tarjeta.append(atributos[0][2])
                    elif tarjeta[1] == 'Grupo':
                        id_tarjeta = tarjeta[0]
                        query = '''
                                SELECT tg.idgrupo, g.nombre AS nombre_grupo, g.icono AS icono_grupo, di.id AS id_dispositivo, di.nombre AS nombre_dispositivo, di.icono AS icono_dispositivo, a.id AS id_atributo, a.nombre AS nombre_atributo, a.unidades, v.valor
                                FROM `tarjetas-grupos` tg
                                JOIN grupos g ON tg.idgrupo = g.id
                                JOIN `dispositivo-grupo` d ON tg.idgrupo = d.`id-grupo`
                                JOIN dispositivos di ON d.`id-dispositivo` = di.id
                                JOIN `valores_actuales` v ON v.`id-dispositivo` = di.id
                                JOIN `atributos` a ON v.`id-atributo` = a.id
                                WHERE tg.`idtarjeta` = %s;
                                '''
                        grupos = self.agent.read_records_by_query(query, (id_tarjeta,))
                        print('grupos',grupos)
                        if grupos:
                            if len(grupos) > 1:
                                id_grupos = [item[0] for item in grupos]
                                nombres_grupos = [item[1] for item in grupos]
                                iconos_grupos = [item[2] for item in grupos]
                                id_dispositivos = [item[3] for item in grupos]
                                nombres_dispositivos = [item[4] for item in grupos]
                                iconos_dispositivos = [item[5] for item in grupos]
                                id_atributos = [item[6] for item in grupos]
                                nombres_atributos = [item[7] for item in grupos]
                                unidades = [item[8] for item in grupos]
                                valores = [item[9] for item in grupos]
                                tarjeta.append(id_grupos)
                                tarjeta.append(nombres_grupos)
                                tarjeta.append(iconos_grupos)
                                tarjeta.append(id_dispositivos)
                                tarjeta.append(nombres_dispositivos)
                                tarjeta.append(iconos_dispositivos)
                                tarjeta.append(id_atributos)
                                tarjeta.append(nombres_atributos)
                                tarjeta.append(unidades)
                                tarjeta.append(valores)
                            else:
                                for i in range(len(grupos[0])):
                                    tarjeta.append(grupos[0][i])
                    print(tarjeta)
                    tarjetas_lists.append(tarjeta)
                self.desconectar()
                return tarjetas_lists
            else:
                self.desconectar()
                return None
        except Exception as ex:
            print(f"Error al obtener las tarjetas de la seccion: {ex}")
            return None

    def crear_tarjeta(self, tarjeta):
        try:
            self.conectar()
            self.agent.start_transaction()
            tarjeta_data = self.obtener_tarjeta_tipo(tarjeta)
            id = self.agent.create_record('tarjetas', tarjeta_data)
            tarjeta_data['id'] = id
            self.agent.commit_transaction()
            self.desconectar()
            return tarjeta_data
        except Exception as ex:
            self.agent.rollback_transaction()
            print(f"Error al crear la tarjeta: {ex}")
            raise
            return None

    def crear_tarjeta_estado(self, id_tarjeta, id_dispositivo, id_atributo):
        try:
            self.conectar()
            self.agent.start_transaction()
            tarjeta_data = {
                'id-tarjeta': id_tarjeta,
                'id-dispositivo': id_dispositivo,
                'id-atributo': id_atributo
            }
            self.agent.create_record('tarjetas-atributos', tarjeta_data)
            self.agent.commit_transaction()
            self.desconectar()
            return tarjeta_data
        except Exception as ex:
            self.agent.rollback_transaction()
            print(f"Error al crear la tarjeta: {ex}")
            raise
            return None
        
    def crear_tarjeta_estado(self, id_tarjeta, id_dispositivo, id_atributo): #Duplicado?
        try:
            self.conectar()
            self.agent.start_transaction()
            tarjeta_data = {
                'id-tarjeta': id_tarjeta,
                'id-dispositivo': id_dispositivo,
                'id-atributo': id_atributo
            }
            self.agent.create_record('tarjetas-atributos', tarjeta_data)
            self.agent.commit_transaction()
            self.desconectar()
            return tarjeta_data
        except Exception as ex:
            self.agent.rollback_transaction()
            print(f"Error al crear la tarjeta: {ex}")
            raise
            return None
        
    def crear_tarjeta_grupo(self, id_tarjeta, id_grupo):
        try:
            self.conectar()
            self.agent.start_transaction()
            tarjeta_data = {
                'idtarjeta': id_tarjeta,
                'idgrupo': id_grupo
            }
            self.agent.create_record('tarjetas-grupos', tarjeta_data)
            self.agent.commit_transaction()
            self.desconectar()
            return tarjeta_data
        except Exception as ex:
            self.agent.rollback_transaction()
            print(f"Error al crear la tarjeta: {ex}")
            raise

    def obtener_atributo(self, id_atributo):
        try:
            self.conectar()
            atributo = self.agent.read_records('atributos', f"id = '{id_atributo}'")
            self.desconectar()
            if atributo:
                return atributo[0]
            else:
                return None
        except Exception as ex:
            print(f"Error al obtener el atributo: {ex}")
            return None

    def obtener_tarjeta_tipo(self, tarjeta):
        datos = {}
        if tarjeta.tipo is None or tarjeta.posicion is None or tarjeta.id_seccion is None:
            print('Tipo, posicion, id_seccion', tarjeta.tipo, tarjeta.posicion, tarjeta.id_seccion)
            raise ValueError("Error en los datos de la tarjeta.")
        else:
            datos['tipo']=tarjeta.tipo
            datos['posicion']=tarjeta.posicion
            datos['id-seccion']=tarjeta.id_seccion
        tarjeta.tipo = tarjeta.tipo.lower()
        if tarjeta.tipo == 'texto':
            if (tarjeta.contenido is None and
                tarjeta.imagen is not None and
                tarjeta.id_dispositivo is not None and
                tarjeta.id_atributo is not None and
                tarjeta.tipo_grafico is not None and
                tarjeta.tiempo_grafico is not None and
                tarjeta.id_grupo is not None and
                tarjeta.grupo is not None and
                tarjeta.icono_grupo is not None):
                raise ValueError("Error en los datos de la tarjeta de tipo texto.")
            else:
                datos['contenido']=tarjeta.contenido
        elif tarjeta.tipo == 'imagen':
            if (tarjeta.contenido is not None and
                tarjeta.imagen is None and
                tarjeta.id_dispositivo is not None and
                tarjeta.id_atributo is not None and
                tarjeta.tipo_grafico is not None and
                tarjeta.tiempo_grafico is not None and
                tarjeta.id_grupo is not None and
                tarjeta.grupo is not None and
                tarjeta.icono_grupo is not None):
                raise ValueError("Error en los datos de la tarjeta de tipo imagen.")
            else:
                datos['imagen']=tarjeta.imagen
        elif tarjeta.tipo == 'grafico':
            if (tarjeta.contenido is not None and
                tarjeta.imagen is not None and
                tarjeta.id_dispositivo is None and
                tarjeta.id_atributo is None and
                tarjeta.tipo_grafico is None and
                tarjeta.tiempo_grafico is None and
                tarjeta.id_grupo is not None and
                tarjeta.grupo is not None and
                tarjeta.icono_grupo is not None):
                raise ValueError("Error en los datos de la tarjeta de tipo imagen.")
            else:
                print('Tarjeta del grafico aqui:', tarjeta.nombre_atributo)
                if (tarjeta.nombre_atributo is not None): #No recuerdo por qué es esto la verdad
                    datos['id-dispositivo']=tarjeta.id_dispositivo
                    datos['id-atributo']=tarjeta.id_atributo
                    datos['tipo-grafico']=tarjeta.tipo_grafico
                    datos['tiempo-grafico']=tarjeta.tiempo_grafico
                    datos['nombre-atributo']=tarjeta.nombre_atributo
                    datos['unidades']=tarjeta.unidades
                    datos['valor']=tarjeta.valor
                    datos['nombre-dispositivo']=tarjeta.nombre_dispositivo
                    datos['icono']=tarjeta.icono
                else:
                    datos['tipo-grafico']=tarjeta.tipo_grafico
                    datos['tiempo-grafico']=tarjeta.tiempo_grafico

        elif tarjeta.tipo == 'estado':
            if (tarjeta.contenido is not None and
                tarjeta.imagen is not None and
                tarjeta.id_dispositivo is None and
                tarjeta.id_atributo is None and
                tarjeta.tipo_grafico is not None and
                tarjeta.tiempo_grafico is not None and
                tarjeta.id_grupo is not None and
                tarjeta.grupo is not None and
                tarjeta.icono_grupo is not None):
                raise ValueError("Error en los datos de la tarjeta de tipo estado.")
            else:
                if (tarjeta.nombre_atributo is not None):
                    datos['id-dispositivo']=tarjeta.id_dispositivo
                    datos['id-atributo']=tarjeta.id_atributo
                    datos['nombre-atributo']=tarjeta.nombre_atributo
                    datos['unidades']=tarjeta.unidades
                    datos['valor']=tarjeta.valor
                    datos['nombre-dispositivo']=tarjeta.nombre_dispositivo
                    datos['icono']=tarjeta.icono
        elif tarjeta.tipo == 'grupo':
            if (tarjeta.contenido is not None and
                tarjeta.imagen is not None and
                tarjeta.id_dispositivo is None and
                tarjeta.id_atributo is None and
                tarjeta.tipo_grafico is not None and
                tarjeta.tiempo_grafico is not None and
                tarjeta.id_grupo is None and
                tarjeta.grupo is None and
                tarjeta.icono_grupo is None):
                raise ValueError("Error en los datos de la tarjeta de tipo grupo.")
            else:
                if (tarjeta.nombre_atributo is not None):
                    datos['id-dispositivo']=tarjeta.id_dispositivo
                    datos['id-atributo']=tarjeta.id_atributo
                    datos['nombre-atributo']=tarjeta.nombre_atributo
                    datos['unidades']=tarjeta.unidades
                    datos['valor']=tarjeta.valor
                    datos['nombre-dispositivo']=tarjeta.nombre_dispositivo
                    datos['icono']=tarjeta.icono
                    datos['id-grupo']=tarjeta.id_grupo
                    datos['grupo']=tarjeta.grupo
                    datos['icono-grupo']=tarjeta.icono_grupo
        elif tarjeta.tipo == 'termostato':
            print('Termostato')
            print(tarjeta.contenido, tarjeta.imagen, tarjeta.id_dispositivo, tarjeta.id_atributo, tarjeta.tipo_grafico, tarjeta.tiempo_grafico)
            if (tarjeta.contenido is not None and
                tarjeta.imagen is not None and
                tarjeta.id_dispositivo is None and
                tarjeta.id_atributo is None and
                tarjeta.tipo_grafico is not None and
                tarjeta.tiempo_grafico is not None and
                tarjeta.id_grupo is not None and
                tarjeta.grupo is not None and
                tarjeta.icono_grupo is not None):
                raise ValueError("Error en los datos de la tarjeta de tipo termostato.")
            else:
                if (tarjeta.nombre_atributo is not None):
                    datos['id-dispositivo']=tarjeta.id_dispositivo
                    datos['id-atributo']=tarjeta.id_atributo
                    datos['nombre-atributo']=tarjeta.nombre_atributo
                    datos['unidades']=tarjeta.unidades
                    datos['valor']=tarjeta.valor
                    datos['nombre-dispositivo']=tarjeta.nombre_dispositivo
                    datos['icono']=tarjeta.icono
        elif tarjeta.tipo == 'plano':
            if (tarjeta.contenido is not None and
                tarjeta.imagen is not None and
                tarjeta.id_dispositivo is not None and
                tarjeta.id_atributo is not None and
                tarjeta.tipo_grafico is not None and
                tarjeta.tiempo_grafico is not None and
                tarjeta.id_grupo is not None and
                tarjeta.grupo is not None and
                tarjeta.icono_grupo is not None):
                raise ValueError("Error en los datos de la tarjeta de tipo plano.")

        else:
            raise ValueError("El tipo de tarjeta debe ser texto, imagen, grafico, estado, grupo o plano.")
        print('Datos:', datos)
        return datos
    
    def eliminar_tarjeta(self, id_tarjeta):
        try:
            self.conectar()
            self.agent.start_transaction()
            self.agent.delete_record('tarjetas', f"id = '{id_tarjeta}'")
            self.agent.delete_record(f"`tarjetas-atributos`", f"`id-tarjeta` = '{id_tarjeta}'")
            self.agent.commit_transaction()
            self.desconectar()
            return True
        except Exception as ex:
            self.agent.rollback_transaction()
            print(f"Error al eliminar la tarjeta: {ex}")
            raise
    
    def setTemperatura(self, id_dispositivo, id_atributo, valor):
        try:
            self.conectar()
            self.agent.start_transaction()
            self.agent.update_record('valores_actuales', {'valor': valor}, f"`id-dispositivo` = '{id_dispositivo}' AND `id-atributo` = '{id_atributo}'")
            self.agent.commit_transaction()
            self.desconectar()
            return True
        except Exception as ex:
            self.agent.rollback_transaction()
            print(f"Error al actualizar el valor de la temperatura: {ex}")
            raise