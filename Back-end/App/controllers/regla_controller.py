# Descripción:
# Blueprint que maneja las rutas relacionadas con las reglas y las alertas. 
# Proporciona rutas para obtener, crear, editar y eliminar reglas y alertas.

from http import HTTPStatus
from flask import Blueprint, jsonify, request, session
from App.services.regla_service import reglaService
from App.services.mysql_dispositivo_service import mysql_dispositivoService

regla_blueprint = Blueprint('regla', __name__)

########HAY QUE HACER ALGO PARA INICIALIZAR LA BASE DE DATOS CON LAS ACCIONES NECESARIAS (1:SET, 2:ALERT)#########

def comprobar_criterios(criterios):
    """
    Descripción:
    Comprueba la validez de una lista de criterios. Al menos uno de los criterios debe ser un disparador.

    Parámetros:
    - criterios: Lista de diccionarios que representan criterios.

    Retorna:
    Response: True si los criterios son válidos, False en caso contrario.

    Excepciones:
    HTTPStatus.BAD_REQUEST: Los criterios de la regla no son válidos.
    """
    if not isinstance(criterios, list):
        return False

    required_keys = {'tipo', 'dispositivo_id', 'atributo_id', 'valor', 'comparador'}
    trigger_found = False

    for criterio in criterios:
        if not isinstance(criterio, dict):
            return False

        # Verifica que el diccionario contiene exactamente las claves requeridas
        if not required_keys == set(criterio.keys()):
            return False

        if criterio['tipo'] not in {"d", "c"}:
            return False

        if criterio['tipo'] == "d":
            trigger_found = True

    return trigger_found

def comprobar_acciones(acciones, isAdmin):
    """
    Descripción:
    Comprueba la validez de una lista de acciones.

    Parámetros:
    - acciones: Lista de diccionarios que representan acciones.
    - isAdmin: True si el usuario es administrador, False en caso contrario.

    Retorna:
    Response: True si las acciones son válidas, False en caso contrario.

    Excepciones:
    HTTPStatus.BAD_REQUEST: Las acciones de la regla no son válidas.
    HTTPStatus.FORBIDDEN: Solo los administradores pueden crear reglas con acciones de tipo set.
    """
    if not isinstance(acciones, list):
        raise ValueError('Las acciones de la regla deben ser una lista de diccionarios')

    required_keys_reglas = {'atributo_id', 'dispositivo_id', 'accion_id', 'valor_accion'}
    # required_keys_set = required_keys.union({'valor'}) # Para lo del valor en caso de set

    for accion in acciones:
        if not isinstance(accion, dict):
            raise ValueError('Las acciones de la regla deben ser un diccionario')

        # Verifica que el diccionario contiene exactamente las claves requeridas
        if not (required_keys_reglas == set(accion.keys())): #or required_keys_set == set(accion.keys())): Para lo del valor en caso de set
            raise ValueError('Las acciones de la regla deben contener los campos requeridos')

        
        # Controlar que si 'accion' no es 'alert', el usuario sea admin
        if accion['accion_id'] != 2 and not isAdmin:
            raise ValueError('Solo los administradores pueden crear reglas con acciones de tipo set')
        
        if accion['atributo_id'] is not None:
            tipo_atributo = mysql_dispositivoService().obtener_tipo_atributo(accion['atributo_id'])
            if tipo_atributo.lower() != 'termostato':
                raise ValueError('Solo se pueden crear reglas de tipo set a dispositivos que sean termostato')

        # Controlar que si 'accion' es 'set', haya un valor válido
        # if accion['accion'] == 'set' and 'valor' not in accion:
        #     return False

    return True


