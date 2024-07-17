import hashlib
from App.model.dashboardDAO import DashboardDAO
from App.model.dashboard import Dashboard
from App.model.seccionDAO import seccionDAO

class dashboardService:
    """
    Descripción:
    Servicio para gestionar operaciones relacionadas con dashboards.
    """
    def obtener_dashboard_por_id_usuario(id):
        """
        Descripción:
        Obtiene todos los dashboards asociados a un usuario específico.

        Parámetros:
        id (int): El ID del usuario cuyos dashboards se desean obtener.

        Retorna:
        list: Lista de diccionarios con los datos de los dashboards asociados al usuario especificado.

        Excepciones:
        Exception: Captura y maneja cualquier excepción que ocurra al intentar obtener los dashboards.
        """
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
        """
        Descripción:
        Obtiene un dashboard específico por su ID y el ID del usuario propietario.

        Parámetros:
        id (int): El ID del dashboard que se desea obtener.
        usuario_id (int): El ID del usuario propietario del dashboard.

        Retorna:
        dict: Diccionario con los datos del dashboard especificado.

        Excepciones:
        Exception: Captura y maneja cualquier excepción que ocurra al intentar obtener el dashboard.
        """
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
        """
        Descripción:
        Crea un nuevo dashboard para un usuario específico.

        Parámetros:
        nombre (str): El nombre del nuevo dashboard.
        icono (str): El icono del nuevo dashboard.
        usuario_id (int): El ID del usuario para el cual se crea el dashboard.

        Retorna:
        dict: Diccionario con los datos del dashboard creado.

        Excepciones:
        Exception: Captura y maneja cualquier excepción que ocurra al intentar crear el dashboard.
        """
        print('ID USUARIO en DAO:', usuario_id)
        dashboard_dao = DashboardDAO()
        dashboard = Dashboard(nombre, icono)
        dashboard_data = dashboard_dao.crear_dashboard_por_usuario_id(dashboard, usuario_id)
        return dashboard_data
    
    def editar_dashboard(nombre, icono, dashboard_id):
        """
        Descripción:
        Edita un dashboard existente.

        Parámetros:
        nombre (str): El nuevo nombre del dashboard.
        icono (str): El nuevo icono del dashboard.
        dashboard_id (int): El ID del dashboard que se desea editar.

        Retorna:
        dict: Diccionario con los datos del dashboard editado.

        Excepciones:
        Exception: Captura y maneja cualquier excepción que ocurra al intentar editar el dashboard.
        """
        dashboard_dao = DashboardDAO()
        dashboard = {
            'id': dashboard_id,
            'nombre': nombre,
            'icono': icono
        }
        dashboard_data = dashboard_dao.editar_dashboard(dashboard)
        return dashboard_data
    
    def eliminar_dashboard(id_dashboard):
        """
        Descripción:
        Elimina un dashboard por su ID.

        Parámetros:
        id_dashboard (int): El ID del dashboard que se desea eliminar.

        Retorna:
        bool: True si el dashboard fue eliminado exitosamente, False en caso contrario.

        Excepciones:
        Exception: Captura y maneja cualquier excepción que ocurra al intentar eliminar el dashboard.
        """
        dashboard_dao = DashboardDAO()
        dashboard_data = dashboard_dao.eliminar_dashboard(id_dashboard)
        return dashboard_data
    
    def comprobar_dashboard(id_dashboard, id_usuario):
        """
        Descripción:
        Comprueba si un dashboard pertenece a un usuario específico.

        Parámetros:
        id_dashboard (int): El ID del dashboard que se desea comprobar.
        id_usuario (int): El ID del usuario propietario del dashboard.

        Retorna:
        bool: True si el dashboard pertenece al usuario especificado, False en caso contrario.

        Excepciones:
        Exception: Captura y maneja cualquier excepción que ocurra al intentar comprobar el dashboard.
        """
        dashboard_dao = DashboardDAO()
        dashboard_found = dashboard_dao.comprobar_dashboard(id_dashboard, id_usuario)
        return dashboard_found