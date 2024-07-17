# Descripción:
# Blueprint que maneja las rutas relacionadas con los dashboards de usuario en la aplicación. 
# Proporciona rutas para obtener, crear, editar y eliminar dashboards.

from http import HTTPStatus
from flask import Blueprint, jsonify, request, session
from App.services.dashboard_service import dashboardService
from App.services.seccion_service import seccionService

dashboard_blueprint = Blueprint('dashboard', __name__)

@dashboard_blueprint.route('/', methods=['GET'])
def get_user_dashboards():
    # Descripción:
    # Obtiene todos los dashboards del usuario actualmente en sesión.

    # Parámetros:

    # Ninguno
    # Retorna:

    # Response: Respuesta HTTP con los dashboards del usuario en formato JSON y un código de estado HTTP.
    # Excepciones:

    # HTTPStatus.UNAUTHORIZED: El usuario no tiene sesión o no está registrado.
    # HTTPStatus.NOT_FOUND: No se encontraron dashboards para el usuario.
    # HTTPStatus.INTERNAL_SERVER_ERROR: Error al obtener el dashboard debido a una excepción.
    try:
        registrado = session.get("register")
        print('Registrado', registrado)
        print('Session:', session)
        if session is None or not registrado:
            return jsonify({'error': 'El usuario no tiene sesión o no está registrado'}), HTTPStatus.UNAUTHORIZED #raise NoSessionSetException("El usuario no tiene sesión o no está registrado")
        dashboard = dashboardService.obtener_dashboard_por_id_usuario(session.get("usuario_id"))
        if dashboard is None:
            return jsonify({'error': 'No se encontraron dashboards para el usuario'}), HTTPStatus.NOT_FOUND
        return jsonify(dashboard), HTTPStatus.OK
    except Exception as ex:
        return jsonify({'error': f'Error al obtener el dashboard: {ex}'}), HTTPStatus.INTERNAL_SERVER_ERROR
    
@dashboard_blueprint.route('/get/<int:id>', methods=['GET'])
def get_user_dashboard(id):
    # Descripción:
    # Obtiene un dashboard específico del usuario basado en el ID proporcionado.

    # Parámetros:
    # id (int): ID del dashboard a obtener.

    # Retorna:
    # Response: Respuesta HTTP con el dashboard del usuario en formato JSON y un código de estado HTTP.
    
    # Excepciones:
    # HTTPStatus.UNAUTHORIZED: El usuario no tiene sesión o no está registrado.
    # HTTPStatus.NOT_FOUND: No se encontraron dashboards para el usuario.
    # HTTPStatus.INTERNAL_SERVER_ERROR: Error al obtener el dashboard debido a una excepción.
    try:
        registrado = session.get("register")
        if session is None or not registrado:
            return jsonify({'error': 'El usuario no tiene sesión o no está registrado'}), HTTPStatus.UNAUTHORIZED #raise NoSessionSetException("El usuario no tiene sesión o no está registrado")
        dashboard = dashboardService.obtener_dashboard_por_id(id, session.get("usuario_id"))
        if dashboard is None:
            return jsonify({'error': 'No se encontraron dashboards para el usuario'}), HTTPStatus.NOT_FOUND
        dashboard_completo = seccionService.obtener_secciones_usuario([dashboard])
        return jsonify(dashboard_completo), HTTPStatus.OK
    except Exception as ex:
        return jsonify({'error': f'Error al obtener el dashboard: {ex}'}), HTTPStatus.INTERNAL_SERVER_ERROR

@dashboard_blueprint.route('/create', methods=['POST'])   
def create_user_dashboard():
    # Descripción:
    # Crea un nuevo dashboard para el usuario actualmente en sesión.

    # Parámetros:
    # Ninguno

    # Retorna:
    # Response: Respuesta HTTP con un mensaje de éxito y los datos del dashboard creado en formato JSON, y un código de estado HTTP.
    
    # Excepciones:
    # HTTPStatus.UNAUTHORIZED: El usuario no tiene sesión o no está registrado.
    # HTTPStatus.FORBIDDEN: No se pueden crear más de 5 dashboards.
    # HTTPStatus.BAD_REQUEST: No se especificó un nombre para el dashboard.
    # HTTPStatus.INTERNAL_SERVER_ERROR: Error al crear el dashboard debido a una excepción.
    try:
        nombre = request.json.get("nombre")
        icono = request.json.get("icono")
        if nombre:
            registrado = session.get("register")
            if session is None or not registrado: #Quiza esto sería forbidden
                return jsonify({'error': 'El usuario no tiene sesión o no está registrado'}), HTTPStatus.UNAUTHORIZED #raise NoSessionSetException("El usuario no tiene sesión o no está registrado")
            print('ID USUARIO en controller:', session.get("usuario_id"))
            usuario_id = session.get("usuario_id")
            dashboards = dashboardService.obtener_dashboard_por_id_usuario(usuario_id)
            if(len(dashboards) >= 5):
                return jsonify({'error': 'No se pueden crear más de 5 dashboards'}), HTTPStatus.FORBIDDEN
            dashboard_data = dashboardService.crear_dashboard_por_usuario_id(nombre, icono, usuario_id)
            return jsonify({'message': 'Dashboard creado correctamente', "datos":dashboard_data}), HTTPStatus.OK
        else:
            return jsonify({'error': 'Se debe especificar un nombre para crear un dashboard'}), HTTPStatus.BAD_REQUEST
    except Exception as ex:
        return jsonify({'error': f'Error al obtener el dashboard: {ex}'}), HTTPStatus.INTERNAL_SERVER_ERROR
    