@regla_blueprint.route('/getAll', methods=['GET'])
def get_user_reglas():
    """
    Descripción:
    Obtiene todas las reglas asociadas al usuario actual.

    Parámetros:
    Ninguno

    Retorna:
    Response: Respuesta HTTP con las reglas en formato JSON y un código de estado HTTP.

    Excepciones:
    HTTPStatus.UNAUTHORIZED: El usuario no tiene sesión o no está registrado.
    HTTPStatus.NOT_FOUND: No se encontraron reglas para el usuario.
    HTTPStatus.INTERNAL_SERVER_ERROR: Error al obtener las reglas debido a una excepción.
    """
    try:
        registrado = session.get("register")
        print('Registrado', registrado)
        print('Session:', session)
        if session is None or not registrado:
            return jsonify({'error': 'El usuario no tiene sesión o no está registrado'}), HTTPStatus.UNAUTHORIZED 
        reglas = reglaService.obtener_reglas_por_id_usuario(session.get("usuario_id"))
        if reglas is None:
            return jsonify({'error': 'No se encontraron reglas para el usuario'}), HTTPStatus.NOT_FOUND
        return jsonify(reglas), HTTPStatus.OK
    except Exception as ex:
        return jsonify({'error': f'Error al obtener el regla: {ex}'}), HTTPStatus.INTERNAL_SERVER_ERROR
    
@regla_blueprint.route('/getAllAlertas', methods=['GET'])
def get_user_alertas():
    """
    Descripción:
    Obtiene todas las alertas asociadas al usuario actual.

    Parámetros:
    Ninguno

    Retorna:
    Response: Respuesta HTTP con las alertas en formato JSON y un código de estado HTTP.

    Excepciones:
    HTTPStatus.UNAUTHORIZED: El usuario no tiene sesión o no está registrado.
    HTTPStatus.NOT_FOUND: No se encontraron alertas para el usuario.
    HTTPStatus.INTERNAL_SERVER_ERROR: Error al obtener las alertas debido a una excepción.
    """
    try:
        registrado = session.get("register")
        print('Registrado', registrado)
        print('Session:', session)
        if session is None or not registrado:
            return jsonify({'error': 'El usuario no tiene sesión o no está registrado'}), HTTPStatus.UNAUTHORIZED 
        reglas = reglaService.obtener_alertas_por_id_usuario(session.get("usuario_id"))
        if reglas is None:
            return jsonify({'error': 'No se encontraron reglas para el usuario'}), HTTPStatus.NOT_FOUND
        return jsonify(reglas), HTTPStatus.OK
    except Exception as ex:
        return jsonify({'error': f'Error al obtener el regla: {ex}'}), HTTPStatus.INTERNAL_SERVER_ERROR
    
@regla_blueprint.route('/<int:id_regla>/dispositivos', methods=['GET'])
def get_dispositivo_reglas(id_regla):
    """
    Descripción:
    Obtiene los dispositivos asociados a una regla específica.

    Parámetros:
    - id_regla: ID de la regla para la cual se quieren obtener los dispositivos.

    Retorna:
    Response: Respuesta HTTP con los dispositivos en formato JSON y un código de estado HTTP.

    Excepciones:
    HTTPStatus.UNAUTHORIZED: El usuario no tiene sesión o no está registrado.
    HTTPStatus.NOT_FOUND: No se encontró la regla o no tiene dispositivos asociados.
    HTTPStatus.INTERNAL_SERVER_ERROR: Error al obtener los dispositivos debido a una excepción.
    """
    try:
        registrado = session.get("register")
        print('Registrado', registrado)
        print('Session:', session)
        if session is None or not registrado:
            return jsonify({'error': 'El usuario no tiene sesión o no está registrado'}), HTTPStatus.UNAUTHORIZED 
        regla = reglaService.obtener_dispositivo_por_regla(id_regla,session.get("usuario_id"))
        if regla is None:
            return jsonify({'error': 'No se encontraron reglas para el usuario'}), HTTPStatus.NOT_FOUND
        return jsonify(regla), HTTPStatus.OK
    except Exception as ex:
        return jsonify({'error': f'Error al obtener el regla: {ex}'}), HTTPStatus.INTERNAL_SERVER_ERROR
    
