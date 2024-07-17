# Descripción:
# Blueprint que maneja las rutas relacionadas con las integraciones. 
# Proporciona rutas para obtener, crear, editar y eliminar integraciones.

from http import HTTPStatus
from flask import Blueprint, jsonify, request, session
from App.exceptions.duplicate import duplicateIntegracionException, duplicateAtributoException
from App.services.integracion_service import integracionService
######################DEBERÍA HACER QUE CUANDO SE EDITE UNA INTEGRACION SE EDITEN LOS DISPOSITIVOS DEL XML#######
######################IGUAL AL ELIMINAR#############################
integracion_blueprint = Blueprint('integracion', __name__)
############VIGILAR QUE ESTE FUNCIONANDO EL ACTUALIZAR SCRIPTS
def validar_atributos(atributos):
    """
    Descripción:
    Valida que los atributos proporcionados sean correctos.

    Parámetros:
    atributos (list): Lista de diccionarios con los atributos a validar.

    Retorna:
    bool: True si los atributos son válidos, False en caso contrario.
    """
    if not isinstance(atributos, list):
        print("Error al validar que atributos sea una lista")
        return False
    
    for atributo in atributos:
        if not isinstance(atributo, dict):
            print("Error al validar que atributo sea un diccionario")
            return False
        
        if "nombre" not in atributo or "unidades" not in atributo or "actuable" not in atributo or "tipo" not in atributo:
            print("Error al validar que atributo tenga los campos nombre, unidades, actuable y tipo")
            return False

        if not isinstance(atributo["nombre"], str) \
                or not isinstance(atributo["unidades"], str) \
                or not isinstance(atributo["actuable"], bool) \
                or ("limite_superior" in atributo and not isinstance(atributo["limite_superior"], (int, float))) \
                or ("limite_inferior" in atributo and not isinstance(atributo["limite_inferior"], (int, float))) \
                or ("limite_superior" in atributo and "limite_inferior" in atributo and atributo["limite_superior"] <= atributo["limite_inferior"]):
            
            print(atributo["nombre"], atributo["unidades"], atributo["actuable"])
            print(isinstance(atributo["nombre"], str), isinstance(atributo["unidades"], str), isinstance(atributo["actuable"], bool))
            if "limite_superior" in atributo:
                print(atributo["limite_superior"])
                print(isinstance(atributo["limite_superior"], (int, float)))
            if "limite_inferior" in atributo:
                print(atributo["limite_inferior"])
                print(isinstance(atributo["limite_inferior"], (int, float)))
            print("Error al validar los tipos de los campos de atributo")
            return False
        
        if atributo["actuable"]:
            atributo["actuable"] = "true"
        else:
            atributo["actuable"] = "false"

    return True

@integracion_blueprint.route('/', methods=['GET'])
def get_integraciones():
    """
    Descripción:
    Obtiene todas las integraciones registradas.

    Parámetros:
    Ninguno

    Retorna:
    Response: Respuesta HTTP con la lista de integraciones en formato JSON y un código de estado HTTP.

    Excepciones:
    HTTPStatus.UNAUTHORIZED: El usuario no tiene sesión o no está registrado.
    HTTPStatus.NOT_FOUND: No se encontraron integraciones.
    HTTPStatus.INTERNAL_SERVER_ERROR: Error al obtener las integraciones debido a una excepción.
    """
    try:
        registrado = session.get("register")
        print('Registrado', registrado)
        print('Session:', session)
        if session is None or not registrado:
            return jsonify({'error': 'El usuario no tiene sesión o no está registrado'}), HTTPStatus.UNAUTHORIZED #raise NoSessionSetException("El usuario no tiene sesión o no no está registrado")
        rol = session.get("rol")
        if rol != 1:
            return jsonify({'error': 'El usuario no tiene permisos para acceder a integraciones'}), HTTPStatus.UNAUTHORIZED
        
        integracion = integracionService.obtener_integraciones()
        if integracion is None:
            return jsonify({'error': 'No se encontraron integraciones'}), HTTPStatus.NOT_FOUND
        return jsonify(integracion), HTTPStatus.OK
    except Exception as ex:
        return jsonify({'error': f'Error al obtener la integracion: {ex}'}), HTTPStatus.INTERNAL_SERVER_ERROR
    
