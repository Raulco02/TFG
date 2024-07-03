import hashlib
from http import HTTPStatus
from flask import Blueprint, jsonify, request, session
from App.services.usuario_service import usuarioService
from App.services.dashboard_service import dashboardService
from App.services.seccion_service import seccionService

###Si ocurre un error dice que se crea correctamente

usuario_blueprint = Blueprint('usuario', __name__)

httpSessions = {}
sessionsUsuarios = {} #Ver si esto es útil

@usuario_blueprint.route('/login', methods=['PUT']) #HACER UN LOGOUT TAMBIÉN
def login():
# Obtener los nuevos datos del usuario del cuerpo de la solicitud
    try:
        correo = request.json.get('correo')
        password = request.json.get('password')
        #print("Correo:", correo)
        #print("Password:", password)
        # Verificar si se proporcionaron todos los datos necesarios
        if correo and password:
            usuario = usuarioService.login(correo, password)
            #print(usuario)
            if usuario:
                # codigo = usuarioService.send_security_code(correo, usuario) #ACTIVAR PARA CODIGO DE SEGURIDAD
                #print(codigo)
                # session = request.environ.get('beaker.session')
                # if session is None:
                #     session = request.environ['beaker.session'] = {}

                session['usuario_id'] = usuario[0]
                session['register'] = True
                session['rol'] = usuario[4]
                #session['usuario'] = usuario ¿Quiero guardar el usuario completo?
                httpId = session.get('_id')
                httpSessions[httpId] = session
                sessionsUsuarios[httpId] = usuario[0]
                return jsonify({"message": "El usuario ha iniciado sesión correctamente"}), HTTPStatus.OK
            else:
                return jsonify({'error': 'Usuario no encontrado'}), HTTPStatus.NOT_FOUND
        else:
            return jsonify({'error': 'Faltan datos del usuario'}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR ##VER INFORMACION QUE SE DEVUELVE

@usuario_blueprint.route('/codigo', methods=['PUT']) 
def verificar_codigo():
    try:
        codigo = request.json.get('codigo')
        usuario = session.get('usuario_id')
        if codigo:
            if usuarioService.verify_security_code(codigo, usuario):
                session['confirmado'] = True
                return jsonify({"message": "Código de seguridad correcto"}), HTTPStatus.OK
            else:
                return jsonify({'error': 'Código de seguridad incorrecto o expirado'}), HTTPStatus.UNAUTHORIZED
        else:
            return jsonify({'error': 'Faltan datos del usuario'}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@usuario_blueprint.route('/perfil', methods=['GET'])
def obtener_perfil():
    try:
        # session = request.environ.get('beaker.session')
        registrado = session.get("register")
        # print('Confirmado:', session.get('confirmado')) DESACTIVAR PARA CODIGO DE SEGURIDAD
        print('Registrado', registrado)
        print('Session:', session)
        if session is None or not registrado:
            return jsonify({'error': 'El usuario no tiene sesión o no está registrado'}), HTTPStatus.UNAUTHORIZED #raise NoSessionSetException("El usuario no tiene sesión o no está registrado")
        # if session.get('confirmado') is None:
        #     return jsonify({'error': 'No se ha confirmado el código de seguridad'}), HTTPStatus.UNAUTHORIZED
        httpId = session.get('_id')
        if httpId in httpSessions:
            usuario_id = session.get('usuario_id')
            if usuario_id:
                usuario = usuarioService.obtener_usuario_por_id(usuario_id)
                if usuario:
                    return jsonify(usuario), HTTPStatus.OK
                else:
                    return jsonify({'error': 'Usuario no encontrado'}), HTTPStatus.NOT_FOUND
            else:
                return jsonify({'error': 'Usuario no ha iniciado sesión'}), HTTPStatus.UNAUTHORIZED
        else:
            return jsonify({'error': 'No se ha iniciado sesión'}), HTTPStatus.UNAUTHORIZED
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@usuario_blueprint.route('/datos', methods=['GET']) #PARA OBTENER DATOS USUARIO+DASHBOARDS+SECCIONES(¿GUARDAR ESTO LUEGO EN NAVEGADOR?)
def obtener_datos_usuario(): #Poner returns en el if
    try:
        registrado = session.get("register")
        print('Registrado', registrado)
        print('Session:', session)
        if session is None or not registrado:
            return jsonify({'error': 'El usuario no tiene sesión o no está registrado'}), HTTPStatus.NOT_FOUND #raise NoSessionSetException("El usuario no tiene sesión o no está registrado")
        # if session.get('confirmado') is None:     #DESACTIVAR PARA CODIGO DE SEGURIDAD
        #     return jsonify({'error': 'No se ha confirmado el código de seguridad'}), HTTPStatus.FORBIDDEN
        httpId = session.get('_id')
        if httpId in httpSessions:
            usuario_id = session.get('usuario_id')
            if usuario_id:
                usuario = usuarioService.obtener_usuario_por_id(usuario_id)
                if usuario:
                    dashboards = dashboardService.obtener_dashboard_por_id_usuario(usuario_id)
                    if dashboards is not []:
                        dashboards_completos = seccionService.obtener_secciones_usuario(dashboards)
                        if dashboards_completos is not None:
                            final = {}
                            final['usuario']=usuario
                            final['dashboards']=dashboards_completos
                            return jsonify(final), HTTPStatus.OK
                        else:
                            return jsonify({'error': 'No se encontraron secciones en los dashboards'}), HTTPStatus.NOT_FOUND
                    else:
                        return jsonify({'error': 'No se encontraron dashboards'}), HTTPStatus.NOT_FOUND
                else:
                    return jsonify({'error': 'Usuario no encontrado'}), HTTPStatus.NOT_FOUND
            else:
                return jsonify({'error': 'Usuario no ha iniciado sesión'}), HTTPStatus.UNAUTHORIZED
        else:
            return jsonify({'error': 'No se ha iniciado sesión'}), HTTPStatus.UNAUTHORIZED
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@usuario_blueprint.route('/registrar', methods=['POST'])
def registrar():
    try:
        info = request.get_json()
        try:
            nombre = info.get("nombre").strip()
            correo = info.get("correo").strip()
            pwd1 = info.get("pwd1").strip()
            pwd2 = info.get("pwd2").strip()
        except Exception as e:
            print("Error al obtener datos del usuario:", e)
            return jsonify({"error": "Error al obtener datos del usuario"}), HTTPStatus.BAD_REQUEST

        usuario = usuarioService.obtener_usuario_por_correo(correo)
        print(usuario)
        if usuario:
            print("El correo ya está en uso")
            return jsonify({"error": "El correo ya está en uso"}), HTTPStatus.BAD_REQUEST

        if len(nombre) < 2:
            print("Error en registro: El nombre debe tener al menos 2 caracteres")
            return jsonify({"error": "El nombre debe tener al menos 2 caracteres"}), HTTPStatus.BAD_REQUEST
        if len(pwd1) < 8:
            print("Error en registro: La contraseña debe tener al menos 8 caracteres")
            return jsonify({"error": "La contraseña debe tener al menos 8 caracteres"}), HTTPStatus.BAD_REQUEST
        if pwd1 != pwd2:
            print("Error en registro: Las contraseñas no coinciden")
            return jsonify({"error": "Las contraseñas no coinciden"}), HTTPStatus.BAD_REQUEST

        # Comprobar que el correo es un correo
        try:
            usuarioService.registrar(nombre, correo, pwd1)
            return jsonify({"message": "Usuario registrado correctamente"}), HTTPStatus.OK
        except Exception as e:
            print("Error al registrar usuario:", e)
            return jsonify({"error": "Error al realizar el registro"}), HTTPStatus.INTERNAL_SERVER_ERROR

    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

# Ruta para logout
@usuario_blueprint.route('/logout', methods=['POST'])
def logout():
    try:
        # Eliminar el usuario_id de la sesión
        session.pop('usuario_id', None)
        # Eliminar cualquier otra información de sesión que desees limpiar
        session.pop('register', None)
        
        # También puedo limpiar el resto de la sesión
        # session.clear()

        # Eliminar la sesión del diccionario
        httpId = session.get("_id")
        if httpId in httpSessions:
            del httpSessions[httpId]
        if httpId in sessionsUsuarios:
            del sessionsUsuarios[httpId]

        return jsonify({'message': 'Logout exitoso'}), HTTPStatus.OK
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

# @usuario_blueprint.route('/<string:nombre>', methods=['GET'])
# def get_usuario_nombre(nombre):
#     ######ESTOS METODOS NO SE SI DEBEN USARSE, EN CASO DE QUE SÍ, RODEAR CON TRY CATCH DE INTERNAL SERVER ERROR
#     usuario_name = session.get('usuario_id')
#     if usuario_name:
#         print(usuario_name)
#         usuario_data = usuarioService.obtener_usuario_por_nombre(nombre)
#         if usuario_data:
#             return jsonify(usuario_data), HTTPStatus.OK
#         else:
#             return jsonify({'error': 'User not found'}), HTTPStatus.NOT_FOUND
#     else:
#         return jsonify({'error': 'No ha iniciado sesión'}), HTTPStatus.UNAUTHORIZED
    
# @usuario_blueprint.route('/<string:correo>', methods=['GET']) ####NO FUNCIONA
# def get_usuario_correo(correo):
#     usuario_data = usuarioService.obtener_usuario_por_correo(correo)
#     if usuario_data:
#         return jsonify(usuario_data), HTTPStatus.OK
#     else:
#         return jsonify({'error': 'User not found'}), HTTPStatus.NOT_FOUND
    
@usuario_blueprint.route('/getAll', methods=['GET'])
def get_usuarios():
    try:
        registrado = session.get("register")
        print('Registrado', registrado)
        print('Session:', session)
        if session is None or not registrado:
            return jsonify({'error': 'El usuario no tiene sesión o no está registrado'}), HTTPStatus.UNAUTHORIZED #raise NoSessionSetException("El usuario no tiene sesión o no no está registrado")
        rol = session.get("rol")
        if rol != 1:
            return jsonify({'error': 'El usuario no tiene permisos para acceder a los usuarios'}), HTTPStatus.UNAUTHORIZED
        usuario_data = usuarioService.obtener_todos_los_usuarios()
        if usuario_data:
            return jsonify(usuario_data), HTTPStatus.OK
        else:
            return jsonify({'error': 'Sensor not found'}), HTTPStatus.NOT_FOUND
    except Exception as e:
        print(e)
        return jsonify({'error': "Error al obtener usuarios"}), HTTPStatus.INTERNAL_SERVER_ERROR
    
# @usuario_blueprint.route('/get_usuario', methods=['GET'])
# def get_usuario_sesion():
#     try:
#         registrado = session.get("register")
#         print('Registrado', registrado)
#         print('Session:', session)
#         if session is None or not registrado:
#             return jsonify({'error': 'El usuario no tiene sesión o no está registrado'}), HTTPStatus.UNAUTHORIZED #raise NoSessionSetException("El usuario no tiene sesión o no no está registrado")
#         usuario_data = usuarioService.obtener_usuario_por_id(session.get('usuario_id'))
#         if usuario_data:
#             return jsonify(usuario_data), HTTPStatus.OK
#         else:
#             return jsonify({'error': 'Sensor not found'}), HTTPStatus.NOT_FOUND
#     except Exception as e:
#         print(e)
#         return jsonify({'error': "Error al obtener usuarios"}), HTTPStatus.INTERNAL_SERVER_ERROR

@usuario_blueprint.route('/crear_usuario', methods=['POST'])
def crear_usuario():
    # Obtener los datos del usuario del cuerpo de la solicitud
    nombre = request.json.get('nombre')
    correo = request.json.get('correo')
    password = request.json.get('password')

    # Verificar si se proporcionaron todos los datos necesarios
    if nombre and correo and password:
        try:
            usuario = usuarioService.obtener_usuario_por_correo(correo)
            if usuario:
                return jsonify({'error': 'El correo ya está en uso'}), HTTPStatus.BAD_REQUEST
            usuarioService.crear_usuario(nombre, correo, password)
            return jsonify({'mensaje': 'Usuario creado exitosamente'}), HTTPStatus.CREATED
        except:
            return jsonify({'error': 'Error al crear el usuario'}), HTTPStatus.INTERNAL_SERVER_ERROR
    else:
        return jsonify({'error': 'Faltan datos del usuario'}), HTTPStatus.BAD_REQUEST

@usuario_blueprint.route('/edit', methods=['PUT'])
def edit_usuario(): #NO ME ACTUALIZA EL CORREO
    try:
        registrado = session.get("register")
        if session is None or not registrado:
            return jsonify({'error': 'El usuario no tiene sesión o no está registrado'}), HTTPStatus.UNAUTHORIZED
        rol = session.get("rol")
        usuario_actual_id = session.get("usuario_id")
        id = request.json.get('id')
        if rol != 1 and usuario_actual_id != id:
            return jsonify({'error': 'El usuario no tiene permisos para editar este usuario'}), HTTPStatus.UNAUTHORIZED
        nuevo_nombre = request.json.get('nuevo_nombre')
        nuevo_correo = request.json.get('nuevo_correo')
        nueva_password = request.json.get('nueva_password')

        # Verificar si se proporcionaron todos los datos necesarios
        if nuevo_nombre and nuevo_correo and nueva_password and id:
            if len(nuevo_nombre) < 2:
                print("Error en registro: El nombre debe tener al menos 2 caracteres")
                return jsonify({"error": "El nombre debe tener al menos 2 caracteres"}), HTTPStatus.BAD_REQUEST
            if len(nueva_password) < 8:
                print("Error en registro: La contraseña debe tener al menos 8 caracteres")
                return jsonify({"error": "La contraseña debe tener al menos 8 caracteres"}), HTTPStatus.BAD_REQUEST
            try:
                usuario = usuarioService.obtener_usuario_por_id(id)
                if not usuario:
                    return jsonify({'error': 'Usuario no encontrado'}), HTTPStatus.NOT_FOUND
                usuarioService.actualizar_usuario(nuevo_nombre, nuevo_correo, nueva_password, id)
                return jsonify({'mensaje': 'Usuario actualizado exitosamente'}), HTTPStatus.OK
            except:
                return jsonify({'error': 'Error al actualizar el usuario'}), HTTPStatus.INTERNAL_SERVER_ERROR
        else:
            return jsonify({'error': 'Faltan datos del usuario'}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        print(e)
        return jsonify({'error': "Error al actualizar usuario"}), HTTPStatus.INTERNAL_SERVER_ERROR
    
@usuario_blueprint.route('/delete/<string:id>', methods=['DELETE'])
def eliminar_usuario(id):
    # Verificar si el usuario existe
    try:
        registrado = session.get("register")
        if session is None or not registrado:
            return jsonify({'error': 'El usuario no tiene sesión o no está registrado'}), HTTPStatus.UNAUTHORIZED
        rol = session.get("rol")
        usuario_actual_id = session.get("usuario_id")
        if rol != 1 and usuario_actual_id != id:
            return jsonify({'error': 'El usuario no tiene permisos para editar este usuario'}), HTTPStatus.UNAUTHORIZED
        usuario_existente = usuarioService.obtener_usuario_por_id(id)
        if usuario_existente:
            # Eliminar el usuario utilizando UsuariosDAO
            usuarioService.eliminar_usuario(id)
            return jsonify({'mensaje': 'Usuario eliminado exitosamente'}), HTTPStatus.OK
        else:
            return jsonify({'error': 'Usuario no encontrado'}), HTTPStatus.NOT_FOUND
    except Exception as e:
        print(e)
        return jsonify({'error': "Error al eliminar usuario"}), HTTPStatus.INTERNAL_SERVER_ERROR
    
# @usuario_blueprint.route('/obtenerDashboard', methods=['GET'])
# def get_dashboards():
#     try:
#         # session = request.environ.get('beaker.session')
#         registrado = session.get("register")
#         httpId = session.get('_id')
#         usuario_id = session.get('usuario_id')
#         if session is None or not registrado or httpId not in httpSessions or usuario_id is None:
#             return jsonify({'error': 'El usuario no tiene sesión o no está registrado'}), HTTPStatus.NOT_FOUND #raise NoSessionSetException("El usuario no tiene sesión o no está registrado")
#         usuarioService.obtener_dashboard(usuario_id)
        