# @regla_blueprint.route('/getAllReglas', methods=['GET'])
# def get_reglas():
#     try:
#         reglas = reglaService.obtener_reglas()
#         if reglas is None:
#             return jsonify({'error': 'No se encontraron reglas'}), HTTPStatus.NOT_FOUND
#         return jsonify(reglas), HTTPStatus.OK
#     except Exception as ex:
#         return jsonify({'error': f'Error al obtener el regla: {ex}'}), HTTPStatus.INTERNAL_SERVER_ERROR
    
@regla_blueprint.route('/create', methods=['POST'])
### Para el tema de vigilar que se cumplan las reglas y ejecutar las acciones, revisar conversación Motor de reglas MySQL ChatGPT 29/05 ###
def create_user_regla():
    """
    Descripción:
    Crea una nueva regla para el usuario actual con los criterios y acciones proporcionados.

    Parámetros:
    Ninguno directamente. Se espera un JSON en el cuerpo de la solicitud con los siguientes campos:
    - nombre: Nombre de la regla.
    - criterios: Lista de criterios para la regla.
    - acciones: Lista de acciones para la regla.

    Retorna:
    Response: Respuesta HTTP con un mensaje de éxito en formato JSON y un código de estado HTTP.

    Excepciones:
    HTTPStatus.UNAUTHORIZED: El usuario no tiene sesión o no está registrado.
    HTTPStatus.BAD_REQUEST: Error al crear la regla debido a datos incorrectos o faltantes.
    HTTPStatus.FORBIDDEN: Solo los administradores pueden crear reglas con acciones de tipo set.
    HTTPStatus.INTERNAL_SERVER_ERROR: Error interno al intentar crear la regla debido a una excepción.
    """
    try:
        registrado = session.get("register")
        print('Registrado', registrado)
        print('Session:', session)
        if session is None or not registrado:
            return jsonify({'error': 'El usuario no tiene sesión o no está registrado'}), HTTPStatus.UNAUTHORIZED 
        isAdmin = session.get("rol") == 1

        nombre = request.json.get("nombre")
        criterios = request.json.get("criterios")
        acciones = request.json.get("acciones")

        if not comprobar_criterios(criterios):
            return jsonify({'error': 'Los criterios de la regla no son válidos'}), HTTPStatus.BAD_REQUEST
        
        if not comprobar_acciones(acciones, isAdmin):
            return jsonify({'error': 'Las acciones de la regla no son válidas'}), HTTPStatus.BAD_REQUEST
        
        if nombre and criterios and acciones: ##Que solo se pueda crear regla set a dispositivos que sean termostato
            data = reglaService.crear_regla_por_usuario_id(nombre, session.get("usuario_id"), criterios, acciones)
            if data:
                return jsonify(data), HTTPStatus.OK
        else:
            print('Error:', 'Se deben especificar el nombre del regla, los criterios y las acciones correctamente para crear una regla')
            return jsonify({'error': 'Se deben especificar el nombre del regla, los criterios y las acciones correctamente para crear una regla'}), HTTPStatus.BAD_REQUEST
    except ValueError as ex:
        if 'Solo los administradores' in str(ex):
            print('Error:', ex)
            return jsonify({'error': f'{ex}'}), HTTPStatus.FORBIDDEN ##O unauthorized
        print('Error:', ex)
        return jsonify({'error': f'{ex}'}), HTTPStatus.BAD_REQUEST
    except Exception as ex:
        print('Error:', ex)
        return jsonify({'error': f'Error al crear el regla: {ex}'}), HTTPStatus.INTERNAL_SERVER_ERROR
    
