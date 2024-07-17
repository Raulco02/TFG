from App.model.agente_mysql import agente_mysql

class DashboardDAO:
    """
    Descripción:
    Clase que gestiona las operaciones de acceso a datos (DAO) relacionadas con los dashboards
    y su interacción con la base de datos MySQL.
    """
    def __init__(self):
        """
        Descripción:
        Inicializa una instancia de `DashboardDAO`, creando una conexión con la base de datos MySQL
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
            raise

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
            raise

    def obtener_dashboard_por_id_usuario(self, id):
        """
        Descripción:
        Obtiene los dashboards asociados a un usuario específico mediante su ID consultando la base de datos.

        Parámetros:
        - id (str): ID del usuario para el cual se obtendrán los dashboards.

        Retorna:
        - list: Lista de dashboards asociados al usuario.
        - None: Si no se encontraron dashboards para el usuario.

        Excepciones:
        Exception: Captura y maneja cualquier excepción que ocurra durante la consulta a la base de datos.
        """
        try:
            self.conectar()
            condition = f"`id-usuario` = '{id}'"
            ids = self.agent.read_records('usuario-dashboard', condition)
            dashboards = []
            if ids:
                for id in ids:
                    dash_id = id[1]
                    condition = f"id = '{dash_id}'"
                    result = self.agent.read_records('dashboards', condition)
                    print('Records en dao:', result)
                    if result:
                        dashboards.append(result[0])
            else:
                result = None

            self.desconectar()
            if dashboards:
                return dashboards
            else:
                return None
        except Exception as ex:
            print(f"Error al obtener el dashboard por id de usuario: {ex}")
            raise

    def obtener_dashboard_por_id(self, id, usuario_id):
        """
        Descripción:
        Obtiene un dashboard específico por su ID y verifica si el usuario tiene acceso a dicho dashboard.

        Parámetros:
        - id (str): ID del dashboard que se desea obtener.
        - usuario_id (str): ID del usuario que desea acceder al dashboard.

        Retorna:
        - dict: Información del dashboard si el usuario tiene acceso.
        - None: Si el dashboard no existe o el usuario no tiene acceso.

        Excepciones:
        Exception: Captura y maneja cualquier excepción que ocurra durante la consulta a la base de datos.
        """
        try:
            self.conectar()
            condition = f"id = '{id}'"
            result = self.agent.read_records('dashboards', condition)
            print('Records en dao:', result)
            if result:
                dash_id = result[0][0]
                dashboard = { "id": dash_id, "nombre": result[0][1], "icono": result[0][2]}
                condition = f"`id-dashboard` = '{dash_id}' AND `id-usuario` = '{usuario_id}'"
                result = self.agent.read_records('usuario-dashboard', condition)
                if result:
                    self.desconectar()
                    return dashboard
            self.desconectar()
            return None
        except Exception as ex:
            print(f"Error al obtener el dashboard por id de usuario: {ex}")
            raise
        
    def crear_dashboard_por_usuario_id(self, dashboard, id_usuario):
        """
        Descripción:
        Crea un nuevo dashboard y lo asocia al usuario especificado por su ID en la base de datos.

        Parámetros:
        - dashboard (objeto): Objeto que contiene los datos del nuevo dashboard.
        - id_usuario (str): ID del usuario al cual se asociará el nuevo dashboard.

        Retorna:
        - dict: Objeto que contiene los IDs del dashboard creado y su sección asociada.
        - None: Si ocurre un error durante la creación del dashboard.

        Excepciones:
        Exception: Captura y maneja cualquier excepción que ocurra durante la creación del dashboard.
        """
        try:
            print('ID USUARIO en DAO:', id_usuario)
            self.conectar()
            self.agent.start_transaction()
            dashboard_data = {
                'nombre': dashboard.nombre,
                'icono': dashboard.icono
            }
            id_dashboard = self.agent.create_record('dashboards', dashboard_data)
            dash_us_data = {
                'id-usuario': id_usuario,
                'id-dashboard': id_dashboard
            }           
            self.agent.create_record('usuario-dashboard', dash_us_data)

            seccion_data = {
                'nombre': "Nueva sección",
                'icono': "default",
                'layout': "g"
            }
            id_seccion = self.agent.create_record('secciones', seccion_data)
            dash_sec_data = {
                'id-dashboard': id_dashboard,
                'id-seccion': id_seccion
            }
            self.agent.create_record('dashboard-seccion', dash_sec_data)
            self.agent.commit_transaction()
            self.desconectar()
            objeto_dashboard = {"id_dashboard": id_dashboard, "id_seccion": id_seccion}
            return objeto_dashboard
        except Exception as ex:
            self.agent.rollback_transaction()
            print(f"Error al crear el dashboard: {ex}")
            raise
        
    def comprobar_dashboard(self, id_dashboard, id_usuario):
        """
        Descripción:
        Verifica si el usuario tiene acceso a un dashboard específico.

        Parámetros:
        - id_dashboard (str): ID del dashboard que se desea verificar.
        - id_usuario (str): ID del usuario que se desea verificar.

        Retorna:
        - bool: True si el usuario tiene acceso al dashboard, False en caso contrario.

        Excepciones:
        Exception: Captura y maneja cualquier excepción que ocurra durante la consulta a la base de datos.
        """
        try:
            self.conectar()
            condition = f"`id-usuario` = '{id_usuario}' AND `id-dashboard` = '{id_dashboard}'"
            result = self.agent.read_records('usuario-dashboard', condition)
            self.desconectar()
            print('Records en dao:', result)
            if result:
                return True
            return False
        except Exception as ex:
            print(f"Error al comprobar el dashboard: {ex}")
            raise
    
    def editar_dashboard(self, dashboard):
        """
        Descripción:
        Actualiza los datos de un dashboard existente en la base de datos.

        Parámetros:
        - dashboard (dict): Diccionario que contiene los nuevos datos del dashboard a actualizar.

        Retorna:
        - bool: True si la operación de actualización fue exitosa, False en caso contrario.

        Excepciones:
        Exception: Captura y maneja cualquier excepción que ocurra durante la actualización del dashboard.
        """
        try:
            self.conectar()
            self.agent.start_transaction()
            self.agent.update_record('dashboards', dashboard, f"id = '{dashboard['id']}'")
            self.agent.commit_transaction()
            self.desconectar()
            return True
        except Exception as ex:
            self.agent.rollback_transaction()
            print(f"Error al crear el dashboard: {ex}")
            raise
        
    def eliminar_dashboard(self, id_dashboard):
        """
        Descripción:
        Elimina un dashboard específico de la base de datos.

        Parámetros:
        - id_dashboard (str): ID del dashboard que se desea eliminar.

        Retorna:
        - bool: True si la operación de eliminación fue exitosa, False en caso contrario.

        Excepciones:
        Exception: Captura y maneja cualquier excepción que ocurra durante la eliminación del dashboard.
        """
        try:
            self.conectar()
            self.agent.start_transaction()
            self.agent.delete_record('dashboards', f"id = '{id_dashboard}'")
            self.agent.commit_transaction()
            self.desconectar()
            return True
        except Exception as ex:
            self.agent.rollback_transaction()
            print(f"Error al eliminar el dashboard: {ex}")
            raise
        
    

        