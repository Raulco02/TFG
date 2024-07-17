from App.model.agente_mysql import agente_mysql

class grupoDAO:
    """
    Descripción:
    Clase que gestiona las operaciones de acceso a datos (DAO) relacionadas con los grupos y su interacción
    con la base de datos MySQL.
    """
    def __init__(self):
        """
        Descripción:
        Inicializa una instancia de `grupoDAO`, creando una conexión con la base de datos MySQL
        utilizando el objeto `agente_mysql` definido en el módulo `App.model`.

        Retorna:
        None
        """
        self.agent = agente_mysql()

    def conectar(self):
        """
        Descripción:
        Establece una conexión activa con la base de datos MySQL utilizando el método `connect()` del agente MySQL.

        Retorna:
        None

        Excepciones:
        Exception: Captura y maneja cualquier excepción que ocurra al intentar conectar con la base de datos.
        """
        try:
            self.agent.connect()
        except Exception as ex:
            print(f"Error al conectar con la base de datos: {ex}")

    def desconectar(self):
        """
        Descripción:
        Cierra la conexión activa con la base de datos MySQL utilizando el método `disconnect()` del agente MySQL.

        Retorna:
        None

        Excepciones:
        Exception: Captura y maneja cualquier excepción que ocurra al intentar desconectar de la base de datos.
        """
        try:
            print('Desconectando', self.agent.connection.is_connected())
            self.agent.disconnect()
        except Exception as ex:
            print('Desconectando', self.agent.connection.is_connected())
            print(f"Error al desconectar de la base de datos: {ex}")

    def obtener_grupos_por_id_usuario(self, id):
        """
        Descripción:
        Obtiene los grupos asociados a un usuario específico mediante su ID consultando la base de datos.

        Parámetros:
        - id (str): ID del usuario para el cual se obtendrán los grupos.

        Retorna:
        - list: Lista de grupos asociados al usuario.
        - None: Si no se encontraron grupos para el usuario.

        Excepciones:
        Exception: Captura y maneja cualquier excepción que ocurra durante la consulta a la base de datos.
        """
        try:
            self.conectar()
            condition = f"`id-usuario` = '{id}'"
            ids = self.agent.read_records('usuario-grupo', condition)
            grupos = []
            if ids:
                for id in ids:
                    grupo_id = id[1]
                    condition = f"id = '{grupo_id}'"
                    result = self.agent.read_records('grupos', condition)
                    print('Records en dao:', result)
                    if result:
                        grupos.append(result[0])
            else:
                result = None

            self.desconectar()
            if grupos:
                return grupos
            else:
                return None
        except Exception as ex:
            print(f"Error al obtener el grupo por id de usuario: {ex}")
            raise

    def obtener_ids_dispositivos_por_grupo(self, id_grupo):
        """
        Descripción:
        Obtiene los IDs de los dispositivos asociados a un grupo específico consultando la base de datos.

        Parámetros:
        - id_grupo (str): ID del grupo para el cual se obtendrán los IDs de los dispositivos.

        Retorna:
        - list: Lista de IDs de dispositivos asociados al grupo.
        - None: Si no se encontraron dispositivos para el grupo.

        Excepciones:
        Exception: Captura y maneja cualquier excepción que ocurra durante la consulta a la base de datos.
        """
        try:
            self.conectar()
            condition = f"`id-grupo` = '{id_grupo}'"
            ids = self.agent.read_records('dispositivo-grupo', condition)
            self.desconectar()
            if ids:
                return ids
            else:
                return None
        except Exception as ex:
            print(f"Error al obtener los dispositivos por grupo: {ex}")
            raise
        
    def crear_grupo_por_usuario_id(self, grupo, id_usuario, dispositivos): #Ver si puede haber 2 grupos con el mismo nombre
        """
        Descripción:
        Crea un nuevo grupo y lo asocia al usuario especificado por su ID en la base de datos,
        además de asociar los dispositivos indicados al grupo.

        Parámetros:
        - grupo (dict): Diccionario que contiene los datos del nuevo grupo a crear (nombre, icono).
        - id_usuario (str): ID del usuario al cual se asociará el nuevo grupo.
        - dispositivos (list): Lista de IDs de dispositivos que se asociarán al grupo.

        Retorna:
        - bool: True si la operación de creación fue exitosa.
        - None: Si ocurre un error durante la creación del grupo.

        Excepciones:
        Exception: Captura y maneja cualquier excepción que ocurra durante la creación del grupo.
        ValueError: Si al menos uno de los dispositivos indicados no existe en la base de datos.
        """
        try:
            print('ID USUARIO en DAO:', id_usuario)
            self.conectar()
            self.agent.start_transaction()
            grupo_data = {
                'nombre': grupo['nombre'],
                'icono': grupo['icono']
            }
            grupo_id = self.agent.create_record('grupos', grupo_data)
            grupo_us_data = {
                'id-usuario': id_usuario,
                'id-grupo': grupo_id
            }
            self.agent.create_record('usuario-grupo', grupo_us_data)

            for dispositivo in dispositivos:
                dispositivo_grupo_data = {
                    'id-dispositivo': dispositivo,
                    'id-grupo': grupo_id
                }
                self.agent.create_record('dispositivo-grupo', dispositivo_grupo_data)
            self.agent.commit_transaction()
            self.desconectar()
            return True
        except Exception as ex:
            self.agent.rollback_transaction()
            if 'fk_iddispositivo_grupo' in str(ex):
                raise ValueError("Al menos uno de los dispositivos indicado no existe")
            print(f"Error al crear el grupo: {ex}")
            raise