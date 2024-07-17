from App.model.mongo_dispositivoDAO import mongo_dispositivoDAO
class dispositivoService:
    """
    Descripción:
    Servicio para interactuar con dispositivos y gestionar mediciones almacenadas en una base de datos MongoDB.
    """
    def almacenarMedicion(self, atributos, sensor):
        """
        Descripción:
        Almacena mediciones de un sensor en la base de datos MongoDB.

        Parámetros:
        atributos (dict): Diccionario con los atributos de la medición.
        sensor (str): Nombre o identificador del sensor que realiza la medición.

        Retorna:
        None

        Excepciones:
        Exception: Captura y maneja cualquier excepción que ocurra al intentar almacenar la medición.
        """
        sensorDAO = mongo_dispositivoDAO()
        sensorDAO.almacenarMedicion(atributos, sensor)
    
    def get_sensor_data(self, filtro):
        """
        Descripción:
        Obtiene datos de sensores almacenados en la base de datos MongoDB según un filtro especificado.

        Parámetros:
        filtro (dict): Diccionario con condiciones de filtro para la consulta.

        Retorna:
        list: Lista de datos de los sensores que cumplen con el filtro especificado.

        Excepciones:
        Exception: Captura y maneja cualquier excepción que ocurra al intentar obtener los datos del sensor.
        """
        sensorDAO = mongo_dispositivoDAO()
        data = sensorDAO.get_sensor_data(filtro)
        return data