@regla_blueprint.route('/create_alerta', methods=['POST'])
### Para el tema de vigilar que se cumplan las reglas y ejecutar las acciones, revisar conversación Motor de reglas MySQL ChatGPT 29/05 ###
def create_user_alerta():
    """
    Descripción:
    Crea una nueva alerta para el usuario actual con los criterios y acciones proporcionados.

    Parámetros:
    Ninguno directamente. Se espera un JSON en el cuerpo de la solicitud con los siguientes campos:
    - nombre: Nombre de la alerta.
    - criterios: Lista de criterios para la alerta.
    - acciones: Lista de acciones para la alerta.

    Retorna:
    Response: Respuesta HTTP con un mensaje de éxito en formato JSON y un código de estado HTTP.

    Excepciones:
    HTTPStatus.UNAUTHORIZED: El usuario no tiene sesión o no está registrado.
    HTTPStatus.BAD_REQUEST: Error al crear la alerta debido a datos incorrectos o faltantes.
    HTTPStatus.FORBIDDEN: Solo los administradores pueden crear alertas con acciones de tipo set.
    HTTPStatus.INTERNAL_SERVER_ERROR: Error interno al intentar crear la alerta debido a una excepción.
    """
    try:
        registrado = session.get("register")
        print('Registrado', registrado)
        print('Session:', session)
        if session is None or not registrado:
            return jsonify({'error': 'El usuario no tiene sesión o no está registrado'}), HTTPStatus.UNAUTHORIZED 
        isAdmin = session.get("rol") == 1

        nombre = request.json.get("nombre")
        criterios = request.json.get("criterios")
        acciones = request.json.get("acciones")

        if not comprobar_criterios(criterios):
            return jsonify({'error': 'Los criterios de la regla no son válidos'}), HTTPStatus.BAD_REQUEST
        
        if not comprobar_acciones(acciones, isAdmin):
            return jsonify({'error': 'Las acciones de la regla no son válidas'}), HTTPStatus.BAD_REQUEST
        
        if nombre and criterios and acciones: ##Que solo se pueda crear regla set a dispositivos que sean termostato
            data = reglaService.crear_regla_por_usuario_id(nombre, session.get("usuario_id"), criterios, acciones, True)
            if data:
                return jsonify(data), HTTPStatus.OK
        else:
            print('Error:', 'Se deben especificar el nombre del regla, los criterios y las acciones correctamente para crear una regla')
            return jsonify({'error': 'Se deben especificar el nombre del regla, los criterios y las acciones correctamente para crear una regla'}), HTTPStatus.BAD_REQUEST
    except ValueError as ex:
        if 'Solo los administradores' in str(ex):
            print('Error:', ex)
            return jsonify({'error': f'{ex}'}), HTTPStatus.FORBIDDEN ##O unauthorized
        print('Error:', ex)
        return jsonify({'error': f'{ex}'}), HTTPStatus.BAD_REQUEST
    except Exception as ex:
        print('Error:', ex)
        return jsonify({'error': f'Error al crear el regla: {ex}'}), HTTPStatus.INTERNAL_SERVER_ERROR
    
@regla_blueprint.route('/delete/<int:id_regla>', methods=['DELETE']) 
def delete_user_regla(id_regla):
    """
    Descripción:
    Elimina una regla existente según el ID proporcionado.

    Parámetros:
    - id_regla: ID de la regla a eliminar.

    Retorna:
    Response: Respuesta HTTP con un mensaje de éxito en formato JSON y un código de estado HTTP.

    Excepciones:
    HTTPStatus.UNAUTHORIZED: El usuario no tiene sesión o no está registrado.
    HTTPStatus.NOT_FOUND: No se encontró la regla a eliminar.
    HTTPStatus.INTERNAL_SERVER_ERROR: Error interno al intentar eliminar la regla debido a una excepción.
    """
    try:
        registrado = session.get("register")
        print('Registrado', registrado)
        print('Session:', session)
        if session is None or not registrado:
            return jsonify({'error': 'El usuario no tiene sesión o no está registrado'}), HTTPStatus.UNAUTHORIZED 
        data = reglaService.eliminar_regla_por_id(id_regla, session.get("usuario_id"))
        if data:
            return jsonify(data), HTTPStatus.OK
        else:
            return jsonify({'error': 'No se encontró la regla a eliminar'}), HTTPStatus.NOT_FOUND
    except Exception as ex:
        print('Error:', ex)
        return jsonify({'error': f'Error al eliminar el regla: {ex}'}), HTTPStatus.INTERNAL_SERVER_ERROR