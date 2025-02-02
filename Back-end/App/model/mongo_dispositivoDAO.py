import secrets
import configparser
import os
from pymongo import MongoClient
from datetime import datetime
from App.model.agente_mongo import Agente

class mongo_dispositivoDAO:
    """
    Descripción:
    Clase para gestionar operaciones CRUD relacionadas con dispositivos en la base de datos MongoDB.
    """
    def __init__(self):
        """
        Descripción:
        Inicializa la clase mongo_dispositivoDAO cargando la configuración de MongoDB desde un archivo de configuración.

        Retorna:
        None

        Excepciones:
        KeyError: Captura y maneja cualquier excepción que ocurra al intentar leer las configuraciones del archivo secrets.cfg.
        """
        self.config = configparser.ConfigParser()
        # Configuración de MongoDB
        current_dir = os.path.dirname(os.path.abspath(__file__))
        print("Directorio actual:", current_dir)
        # Cargar la configuración desde el archivo secrets.cfg
        # Construir la ruta completa del archivo secrets.cfg
        self.secrets_path = os.path.join(current_dir, '..', '..\Config', 'secrets.cfg')
        print("Ruta de secrets.cfg:", self.secrets_path)
        self.config.read(self.secrets_path)
        try:
            self.mongodb_host = self.config['MONGODB']['mongodb_host']
            self.mongodb_port = self.config['MONGODB']['mongodb_port']
            self.mongodb_database = self.config['MONGODB']['mongodb_database']
            self.mongodb_collection = self.config['MONGODB']['mongodb_collection']
            self.mongodb_user = self.config['MONGODB']['mongodb_user']
            self.mongodb_password = self.config['MONGODB']['mongodb_password']
        except KeyError:
            print("Error: Configuración 'MONGO' no encontrada en secrets.cfg")
            self.mongodb_host = None
            self.mongodb_port = None
            self.mongodb_database = None
            self.mongodb_collection = None
            self.mongodb_user = None
            self.mongodb_password = None

    def almacenarMedicion(self, atributos, sensor):
        """
        Descripción:
        Almacena una medición en la base de datos MongoDB.

        Parámetros:
        atributos (dict): Diccionario que contiene los atributos de la medición.
        sensor (str): Identificador del sensor.

        Retorna:
        None

        Excepciones:
        Exception: Captura y maneja cualquier excepción que ocurra al intentar crear el agente de MongoDB o insertar un documento.
        """
        payload = {
            "sensor": sensor,#Cuidado
            "timestamp": datetime.utcnow(),
            "attributes": atributos
        }
        try:
            agente = Agente(self.mongodb_host, self.mongodb_port, self.mongodb_database, self.mongodb_collection, self.mongodb_user, self.mongodb_password)
        except Exception as ex:
            print(f"Error al crear el agente de MongoDB: {ex}")
        try:
            agente.insertar_documento(payload)
            print("Documento insertado correctamente en MongoDB.")
        except Exception as ex:
            print(f"Error al insertar en MongoDB: {ex}")
    
    def get_sensor_data(self, filtro, campos=None):
        """
        Descripción:
        Obtiene datos del sensor desde la base de datos MongoDB basándose en un filtro y campos opcionales.

        Parámetros:
        filtro (dict): Diccionario que contiene los criterios de búsqueda.
        campos (dict, opcional): Diccionario que especifica los campos a devolver.

        Retorna:
        list: Lista de documentos que coinciden con el filtro.

        Excepciones:
        Exception: Captura y maneja cualquier excepción que ocurra al intentar crear el agente de MongoDB o buscar documentos.
        """
        try:
            agente = Agente(self.mongodb_host, self.mongodb_port, self.mongodb_database, self.mongodb_collection, self.mongodb_user, self.mongodb_password)
        except Exception as ex:
            print(f"Error al crear el agente de MongoDB: {self.secrets_path}")
        try:
            print(filtro)
            data_cursor = agente.buscar_documentos(filtro, campos)
            #############SI NO QUIERO DEVOLVER EL OBJECT_ID ############
            data = [{key: value for key, value in doc.items() if key != '_id'} for doc in data_cursor]
            #############SI QUIERO DEVOLVER EL OBJECT_ID COMO STRING############
            # data = []
            # for doc in data_cursor:
            #     doc_dict = dict(doc)
            #     doc_dict['_id'] = str(doc_dict['_id'])  # Convertir ObjectId a str
            #     data.append(doc_dict)
            print("Documento encontrado correctamente en MongoDB.")
            return data
        except Exception as ex:
            print(f"Error al buscar en MongoDB: {ex}")
    
    def get_sensor_last_value(self, filtro):
        """
        Descripción:
        Obtiene el último valor del sensor desde la base de datos MongoDB basándose en un filtro.

        Parámetros:
        filtro (dict): Diccionario que contiene los criterios de búsqueda.

        Retorna:
        dict: Documento que contiene el último valor del sensor.

        Excepciones:
        Exception: Captura y maneja cualquier excepción que ocurra al intentar crear el agente de MongoDB o buscar un documento.
        """
        try:
            agente = Agente(self.mongodb_host, self.mongodb_port, self.mongodb_database, self.mongodb_collection, self.mongodb_user, self.mongodb_password)
        except Exception as ex:
            print(f"Error al crear el agente de MongoDB: {ex}")
        try:
            data_cursor = agente.buscar_documento(filtro, sort=[('timestamp', -1)])
            #############SI NO QUIERO DEVOLVER EL OBJECT_ID ############
            data = {key: value for key, value in data_cursor.items() if key != '_id'}
            print("Documento encontrado correctamente en MongoDB.")
            return data
        except Exception as ex:
            print(f"Error al buscar en MongoDB: {ex}")