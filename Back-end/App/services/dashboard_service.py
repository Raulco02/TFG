import hashlib
from App.model.dashboardDAO import DashboardDAO
from App.model.dashboard import Dashboard
from App.model.seccionDAO import seccionDAO

class dashboardService:
    def obtener_dashboard_por_id_usuario(id):
        dashboard_dao = DashboardDAO()
        dashboard_data = dashboard_dao.obtener_dashboard_por_id_usuario(id)
        print("DASHBOARD DATA:", dashboard_data)
        dashboards=[]
        if dashboard_data is not None:
            for dashboard in dashboard_data:
                dashboards.append({"id": dashboard[0], "nombre": dashboard[1], "icono": dashboard[2]})
            print("Dashboards:", dashboards)
        return dashboards

    def obtener_dashboard_por_id(id, usuario_id):
        dashboard_dao = DashboardDAO()
        dashboard_data = dashboard_dao.obtener_dashboard_por_id(id, usuario_id)
        # seccion_dao = seccionDAO()
        # secciones_data = seccion_dao.obtener_secciones(id) ##¿Al hacer esto rompo el MVC? En caso de que sí, ver si helper
        
        # print("DASHBOARD DATA:", dashboard_data)

        # secciones = []
        # if secciones_data is not None:
        #     for seccion in secciones_data:
        #         secciones.append({"id": seccion[0], "nombre": seccion[1], "icono": seccion[2], "layout": seccion[3], "numFilas": seccion[4]})
        
        if dashboard_data is not None:
            # dashboard = dashboard_data
            # dashboard['secciones'] = secciones
            # print("Dashboard:", dashboard)
            # return dashboard
            return dashboard_data
        else:
            return None
    
    def crear_dashboard_por_usuario_id(nombre, icono, usuario_id):
        print('ID USUARIO en DAO:', usuario_id)
        dashboard_dao = DashboardDAO()
        dashboard = Dashboard(nombre, icono)
        dashboard_data = dashboard_dao.crear_dashboard_por_usuario_id(dashboard, usuario_id)
        return dashboard_data
    
    def editar_dashboard(nombre, icono, dashboard_id):
        dashboard_dao = DashboardDAO()
        dashboard = {
            'id': dashboard_id,
            'nombre': nombre,
            'icono': icono
        }
        dashboard_data = dashboard_dao.editar_dashboard(dashboard)
        return dashboard_data
    
    def eliminar_dashboard(id_dashboard):
        dashboard_dao = DashboardDAO()
        dashboard_data = dashboard_dao.eliminar_dashboard(id_dashboard)
        return dashboard_data
    
    def comprobar_dashboard(id_dashboard, id_usuario):
        dashboard_dao = DashboardDAO()
        dashboard_found = dashboard_dao.comprobar_dashboard(id_dashboard, id_usuario)
        return dashboard_found