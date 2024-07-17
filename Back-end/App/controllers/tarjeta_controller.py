# Descripción:
# Blueprint que maneja las rutas relacionadas con las tarjetas. 
# Proporciona rutas para obtener, crear, editar y eliminar tarjetas.

from http import HTTPStatus
from flask import Blueprint, jsonify, request, session
from App.services.tarjeta_service import tarjetaService
from App.services.grupo_service import grupoService

tarjeta_blueprint = Blueprint('tarjeta', __name__)

#####HACE FALTA?!?#######
# @tarjeta_blueprint.route('/<string:id_seccion>', methods=['GET'])
# def get_seccion_tarjetas(id_seccion):
#     try:
#         registrado = session.get("register")
#         print('Registrado', registrado)
#         print('Session:', session)
#         if session is None or not registrado:
#             return jsonify({'error': 'El usuario no tiene sesión o no está registrado'}), HTTPStatus.UNAUTHORIZED #raise NoSessionSetException("El usuario no tiene sesión o no está registrado")
#         tarjetas = tarjetaService.obtener_tarjetas_seccion(id_seccion)
#         if tarjetas is None:
#             return jsonify({'error': 'No se encontraron dashboards para el usuario'}), HTTPStatus.NOT_FOUND
#         return jsonify(tarjetas), HTTPStatus.OK
#     except Exception as ex:
#         return jsonify({'error': f'Error al obtener el dashboard: {ex}'}), HTTPStatus.INTERNAL_SERVER_ERROR

@tarjeta_blueprint.route('/get/<int:id_seccion>', methods=['GET']) #Comprobacion de usuario en todos los métodos
def get_seccion_tarjetas(id_seccion):
    """
    Descripción:
    Obtiene todas las tarjetas asociadas a una sección específica si el usuario tiene sesión válida.

    Parámetros:
    id_seccion (int): Identificador de la sección de la cual se desean obtener las tarjetas.

    Retorna:
    Response: JSON con las tarjetas de la sección y código de estado HTTP.

    Excepciones:
    HTTPStatus.UNAUTHORIZED: El usuario no tiene sesión o no está registrado.
    HTTPStatus.NOT_FOUND: No se encontraron tarjetas para la sección especificada.
    HTTPStatus.INTERNAL_SERVER_ERROR: Error interno al obtener las tarjetas.
    """
    try:
        registrado = session.get("register")
        print('Registrado', registrado)
        print('Session:', session)
        if session is None or not registrado:
            return jsonify({'error': 'El usuario no tiene sesión o no está registrado'}), HTTPStatus.UNAUTHORIZED
        tarjetas = tarjetaService.obtener_tarjetas_seccion(id_seccion)
        if tarjetas is None:
            return jsonify({'error': 'No se encontraron tarjetas para la sección'}), HTTPStatus.NOT_FOUND
        return jsonify(tarjetas), HTTPStatus.OK
    except Exception as ex:
        return jsonify({'error': f'Error al obtener las tarjetas de la sección: {ex}'}), HTTPStatus.INTERNAL_SERVER_ERROR

