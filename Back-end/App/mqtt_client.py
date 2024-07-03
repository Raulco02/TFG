from Config.procesamiento_config import procesamiento_config
from jinja2 import Template
from App.helpers.poll_dispositivos_integraciones import poll
import configparser
import paho.mqtt.client as mqtt
import os

class mqtt_client:
    def __init__(self, publish=False):
        print("Creando instancia del cliente MQTT...")
        self.configured = False
        self.publish = publish
        if publish:
            self.iniciar_cliente()
        else:
            self.run()
    
    def configurar_cliente(self):
        if not self.configured:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            print("Directorio actual:", current_dir)
            secrets_path = os.path.join(current_dir, '..', 'Config', 'secrets.cfg')
            print("Ruta de secrets.cfg:", secrets_path)
            
            self.config = configparser.ConfigParser()
            self.config.read(secrets_path)
            
            try:
                self.mqtt_broker_host = self.config['MQTT']['mqtt_broker_host'].strip()
                self.mqtt_broker_port = int(self.config['MQTT']['mqtt_broker_port'].strip())
                print(f"Host: {self.mqtt_broker_host}, Port: {self.mqtt_broker_port}")
            except KeyError:
                print("Error: Configuración 'MQTT' no encontrada en secrets.cfg")
                self.mqtt_broker_host = None
                self.mqtt_broker_port = None

            try:
                if self.publish is False:
                    self.xml_config = procesamiento_config(self.config)
                    self.topics = self.getTopics()
                    print(f"Configuración XML: {self.xml_config}, Topics: {self.topics}")
            except KeyError:
                print("Error: Configuración 'FILES' no encontrada en secrets.cfg")
                self.xml_config = None
                self.topics = None
            
            self.configured = True
    
    def iniciar_cliente(self):
        self.configurar_cliente()
        try:
            self.mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
        except Exception as e:
            print(f"Error al iniciar el cliente MQTT: {e}")

    def run(self):
        # poll_thread = poll() ########Comprobar que esto funciona#######QUIZAA SE INICIALIZA EN PROCESAMIENTO
        # poll_thread.start()
        self.configurar_cliente()
        try:
            self.mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
            self.mqtt_client.on_message = self.on_message
            self.mqtt_client.connect(self.mqtt_broker_host, self.mqtt_broker_port, 60)

            for topic in self.topics:
                self.mqtt_client.subscribe(topic)

            print("Iniciando el cliente MQTT...")
            self.mqtt_client.loop_forever()
        except Exception as e:
            print(f"Error al iniciar el cliente MQTT: {e}")

    def publish_message(self, topic, plantilla, datos):
        print("Conectando con broker MQTT...")
        self.configurar_cliente()
        try:
            print("Renderizando plantilla...")
            payload = Template(plantilla).render(datos)
            print("Publicando mensaje MQTT...", payload)
            self.mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
            self.mqtt_client.connect(self.mqtt_broker_host, self.mqtt_broker_port, 60)
            self.mqtt_client.publish(topic, payload)
            self.mqtt_client.disconnect()
            return True
        except Exception as e:
            print(f"Error al publicar mensaje MQTT: {e}")
            return False

    def on_message(self, client, userdata, msg):
        try:
            ##Cada vez que me llega un mensaje pido todo dispositivos y todo integraciones, carga alta
            self.xml_config.procesarSensor(msg)
        except Exception as e:
            print(f"Error al procesar mensaje: {e}")

    def getTopics(self):
        return self.xml_config.getTopics()
    
if __name__ == '__main__':
    cliente_mqtt = mqtt_client()


# from Config.procesamiento_config import procesamiento_config
# from jinja2 import Template
# import configparser
# import paho.mqtt.client as mqtt
# import os

# class mqtt_client:
#     def __init__(self, publish=False):
#         print("Creando instancia del cliente MQTT...")
#         if publish:
#             self.iniciar_cliente()
#         else:
#             self.run()
#         # threading.Thread.__init__(self)

#     def iniciar_cliente(self):
#         current_dir = os.path.dirname(os.path.abspath(__file__))
#         print("Directorio actual:", current_dir)
#         # Cargar la configuración desde el archivo secrets.cfg
#         # Construir la ruta completa del archivo secrets.cfg
#         secrets_path = os.path.join(current_dir, '..', 'Config', 'secrets.cfg')
#         print("Ruta de secrets.cfg:", secrets_path)

#         # Leer el archivo de configuración
#         self.config = configparser.ConfigParser()
#         self.config.read(secrets_path)
        
