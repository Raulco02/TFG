import hashlib
import smtplib
import random
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from App.model.usuariosDAO import UsuariosDAO
from App.model.usuario import Usuario

nombre_id = {} ##VER SI ES NECESARIO, Y SI AQUI O EN EL CONTROLLER
security_codes = {}
users_security_code = {}

class usuarioService:
    def login(correo, password): 
        usuario_encontrado = False 
        # Crear una instancia de UsuariosDAO
        usuario_dao = UsuariosDAO()
        #print('Correo en login:',correo)
        usuario_data = usuario_dao.obtener_usuario_por_correo(correo)
        #print('Usuario_data en login', usuario_data)
        if usuario_data is not None:
            nombre_id[usuario_data[1]] = usuario_data[0]
            if usuario_data[3] == hashlib.sha256(password.encode()).hexdigest():
                usuario_encontrado = True
                print("Usuario encontrado")
                return usuario_data
            else:
                print("Contraseña incorrecta")
                return usuario_encontrado
        else:
            print("Usuario no encontrado")
            return usuario_encontrado
    
    def registrar(nombre, correo, password):
        # Crear una instancia de Usuario
        nuevo_usuario = Usuario(nombre, correo, password)

        # Crear una instancia de UsuariosDAO
        usuarios_dao = UsuariosDAO()

        # Crear el usuario utilizando UsuariosDAO
        usuarios_dao.crear_usuario(nuevo_usuario)

    def send_security_code(email, id_usuario):
        ###ERROR Failed to process message due to a permanent exception with message [BeginDiagnosticData]WASCL UserAction verdict is not None. Actual verdict is RefuseQuota, ShowTierUpgrade. OutboundSpamException: WASCL UserAction verdict is not None. Actual verdict is RefuseQuota, ShowTierUpgrade.[EndDiagnosticData]: 
        # Configurar conexión SMTP
        smtp_server = 'smtp-mail.outlook.com'
        smtp_port = 587
        sender_email = 'prueba_smartesi@outlook.com'
        password = 'Contrasena'
        security_code = ''.join(random.choices('0123456789', k=6))
        security_codes[security_code] = time.time()
        users_security_code[security_code] = id_usuario

        # Construir el correo electrónico
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = email
        message['Subject'] = 'Código de seguridad de inicio de sesión'

        body = f'Su código de seguridad es: {security_code}'
        message.attach(MIMEText(body, 'plain'))

        # Enviar el correo electrónico
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, email, message.as_string())

    def verify_security_code(security_code, id_usuario):
        print('Security code:', security_code)
        print('Security codes:', security_codes)
        print('Users security code:', users_security_code)
        print('users_security_code[security_code]', users_security_code[security_code])
        if security_code in security_codes and security_code in users_security_code:
        # Verifica si han pasado 3 minutos desde que se generó el código
            if time.time() - security_codes[security_code] <= 180 and users_security_code[security_code][0] == id_usuario:  # 180 segundos = 3 minutos
                return True
            else:
                # Elimina el código si ha expirado
                del security_codes[security_code]
                del users_security_code[security_code]
        return False
    
    def cleanup_expired_codes(): ##VER SI ES NECESARIO, Y SI SERÍA LA FORMA
        while True:
            current_time = time.time()
            # Itera sobre todos los códigos y elimina los caducados
            for code, timestamp in list(security_codes.items()):
                if current_time - timestamp > 180:  # 180 segundos = 3 minutos
                    del security_codes[code]
            # Espera 1 minuto antes de volver a verificar
            time.sleep(60)

    def obtener_usuario_por_id(id):
        usuario_dao = UsuariosDAO()
        usuario_data = usuario_dao.obtener_usuario_por_id(id)
        if(usuario_data is None):
            return None
        usuario_json = {"id": usuario_data[0], "nombre": usuario_data[1], "correo": usuario_data[2], "rol": usuario_data[4], "password": usuario_data[3]}
        return usuario_json

    def obtener_usuario_por_nombre(nombre):
        usuario_dao = UsuariosDAO()
        usuario_data = usuario_dao.obtener_usuario_por_nombre(nombre)
        return usuario_data

    def obtener_usuario_por_correo(correo):
        usuario_dao = UsuariosDAO()
        usuario_data = usuario_dao.obtener_usuario_por_correo(correo)
        return usuario_data

    def obtener_todos_los_usuarios():
        usuario_dao = UsuariosDAO()
        usuario_data = usuario_dao.obtener_todos_los_usuarios()
        usuarios_list = []
        for usuario in usuario_data:
            usuario_json = {"id": usuario[0], "nombre": usuario[1], "correo": usuario[2], "rol": usuario[4]}
            usuarios_list.append(usuario_json)
        return usuarios_list

    def crear_usuario(nombre, correo, password):
        # Crear una instancia de Usuario
        nuevo_usuario = Usuario(nombre, correo, password)

        # Crear una instancia de UsuariosDAO
        usuarios_dao = UsuariosDAO()

        # Crear el usuario utilizando UsuariosDAO
        usuarios_dao.crear_usuario(nuevo_usuario)

    def eliminar_usuario(id):
        # Crear una instancia de UsuariosDAO
        usuarios_dao = UsuariosDAO()

        # Eliminar el usuario utilizando UsuariosDAO
        usuarios_dao.eliminar_usuario(id)

    def actualizar_usuario(nuevo_nombre, nuevo_correo, nueva_password, id):
        # Crear una instancia de Usuario con los nuevos datos
        nuevo_usuario = Usuario(nuevo_nombre, nuevo_correo, nueva_password)

        # Crear una instancia de UsuariosDAO
        usuarios_dao = UsuariosDAO()

        # Actualizar el usuario utilizando UsuariosDAO
        usuarios_dao.actualizar_usuario(id, nuevo_usuario)
    