@tarjeta_blueprint.route('/create', methods=['POST']) ##AUNQUE DE ERRORES DA 200
def create_tarjeta():
    """
    Descripción:
    Crea una nueva tarjeta según los datos proporcionados si el usuario tiene sesión válida.

    Parámetros:
    JSON en el cuerpo de la solicitud con los datos de la tarjeta a crear.

    Retorna:
    Response: Mensaje de éxito si la tarjeta se crea correctamente y código de estado HTTP.

    Excepciones:
    HTTPStatus.UNAUTHORIZED: El usuario no tiene sesión o no está registrado.
    HTTPStatus.BAD_REQUEST: Los datos proporcionados para crear la tarjeta son inválidos.
    HTTPStatus.INTERNAL_SERVER_ERROR: Error interno al crear la tarjeta.
    """
    try:
        registrado = session.get("register")
        print('Registrado', registrado)
        print('Session:', session)
        if session is None or not registrado:
            return jsonify({'error': 'El usuario no tiene sesión o no está registrado'}), HTTPStatus.UNAUTHORIZED
        tipo = request.json.get("tipo")
        posicion = request.json.get("posicion")
        contenido = request.json.get("contenido")
        imagen = request.json.get("imagen")
        id_dispositivo = request.json.get("id-dispositivo")
        id_atributo = request.json.get("id-atributo")
        tipo_grafico = request.json.get("tipo-grafico")
        tiempo_grafico = request.json.get("tiempo-grafico")
        id_seccion = request.json.get("id-seccion")
        if tipo and posicion and id_seccion:
            ####Igual tengo que hacer un create texto, create imagen, create grafico, create estado
            ####COMPROBAR QUE LA SECCION CORRESPONDE AL USUARIO DE LA SESION
            if tipo == 'grafico' and (id_dispositivo is None or id_atributo is None or tipo_grafico is None or tiempo_grafico is None):
                return jsonify({'error': 'Se debe especificar un id de dispositivo, id de atributo, tipo de gráfico y tiempo de gráfico para crear una tarjeta de tipo gráfico'}), HTTPStatus.BAD_REQUEST
            elif tipo == 'grafico' and (contenido is not None or imagen is not None):
                return jsonify({'error': 'No se debe especificar contenido o imagen para crear una tarjeta de tipo gráfico'}), HTTPStatus.BAD_REQUEST
            elif tipo == 'texto' and (contenido is None):
                return jsonify({'error': 'Se debe especificar un contenido para crear una tarjeta de tipo texto'}), HTTPStatus.BAD_REQUEST
            elif tipo == 'texto' and (imagen is not None or id_dispositivo is not None or id_atributo is not None or tipo_grafico is not None or tiempo_grafico is not None):
                return jsonify({'error': 'No se debe especificar imagen, id de dispositivo, id de atributo, tipo de gráfico o tiempo de gráfico para crear una tarjeta de tipo texto'}), HTTPStatus.BAD_REQUEST
            elif tipo == 'imagen' and (imagen is None):
                return jsonify({'error': 'Se debe especificar una imagen para crear una tarjeta de tipo imagen'}), HTTPStatus.BAD_REQUEST
            elif tipo == 'imagen' and (contenido is not None or id_dispositivo is not None or id_atributo is not None or tipo_grafico is not None or tiempo_grafico is not None):
                return jsonify({'error': 'No se debe especificar contenido, id de dispositivo, id de atributo, tipo de gráfico o tiempo de gráfico para crear una tarjeta de tipo imagen'}), HTTPStatus.BAD_REQUEST
            elif tipo == 'estado' and (id_dispositivo is not None or id_atributo is not None):
                return jsonify({'error': 'No se debe especificar id de dispositivo o id de atributo para crear una tarjeta de tipo estado'}), HTTPStatus.BAD_REQUEST
            elif tipo == 'estado' and (contenido is None or imagen is None or tipo_grafico is None or tiempo_grafico is None):
                return jsonify({'error': 'Se debe especificar contenido, imagen, tipo de gráfico y tiempo de gráfico para crear una tarjeta de tipo estado'}), HTTPStatus.BAD_REQUEST
            tarjetaService.crear_tarjeta(tipo, posicion, id_seccion, contenido, imagen, id_dispositivo, id_atributo, tipo_grafico, tiempo_grafico)
            return jsonify({'message': 'Tarjeta creada correctamente'}), HTTPStatus.OK
        else:
            return jsonify({'error': 'Se debe especificar un tipo, posicion e id de sección para crear una tarjeta'}), HTTPStatus.BAD_REQUEST
    except Exception as ex:
        return jsonify({'error': f'Error al crear la tarjeta: {ex}'}), HTTPStatus.INTERNAL_SERVER_ERROR
    
