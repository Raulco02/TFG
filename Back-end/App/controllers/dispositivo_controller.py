from http import HTTPStatus
from flask import Blueprint, jsonify, request, session
from App.services.mysql_dispositivo_service import mysql_dispositivoService 
from App.exceptions.duplicate import duplicateDispositivoException

dispositivo_blueprint = Blueprint('dispositivo', __name__)

@dispositivo_blueprint.route('/getAll', methods=['GET'])
def get_dispositivos():
    try:
        data = mysql_dispositivoService().obtener_dispositivos()
        if data:
            return jsonify(data), HTTPStatus.OK
        else:
            return jsonify({'error': 'Dispositivo not found'}), HTTPStatus.NOT_FOUND
    except Exception as ex:
        print(f'Error al obtener los dispositivos: {ex}')
        return jsonify({'error': f'Error al obtener los dispositivos'}), HTTPStatus.INTERNAL_SERVER_ERROR
    
@dispositivo_blueprint.route('/getAllTermostato', methods=['GET'])
def get_dispositivos_temperatura():
    try:
        data = mysql_dispositivoService().obtener_dispositivos_temperatura()
        if data:
            return jsonify(data), HTTPStatus.OK
        else:
            return jsonify({'error': 'Dispositivo not found'}), HTTPStatus.NOT_FOUND
    except Exception as ex:
        print(f'Error al obtener los dispositivos: {ex}')
        return jsonify({'error': f'Error al obtener los dispositivos'}), HTTPStatus.INTERNAL_SERVER_ERROR
    
@dispositivo_blueprint.route('/getAll/<string:id>', methods=['GET'])
def get_dispositivos_por_atributo(id):
    try:
        if not id or id == '':
            return jsonify({'error': 'No se especificó un id de atributo'}), HTTPStatus.BAD_REQUEST
        data = mysql_dispositivoService().obtener_dispositivos_por_atributo(id)
        if data:
            return jsonify(data), HTTPStatus.OK
        else:
            return jsonify({'error': 'Dispositivo not found'}), HTTPStatus.NOT_FOUND
    except Exception as ex:
        print(f'Error al obtener los dispositivos: {ex}')
        return jsonify({'error': f'Error al obtener los dispositivos'}), HTTPStatus.INTERNAL_SERVER_ERROR
    
@dispositivo_blueprint.route('/get/<string:id>', methods=['GET']) ##Tengo que validar el valor del id
def get_dispositivo(id):
    try:
        data = mysql_dispositivoService().obtener_dispositivo_por_id(id)
        if data:
            return jsonify(data), HTTPStatus.OK
        else:
            return jsonify({'error': 'Dispositivo not found'}), HTTPStatus.NOT_FOUND
    except Exception as ex:
        print(f'Error al obtener el dispositivo: {ex}')
        return jsonify({'error': f'Error al obtener el dispositivo: {ex}'}), HTTPStatus.INTERNAL_SERVER_ERROR
    
@dispositivo_blueprint.route('/create', methods=['POST'])
def create_dispositivo():
    try:
        registrado = session.get("register")
        print('Registrado', registrado)
        print('Session:', session)
        if session is None or not registrado:
            return jsonify({'error': 'El usuario no tiene sesión o no está registrado'}), HTTPStatus.UNAUTHORIZED #raise NoSessionSetException("El usuario no tiene sesión o no no está registrado")
        rol = session.get("rol")
        if rol != 1:
            return jsonify({'error': 'El usuario no tiene permisos para crear dispositivos'}), HTTPStatus.UNAUTHORIZED

        id = request.json.get("id")
        nombre = request.json.get("nombre")
        topic = request.json.get("topic")
        nombre_integracion = request.json.get("nombre_integracion")
        ubicacion = request.json.get("ubicacion")
        topics_actuacion = request.json.get("topics_actuacion")
        plantillas_actuacion = request.json.get("plantillas_actuacion")

        if id and nombre and topic and nombre_integracion and ubicacion:
            data = mysql_dispositivoService().crear_dispositivo_http(id, nombre, topic, nombre_integracion, ubicacion, topics_actuacion, plantillas_actuacion)
            print('ALGO')
            if data:
                return jsonify(data), HTTPStatus.OK
        else:
            return jsonify({'error': 'Se deben especificar id, nombre, topic y nombre de integracion correctamente para crear un dispositivo'}), HTTPStatus.BAD_REQUEST
    except duplicateDispositivoException as ex:
        return jsonify({'error': f'{ex}'}), HTTPStatus.BAD_REQUEST
    except ValueError as ex:
        return jsonify({'error': f'{ex}'}), HTTPStatus.BAD_REQUEST
    except Exception as ex:
        return jsonify({'error': f'Error al crear el dispositivo: {ex}'}), HTTPStatus.INTERNAL_SERVER_ERROR
    
