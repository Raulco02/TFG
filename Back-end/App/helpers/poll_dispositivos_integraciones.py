import threading
import time
import App.services.mysql_dispositivo_service as mysql_dispositivo_service
from App.services.integracion_service import integracionService

class poll(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
        self.dispositivos = []
        self.integraciones = []
        self.dispositivo_service = mysql_dispositivo_service.mysql_dispositivoService()
        #self.integracion_service = integracion_service.integracionService()
        self.running = True

    def run(self):
        while self.running:
            print("Ejecutando reglas")
            self.dispositivos = self.dispositivo_service.obtener_dispositivos()
            self.integraciones = integracionService.obtener_integraciones()
            time.sleep(5)

    def stop(self):
        self.running = False

    def getDatos(self):
        return self.dispositivos, self.integraciones
    
    def getDispositivos(self):
        return self.dispositivos
    
    def getIntegraciones(self):
        return self.integraciones