#         # Configuración del broker MQTT
#         # Acceder a las configuraciones específicas
#         try:
#             self.mqtt_broker_host = self.config['MQTT']['mqtt_broker_host']
#             self.mqtt_broker_port = self.config['MQTT']['mqtt_broker_port']
#         except KeyError:
#             print("Error: Configuración 'MQTT' no encontrada en secrets.cfg")
#             self.mqtt_broker_host = None
#             self.mqtt_broker_port = None

#         try:
#             self.xml_config = procesamiento_config(self.config)
#             self.topics = self.getTopics() 
#         except KeyError:
#             print("Error: Configuración 'FILES' no encontrada en secrets.cfg")
#             self.xml_config = None
#             self.topics = None

#         try:
#             # Configuración del cliente MQTT
#             mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
#         except Exception as e:
#             print(f"Error al iniciar el cliente MQTT: {e}")

#     def run(self):
#         current_dir = os.path.dirname(os.path.abspath(__file__))
#         print("Directorio actual:", current_dir)
#         # Cargar la configuración desde el archivo secrets.cfg
#         # Construir la ruta completa del archivo secrets.cfg
#         secrets_path = os.path.join(current_dir, '..', 'Config', 'secrets.cfg')
#         print("Ruta de secrets.cfg:", secrets_path)

#         # Leer el archivo de configuración
#         self.config = configparser.ConfigParser()
#         self.config.read(secrets_path)
        
#         # Configuración del broker MQTT
#         # Acceder a las configuraciones específicas
#         try:
#             self.mqtt_broker_host = self.config['MQTT']['mqtt_broker_host']
#             self.mqtt_broker_port = self.config['MQTT']['mqtt_broker_port']
#         except KeyError:
#             print("Error: Configuración 'MQTT' no encontrada en secrets.cfg")
#             self.mqtt_broker_host = None
#             self.mqtt_broker_port = None

#         try:
#             self.xml_config = procesamiento_config(self.config)
#             self.topics = self.getTopics() 
#         except KeyError:
#             print("Error: Configuración 'FILES' no encontrada en secrets.cfg")
#             self.xml_config = None
#             self.topics = None

#         try:
#             # Configuración del cliente MQTT
#             mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
#             mqtt_client.on_message = self.on_message
#             mqtt_client.connect(self.mqtt_broker_host, int(self.mqtt_broker_port), 60)

#             for topic in self.topics:
#                 mqtt_client.subscribe(topic)

#             # Iniciar el bucle de recepción de mensajes
#             print("Iniciando el cliente MQTT...")
#             mqtt_client.loop_forever()

#         except Exception as e:
#             print(f"Error al iniciar el cliente MQTT: {e}")


#     # Función para manejar mensajes MQTT
#     def on_message(self, client, userdata, msg):
#         try:
#             self.xml_config.procesarSensor(msg)
#         except Exception as e:
#             print(f"Error al procesar mensaje: {e}")

#         # try:
#         #     payload = json.loads(msg.payload.decode('utf-8', 'replace'))
#         # except json.decoder.JSONDecodeError as e:
#         #     print(f"Ignorando mensaje no JSON: {msg.payload}")
#         #     return  # Salir de la función si no es JSON válido

#         # # Verificar si el payload es un diccionario (JSON válido)
#         # if isinstance(payload, dict):
#         #     payload['timestamp'] = datetime.utcnow()
#         #     payload['topic'] = msg.topic

#         #     # Almacenar en MongoDB
#         #     agente = Agente(self.mongodb_host, self.mongodb_port)
#         #     try:
#         #         agente.insertar_documento(payload)
#         #         print("Documento insertado correctamente en MongoDB.")
#         #     except Exception as ex:
#         #         print(f"Error al insertar en MongoDB: {ex}")
#         #     finally:
#         #         client.close()

#     def getTopics(self):
#         return self.xml_config.getTopics()
    
#     # def start_mqtt_loop(self):
#     #     # Iniciar el hilo para el bucle de recepción de mensajes MQTT
#     #     self.run()

#     # def publish(self, topic, plantilla, datos):
#     #     # Publicar un mensaje en un tópico MQTT
#     #     try:
#     #         print("Publicando mensaje MQTT...")
#     #         # Renderizar la plantilla con los datos
#     #         payload = Template(plantilla).render(datos)
#     #         print(payload)
#     #         mqtt_client = mqtt.Client()
#     #         mqtt_client.connect(self.mqtt_broker_host, int(self.mqtt_broker_port), 60)
#     #         mqtt_client.publish(topic, payload)
#     #         mqtt_client.disconnect()
#     #         return True
#     #     except Exception as e:
#     #         print(f"Error al publicar mensaje MQTT: {e}")
#     #         raise
    

# if __name__ == '__main__':
#     cliente_mqtt = mqtt_client()

