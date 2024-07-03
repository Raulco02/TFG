from http import HTTPStatus
from flask import Blueprint, jsonify, request, session
from App.exceptions.wrongLayout import wrongLayoutException
from App.services.seccion_service import seccionService
from App.services.dashboard_service import dashboardService

seccion_blueprint = Blueprint('seccion', __name__)

@seccion_blueprint.route('/<string:id_dashboard>', methods=['GET']) #Igual debería añadir comprobación de usuario en todos los métodos
def get_seccions(id_dashboard):
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