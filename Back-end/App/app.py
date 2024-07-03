import sys
import secrets
import threading
import signal
import atexit
from flask import Flask
from flask_cors import CORS
from flask_session import Session
from beaker.middleware import SessionMiddleware
from App.controllers.historico_controller import historico_blueprint
from App.controllers.dispositivo_controller import dispositivo_blueprint
from App.controllers.usuario_controller import usuario_blueprint
from App.controllers.dashboard_controller import dashboard_blueprint
from App.controllers.seccion_controller import seccion_blueprint
from App.controllers.tarjeta_controller import tarjeta_blueprint
from App.controllers.integracion_controller import integracion_blueprint
from App.controllers.grupo_controller import grupo_blueprint
from App.controllers.regla_controller import regla_blueprint
from App.motor_reglas.motor_reglas import MotorReglas

# # Crear una instancia del cliente MQTT
# cliente_mqtt = mqtt_client()

# if __name__ == '__main__':
#     mqtt_client.run

# Crear una instancia de la aplicación Flask
app = Flask(__name__)
# Configuración de CORS para permitir credenciales
cors = CORS(app, supports_credentials=True)
# app.config['SESSION_TYPE'] = 'filesystem' 
# app.config['SECRET_KEY'] = os.urandom(24)
# Session(app)

# Configuración de la sesión con Beaker
session_key = secrets.token_hex(32)
session_opts = {
    'session.type': 'file',
    'session.data_dir': './data',
    'session.auto': True,
    'session.cookie_expires': True,
    'session.key': session_key
}

app.secret_key = session_key

# Configurar la base de datos, extensiones, etc.

# Registrar blueprints
app.register_blueprint(historico_blueprint, url_prefix='/historico')
app.register_blueprint(dispositivo_blueprint, url_prefix='/dispositivo')
app.register_blueprint(usuario_blueprint, url_prefix='/usuario')
app.register_blueprint(dashboard_blueprint, url_prefix='/dashboard')
app.register_blueprint(seccion_blueprint, url_prefix='/seccion')
app.register_blueprint(tarjeta_blueprint, url_prefix='/tarjeta')
app.register_blueprint(integracion_blueprint, url_prefix='/integracion')
app.register_blueprint(grupo_blueprint, url_prefix='/grupo')
app.register_blueprint(regla_blueprint, url_prefix='/regla')



# def signal_handler(sig, frame):
#     print("Programa terminado.")
#     stop_motor_reglas(motor_reglas_instance)
#     sys.exit(0)

# # Registra la función de manejo de señales para SIGTERM en Windows o SIGINT en Linux

# signal.signal(signal.SIGTERM, signal_handler)
# signal.signal(signal.SIGINT, signal_handler)

# def start_motor_reglas():
#     # motorReglas = motor_reglas.motorReglas()
#     # rule_engine_thread = threading.Thread(target=motorReglas.check_rules, daemon=True)
#     # rule_engine_thread.start()
#     motorReglas = motor_reglas.motorReglas() #Yo creo que no es necesario crear hilo de check porque lo hace la clase motor_reglas
#     #rule_engine_thread = threading.Thread(target=motorReglas.check_rules, daemon=True)
#     #rule_engine_thread.start()
#     return motorReglas

# def stop_motor_reglas(motor_reglas_instance):
#     motor_reglas_instance.stop()

if __name__ == '__main__':
#     # Registrar la función de manejo de señales para SIGINT
#     signal.signal(signal.SIGINT, signal_handler)###########NO FUNCIONA EN WINDOWS

#     # Crear un hilo para ejecutar el cliente MQTT
#     mqtt_thread = threading.Thread(target=cliente_mqtt.run)
#     mqtt_thread.start()
    try:
        # motor_reglas_instance = start_motor_reglas()

        # atexit.register(stop_motor_reglas, motor_reglas_instance)


        # motorReglas = MotorReglas()
        # motorReglas.start()

        # Ejecutar la aplicación Flask en el hilo principal
        app.wsgi_app = SessionMiddleware(app.wsgi_app, session_opts)
        #start_motor_reglas()
        app.run(debug=True)
    except SystemExit as e:
        # stop_motor_reglas(motor_reglas_instance)


        # if motorReglas:
        #     motorReglas.stop()
        sys.exit(0)