@tarjeta_blueprint.route('/create_texto', methods=['POST']) ##AUNQUE DE ERRORES DA 200
def create_texto():
    """
    Descripción:
    Crea una nueva tarjeta de tipo texto según los datos proporcionados si el usuario tiene sesión válida.

    Parámetros:
    JSON en el cuerpo de la solicitud con los datos de la tarjeta de texto a crear.

    Retorna:
    Response: Mensaje de éxito si la tarjeta de texto se crea correctamente y código de estado HTTP.

    Excepciones:
    HTTPStatus.UNAUTHORIZED: El usuario no tiene sesión o no está registrado.
    HTTPStatus.BAD_REQUEST: Los datos proporcionados para crear la tarjeta de texto son inválidos.
    HTTPStatus.INTERNAL_SERVER_ERROR: Error interno al crear la tarjeta de texto.
    """
    try:
        registrado = session.get("register")
        print('Registrado', registrado)
        print('Session:', session)
        if session is None or not registrado:
            return jsonify({'error': 'El usuario no tiene sesión o no está registrado'}), HTTPStatus.UNAUTHORIZED
        tipo = request.json.get("tipo")
        posicion = request.json.get("posicion")
        contenido = request.json.get("contenido")
        id_seccion = request.json.get("id_seccion")
        print("tipo, posicion,contenido,id_seccion",tipo, posicion, contenido, id_seccion)
        if tipo and posicion and id_seccion and contenido:
            ####COMPROBAR QUE LA SECCION CORRESPONDE AL USUARIO DE LA SESION
            tarjetaService.crear_tarjeta(tipo, posicion, contenido, None, None, None, None, None, id_seccion)
            return jsonify({'message': 'Tarjeta creada correctamente'}), HTTPStatus.OK
        else:
            return jsonify({'error': 'Se debe especificar un tipo, posicion, contenido e id de sección para crear una tarjeta de texto'}), HTTPStatus.BAD_REQUEST
    except Exception as ex:
        return jsonify({'error': f'Error al crear la tarjeta: {ex}'}), HTTPStatus.INTERNAL_SERVER_ERROR
    
@tarjeta_blueprint.route('/create_imagen', methods=['POST']) ##AUNQUE DE ERRORES DA 200
def create_imagen():
    """
    Descripción:
    Crea una nueva tarjeta de tipo imagen según los datos proporcionados si el usuario tiene sesión válida.

    Parámetros:
    JSON en el cuerpo de la solicitud con los datos de la tarjeta de imagen a crear.

    Retorna:
    Response: Mensaje de éxito si la tarjeta de imagen se crea correctamente y código de estado HTTP.

    Excepciones:
    HTTPStatus.UNAUTHORIZED: El usuario no tiene sesión o no está registrado.
    HTTPStatus.BAD_REQUEST: Los datos proporcionados para crear la tarjeta de imagen son inválidos.
    HTTPStatus.INTERNAL_SERVER_ERROR: Error interno al crear la tarjeta de imagen.
    """
    try:
        registrado = session.get("register")
        print('Registrado', registrado)
        print('Session:', session)
        if session is None or not registrado:
            return jsonify({'error': 'El usuario no tiene sesión o no está registrado'}), HTTPStatus.UNAUTHORIZED
        tipo = request.json.get("tipo")
        posicion = request.json.get("posicion")
        imagen = request.json.get("imagen")
        id_seccion = request.json.get("id_seccion")
        if tipo and posicion and id_seccion and imagen:
            ####COMPROBAR QUE LA SECCION CORRESPONDE AL USUARIO DE LA SESION
            tarjetaService.crear_tarjeta(tipo, posicion, None, imagen, None, None, None, None, id_seccion)
            return jsonify({'message': 'Tarjeta creada correctamente'}), HTTPStatus.OK
        else:
            return jsonify({'error': 'Se debe especificar un tipo, posicion, imagen e id de sección para crear una tarjeta de imagen'}), HTTPStatus.BAD_REQUEST
    except Exception as ex:
        return jsonify({'error': f'Error al crear la tarjeta: {ex}'}), HTTPStatus.INTERNAL_SERVER_ERROR

