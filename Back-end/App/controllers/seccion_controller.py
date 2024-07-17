# Descripción:
# Blueprint que maneja las rutas relacionadas con las secciones. 
# Proporciona rutas para obtener, crear, editar y eliminar secciones.

from http import HTTPStatus
from flask import Blueprint, jsonify, request, session
from App.exceptions.wrongLayout import wrongLayoutException
from App.services.seccion_service import seccionService
from App.services.dashboard_service import dashboardService

seccion_blueprint = Blueprint('seccion', __name__)

@seccion_blueprint.route('/<string:id_dashboard>', methods=['GET']) #Igual debería añadir comprobación de usuario en todos los métodos
def get_seccions(id_dashboard):
    """
    Descripción:
    Obtiene las secciones de un dashboard específico si el usuario tiene sesión válida.

    Parámetros:
    id_dashboard (str): ID del dashboard del cual obtener las secciones.

    Retorna:
    Response: JSON con las secciones del dashboard y código de estado HTTP.

    Excepciones:
    HTTPStatus.UNAUTHORIZED: El usuario no tiene sesión o no está registrado.
    HTTPStatus.NOT_FOUND: No se encontraron secciones en el dashboard.
    HTTPStatus.INTERNAL_SERVER_ERROR: Error interno al obtener las secciones.
    """
    try:
        registrado = session.get("register")
        print('Registrado', registrado)
        print('Session:', session)
        if session is None or not registrado:
            return jsonify({'error': 'El usuario no tiene sesión o no está registrado'}), HTTPStatus.UNAUTHORIZED #raise NoSessionSetException("El usuario no tiene sesión o no está registrado")
        seccion = seccionService.obtener_secciones(id_dashboard)
        if seccion is None:
            return jsonify({'error': 'No se encontraron secciones en este dashboard'}), HTTPStatus.NOT_FOUND
        return jsonify(seccion), HTTPStatus.OK
    except Exception as ex:
        return jsonify({'error': f'Error al obtener el seccion: {ex}'}), HTTPStatus.INTERNAL_SERVER_ERROR
    
@seccion_blueprint.route('/get/<string:id_seccion>', methods=['GET']) 
def get_seccion(id_seccion):
    """
    Descripción:
    Obtiene los detalles de una sección específica si el usuario tiene permisos para acceder a ella.

    Parámetros:
    id_seccion (str): ID de la sección que se desea obtener.

    Retorna:
    Response: JSON con la información de la sección y código de estado HTTP.

    Excepciones:
    HTTPStatus.UNAUTHORIZED: El usuario no tiene permisos para acceder a esta sección.
    HTTPStatus.NOT_FOUND: No se encontró la sección especificada.
    HTTPStatus.INTERNAL_SERVER_ERROR: Error interno al obtener la sección.
    """
    try:
        registrado = session.get("register")
        if session is None or not registrado:
            return jsonify({'error': 'Esta sección no te pertenece'}), HTTPStatus.NOT_FOUND
        existe = seccionService.comprobar_seccion(id_seccion, session.get("usuario_id"))
        if not existe:
            return jsonify({'error': 'El usuario no tiene permisos para acceder a esta seccion'}), HTTPStatus.UNAUTHORIZED
        seccion = seccionService.obtener_seccion(id_seccion)
        if seccion is None:
            return jsonify({'error': 'No se encontró la sección'}), HTTPStatus.NOT_FOUND
        return jsonify(seccion), HTTPStatus.OK
    except Exception as ex:
        return jsonify({'error': f'Error al obtener el seccion: {ex}'}), HTTPStatus.INTERNAL_SERVER_ERROR

@seccion_blueprint.route('/create', methods=['POST'])   
def create_seccion():
    """
    Descripción:
    Crea una nueva sección en un dashboard específico si el usuario tiene permisos para ello.

    Parámetros:
    dashboard_id (str): ID del dashboard donde se creará la sección.
    nombre (str): Nombre de la nueva sección.
    icono (str): Ícono de la nueva sección.
    layout (str): Layout de la nueva sección.

    Retorna:
    Response: JSON con mensaje de éxito y código de estado HTTP.

    Excepciones:
    HTTPStatus.UNAUTHORIZED: El usuario no tiene sesión o no está registrado.
    HTTPStatus.BAD_REQUEST: Error en el layout proporcionado o falta de datos requeridos.
    HTTPStatus.FORBIDDEN: No se pueden crear más de 10 secciones en un dashboard.
    HTTPStatus.INTERNAL_SERVER_ERROR: Error interno al crear la sección.
    """
    try:
        id_dashboard = request.json.get("dashboard_id")
        nombre = request.json.get("nombre")
        icono = request.json.get("icono")
        layout = request.json.get("layout")
        if nombre:
            registrado = session.get("register")
            if session is None or not registrado: #Quiza esto sería forbidden
                return jsonify({'error': 'El usuario no tiene sesión o no está registrado'}), HTTPStatus.UNAUTHORIZED #raise NoSessionSetException("El usuario no tiene sesión o no está registrado")
            id_usuario = session.get("usuario_id")
            dashboard_found = dashboardService.comprobar_dashboard(id_dashboard, id_usuario)
            print('DASHBOARD FOUND:' + str(dashboard_found))
            if not dashboard_found:
                return jsonify({'error': 'El usuario no tiene permisos para acceder a esta seccion'}), HTTPStatus.UNAUTHORIZED
            seccions = seccionService.obtener_secciones(id_dashboard)
            if seccions is not None:
                if(len(seccions) >= 10):
                    return jsonify({'error': 'No se pueden crear más de 10 secciones'}), HTTPStatus.FORBIDDEN
            id_seccion = seccionService.crear_seccion_por_dashboard_id(nombre, icono, layout, id_dashboard)
            return jsonify({'message': 'Seccion creada correctamente', "id": id_seccion}), HTTPStatus.OK
        else:
            return jsonify({'error': 'Se debe especificar un nombre para crear un seccion'}), HTTPStatus.BAD_REQUEST
    except wrongLayoutException as ex:
        return jsonify({'error': f'Error al obtener el seccion: {ex}'}), HTTPStatus.BAD_REQUEST
    except Exception as ex:
        return jsonify({'error': f'Error al obtener el seccion: {ex}'}), HTTPStatus.INTERNAL_SERVER_ERROR
        
