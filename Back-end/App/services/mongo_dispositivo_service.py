from App.model.mongo_dispositivoDAO import mongo_dispositivoDAO
class dispositivoService:
    def almacenarMedicion(self, atributos, sensor):
        sensorDAO = mongo_dispositivoDAO()
        sensorDAO.almacenarMedicion(atributos, sensor)
    
    def get_sensor_data(self, filtro):
        sensorDAO = mongo_dispositivoDAO()
        data = sensorDAO.get_sensor_data(filtro)
        return data