@tarjeta_blueprint.route('/create_estado', methods=['POST']) ##AUNQUE DE ERRORES DA 200
def create_estado():
    """
    Descripción:
    Crea una nueva tarjeta de tipo estado según los datos proporcionados si el usuario tiene sesión válida.

    Parámetros:
    JSON en el cuerpo de la solicitud con los datos de la tarjeta de estado a crear.

    Retorna:
    Response: Mensaje de éxito si la tarjeta de estado se crea correctamente y código de estado HTTP.

    Excepciones:
    HTTPStatus.UNAUTHORIZED: El usuario no tiene sesión o no está registrado.
    HTTPStatus.BAD_REQUEST: Los datos proporcionados para crear la tarjeta de estado son inválidos.
    HTTPStatus.INTERNAL_SERVER_ERROR: Error interno al crear la tarjeta de estado.
    """
    try:
        registrado = session.get("register")
        print('Registrado', registrado)
        print('Session:', session)
        if session is None or not registrado:
            return jsonify({'error': 'El usuario no tiene sesión o no está registrado'}), HTTPStatus.UNAUTHORIZED
        tipo = request.json.get("tipo")
        posicion = request.json.get("posicion")
        id_seccion = request.json.get("id_seccion")
        id_dispositivo = request.json.get("id_dispositivo")
        id_atributo = request.json.get("id_atributo")
        if tipo and posicion and id_seccion and id_atributo and id_dispositivo:
            ####COMPROBAR QUE LA SECCION CORRESPONDE AL USUARIO DE LA SESION
            tarjetaService.crear_tarjeta(tipo, posicion, None, None, id_dispositivo, id_atributo, None, None, id_seccion)
            return jsonify({'message': 'Tarjeta creada correctamente'}), HTTPStatus.OK
        else:
            print(tipo, posicion, id_seccion, id_atributo, id_dispositivo)
            print('Error al crear tarjeta estado, faltan datos')
            return jsonify({'error': 'Se debe especificar un tipo, posicion, id de dispositivo, id de atributo e id de sección para crear una tarjeta de imagen'}), HTTPStatus.BAD_REQUEST
    except ValueError as ex:
        print('Error al crear tarjeta estado: ', ex)
        return jsonify({'error': f'{ex}'}), HTTPStatus.BAD_REQUEST
    except Exception as ex:
        return jsonify({'error': f'Error al crear la tarjeta: {ex}'}), HTTPStatus.INTERNAL_SERVER_ERROR

