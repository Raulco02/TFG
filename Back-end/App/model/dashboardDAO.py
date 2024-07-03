from App.model.agente_mysql import agente_mysql

class DashboardDAO:
    def __init__(self):
        self.agent = agente_mysql()

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

    def obtener_dashboard_por_id_usuario(self, id):
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
        
    

        