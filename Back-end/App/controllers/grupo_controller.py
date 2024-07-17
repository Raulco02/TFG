# Descripción:
# Blueprint que maneja las rutas relacionadas con los grupos de dispositivos en la aplicación. 
# Proporciona rutas para obtener, crear, editar y eliminar grupos de dispositivos.

from http import HTTPStatus
from flask import Blueprint, jsonify, request, session
from App.services.grupo_service import grupoService

grupo_blueprint = Blueprint('grupo', __name__)

@grupo_blueprint.route('/', methods=['GET'])
def get_user_grupos():
    # Descripción:
    # Obtiene los grupos del usuario actual.

    # Parámetros:
    # Ninguno

    # Retorna:
    # Response: Respuesta HTTP con los grupos en formato JSON y un código de estado HTTP.

    # Excepciones:
    # HTTPStatus.UNAUTHORIZED: El usuario no tiene sesión o no está registrado.
    # HTTPStatus.NOT_FOUND: No se encontraron grupos para el usuario.
    # HTTPStatus.INTERNAL_SERVER_ERROR: Error al obtener los grupos debido a una excepción.
    try:
        registrado = session.get("register")
        print('Registrado', registrado)
        print('Session:', session)
        if session is None or not registrado:
            return jsonify({'error': 'El usuario no tiene sesión o no está registrado'}), HTTPStatus.UNAUTHORIZED 
        grupo = grupoService.obtener_grupos_por_id_usuario(session.get("usuario_id"))
        if grupo is None:
            return jsonify({'error': 'No se encontraron grupos para el usuario'}), HTTPStatus.NOT_FOUND
        return jsonify(grupo), HTTPStatus.OK
    except Exception as ex:
        return jsonify({'error': f'Error al obtener el grupo: {ex}'}), HTTPStatus.INTERNAL_SERVER_ERROR
    
@grupo_blueprint.route('/<int:id_grupo>/dispositivos', methods=['GET'])
def get_dispositivo_grupos(id_grupo):
    # Descripción:
    # Obtiene los dispositivos de un grupo específico.

    # Parámetros:
    # id_grupo (int): ID del grupo.

    # Retorna:
    # Response: Respuesta HTTP con los dispositivos del grupo en formato JSON y un código de estado HTTP.

    # Excepciones:
    # HTTPStatus.UNAUTHORIZED: El usuario no tiene sesión o no está registrado.
    # HTTPStatus.NOT_FOUND: No se encontraron grupos para el usuario.
    # HTTPStatus.INTERNAL_SERVER_ERROR: Error al obtener los dispositivos del grupo debido a una excepción.
    try:
        registrado = session.get("register")
        print('Registrado', registrado)
        print('Session:', session)
        if session is None or not registrado:
            return jsonify({'error': 'El usuario no tiene sesión o no está registrado'}), HTTPStatus.UNAUTHORIZED 
        grupo = grupoService.obtener_dispositivo_por_grupo(id_grupo,session.get("usuario_id"))
        if grupo is None:
            return jsonify({'error': 'No se encontraron grupos para el usuario'}), HTTPStatus.NOT_FOUND
        return jsonify(grupo), HTTPStatus.OK
    except Exception as ex:
        return jsonify({'error': f'Error al obtener el grupo: {ex}'}), HTTPStatus.INTERNAL_SERVER_ERROR
    
@grupo_blueprint.route('/create', methods=['POST'])
def create_user_grupo():
    # Descripción:
    # Crea un nuevo grupo para el usuario actual.

    # Parámetros:
    # Ninguno

    # Retorna:
    # Response: Respuesta HTTP con los datos del grupo creado en formato JSON y un código de estado HTTP.

    # Excepciones:
    # HTTPStatus.UNAUTHORIZED: El usuario no tiene sesión o no está registrado.
    # HTTPStatus.BAD_REQUEST: Los dispositivos deben ser una lista de IDs de dispositivos.
    # HTTPStatus.BAD_REQUEST: Se deben especificar el nombre del grupo y los dispositivos correctamente para crear un grupo.
    # HTTPStatus.INTERNAL_SERVER_ERROR: Error al crear el grupo debido a una excepción.
    try:
        registrado = session.get("register")
        print('Registrado', registrado)
        print('Session:', session)
        if session is None or not registrado:
            return jsonify({'error': 'El usuario no tiene sesión o no está registrado'}), HTTPStatus.UNAUTHORIZED 
        
        grupo_nombre = request.json.get("grupo_nombre")
        grupo_icono = request.json.get("grupo_icono")
        dispositivos = request.json.get("dispositivos")

        if not isinstance(dispositivos, list):
            return jsonify({'error': 'Los dispositivos deben ser una lista de IDs de dispositivos'}), HTTPStatus.BAD_REQUEST
        
        if grupo_nombre and dispositivos:
            data = grupoService.crear_grupo_por_usuario_id(grupo_nombre, grupo_icono, session.get("usuario_id"), dispositivos)
            if data:
                return jsonify(data), HTTPStatus.OK
        else:
            return jsonify({'error': 'Se deben especificar el nombre del grupo y los dispositivos correctamente para crear un grupo'}), HTTPStatus.BAD_REQUEST
    except ValueError as ex:
        return jsonify({'error': f'{ex}'}), HTTPStatus.BAD_REQUEST
    except Exception as ex:
        return jsonify({'error': f'Error al crear el grupo: {ex}'}), HTTPStatus.INTERNAL_SERVER_ERROR