@integracion_blueprint.route('/tipos', methods=['GET'])
def get_tipos():
    """
    Descripción:
    Obtiene todos los tipos de integraciones disponibles.

    Parámetros:
    Ninguno

    Retorna:
    Response: Respuesta HTTP con los tipos de integraciones en formato JSON y un código de estado HTTP.

    Excepciones:
    HTTPStatus.UNAUTHORIZED: El usuario no tiene sesión o no está registrado.
    HTTPStatus.NOT_FOUND: No se encontraron tipos de integraciones.
    HTTPStatus.INTERNAL_SERVER_ERROR: Error al obtener los tipos de integraciones debido a una excepción.
    """
    try:
        registrado = session.get("register")
        print('Registrado', registrado)
        print('Session:', session)
        if session is None or not registrado:
            return jsonify({'error': 'El usuario no tiene sesión o no está registrado'}), HTTPStatus.UNAUTHORIZED #raise NoSessionSetException("El usuario no tiene sesión o no no está registrado")
        rol = session.get("rol")
        if rol != 1:
            return jsonify({'error': 'El usuario no tiene permisos para acceder a integraciones'}), HTTPStatus.UNAUTHORIZED
        
        tipos = integracionService.obtener_tipos()
        if tipos is None:
            return jsonify({'error': 'No se encontraron tipos'}), HTTPStatus.NOT_FOUND
        return jsonify(tipos), HTTPStatus.OK
    except Exception as ex:
        return jsonify({'error': f'Error al obtener los tipos de integracion: {ex}'}), HTTPStatus.INTERNAL_SERVER_ERROR
    
@integracion_blueprint.route('/add', methods=['POST'])
def add_integracion():
    """
    Descripción:
    Crea una nueva integración con los datos proporcionados.

    Parámetros:
    Ninguno

    Retorna:
    Response: Respuesta HTTP con un mensaje de éxito y el ID de la integración creada en formato JSON y un código de estado HTTP.

    Excepciones:
    HTTPStatus.UNAUTHORIZED: El usuario no tiene sesión o no está registrado.
    HTTPStatus.BAD_REQUEST: Error al crear la integración debido a datos incorrectos o faltantes.
    HTTPStatus.INTERNAL_SERVER_ERROR: Error interno al intentar crear la integración debido a una excepción.
    """
    try:
        registrado = session.get("register")
        print('Registrado', registrado)
        print('Session:', session)
        if session is None or not registrado:
            return jsonify({'error': 'El usuario no tiene sesión o no está registrado'}), HTTPStatus.UNAUTHORIZED #raise NoSessionSetException("El usuario no tiene sesión o no no está registrado")
        rol = session.get("rol")
        if rol != 1:
            return jsonify({'error': 'El usuario no tiene permisos para acceder a integraciones'}), HTTPStatus.UNAUTHORIZED
        
        print(request.json)
        nombre = request.json.get("nombre")
        nombre_script = request.json.get("nombre_script")
        script = request.json.get("script")
        atributos = request.json.get("atributos")
        if nombre and nombre_script and script and atributos and validar_atributos(atributos):
            print('ic:',atributos)
            integracion_data = integracionService.crear_integracion(nombre, nombre_script, script, atributos)
            return jsonify({'message': 'Integracion creada correctamente', 'id': integracion_data}), HTTPStatus.OK
        else:
            print(nombre, nombre_script, script, atributos)
            print(validar_atributos(atributos))
            print("Error al crear la integracion: Se deben especificar nombre, script y atributos correctamente para crear una integracion")
            return jsonify({'error': 'Se deben especificar nombre, script y atributos correctamente para crear una integracion'}), HTTPStatus.BAD_REQUEST
    except duplicateIntegracionException as ex:
        print("Error al crear la integracion: ", ex)
        return jsonify({'error': f'Error al crear la integracion: {ex}'}), HTTPStatus.BAD_REQUEST
    except duplicateAtributoException as ex:
        print("Error al crear la integracion: ", ex)
        return jsonify({'error': f'Error al crear la integracion: {ex}'}), HTTPStatus.BAD_REQUEST
    except ValueError as ex:
        print("Error al crear la integracion: ", ex)
        return jsonify({'error': f'Error al crear la integracion: {ex}'}), HTTPStatus.BAD_REQUEST
    except Exception as ex:
        print("Error al crear la integracion: ", ex)
        return jsonify({'error': f'Error al crear la integracion: {ex}'}), HTTPStatus.INTERNAL_SERVER_ERROR
    
