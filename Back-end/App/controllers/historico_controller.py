# Descripción:
# Blueprint que maneja las rutas relacionadas con los dispositivos en la base de datos mongodb. 
# Proporciona rutas para obtener información de los dispositivos.
from http import HTTPStatus
from flask import Blueprint, jsonify, request
from App.model.mongo_dispositivoDAO import mongo_dispositivoDAO
from datetime import datetime

historico_blueprint = Blueprint('historico', __name__)

@historico_blueprint.route('/<string:id_dispositivo>', methods=['GET'])
def get_sensor(id_dispositivo):
    # Descripción:
    # Obtiene los datos del sensor basado en el ID del dispositivo proporcionado.

    # Parámetros:
    # id_dispositivo (string): ID del dispositivo.

    # Retorna:
    # Response: Respuesta HTTP con los datos del sensor en formato JSON y un código de estado HTTP.

    # Excepciones:
    # HTTPStatus.NOT_FOUND: Dispositivo no encontrado.
    filtro = {"dispositivo": id_dispositivo}
    sensor_dao = mongo_dispositivoDAO()
    sensor_data = sensor_dao.get_sensor_data(filtro)
    if sensor_data:
        return jsonify(sensor_data), HTTPStatus.OK
    else:
        return jsonify({'error': 'Dispositivo not found'}), HTTPStatus.NOT_FOUND

@historico_blueprint.route('/last/<string:id_dispositivo>', methods=['GET'])
def get_sensor_last_value(id_dispositivo):
    # Descripción:
    # Obtiene el último valor del sensor basado en el ID del dispositivo proporcionado.

    # Parámetros:
    # id_dispositivo (string): ID del dispositivo.

    # Retorna:
    # Response: Respuesta HTTP con el último valor del sensor en formato JSON y un código de estado HTTP.

    # Excepciones:
    # HTTPStatus.NOT_FOUND: Dispositivo no encontrado.
    filtro = {"dispositivo": id_dispositivo}
    sensor_dao = mongo_dispositivoDAO()
    sensor_data = sensor_dao.get_sensor_last_value(filtro)
    if sensor_data:
        return jsonify(sensor_data), HTTPStatus.OK
    else:
        return jsonify({'error': 'Dispositivo not found'}), HTTPStatus.NOT_FOUND
    
@historico_blueprint.route('/lista', methods=['GET'])
def get_sensores():
    # Descripción:
    # Obtiene los datos de los sensores basados en los IDs de los dispositivos proporcionados y los filtros opcionales de fecha.

    # Parámetros:
    # Ninguno

    # Retorna:
    # Response: Respuesta HTTP con los datos de los sensores en formato JSON y un código de estado HTTP.

    # Excepciones:
    # HTTPStatus.BAD_REQUEST: No se proporcionaron IDs de sensores.
    # HTTPStatus.NOT_FOUND: Dispositivos no encontrados.
    id_dispositivos = request.args.getlist('id')  # Obtener lista de valores para 'id_dispositivo' de los parámetros de consulta
    atributos = request.args.getlist('atributo')
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    if not id_dispositivos:
        return jsonify({'error': 'No sensor ids provided'}), HTTPStatus.BAD_REQUEST
    if fecha_inicio and fecha_fin:
        fecha_inicio = datetime.strptime(fecha_inicio, '%d-%m-%Y %H:%M:%S')
        fecha_fin = datetime.strptime(fecha_fin, '%d-%m-%Y %H:%M:%S')
        filtros = [{"dispositivo": id_dispositivo, "timestamp": {"$gte": fecha_inicio, "$lte": fecha_fin}} for id_dispositivo in id_dispositivos]
    elif fecha_inicio and not fecha_fin:
        fecha_inicio = datetime.strptime(fecha_inicio, '%d-%m-%Y %H:%M:%S')
        filtros = [{"dispositivo": id_dispositivo, "timestamp": {"$gte": fecha_inicio}} for id_dispositivo in id_dispositivos]
    elif not fecha_inicio and fecha_fin:
        fecha_fin = datetime.strptime(fecha_fin, '%d-%m-%Y %H:%M:%S')
        filtros = [{"dispositivo": id_dispositivo, "timestamp": {"$lte": fecha_fin}} for id_dispositivo in id_dispositivos]
    else:
        filtros = [{"dispositivo": id_dispositivo} for id_dispositivo in id_dispositivos]
    sensor_dao = mongo_dispositivoDAO()
    sensor_data = []

    for filtro in filtros:
        if atributos:
            data = sensor_dao.get_sensor_data(filtro, atributos)
        else:
            data = sensor_dao.get_sensor_data(filtro)
        if data:
            sensor_data.extend(data)

    if sensor_data:
        return jsonify(sensor_data), HTTPStatus.OK
    else:
        return jsonify({'error': 'Dispositivos not found'}), HTTPStatus.NOT_FOUND
    
# @historico_blueprint.route('/lista', methods=['GET'])
# def get_sensores(atributo):
#     id_sensores = request.args.getlist('id')  # Obtener lista de valores para 'id_sensor' de los parámetros de consulta
#     if not id_sensores or not atributo:
#         return jsonify({'error': 'No sensor ids provided'}), HTTPStatus.BAD_REQUEST

#     filtros = [{"sensor": id_sensor} for id_sensor in id_sensores]
#     sensor_dao = mongo_dispositivoDAO()
#     sensor_data = []

#     for filtro in filtros:
#         data = sensor_dao.get_sensor_data(filtro)
#         if data:
#             sensor_data.extend(data)

#     if sensor_data:
#         return jsonify(sensor_data), HTTPStatus.OK
#     else:
#         return jsonify({'error': 'Sensors not found'}), HTTPStatus.NOT_FOUND
