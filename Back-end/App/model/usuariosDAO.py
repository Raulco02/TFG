# import os
# import configparser
from App.model.agente_mysql import agente_mysql

class UsuariosDAO:
    def __init__(self):
        self.agent = agente_mysql()
        # self.config = configparser.ConfigParser()
        # # Configuración de MongoDB
        # current_dir = os.path.dirname(os.path.abspath(__file__))
        # print("Directorio actual:", current_dir)
        # # Cargar la configuración desde el archivo secrets.cfg
        # # Construir la ruta completa del archivo secrets.cfg
        # self.secrets_path = os.path.join(current_dir, '..', '..\Config', 'secrets.cfg')
        # print("Ruta de secrets.cfg:", self.secrets_path)
        # self.config.read(self.secrets_path)
        # try:
        #     self.mysql_host = self.config['MYSQL']['mysql_host']
        #     self.mysql_username = self.config['MYSQL']['mysql_username']
        #     self.mysql_password = self.config['MYSQL']['mysql_password']
        #     self.mysql_database = self.config['MYSQL']['mysql_database']
        #     self.agent = agente_mysql(self.mysql_host, self.mysql_username, self.mysql_password, self.mysql_database)
        # except KeyError:
        #     print("Error: Configuración 'MYSQL' no encontrada en secrets.cfg")
        #     self.mysql_host = None
        #     self.mysql_username = None
        #     self.mysql_password = None
        #     self.mysql_database = None

    def conectar(self):
        try:
            self.agent.connect()
        except Exception as ex:
            print(f"Error al conectar con la base de datos: {ex}")
            raise

    def desconectar(self):
        try:
            print('Desconectando', self.agent.connection.is_connected())
            self.agent.disconnect()
        except Exception as ex:
            print('Desconectando', self.agent.connection.is_connected())
            print(f"Error al desconectar de la base de datos: {ex}")
            raise

    def crear_usuario(self, usuario):
        # Inserta un nuevo usuario en la base de datos
        try:
            self.conectar()
            self.agent.start_transaction()
            data = {
                'id': usuario.id,
                'nombre': usuario.nombre,
                'correo': usuario.correo,
                'password': usuario.password,
                'rol_id': usuario.rol_id
            }
            self.agent.create_record('usuarios', data)

            #CREAR DASHBOARD PARA EL USUARIO#

            dashboard_data = {
                'nombre': "Nuevo dashboard",
                'icono': "dashboard"
            }
            id_dashboard = self.agent.create_record('dashboards', dashboard_data)
            dash_us_data = {
                'id-usuario': usuario.id,
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


            ##################################
            self.agent.commit_transaction()
            self.desconectar()
            return True
        except Exception as ex:
            self.agent.rollback_transaction()
            print(f"Error al crear el usuario: {ex}")
            raise


    def actualizar_usuario(self, id, nuevo_usuario):
        # Actualiza un usuario existente en la base de datos
        try:
            self.conectar()
            self.agent.start_transaction()
            data = {
                'nombre': nuevo_usuario.nombre,
                'correo': nuevo_usuario.correo,
                'password': nuevo_usuario.password
            }
            condition = f"id = '{id}'"
            self.agent.update_record('usuarios', data, condition)
            self.agent.commit_transaction()
            self.desconectar()
            return True
        except Exception as ex:
            self.agent.rollback_transaction()
            print(f"Error al actualizar el usuario: {ex}")
            raise

    def obtener_usuario_por_id(self, id):
        # Obtiene un usuario por su nombre
        try:
            self.conectar()
            condition = f"id = '{id}'"
            result = self.agent.read_records('usuarios', condition)
            self.desconectar()
            if result:
                return result[0]
            else:
                return None
        except Exception as ex:
            print(f"Error al obtener el usuario por id: {ex}")
            raise

    def obtener_usuario_por_nombre(self, nombre):
        # Obtiene un usuario por su nombre
        try:
            self.conectar()
            condition = f"nombre = '{nombre}'"
            result = self.agent.read_records('usuarios', condition)
            self.desconectar()
            if result:
                return result[0]
            else:
                return None
        except Exception as ex:
            print(f"Error al obtener el usuario por nombre: {ex}")
            raise

    def obtener_usuario_por_correo(self, correo):
        # Obtiene un usuario por su correo
        try:
            self.conectar()
            condition = f"correo = '{correo}'"
            print('Condition:', condition)
            result = self.agent.read_records('usuarios', condition)
            print('result:', result)
            self.desconectar()
            if result is None or result == []:
                return result
            else:
                return result[0]
        except Exception as ex:
            print(f"Error al obtener el usuario por correo: {ex}")
            raise

    def obtener_todos_los_usuarios(self):
        # Obtiene todos los usuarios
        try:
            self.conectar()
            result = self.agent.read_records('usuarios')
            self.desconectar()
            return result
        except Exception as ex:
            print(f"Error al obtener todos los usuarios: {ex}")
            raise

    def eliminar_usuario(self, id):
        # Elimina un usuario por su id
        try:
            self.conectar()
            self.agent.start_transaction()
            condition = f"id = '{id}'"
            self.agent.delete_record('usuarios', condition)
            self.agent.commit_transaction()
            self.desconectar()
            return True
        except Exception as ex:
            self.agent.rollback_transaction()
            print(f"Error al eliminar el usuario: {ex}")
            raise