from App.model.agente_mysql import agente_mysql

class grupoDAO:
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

    def obtener_grupos_por_id_usuario(self, id):
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