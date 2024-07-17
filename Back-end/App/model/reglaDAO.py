from App.model.agente_mysql import agente_mysql 

### Para el tema de vigilar que se cumplan las reglas y ejecutar las acciones, revisar conversación Motor de reglas MySQL ChatGPT 29/05 ###
class reglaDAO:
    def __init__(self):
        """
        Descripción:
        Inicializa una nueva instancia del objeto reglaDAO.

        Parámetros:
        Ninguno.
        
        Retorna:
        Ninguno.
        """
        self.agent = agente_mysql()

    def conectar(self):
        """
        Descripción:
        Conecta con la base de datos MySQL.

        Parámetros:
        Ninguno.

        Retorna:
        Ninguno.

        Excepciones:
        Exception: Captura y maneja cualquier excepción que ocurra durante la conexión a la base de datos.
        """
        try:
            self.agent.connect()
        except Exception as ex:
            print(f"Error al conectar con la base de datos: {ex}")

    def desconectar(self):
        """
        Descripción:
        Desconecta de la base de datos MySQL.

        Parámetros:
        Ninguno.

        Retorna:
        Ninguno.

        Excepciones:
        Exception: Captura y maneja cualquier excepción que ocurra durante la desconexión de la base de datos.
        """
        try:
            print('Desconectando', self.agent.connection.is_connected())
            self.agent.disconnect()
        except Exception as ex:
            print('Desconectando', self.agent.connection.is_connected())
            print(f"Error al desconectar de la base de datos: {ex}")

    def obtener_reglas_por_id_usuario(self, id, alerta=False):
        """
        Descripción:
        Obtiene todas las reglas asociadas a un usuario específico desde la base de datos MySQL.

        Parámetros:
        id (int): El ID del usuario cuyas reglas se desean obtener.
        alerta (bool): Indica si se deben filtrar las reglas de alerta.

        Retorna:
        list: Lista de reglas asociadas al usuario especificado.

        Excepciones:
        Exception: Captura y maneja cualquier excepción que ocurra al intentar obtener las reglas.
        """
        try:
            self.conectar()
            condition = f"`usuario_id` = '{id}'"
            reglas = self.agent.read_records('reglas', condition)
            print('reglas:', reglas)
            devolver = []
            if reglas:
                for regla in reglas:
                    add = False
                    objeto = {}
                    criterios = []
                    acciones = []
                    regla_id = regla[0]
                    condition = f"regla_id = '{regla_id}'"
                    result = self.agent.read_records('criterios', condition)
                    for res in result:
                        criterios.append({"id": res[0], "atributo_id": res[2], "dispositivo_id": res[3], "valor": res[4], "comparador": res[5], "tipo": res[6]})
                        #criterios.append(res)
                    #criterios.append(result)
                    print('Records en dao:', result)
                    # if result:
                    #     reglas.append(result[0])
                    acciones_result = self.agent.read_records('acciones-reglas', condition)
                    for res in acciones_result:
                        if (alerta and res[3] == 2) or (not alerta and res[3] != 2):
                            add = True
                            acciones.append({"atributo_id": res[1], "dispositivo_id": res[2], "accion_id": res[3] ,"valor_accion": res[4]})
                        #acciones.append(res)
                    #acciones.append(acciones_result)
                    if add:
                        objeto["id"]=regla[0]
                        objeto["nombre"]=regla[1]
                        objeto["criterios"]=criterios
                        objeto["acciones"]=acciones
                        print("OBJETO:", objeto)
                        devolver.append(objeto)
                # objeto.append(reglas)
                # objeto.append(criterios)
                # objeto.append(acciones)
                # devolver.append(objeto)
                # reglas.append(objeto)
                # reglas.append(criterios)
                # reglas.append(acciones)
            else:
                result = None

            self.desconectar()
            if devolver:
                return devolver
            else:
                return None
        except Exception as ex:
            print(f"Error al obtener el regla por id de usuario: {ex}")
            raise

    def obtener_ids_dispositivos_por_regla(self, id_regla):
        """
        Descripción:
        Obtiene los IDs de dispositivos asociados a una regla específica desde la base de datos MySQL.

        Parámetros:
        id_regla (int): El ID de la regla cuyas IDs de dispositivos se desean obtener.

        Retorna:
        list: Lista de IDs de dispositivos asociados a la regla especificada.

        Excepciones:
        Exception: Captura y maneja cualquier excepción que ocurra al intentar obtener los IDs de dispositivos.
        """
        try:
            self.conectar()
            condition = f"`id-regla` = '{id_regla}'"
            ids = self.agent.read_records('dispositivo-regla', condition)
            self.desconectar()
            if ids:
                return ids
            else:
                return None
        except Exception as ex:
            print(f"Error al obtener los dispositivos por regla: {ex}")
            raise

    # def obtener_reglas(self):
    #     try:
    #         self.conectar()
    #         reglas = []
    #         reglas_result = self.agent.read_records('reglas')
    #         if reglas_result:
    #             for regla in reglas_result:
    #                 reglas.append({"id": regla[0], "nombre": regla[1], "usuario": regla[2]})
    #                 criterios = []
    #                 criterios_result = self.agent.read_records('criterios', f"regla_id = '{regla[0]}'")
    #                 if criterios_result:
    #                     for criterio in criterios_result:
    #                         criterios.append({"id": criterio[0], "atributo_id": criterio[2], "dispositivo_id": criterio[3], "valor": criterio[4], "comparador": criterio[5], "tipo": criterio[6]})
    #                     reglas[-1]['criterios'] = criterios
    #                 acciones = []
    #                 query = """
    #                 SELECT a.nombre, ar.dispositivo_id, ar.atributo_id
    #                 FROM `acciones-reglas` ar
    #                 JOIN acciones a ON ar.accion_id = a.id
    #                 WHERE regla_id = %s
    #                 """
    #                 acciones_result = self.agent.read_records_by_query(query, (regla[0],))
    #                 if acciones_result:
    #                     for accion in acciones_result:
    #                         acciones.append({"nombre": accion[0], "dispositivo_id": accion[1], "atributo_id": accion[2]})
    #                     reglas[-1]['acciones'] = acciones
    #         self.desconectar()
    #         if reglas != []:
    #             return reglas
    #         else:
    #             return None
    #     except Exception as ex:
    #         print(f"Error al obtener las reglas: {ex}")
    #         raise

    def obtener_reglas(self):
        """
        Descripción:
        Obtiene todas las reglas desde la base de datos MySQL, junto con sus criterios y acciones asociadas.

        Parámetros:
        Ninguno.

        Retorna:
        list: Lista de reglas con sus criterios y acciones asociadas.

        Excepciones:
        Exception: Captura y maneja cualquier excepción que ocurra al intentar obtener las reglas.
        """
        try:
            self.conectar()
            
            # Unificar consultas para obtener reglas, criterios y acciones en una sola llamada
            query = """
            SELECT r.id AS regla_id, r.nombre AS regla_nombre, r.usuario_id AS regla_usuario,
                c.id AS criterio_id, c.atributo_id AS criterio_atributo_id, c.dispositivo_id AS criterio_dispositivo_id,
                c.valor AS criterio_valor, c.comparador AS criterio_comparador, c.tipo AS criterio_tipo,
                a.nombre AS accion_nombre, ar.dispositivo_id AS accion_dispositivo_id, ar.atributo_id AS accion_atributo_id, ar.valor_accion AS accion_valor
            FROM reglas r
            LEFT JOIN criterios c ON r.id = c.regla_id
            LEFT JOIN `acciones-reglas` ar ON r.id = ar.regla_id
            LEFT JOIN acciones a ON ar.accion_id = a.id
            """
            
            # Leer todos los registros con una única consulta
            resultados = self.agent.read_records_by_query(query, None)

            print(resultados)
            
            reglas_dict = {}
            
            for fila in resultados:
                print(fila)
                regla_id = fila[0]
                if regla_id not in reglas_dict:
                    reglas_dict[regla_id] = {
                        "id": regla_id,
                        "nombre": fila[1],
                        "usuario": fila[2],
                        "criterios": [],
                        "acciones": []
                    }
                
                # Agregar criterios si existen
                if fila[3] is not None:
                    reglas_dict[regla_id]['criterios'].append({
                        "id": fila[3],
                        "atributo_id": fila[4],
                        "dispositivo_id": fila[5],
                        "valor": fila[6],
                        "comparador": fila[7],
                        "tipo": fila[8]
                    })
                
                # Agregar acciones si existen
                if fila[9] is not None:
                    objeto_accion = {
                        "nombre": fila[9],
                        "dispositivo_id": fila[10],
                        "atributo_id": fila[11],
                        "valor_accion": fila[12]
                    }
                    if reglas_dict[regla_id]['acciones'] is None or reglas_dict[regla_id]['acciones'] == [] or objeto_accion not in reglas_dict[regla_id]['acciones']:
                        reglas_dict[regla_id]['acciones'].append(objeto_accion)
            
            # Convertir el diccionario de reglas a una lista
            reglas = list(reglas_dict.values())
            
            self.desconectar()
            return reglas if reglas else None
        except Exception as ex:
            print(f"Error al obtener las reglas: {ex}")
            self.desconectar()  # Asegurarse de desconectar en caso de error
            raise
        
    def crear_regla_por_usuario_id(self, regla, alerta): #Ver si puede haber 2 reglas con el mismo nombre
        """
        Descripción:
        Crea una nueva regla asociada a un usuario específico en la base de datos MySQL.

        Parámetros:
        regla (dict): Diccionario que contiene la información de la regla a crear.
        alerta (bool): Indica si la regla es una alerta.

        Retorna:
        bool: True si la regla fue creada exitosamente, False en caso contrario.

        Excepciones:
        ValueError: Excepción específica para dispositivos inexistentes.
        Exception: Captura y maneja cualquier otra excepción que ocurra durante la creación de la regla.
        """
        try:
            print('ID USUARIO en DAO:', regla['id_usuario'])
            self.conectar()
            self.agent.start_transaction()
            regla_data = {
                'nombre': regla['nombre'],
                'usuario_id': regla['id_usuario'],
            }
            regla_id = self.agent.create_record('reglas', regla_data)
            for criterio in regla['criterios']:
                criterio_data = {
                    'regla_id': regla_id,
                    'atributo_id': criterio['atributo_id'],
                    'dispositivo_id': criterio['dispositivo_id'],
                    'valor': criterio['valor'],
                    'comparador': criterio['comparador'],
                    'tipo': criterio['tipo']
                }
                self.agent.create_record('criterios', criterio_data)
            if not alerta:
                print("NO ALERTA")
                for accion in regla['acciones']:
                    accion_data = {
                        'regla_id': regla_id,
                        'dispositivo_id': accion['dispositivo_id'],
                        'atributo_id': accion['atributo_id'],
                        'valor_accion': accion['valor_accion'],
                        'accion_id': accion['accion_id']
                    }
                    self.agent.create_record('acciones-reglas', accion_data)
            else:
                print("ALERTA")
                for accion in regla['acciones']:
                    accion_data = {
                        'regla_id': regla_id,
                        'valor_accion': accion['valor_accion'],
                        'accion_id': accion['accion_id']
                    }
                    self.agent.create_record('acciones-reglas', accion_data)
            self.agent.commit_transaction()
            self.desconectar()
            return True
        except Exception as ex:
            self.agent.rollback_transaction()
            if 'fk_iddispositivo_regla' in str(ex):
                raise ValueError("Al menos uno de los dispositivos indicado no existe")
            print(f"Error al crear el regla: {ex}")
            raise

    def eliminar_regla_por_id(self, id, usuario_id):
        """
        Descripción:
        Elimina una regla específica por su ID y el ID del usuario desde la base de datos MySQL.

        Parámetros:
        id (int): El ID de la regla que se desea eliminar.
        usuario_id (int): El ID del usuario al que pertenece la regla.

        Retorna:
        bool: True si la regla fue eliminada exitosamente, False en caso contrario.

        Excepciones:
        Exception: Captura y maneja cualquier excepción que ocurra al intentar eliminar la regla.
        """
        try:
            self.conectar()
            self.agent.start_transaction()
            self.agent.delete_record('reglas', f"id = '{id}' AND usuario_id = '{usuario_id}'")
            # self.agent.delete_record('criterios', f"regla_id = '{id}'")
            # self.agent.delete_record('acciones-reglas', f"regla_id = '{id}'")
            self.agent.commit_transaction()
            self.desconectar()
            return True
        except Exception as ex:
            self.agent.rollback_transaction()
            print(f"Error al eliminar el regla: {ex}")
            raise