@integracion_blueprint.route('/edit', methods=['PUT'])
def edit_integracion():
    """
    Descripción:
    Edita una integración existente con los datos proporcionados.

    Parámetros:
    Ninguno

    Retorna:
    Response: Respuesta HTTP con un mensaje de éxito en formato JSON y un código de estado HTTP.

    Excepciones:
    HTTPStatus.UNAUTHORIZED: El usuario no tiene sesión o no está registrado.
    HTTPStatus.BAD_REQUEST: Error al editar la integración debido a datos incorrectos o faltantes.
    HTTPStatus.NOT_FOUND: No se encontró la integración a editar.
    HTTPStatus.INTERNAL_SERVER_ERROR: Error interno al intentar editar la integración debido a una excepción.
    """
    try:
        registrado = session.get("register")
        print('Registrado', registrado)
        print('Session:', session)
        if session is None or not registrado:
            return jsonify({'error': 'El usuario no tiene sesión o no está registrado'}), HTTPStatus.UNAUTHORIZED #raise NoSessionSetException("El usuario no tiene sesión o no no está registrado")
        rol = session.get("rol")
        if rol != 1:
            return jsonify({'error': 'El usuario no tiene permisos para acceder a integraciones'}), HTTPStatus.UNAUTHORIZED
        
        print("Peticion",request.json)
        prev_nombre = request.json.get("prev_nombre")
        nombre = request.json.get("nombre")
        nombre_script = request.json.get("nombre_script")
        script = request.json.get("script")
        atributos = request.json.get("atributos")
        if prev_nombre and nombre and nombre_script and script and atributos and validar_atributos(atributos):
            print('ic:',atributos)
            integracionService.edit_integracion(prev_nombre, nombre, nombre_script, script, atributos)
            return jsonify({'message': 'Integracion editada correctamente'}), HTTPStatus.OK
        else:
            print(nombre, nombre_script, script, atributos)
            print(validar_atributos(atributos))
            print("Error al editar la integracion: Se deben especificar prev_nombre, nombre, script y atributos correctamente para editar una integracion")
            return jsonify({'error': 'Se deben especificar prev_nombre, nombre, script y atributos correctamente para editar una integracion'}), HTTPStatus.BAD_REQUEST
    except duplicateIntegracionException as ex:
        print("Error al editar la integracion: ", ex)
        return jsonify({'error': f'Error al editar la integracion: {ex}'}), HTTPStatus.BAD_REQUEST
    except duplicateAtributoException as ex:
        print("Error al editar la integracion: ", ex)
        return jsonify({'error': f'Error al editar la integracion: {ex}'}), HTTPStatus.BAD_REQUEST
    except ValueError as ex:
        if "No se ha encontrado la integración a editar" in str(ex):
            print("Error al editar la integracion: ", ex)
            return jsonify({'error': f'Error al editar la integracion: {ex}'}), HTTPStatus.NOT_FOUND
        print("Error al editar la integracion: ", ex)
        return jsonify({'error': f'Error al editar la integracion: {ex}'}), HTTPStatus.BAD_REQUEST
    except Exception as ex:
        print("Error al editar la integracion: ", ex)
        return jsonify({'error': f'Error al editar la integracion: {ex}'}), HTTPStatus.INTERNAL_SERVER_ERROR
    
@integracion_blueprint.route('/delete', methods=['DELETE'])
def delete_integracion():
    """
    Descripción:
    Elimina una integración existente según el ID proporcionado.

    Parámetros:
    Ninguno

    Retorna:
    Response: Respuesta HTTP con un mensaje de éxito en formato JSON y un código de estado HTTP.

    Excepciones:
    HTTPStatus.UNAUTHORIZED: El usuario no tiene sesión o no está registrado.
    HTTPStatus.BAD_REQUEST: Error al eliminar la integración debido a datos incorrectos o faltantes.
    HTTPStatus.NOT_FOUND: No se encontró la integración a eliminar.
    HTTPStatus.INTERNAL_SERVER_ERROR: Error interno al intentar eliminar la integración debido a una excepción.
    """
    try:
        registrado = session.get("register")
        print('Registrado', registrado)
        print('Session:', session)
        if session is None or not registrado:
            return jsonify({'error': 'El usuario no tiene sesión o no está registrado'}), HTTPStatus.UNAUTHORIZED #raise NoSessionSetException("El usuario no tiene sesión o no no está registrado")
        rol = session.get("rol")
        if rol != 1:
            return jsonify({'error': 'El usuario no tiene permisos para acceder a integraciones'}), HTTPStatus.UNAUTHORIZED

        id = request.json.get("id")
        if id:
            integracionService.eliminar_integracion(id)
            return jsonify({'message': 'Integracion eliminada correctamente'}), HTTPStatus.OK
        else:
            print("Error al eliminar la integracion: Se debe especificar el id de la integracion a eliminar")
            return jsonify({'error': 'Se debe especificar el id de la integracion a eliminar'}), HTTPStatus.BAD_REQUEST
    except ValueError as ex:
        if "No se ha encontrado la integración a eliminar" in str(ex):
            print("Error al eliminar la integracion: ", ex)
            return jsonify({'error': f'Error al eliminar la integracion: {ex}'}), HTTPStatus.NOT_FOUND
        print("Error al eliminar la integracion: ", ex)
        return jsonify({'error': f'Error al eliminar la integracion: {ex}'}), HTTPStatus.BAD_REQUEST
    except Exception as ex:
        return jsonify({'error': f'Error al eliminar la integracion: {ex}'}), HTTPStatus.INTERNAL_SERVER_ERROR
        
    