@dispositivo_blueprint.route('/edit', methods=['PUT'])
def edit_dispositivo():
    try:
        registrado = session.get("register")
        print('Registrado', registrado)
        print('Session:', session)
        if session is None or not registrado:
            return jsonify({'error': 'El usuario no tiene sesión o no está registrado'}), HTTPStatus.UNAUTHORIZED #raise NoSessionSetException("El usuario no tiene sesión o no no está registrado")
        rol = session.get("rol")
        if rol != 1:
            return jsonify({'error': 'El usuario no tiene permisos para editar dispositivos'}), HTTPStatus.UNAUTHORIZED

        prev_id = request.json.get("prev_id")
        id = request.json.get("id")
        nombre = request.json.get("nombre")
        topic = request.json.get("topic")
        nombre_integracion = request.json.get("nombre_integracion")
        ubicacion = request.json.get("ubicacion")
        topics_actuacion = request.json.get("topics_actuacion")
        plantillas_actuacion = request.json.get("plantillas_actuacion")

        if prev_id and id and nombre and topic and nombre_integracion and ubicacion:
            data = mysql_dispositivoService().edit_dispositivo_http(prev_id, id, nombre, topic, nombre_integracion, ubicacion, topics_actuacion, plantillas_actuacion)
            print('ALGO')
            if data:
                return jsonify(data), HTTPStatus.OK
        else:
            return jsonify({'error': 'Se deben especificar prev_id, id, nombre, topic y nombre de integracion correctamente para crear un dispositivo'}), HTTPStatus.BAD_REQUEST
    except duplicateDispositivoException as ex:
        return jsonify({'error': f'{ex}'}), HTTPStatus.BAD_REQUEST
    except ValueError as ex:
        return jsonify({'error': f'{ex}'}), HTTPStatus.BAD_REQUEST
    except Exception as ex:
        return jsonify({'error': f'Error al editar el dispositivo: {ex}'}), HTTPStatus.INTERNAL_SERVER_ERROR
    
@dispositivo_blueprint.route('/delete/<string:id>', methods=['DELETE'])
def delete_dispositivo(id):
    try:
        registrado = session.get("register")
        print('Registrado', registrado)
        print('Session:', session)
        if session is None or not registrado:
            return jsonify({'error': 'El usuario no tiene sesión o no está registrado'}), HTTPStatus.UNAUTHORIZED #raise NoSessionSetException("El usuario no tiene sesión o no no está registrado")
        rol = session.get("rol")
        if rol != 1:
            return jsonify({'error': 'El usuario no tiene permisos para eliminar dispositivos'}), HTTPStatus.UNAUTHORIZED

        if not id:
            return jsonify({'error': 'No se especificó un id de dispositivo'}), HTTPStatus.BAD_REQUEST
        
        data = mysql_dispositivoService().eliminar_dispositivo(id)
        if data:
            return jsonify(data), HTTPStatus.OK
        else:
            return jsonify({'error': 'Dispositivo not found'}), HTTPStatus.NOT_FOUND
    except Exception as ex:
        return jsonify({'error': f'Error al eliminar el dispositivo: {ex}'}), HTTPStatus.INTERNAL_SERVER_ERROR

@dispositivo_blueprint.route('/getAllAtributos', methods=['GET'])  
def get_all_atributos():
    data = mysql_dispositivoService().obtener_atributos()
    if data:
        return jsonify(data), HTTPStatus.OK
    else:
        return jsonify({'error': 'Atributos not found'}), HTTPStatus.NOT_FOUND