@seccion_blueprint.route('/edit', methods=['PUT'])   
def edit_seccion():
    """
    Descripción:
    Edita una sección existente si el usuario tiene permisos sobre el dashboard al cual pertenece.

    Parámetros:
    id (str): ID de la sección que se desea editar.
    dashboard_id (str): ID del nuevo dashboard al que se asociará la sección (opcional).
    nombre (str): Nuevo nombre de la sección (opcional).
    icono (str): Nuevo ícono de la sección (opcional).
    layout (str): Nuevo layout de la sección (opcional).

    Retorna:
    Response: JSON con mensaje de éxito y código de estado HTTP.

    Excepciones:
    HTTPStatus.UNAUTHORIZED: El usuario no tiene sesión o no está registrado.
    HTTPStatus.BAD_REQUEST: Error en el layout proporcionado o falta de datos requeridos.
    HTTPStatus.INTERNAL_SERVER_ERROR: Error interno al editar la sección.
    """
    try:
        id = request.json.get("id")
        #id_dashboard_antiguo = request.json.get("dashboard_id") HAY QUE AÑADIR EL DASHBOARD_ID ANTIGUO PARA PODER CAMBIARLO DE DASHBOARD
        id_dashboard = request.json.get("dashboard_id")
        nombre = request.json.get("nombre")
        icono = request.json.get("icono")
        layout = request.json.get("layout")
        if nombre:
            registrado = session.get("register")
            if session is None or not registrado: #Quiza esto sería forbidden
                return jsonify({'error': 'El usuario no tiene sesión o no está registrado'}), HTTPStatus.UNAUTHORIZED #raise NoSessionSetException("El usuario no tiene sesión o no está registrado")
            id_usuario = session.get("usuario_id")
            dashboard_found = dashboardService.comprobar_dashboard(id_dashboard, id_usuario)
            print('DASHBOARD FOUND:' + str(dashboard_found))
            if not dashboard_found:
                return jsonify({'error': 'El usuario no tiene permisos para acceder a esta seccion'}), HTTPStatus.UNAUTHORIZED
            seccion = seccionService.editar_seccion(id, nombre, icono, layout, id_dashboard)
            # seccions = seccionService.obtener_seccion(id_dashboard)
            # if seccions is not None:
            #     if(len(seccions) >= 10):
            #         return jsonify({'error': 'No se pueden crear más de 10 secciones'}), HTTPStatus.FORBIDDEN
            # seccionService.crear_seccion_por_dashboard_id(nombre, icono, layout, id_dashboard)
            return jsonify({'message': 'Seccion creada correctamente'}), HTTPStatus.OK
        else:
            return jsonify({'error': 'Se debe especificar un nombre para crear un seccion'}), HTTPStatus.BAD_REQUEST
    except wrongLayoutException as ex:
        return jsonify({'error': f'Error al obtener el seccion: {ex}'}), HTTPStatus.BAD_REQUEST
    except Exception as ex:
        return jsonify({'error': f'Error al obtener el seccion: {ex}'}), HTTPStatus.INTERNAL_SERVER_ERROR

@seccion_blueprint.route('/num_filas_up', methods=['PUT'])  
def subir_numero_filas():
    """
    Descripción:
    Incrementa el número de filas de una sección si el usuario tiene permisos sobre el dashboard al cual pertenece la sección.

    Parámetros:
    id (str): ID de la sección a la cual se le incrementará el número de filas.

    Retorna:
    Response: JSON con mensaje de éxito y código de estado HTTP.

    Excepciones:
    HTTPStatus.UNAUTHORIZED: El usuario no tiene sesión o no está registrado.
    HTTPStatus.BAD_REQUEST: No se especificó un ID de sección válido.
    HTTPStatus.INTERNAL_SERVER_ERROR: Error interno al subir el número de filas de la sección.
    """
    try:
        id = request.json.get("id")
        if not id:
            return jsonify({'error': 'Se debe especificar un id de sección para subir el número de filas'}), HTTPStatus.BAD_REQUEST
        registrado = session.get("register")
        if session is None or not registrado: #Quiza esto sería forbidden
            return jsonify({'error': 'El usuario no tiene sesión o no está registrado'}), HTTPStatus.UNAUTHORIZED #raise NoSessionSetException("El usuario no tiene sesión o no está registrado")
        id_usuario = session.get("usuario_id")
        id_dashboard = seccionService.obtener_dashboard_por_seccion(id)
        print('DASHBOARD:', id_dashboard)
        dashboard_found = dashboardService.comprobar_dashboard(id_dashboard, id_usuario)
        print('DASHBOARD FOUND:' + str(dashboard_found))
        if not dashboard_found:
            return jsonify({'error': 'El usuario no tiene permisos para acceder a esta seccion'}), HTTPStatus.UNAUTHORIZED
        seccion = seccionService.subir_numero_filas(id)
        return jsonify({'message': 'Número de filas subido correctamente'}), HTTPStatus.OK

    except Exception as ex:
        return jsonify({'error': f'Error al obtener el seccion: {ex}'}), HTTPStatus.INTERNAL_SERVER_ERROR