@tarjeta_blueprint.route('/create_termostato', methods=['POST'])   
def create_termostato():
    """
    Descripción:
    Crea una nueva tarjeta de tipo termostato según los datos proporcionados si el usuario tiene sesión válida y permisos de administrador.

    Parámetros:
    JSON en el cuerpo de la solicitud con los datos de la tarjeta de termostato a crear.

    Retorna:
    Response: Mensaje de éxito si la tarjeta de termostato se crea correctamente y código de estado HTTP.

    Excepciones:
    HTTPStatus.UNAUTHORIZED: El usuario no tiene sesión o no está registrado.
    HTTPStatus.UNAUTHORIZED: El usuario no tiene permisos para acceder a integraciones.
    HTTPStatus.BAD_REQUEST: Los datos proporcionados para crear la tarjeta de termostato son inválidos.
    HTTPStatus.INTERNAL_SERVER_ERROR: Error interno al crear la tarjeta de termostato.
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
        
        tipo = request.json.get("tipo")
        posicion = request.json.get("posicion")
        id_seccion = request.json.get("id_seccion")
        id_dispositivo = request.json.get("id_dispositivo")
        id_atributo = request.json.get("id_atributo")
        if tipo and posicion and id_seccion and id_atributo and id_dispositivo:
            ####COMPROBAR QUE LA SECCION CORRESPONDE AL USUARIO DE LA SESION
            tarjetaService.crear_tarjeta(tipo, posicion, None, None, id_dispositivo, id_atributo, None, None, id_seccion)
            return jsonify({'message': 'Tarjeta creada correctamente'}), HTTPStatus.OK
        else:
            print('Error al crear tarjeta termostato', tipo, posicion, id_seccion, id_atributo, id_dispositivo)
            return jsonify({'error': 'Se debe especificar un tipo, posicion, id de dispositivo, id de atributo e id de sección para crear una tarjeta de imagen'}), HTTPStatus.BAD_REQUEST
    except ValueError as ex:
        print('Error al crear tarjeta termostato: ', ex)
        return jsonify({'error': f'{ex}'}), HTTPStatus.BAD_REQUEST
    except Exception as ex:
        print('Error al crear tarjeta termostato: ', ex)
        return jsonify({'error': f'Error al crear el termostato: {ex}'}), HTTPStatus.INTERNAL_SERVER_ERROR
    
@tarjeta_blueprint.route('/create_tarjeta_grupo', methods=['POST'])
def create_tarjeta_grupo():
    """
    Descripción:
    Añade una tarjeta tipo grupo según los datos proporcionados si el usuario tiene sesión válida.

    Parámetros:
    JSON en el cuerpo de la solicitud con los datos de la tarjeta y el grupo correspondiente.

    Retorna:
    Response: Mensaje de éxito si la tarjeta  grupo se crea correctamente y código de estado HTTP.

    Excepciones:
    HTTPStatus.UNAUTHORIZED: El usuario no tiene sesión o no está registrado.
    HTTPStatus.BAD_REQUEST: Los datos proporcionados para añadir la tarjeta al grupo son inválidos.
    HTTPStatus.INTERNAL_SERVER_ERROR: Error interno al añadir la tarjeta al grupo.
    """
    try:
        registrado = session.get("register")
        print('Registrado', registrado)
        print('Session:', session)
        if session is None or not registrado:
            return jsonify({'error': 'El usuario no tiene sesión o no está registrado'}), HTTPStatus.UNAUTHORIZED
        tipo = request.json.get("tipo")
        posicion = request.json.get("posicion")
        id_grupo = request.json.get("id_grupo")
        id_seccion = request.json.get("id_seccion")
        if tipo and posicion and id_grupo:
            dispositivos_grupo = grupoService.obtener_dispositivo_por_grupo(id_grupo, session.get("usuario_id"))
            print('Grupo:', dispositivos_grupo)
            tarjetaService.crear_tarjeta(tipo, posicion, None, None, None, None, None, None, id_seccion, id_grupo)
            return jsonify({'message': 'Tarjeta añadida al grupo correctamente'}), HTTPStatus.OK
        else:
            return jsonify({'error': 'Se debe especificar un id de tarjeta y un id de grupo para añadir la tarjeta al grupo'}), HTTPStatus.BAD_REQUEST
    except Exception as ex:
        return jsonify({'error': f'Error al añadir la tarjeta al grupo: {ex}'}), HTTPStatus.INTERNAL_SERVER_ERROR

@tarjeta_blueprint.route('/set_temperatura', methods=['PUT'])   #########En vez de temperatura creo que sería atributo sin más, para eso está la plantilla
def setTemperatura():
    """
    Descripción:
    Actualiza la temperatura de una dispositivo tipo termostato según los datos proporcionados si el usuario tiene sesión válida y permisos de administrador.

    Parámetros:
    JSON en el cuerpo de la solicitud con los datos de la tarjeta.

    Retorna:
    Response: Mensaje de éxito si la tarjeta  grupo se crea correctamente y código de estado HTTP.

    Excepciones:
    HTTPStatus.UNAUTHORIZED: El usuario no tiene sesión, no está registrado o no es admin.
    HTTPStatus.BAD_REQUEST: Los datos proporcionados son inválidos.
    HTTPStatus.INTERNAL_SERVER_ERROR: Error interno.
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

        id_dispositivo = request.json.get("id_dispositivo")
        id_atributo = request.json.get("id_atributo")
        valor = request.json.get("valor")

        if id_dispositivo and id_atributo and valor:
            if tarjetaService.setTemperatura(id_dispositivo, id_atributo, valor) is False:
                return jsonify({'error': 'No tengo claro'}), HTTPStatus.NOT_FOUND ################################
            return jsonify({'message': 'Temperatura actualizada correctamente'}), HTTPStatus.OK
        else:
            return jsonify({'error': 'Se debe especificar un id de dispositivo, id de atributo y valor para actualizar la temperatura'}), HTTPStatus.BAD_REQUEST
    except ValueError as ex:
        print('Error al establecer temperatura de tarjeta termostato: ', ex)
        return jsonify({'error': f'{ex}'}), HTTPStatus.BAD_REQUEST
    except Exception as ex:
        print('Error al establecer temperatura de tarjeta termostato: ',ex)
        return jsonify({'error': f'Error al establecer temperatura de tarjeta termostato: {ex}'}), HTTPStatus.INTERNAL_SERVER_ERROR  
    