@dashboard_blueprint.route('/edit', methods=['PUT'])   
def edit_user_dashboard():
    # Descripción:
    # Edita un dashboard existente del usuario actualmente en sesión.

    # Parámetros:
    # Ninguno
    
    # Retorna:
    # Response: Respuesta HTTP con un mensaje de éxito en formato JSON y un código de estado HTTP.

    # Excepciones:
    # HTTPStatus.UNAUTHORIZED: El usuario no tiene sesión o no está registrado.
    # HTTPStatus.NOT_FOUND: El usuario no es dueño de este dashboard.
    # HTTPStatus.BAD_REQUEST: No se especificó un nombre para el dashboard.
    # HTTPStatus.INTERNAL_SERVER_ERROR: Error al editar el dashboard debido a una excepción.
    try:
        id = request.json.get("id")
        nombre = request.json.get("nombre")
        icono = request.json.get("icono")
        if nombre:
            registrado = session.get("register")
            if session is None or not registrado: #Quiza esto sería forbidden
                return jsonify({'error': 'El usuario no tiene sesión o no está registrado'}), HTTPStatus.UNAUTHORIZED #raise NoSessionSetException("El usuario no tiene sesión o no está registrado")
            print('ID USUARIO en controller:', session.get("usuario_id"))
            usuario_id = session.get("usuario_id")
            dashboards = dashboardService.obtener_dashboard_por_id_usuario(usuario_id)
            existing_dashboard = False
            for dashboard in dashboards:
                if dashboard['id'] == id:
                    existing_dashboard = True
                    dashboardService.editar_dashboard(nombre, icono, id)
                    return jsonify({'message': 'Dashboard editado correctamente'}), HTTPStatus.OK
            if not existing_dashboard:
                return jsonify({'error': 'El usuario no es dueño de este dashboard'}), HTTPStatus.NOT_FOUND
        else:
            return jsonify({'error': 'Se debe especificar un nombre para crear un dashboard'}), HTTPStatus.BAD_REQUEST
    except Exception as ex:
        return jsonify({'error': f'Error al obtener el dashboard: {ex}'}), HTTPStatus.INTERNAL_SERVER_ERROR
    
@dashboard_blueprint.route('/delete/<int:id>', methods=['DELETE'])
def delete_user_dashboard(id):
    # Descripción:
    # Elimina un dashboard específico del usuario basado en el ID proporcionado.

    # Parámetros:
    # id (int): ID del dashboard a eliminar.

    # Retorna:
    # Response: Respuesta HTTP con un mensaje de éxito en formato JSON y un código de estado HTTP.

    # Excepciones:
    # HTTPStatus.UNAUTHORIZED: El usuario no tiene sesión o no está registrado.
    # HTTPStatus.NOT_FOUND: El usuario no es dueño de este dashboard.
    # HTTPStatus.INTERNAL_SERVER_ERROR: Error al eliminar el dashboard debido a una excepción.
    try:
        registrado = session.get("register")
        if session is None or not registrado: #Quiza esto sería forbidden
            return jsonify({'error': 'El usuario no tiene sesión o no está registrado'}), HTTPStatus.UNAUTHORIZED #raise NoSessionSetException("El usuario no tiene sesión o no está registrado")
        print('ID USUARIO en controller:', session.get("usuario_id"))
        usuario_id = session.get("usuario_id")
        dashboards = dashboardService.obtener_dashboard_por_id_usuario(usuario_id)
        existing_dashboard = False
        for dashboard in dashboards:
            print('DASHBOARD:', dashboard)
            print('ID:', id, type(id), dashboard['id'], type(dashboard['id']))
            if dashboard['id'] == id:
                existing_dashboard = True
                dashboardService.eliminar_dashboard(id)
                return jsonify({'message': 'Dashboard eliminado correctamente'}), HTTPStatus.OK
        if not existing_dashboard:
            return jsonify({'error': 'El usuario no es dueño de este dashboard'}), HTTPStatus.NOT_FOUND
    except Exception as ex:
        return jsonify({'error': f'Error al obtener el dashboard: {ex}'}), HTTPStatus.INTERNAL_SERVER_ERROR