from App.model.agente_mysql import agente_mysql

class seccionDAO:
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

    def obtener_seccion(self, id_seccion):
        try:
            self.conectar()
            condition = f"id = '{id_seccion}'"
            result = self.agent.read_records('secciones', condition)
            if result:
                return result[0]
            return None
        except Exception as ex:
            print(f"Error al obtener la seccion: {ex}")
            raise

    def obtener_secciones(self, id_dashboard):
        try:
            self.conectar()
            condition = f"`id-dashboard` = '{id_dashboard}'"
            ids = self.agent.read_records('dashboard-seccion', condition)
            seccions = []
            if ids:
                for id in ids:
                    seccion_id = id[1]
                    condition = f"id = '{seccion_id}'"
                    result = self.agent.read_records('secciones', condition)
                    # condition_tarjetas = f"`id-seccion` = '{seccion_id}'"
                    # tarjetas = self.agent.read_records('tarjetas', condition_tarjetas) 
                    # print('Records en dao:', result)
                    if result:
                    #     seccion = list(result[0])
                    #     seccion.append(tarjetas)
                    #     print('SEECCIOON:', seccion)
                    #     seccions.append(seccion)
                        seccions.append(result[0])
            else:
                result = None

            self.desconectar()
            if seccions:
                return seccions
            else:
                return None
        except Exception as ex:
            print(f"Error al obtener la seccion por id de usuario: {ex}")
            return None
        
    def comprobar_seccion(self, id_seccion, id_usuario):
        try:
            self.conectar()
            condition = f"`id-seccion` = '{id_seccion}'"
            result = self.agent.read_records('dashboard-seccion', condition)
            if result:
                condition = f"`id-dashboard` = '{result[0][0]}'"
                result = self.agent.read_records(f"usuario-dashboard", condition)
                if result:
                    if result[0][0] == id_usuario:
                        return True
            return False
        except Exception as ex:
            print(f"Error al comprobar la seccion: {ex}")
            return False
        
    def crear_seccion_por_usuario_id(self, seccion, id_dashboard):
        try:
            print('ID DASHBOARD en DAO:', id_dashboard)
            self.conectar()
            self.agent.start_transaction()
            seccion_data = {
                'nombre': seccion.nombre,
                'icono': seccion.icono,
                'layout': seccion.layout
            }
            id_seccion = self.agent.create_record('secciones', seccion_data)
            dash_sec_data = {
                'id-dashboard': id_dashboard,
                'id-seccion': id_seccion
            }
            self.agent.create_record('dashboard-seccion', dash_sec_data)
            self.agent.commit_transaction()
            self.desconectar()
            return id_seccion
        except Exception as ex:
            self.agent.rollback_transaction()
            print(f"Error al crear el seccion: {ex}")
            return False
    
    def editar_seccion(self, id, nombre, icono, layout, dashboard_id):
        try:
            self.conectar()
            self.agent.start_transaction()
            condition = f"id = '{id}'"
            seccion_data = {
                'nombre': nombre,
                'icono': icono,
                'layout': layout
            }
            self.agent.update_record('secciones', seccion_data, condition)
            self.agent.commit_transaction()
            self.desconectar()
            return True
        except Exception as ex:
            self.agent.rollback_transaction()
            print(f"Error al editar la seccion: {ex}")
            return False
        
    def obtener_dashboard_por_seccion(self, id):
        try:
            self.conectar()
            condition = f"`id-seccion` = '{id}'"
            result = self.agent.read_records('dashboard-seccion', condition)
            print('Records en dao:', result)
            if result:
                return result[0]
            return None
        except Exception as ex:
            print(f"Error al obtener el dashboard por seccion: {ex}")
            raise
    
    def subir_numero_filas(self, id_seccion):
        try:
            self.conectar()
            self.agent.start_transaction()
            numFilas = self.agent.read_records('secciones', f"id = '{id_seccion}'")[0][4]
            print('Numero de filas actual:', numFilas)
            condition = f"id = '{id_seccion}'"
            seccion_data = {
                'numFilas': numFilas + 1
            }
            self.agent.update_record('secciones', seccion_data, condition)
            self.agent.commit_transaction()
            self.desconectar()
            return True
        except Exception as ex:
            self.agent.rollback_transaction()
            print(f"Error al subir el numero de filas: {ex}")
            raise
        