@tarjeta_blueprint.route('/create_grafico', methods=['POST'])  
def create_grafico():
    try:
        registrado = session.get("register")
        print('Registrado', registrado)
        print('Session:', session)
        if session is None or not registrado:
            return jsonify({'error': 'El usuario no tiene sesión o no está registrado'}), HTTPStatus.UNAUTHORIZED
        tipo = request.json.get("tipo")
        posicion = request.json.get("posicion")
        id_seccion = request.json.get("id_seccion")
        id_dispositivos = request.json.get("id_dispositivos")
        id_atributo = request.json.get("id_atributo")
        tipo_grafico = request.json.get("tipo_grafico")
        tiempo_grafico = request.json.get("tiempo_grafico")
        if tipo and posicion and id_seccion and id_atributo and id_dispositivos and tipo_grafico and tiempo_grafico:
            ####COMPROBAR QUE LA SECCION CORRESPONDE AL USUARIO DE LA SESION
            tarjetaService.crear_tarjeta(tipo, posicion, None, None, id_dispositivos, id_atributo, tipo_grafico, tiempo_grafico, id_seccion)
            return jsonify({'message': 'Tarjeta creada correctamente'}), HTTPStatus.OK
        else:
            return jsonify({'error': 'Se debe especificar un tipo, posicion, id de dispositivo, id de atributo, id de sección, tipo gráfico y tiempo gráfico para crear una tarjeta de gráfico'}), HTTPStatus.BAD_REQUEST
    except Exception as ex:
        return jsonify({'error': f'Error al crear la tarjeta: {ex}'}), HTTPStatus.INTERNAL_SERVER_ERROR

@tarjeta_blueprint.route('/create_plano', methods=['POST'])    
def create_plano():
    try:
        registrado = session.get("register")
        print('Registrado', registrado)
        print('Session:', session)
        if session is None or not registrado:
            return jsonify({'error': 'El usuario no tiene sesión o no está registrado'}), HTTPStatus.UNAUTHORIZED
        tipo = request.json.get("tipo")
        posicion = request.json.get("posicion")
        id_seccion = request.json.get("id_seccion")
        if tipo and posicion:
            ####COMPROBAR QUE LA SECCION CORRESPONDE AL USUARIO DE LA SESION
            tarjetaService.crear_tarjeta(tipo, posicion, None, None, None, None, None, None, id_seccion)
            return jsonify({'message': 'Tarjeta creada correctamente'}), HTTPStatus.OK
        else:
            return jsonify({'error': 'Se debe especificar un tipo, posicion, id de dispositivo, id de atributo e id de sección para crear una tarjeta de imagen'}), HTTPStatus.BAD_REQUEST
    except Exception as ex:
        return jsonify({'error': f'Error al crear la tarjeta: {ex}'}), HTTPStatus.INTERNAL_SERVER_ERROR
