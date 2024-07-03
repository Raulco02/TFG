import xml.etree.ElementTree as ET
import subprocess
import os
import json
import secrets
import App.services.integracion_service as integracion_service
import App.services.mysql_dispositivo_service as mysql_dispositivo_service
from App.model import mysql_dispositivo
from App.helpers.poll_dispositivos_integraciones import poll

class procesamiento_config:
    def __init__(self, configParser):
        # Parse the XML file
        config_file_relative = configParser['FILES']['config']
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        print("Directorio actual:", self.current_dir)
        config_file_absolute = os.path.join(self.current_dir, '..', config_file_relative)
        print("Ruta de config.xml:", config_file_absolute)
        tree = ET.parse(config_file_absolute)
        self.root = tree.getroot()
        self.topic_to_sensor = {sensor.find('topic').text: sensor for sensor in self.root.findall('sensor')}
        self.dispositivo_service = mysql_dispositivo_service.mysql_dispositivoService()
        # self.integracion_service = integracion_service.integracionService()
        self.poll_thread = poll()
        self.poll_thread.start()
        ##Si obtengo integraciones, puedo comprobar que los dispositivos tengan los atributos que deben, y si no, dar error y pedir que cambien el XML o la integración
        ##Si cambio la integracion directamente en vez de levantar el error, puedo causar errores en cadena en otros dispositivos, por lo que no es buena idea
    
    def obtenerDatos(self):
        self.dispositivos = self.poll_thread.getDispositivos()
        self.integraciones = self.poll_thread.getIntegraciones()
        print("Dispositivos:", self.dispositivos)
        print("Integraciones:", self.integraciones)
        # self.dispositivos = self.dispositivo_service.obtener_dispositivos()
        # self.integraciones = self.integracion_service.obtener_integraciones()

    def procesarSensor(self, msg):
        self.obtenerDatos()
        self.imprimirDispositivo()
        topic_recibido = msg.topic
        sensor = self.topic_to_sensor.get(topic_recibido)
        if sensor:
            print(sensor.find('topic').text)
            print(sensor.find('id').text)
            print(sensor.find('nombre').text)
            argumentos = []
            nombre = sensor.find('nombre').text ##Habría que obtener una lista de nombres de la mySQL y comprobar si está, en caso contrario, meterlo
            id = sensor.find('id').text
            dispositivo_creado = self.comprobarDispositivo(id)
            print("Dispositivo creado:", dispositivo_creado)
            message = msg.payload.decode('utf-8', 'replace')
            # atributos.append(message)
            # atributos.append(nombre)
            # argumentos.append(id)
            # argumentos.append(dispositivo_creado)
            argumentos.append(message)
            argumentos.append(id)
            atributos = {}
            for atributo in sensor.findall('atributo'):
                nombre_atributo = atributo.find('nombre').text
                unidad = atributo.find('unidad').text
                if unidad is not None:
                    atributos[nombre_atributo] = unidad
                else:
                    print(f"No se encontró la unidad para el atributo '{nombre_atributo}'")
                    atributos[nombre_atributo] = ' '#o None, no se
                argumentos.append(nombre_atributo)

            print('ARGUMENTOS')
            print(argumentos)
            try:
                print("Ejecutando subprocess...")
                print(sensor.find('script').text)
                output = subprocess.check_output(['python', self.current_dir+'\..\\Dispositivos\\'+sensor.find('script').text] + argumentos, universal_newlines=True)
                print(f"Subprocess output: {output}")#¿ES NECESARIO COGER EL OUTPUT?NO ESTA RELACIONADO, ¿NO?
                # Capturar solo la última línea de la salida
                if 'Error:' in output: ##No es muy robusto, debería ser más específico
                    raise ValueError(output)
                last_line = output.strip().split('\n')[-1].split('|')
                # Ahora 'last_line' contendrá la última línea de la salida del proceso
                print("La última línea de la salida del proceso es:", last_line)
                diccionario_datos = {}
                for dato in last_line:
                    if dato:  # Ignorar elementos vacíos
                        clave, valor = dato.split(":")
                        diccionario_datos[clave] = valor
                print("Diccionario de datos:", diccionario_datos)
                valores = [float(diccionario_datos[attr]) for attr in atributos.keys()]
                print("Valores:", valores)
                dispositivo = mysql_dispositivo.mysql_dispositivo(id, nombre, atributos)
                print("Dispositivo:", dispositivo.id, dispositivo.nombre, dispositivo.atributos)
                if dispositivo_creado:
                    i = 0
                    nombres_atributos = list(atributos.keys())
                    valores_dispositivo = {}
                    for valor in valores:
                        valores_dispositivo['valor'] = valor
                        valores_dispositivo['id-dispositivo'] = id
                        valores_dispositivo['nombre-atributo'] = nombres_atributos[i]
                        i += 1
                    self.dispositivo_service.valores_actuales_xml(valores)
                self.dispositivo_service.crear_dispositivo(dispositivo, valores) ##AQUI HAY ERROR DE PLANTEAMIENTO, DEBERÍA INTENTAR CREAR, Y SI NO, EDITAR
            except subprocess.CalledProcessError as e:                           ##CREO QUE DE LA FORMA QUE ESTÁ PLANTEADO, FUNCIONA COMO DEBE. FALLA TRANSACCION DE CREACION Y CAMBIA VALOR
                print("Error:", e)                                               ##AUNQUE IGUAL DEBERÍA HACER PREVALECER LO QUE HAY EN EL DOCUMENTO XML Y EDITAR ATRIBUTOS Y ESO SI CAMBIA ALGO
            
            # try:
            #     if dispositivo_creado == 'False':
            #         dispositivo = mysql_dispositivo.mysql_dispositivo(id, nombre, atributos)
            #         self.dispositivo_service.crear_dispositivo(dispositivo)
            #         print(dispositivo.id)
            #         print(dispositivo.nombre)
            #         print(dispositivo.atributos)
            #     self.dispositivo_service.crear_dispositivo(dispositivo)
            # except Exception as e:
            #     print(f"Error al crear el dispositivo: {e}")

    def getTopics(self):
        topics = []
        for sensor in self.root.findall('sensor'):
            topic = sensor.find('topic').text
            topics.append(topic)
        return topics
    
    def comprobarDispositivo(self, dispositivo_id):
        # Comprobar si el dispositivo ya está en la base de datos
        # Si no está, insertarlo
        # Si está, actualizarlo
        coincidencia = any(dispositivo_id == item['id'] for item in self.dispositivos)
        print('DISPOSITIVOS EN LA BASE DE DATOS:')
        for dispositivo in self.dispositivos:
            print(dispositivo['id'])
        return coincidencia

    def imprimirDispositivo(self):
        print('DISPOSITIVOS EN LA BASE DE DATOS:')
        for dispositivo in self.dispositivos:
            print(dispositivo['id'])
            print(dispositivo['nombre'])
            print("----")


