from App.model.agente_mysql import agente_mysql
from App.exceptions.duplicate import duplicateDispositivoException
# import MySQLdb

###NO HAY NADA DE UBICACION MAS ALLA DE GET, VER SI TENGO QUE MANEJAR ALGUN ERROR### ###VER ICONO DE ATRIBUTOS Y SI FALTA POR INCLUIR EN ALGUNO
class mysql_dispositivoDAO:
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

    def obtener_dispositivos(self):
        try:
            self.agent.connect()
            query = """
                SELECT d.id, d.nombre, d.icono, d.topic, d.ubicacion, v.valor, a.id, a.nombre, a.unidades, a.icono, a.limite_superior, a.limite_inferior, i.nombre, v.`topic-actuacion`, v.plantilla	
                FROM dispositivos d
                JOIN valores_actuales v ON d.id = v.`id-dispositivo`
                JOIN atributos a ON v.`id-atributo` = a.id
                JOIN `dispositivos-integraciones` di ON d.id = di.iddispositivos
                JOIN integraciones i ON di.idintegraciones = i.id
            """
            result = self.agent.read_records_by_query(query, None)
            #print(result)
            dispositivos_con_datos = {}
            for row in result:
                dispositivo_id = row[0]
                nombre_dispositivo = row[1]
                icono = row[2]
                topic = row[3]
                ubicacion = row[4]
                valor = row[5]
                atributo_id = row[6]
                nombre_atributo = row[7]
                unidades = row[8]
                icono_a = row[9]
                limite_superior = row[10]
                limite_inferior = row[11]
                integracion = row[12]
                topic_actuacion = row[13]
                plantilla = row[14]

                if dispositivo_id not in dispositivos_con_datos:
                    dispositivos_con_datos[dispositivo_id] = {
                        "icono": icono,
                        "id": dispositivo_id,
                        "nombre": nombre_dispositivo,
                        "topic": topic, 
                        "ubicacion": ubicacion,
                        "atributos": [],
                        "integracion": integracion
                    }
                dispositivos_con_datos[dispositivo_id]["atributos"].append({
                    "id": atributo_id,
                    "nombre_atributo": nombre_atributo,
                    "unidades": unidades,
                    "icono": icono_a,
                    "limite_superior": limite_superior,
                    "limite_inferior": limite_inferior,
                    "valor": valor,
                    **({"topic-actuacion": topic_actuacion} if topic_actuacion is not None else {}),
                    **({"plantilla": plantilla} if plantilla is not None else {})
                })

            dispositivos_con_datos_list = list(dispositivos_con_datos.values())
            self.agent.disconnect()
            
            return dispositivos_con_datos_list
        except Exception as ex:
            print(f"Error al obtener todos los dispositivos: {ex}")
            raise
            

    def obtener_dispositivos_temperatura(self):
        try:
            self.agent.connect()
            query = """
                SELECT d.id, d.nombre, d.icono, d.topic, d.ubicacion, v.valor, a.id, a.nombre, a.unidades, a.icono, i.nombre, v.`topic-actuacion`, v.plantilla	
                FROM dispositivos d
                JOIN valores_actuales v ON d.id = v.`id-dispositivo`
                JOIN atributos a ON v.`id-atributo` = a.id
                JOIN `dispositivos-integraciones` di ON d.id = di.iddispositivos
                JOIN integraciones i ON di.idintegraciones = i.id
                WHERE a.tipo = '2'
            """
            result = self.agent.read_records_by_query(query, None)
            print(result)
            dispositivos_con_datos = {}
            for row in result:
                dispositivo_id = row[0]
                nombre_dispositivo = row[1]
                icono = row[2]
                topic = row[3]
                ubicacion = row[4]
                valor = row[5]
                atributo_id = row[6]
                nombre_atributo = row[7]
                unidades = row[8]
                icono_a = row[9]
                integracion = row[10]
                topic_actuacion = row[11]
                plantilla = row[12]

                if dispositivo_id not in dispositivos_con_datos:
                    dispositivos_con_datos[dispositivo_id] = {
                        "icono": icono,
                        "id": dispositivo_id,
                        "nombre": nombre_dispositivo,
                        "topic": topic, 
                        "ubicacion": ubicacion,
                        "atributos": [],
                        "integracion": integracion
                    }
                dispositivos_con_datos[dispositivo_id]["atributos"].append({
                    "id": atributo_id,
                    "nombre_atributo": nombre_atributo,
                    "unidades": unidades,
                    "icono": icono_a,
                    "valor": valor,
                    **({"topic-actuacion": topic_actuacion} if topic_actuacion is not None else {}),
                    **({"plantilla": plantilla} if plantilla is not None else {})
                })

            dispositivos_con_datos_list = list(dispositivos_con_datos.values())
            self.agent.disconnect()
            return dispositivos_con_datos_list
        except Exception as ex:
            print(f"Error al obtener todos los dispositivos: {ex}")
            raise
        
    def obtener_dispositivos_por_atributo(self, atributo):
        try:
            self.agent.connect()
            query = """
                SELECT d.id, d.nombre, d.icono, d.ubicacion, v.valor, a.nombre, a.unidades, a.icono
                FROM dispositivos d
                JOIN valores_actuales v ON d.id = v.`id-dispositivo`
                JOIN atributos a ON v.`id-atributo` = a.id
                WHERE a.id = %s
            """
            result = self.agent.read_records_by_query(query, (atributo,))
            dispositivos_con_datos = {}
            for row in result:
                dispositivo_id = row[0]
                nombre_dispositivo = row[1]
                icono = row[2]
                ubicacion = row[3]
                valor = row[4]
                nombre_atributo = row[5]
                unidades = row[6]
                icono_a = row[7]

                if dispositivo_id not in dispositivos_con_datos:
                    dispositivos_con_datos[dispositivo_id] = {
                        "icono": icono,
                        "id": dispositivo_id,
                        "nombre": nombre_dispositivo,
                        "ubicacion": ubicacion,
                        "atributos": []
                    }
                dispositivos_con_datos[dispositivo_id]["atributos"].append({
                    "nombre_atributo": nombre_atributo,
                    "unidades": unidades,
                    "valor": valor,
                    "icono": icono_a
                })

            dispositivos_con_datos_list = list(dispositivos_con_datos.values())
            self.agent.disconnect()
            return dispositivos_con_datos_list
        except Exception as ex:
            print(f"Error al obtener todos los dispositivos: {ex}")
            raise
        
    def obtener_dispositivo_por_id(self, id):
        try:
            print('ID;',id)
            self.agent.connect()
            query = """
                SELECT d.id, d.nombre, d.icono, d.ubicacion, v.valor, a.nombre, a.unidades, a.icono, a.id
                FROM dispositivos d
                JOIN valores_actuales v ON d.id = v.`id-dispositivo`
                JOIN atributos a ON v.`id-atributo` = a.id
                WHERE d.id = %s
            """
            result = self.agent.read_records_by_query(query, (id,))
            dispositivos_con_datos = {}
            for row in result:
                dispositivo_id = row[0]
                nombre_dispositivo = row[1]
                icono = row[2]
                ubicacion = row[3]
                valor = row[4]
                nombre_atributo = row[5]
                unidades = row[6]
                icono_a = row[7]
                atributo_id = row[8]

                if dispositivo_id not in dispositivos_con_datos:
                    dispositivos_con_datos[dispositivo_id] = {
                        "icono": icono,
                        "id": dispositivo_id,
                        "nombre": nombre_dispositivo,
                        "ubicacion": ubicacion,
                        "atributos": []
                    }
                dispositivos_con_datos[dispositivo_id]["atributos"].append({
                    "id": atributo_id,
                    "nombre_atributo": nombre_atributo,
                    "unidades": unidades,
                    "valor": valor,
                    "icono": icono_a
                })

            dispositivos_con_datos_list = list(dispositivos_con_datos.values())
            self.agent.disconnect()
            return dispositivos_con_datos_list
        except Exception as ex:
            print(f"Error al obtener todos los dispositivos: {ex}")
            raise
    
    def crear_dispositivo(self, dispositivo):
        try:
            self.conectar()
            self.agent.start_transaction()
            data = {
                'id': dispositivo.id,
                'nombre': dispositivo.nombre,
            }
            self.agent.create_record('dispositivos', data)
            self.agent.commit_transaction()
            self.desconectar()##PORQUE EN OBTENER_ATRIBUTOS SE HACE CONECTAR Y DESCONECTAR
            atributos=self.obtener_atributos()
            # for atributo in dispositivo.atributos:
            #     coincidencia = any(atributo == item['nombre'] for item in atributos)
            #     print(atributo, coincidencia)
            #     if not coincidencia:
            #         data = { ##El atributos de dispositivos debe ser un diccionario con nombre y unidades
            #             'nombre': atributo,
            #             'unidades': 'N/A'
            #         }
            #         self.agent.create_record('atributos', data)
            self.conectar()##POR LO DE QUE SE HA DESCONECTADO en obtener_atributos
            self.agent.start_transaction()
            for nombre, unidad in dispositivo.atributos.items():
                coincidencia = any(nombre == item['nombre'] for item in atributos)
                print(nombre, coincidencia)
                if not coincidencia:
                    data = {
                        'nombre': nombre,
                        'unidades': unidad
                    }
                    self.agent.create_record('atributos', data)
            self.agent.commit_transaction()
            self.desconectar()
            return True
        except Exception as ex:
            self.agent.rollback_transaction()
            print(f"Error al crear el dispositivo: {ex}")
            raise
    
    def valores_actuales(self, valores):
        try:
            self.conectar()
            self.agent.start_transaction()
            for valor in valores:
                # Verificar si el registro ya existe
                existente = self.agent.read_records('valores_actuales', f'''`id-dispositivo` = '{valor['id-dispositivo']}' AND `id-atributo` = '{valor['id-atributo']}' ''')
                if existente:
                    # Si el registro existe, actualizar el valor
                    self.agent.update_record('valores_actuales', {'valor': valor['valor']}, f'''id = {existente[0][0]}''')
                else:
                    # Si el registro no existe, crear uno nuevo
                    data = {
                        'id-dispositivo': valor['id-dispositivo'],
                        'id-atributo': valor['id-atributo'],
                        'valor': valor['valor']
                    }
                    self.agent.create_record('valores_actuales', data)
            self.agent.commit_transaction()
            self.desconectar()
            return True
        except Exception as ex:
            self.agent.rollback_transaction()
            print(f"Error al crear o actualizar los valores actuales: {ex}")
            raise
    
    def valores_actuales_xml(self, valores):
        try:
            self.conectar()
            self.agent.start_transaction()
            for valor in valores:
                # Verificar si el registro ya existe
                atributo = self.agent.read_records('atributos', f'id = {valor["nombre-atributo"]}')
                existente = self.agent.read_records('valores_actuales', f'''`id-dispositivo` = '{valor['id-dispositivo']}' AND `id-atributo` = '{atributo}' ''')
                if existente:
                    # Si el registro existe, actualizar el valor
                    self.agent.update_record('valores_actuales', {'valor': valor['valor']}, f'''id = {existente[0][0]}''')
                else:
                    # Si el registro no existe, crear uno nuevo
                    data = {
                        'id-dispositivo': valor['id-dispositivo'],
                        'id-atributo': valor['id-atributo'],
                        'valor': valor['valor']
                    }
                    self.agent.create_record('valores_actuales', data)
            self.agent.commit_transaction()
            self.desconectar()
            return True
        except Exception as ex:
            self.agent.rollback_transaction()
            print(f"Error al crear o actualizar los valores actuales: {ex}")
            raise

    def obtener_valor(self, id_dispositivo, id_atributo):
        try:
            self.conectar()
            result = self.agent.read_records('valores_actuales', f"`id-dispositivo` = '{id_dispositivo}' AND `id-atributo` = {id_atributo}")
            if result:
                return result[0][1]
            else:
                return None
        except Exception as ex:
            print(f"Error al obtener el valor actual: {ex}")
            raise
            return None
        finally:
            self.desconectar()

    
    def obtener_atributos(self):
        try:
            self.agent.connect()
            result = self.agent.read_records('atributos')
            atributos = []
            for row in result:
                atributo = {
                    'id': row[0],
                    'nombre': row[1],
                    'unidades': row[2]
                }
                atributos.append(atributo)

            self.agent.disconnect()
            return atributos
        except Exception as ex:
            print(f"Error al obtener todos los atributos: {ex}")
            raise
        
    def crear_dispositivo_http(self, id, nombre, topic, integracion, ubicacion):
        try:
            self.conectar()
            self.agent.start_transaction()
            data = {
                'id': id,
                'nombre': nombre,
                'topic': topic,
                'ubicacion': ubicacion
            }
            self.agent.create_record('dispositivos', data)
            for atributo in integracion['atributos']:
                atributo_bbdd = self.agent.read_records('atributos', 'id = ' + atributo['id'])[0]
                print('atributo_bbdd[3]:', atributo_bbdd[3])
                if not atributo_bbdd:
                    raise ValueError(f"El atributo con id {atributo['id']} no existe.")
                if atributo_bbdd[3] != True and atributo_bbdd[3] != 'true':
                    self.agent.create_record('valores_actuales', {'id-dispositivo': id, 'id-atributo': atributo['id']})
                else:
                    if 'topic' not in atributo:
                        raise ValueError(f"El atributo {atributo['nombre']} no tiene un topic de actuación.")
                    if 'plantilla' not in atributo:
                        raise ValueError(f"El atributo {atributo['nombre']} no tiene una plantilla de actuación.")
                    self.agent.create_record('valores_actuales', {'id-dispositivo': id, 'id-atributo': atributo['id'], 'topic-actuacion': atributo['topic'], 'plantilla': atributo['plantilla']})
            self.agent.create_record('dispositivos-integraciones', {'iddispositivos': id, 'idintegraciones': integracion['id']})########Probar esto
            self.agent.commit_transaction()
            self.desconectar()
            return True
        except Exception as ex:
            self.agent.rollback_transaction()
            self.desconectar()
            #self.desconectar()
            #Habria que hacer el desconectar, pero habría que controlar si está conectado
            print(f"Error al crear el dispositivo: {ex}")
            if "Duplicate entry" in str(ex) and ("dispositivos.nombre_UNIQUE" in str(ex) or "dispositivos.PRIMARY" in str(ex)):
                raise duplicateDispositivoException()
            raise
        
    def edit_dispositivo_http(self, prev_id, id, nombre, topic, integracion, ubicacion):
        try:
            self.conectar()
            data = {
                'id': id,
                'nombre': nombre,
                'topic': topic,
                'ubicacion': ubicacion
            }
            self.agent.start_transaction()
            dispositivo_actualizado = self.agent.update_record('dispositivos', data, f"id = '{prev_id}'")
            va_dispositivo = self.agent.read_records("valores_actuales", f"`id-dispositivo` = '{id}'")
            print('dispositivo actualizado',dispositivo_actualizado)
            print('valores del dispositivo',va_dispositivo)
            if(not dispositivo_actualizado or va_dispositivo == []):
                self.agent.rollback_transaction()
                raise ValueError(f"El dispositivo con id '{prev_id}' no existe.")
            atributos_dispositivo = [{"id_atributo":tupla[3], "encontrado":False} for tupla in va_dispositivo]
            print('Los atributos son',atributos_dispositivo)
            for atributo in integracion['atributos']:
                atributo_bbdd = self.agent.read_records('atributos', 'id = ' + atributo['id'])[0]
                print('atributo_bbdd[3]:', atributo_bbdd[3])
                print('atributo', atributo)
                if not atributo_bbdd:
                    self.agent.rollback_transaction()
                    raise ValueError(f"El atributo con id {atributo['id']} no existe.")
                presente = any(d["id_atributo"] == atributo_bbdd[0] for d in atributos_dispositivo)
                if not presente:
                    print('Esto')
                    if atributo_bbdd[3] != True and atributo_bbdd[3] != 'true':
                        self.agent.create_record('valores_actuales', {'id-dispositivo': id, 'id-atributo': atributo['id']})
                    else:
                        if 'topic' not in atributo:
                            self.agent.rollback_transaction()
                            raise ValueError(f"El atributo {atributo['nombre']} no tiene un topic de actuación.")
                        if 'plantilla' not in atributo:
                            self.agent.rollback_transaction()
                            raise ValueError(f"El atributo {atributo['nombre']} no tiene una plantilla de actuación.")
                        self.agent.create_record('valores_actuales', {'id-dispositivo': id, 'id-atributo': atributo['id'], 'topic-actuacion': atributo['topic'], 'plantilla': atributo['plantilla']})
                else:
                    print('Esto otro')
                    for a in atributos_dispositivo:
                        if a["id_atributo"] == atributo_bbdd[0]:
                            a["encontrado"] = True
                            break
                    if atributo_bbdd[3] != True and atributo_bbdd[3] != 'true': #############Hay que comprobar si ya estaba y si no crearlo, y si habia uno que ya no, borrarlo y lo de abajo igual
                        self.agent.update_record('valores_actuales', {'`id-dispositivo`': id, '`id-atributo`': atributo['id']}, f"`id-dispositivo` = '{id}' AND `id-atributo` = '{atributo['id']}'")
                        print('Por aqui')
                    else:
                        if 'topic' not in atributo:
                            self.agent.rollback_transaction()
                            raise ValueError(f"El atributo {atributo['nombre']} no tiene un topic de actuación.")
                        if 'plantilla' not in atributo:
                            self.agent.rollback_transaction()
                            raise ValueError(f"El atributo {atributo['nombre']} no tiene una plantilla de actuación.")
                        self.agent.update_record('valores_actuales', {'`id-dispositivo`': id, '`id-atributo`': atributo['id'], '`topic-actuacion`': atributo['topic'], 'plantilla': atributo['plantilla']}, f"`id-dispositivo` = '{id}' AND `id-atributo` = '{atributo['id']}'")
                        print('Else por aqui')
            print('Por aqui tambien')
            self.agent.update_record('`dispositivos-integraciones`', {'iddispositivos': id, 'idintegraciones': integracion['id']}, f"iddispositivos = '{id}'")########Probar esto
            print('Acabando')
            for atributo in atributos_dispositivo:
                if not atributo["encontrado"]:
                    self.agent.delete_record('valores_actuales', f"`id-dispositivo` = '{id}' AND `id-atributo` = '{atributo['id_atributo']}'")
            self.agent.commit_transaction()
            self.desconectar()
            return True
        except Exception as ex:
            #self.desconectar()
            #Habria que hacer el desconectar, pero habría que controlar si está conectado
            print(f"Error al crear el dispositivo: {ex}")
            self.desconectar()
            if "Duplicate entry" in str(ex) and ("dispositivos.nombre_UNIQUE" in str(ex) or "dispositivos.PRIMARY" in str(ex)):
                raise duplicateDispositivoException()
            raise
            return False
        
    def eliminar_dispositivo(self, id):
        try:
            self.conectar()
            self.agent.start_transaction()
            self.agent.delete_record('dispositivos', f"id = '{id}'")
            # self.agent.delete_record('valores_actuales', f"`id-dispositivo` = '{id}'")
            # self.agent.delete_record('`dispositivos-integraciones`', f"iddispositivos = '{id}'")
            self.agent.commit_transaction()
            self.desconectar()
            return True
        except Exception as ex:
            self.agent.rollback_transaction()
            print(f"Error al eliminar el dispositivo: {ex}")
            raise
            return False
        
    
    def obtener_datos_actuacion(self, id_dispositivo, id_atributo):
        try:
            self.conectar()
            id_dispositivo = id_dispositivo
            print('id_dispositivo', id_dispositivo, 'id_atributo', id_atributo)
            result = self.agent.read_records('valores_actuales', f"`id-dispositivo` = '{id_dispositivo}' AND `id-atributo` = {id_atributo}")
            self.desconectar()
            if result:
                datos = {
                    'topic': result[0][4],
                    'plantilla': result[0][5]
                }
                return datos
            else:
                return None
        except Exception as ex:
            print(f"Error al obtener los datos de actuación: {ex}")
            raise

    def obtener_tipo_atributo(self, id_atributo):
        try:
            self.conectar()
            query = """
                SELECT t.nombre
                FROM atributos a
                JOIN tipos_atributos t ON a.tipo = t.id
                WHERE a.id = %s
            """
            result = self.agent.read_records_by_query(query, (id_atributo,))
            self.desconectar()
            if result:
                return result[0][0]
            else:
                return None
        except Exception as ex:
            self.desconectar()
            print(f"Error al obtener el tipo de atributo: {ex}")
            raise

    def obtener_todos_los_valores(self):
        try:
            self.agent.connect()
            query = """
                SELECT `id-dispositivo`, `id-atributo`, valor
                FROM valores_actuales
            """
            result = self.agent.read_records_by_query(query, None)
            self.agent.disconnect()
            return result
        except Exception as ex:
            print(f"Error al obtener todos los valores: {ex}")
            self.agent.disconnect()
            raise

    def obtener_valores_dispositivos_atributos(self, dispositivos_atributos):
        try:
            self.agent.connect()
            # Construir la lista de condiciones para la cláusula WHERE
            condiciones = []
            for item in dispositivos_atributos:
                id_dispositivo, id_atributo = item
                condiciones.append(f"(`id-dispositivo` = '{id_dispositivo}' AND `id-atributo` = '{id_atributo}')")

            # Unir todas las condiciones con OR
            condiciones_str = " OR ".join(condiciones)

            # Construir la consulta SQL completa
            query = f"""
                SELECT `id-dispositivo`, `id-atributo`, valor
                FROM valores_actuales
                WHERE {condiciones_str}
            """

            result = self.agent.read_records_by_query(query, None)
            self.agent.disconnect()
            return result
        except Exception as ex:
            print(f"Error al obtener los valores de dispositivos y atributos: {ex}")
            self.agent.disconnect()
            raise




