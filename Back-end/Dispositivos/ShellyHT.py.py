import sys
import json
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
# print("Directorio actual:", current_dir)
config_file_absolute = os.path.join(current_dir, '..')
# print("Ruta anterior", config_file_absolute)
sys.path.append(config_file_absolute)
# print(sys.path)
from App.services.mongo_dispositivo_service import dispositivoService
# from App.services.mysql_dispositivo_service import mysql_dispositivoService
from App.model.mysql_dispositivo import mysql_dispositivo

# Función principal que procesa los argumentos y realiza el procesamiento del libro
def main():
    # print("En ShellyHT.py")
    if len(sys.argv) < 6:
        print("Error: Se requieren más argumentos. <msg> <id> <nombre> <dispositivo_creado> <atributos>")
        return
    
    # for i in range(0, len(sys.argv)):
    #     print(f"Argumento {i}: {sys.argv[i]}")  

    # Cargar el objeto JSON del primer argumento
    try:
        print(f"Argumento 1: {sys.argv[1]}")
        msg_json = json.loads(sys.argv[1])
        # print(f"Mensaje JSON: {msg_json}")
    except json.JSONDecodeError:
        print("Error: El primer argumento no es un JSON válido.")
        return
    
    try:
        id = sys.argv[2]
    except Exception as e:
        print(f"Error: El segundo argumento no es un nombre válido. {e}")
        return
    
    # Acceder a los datos dentro del objeto JSON
    # Ejemplo de cómo acceder a los datos:
    params = msg_json.get('params', '')
    temperatura = params["temperature:0"]["tC"]
    if isinstance(temperatura,int) or isinstance(temperatura,float):
        temperatura = round(temperatura, 2)
    else:
        temperatura = None
        print("Error: La temperatura no es un número.")
        return
    
    humedad = params["humidity:0"]["rh"]
    if isinstance(humedad,int) or isinstance(humedad,float):
        humedad = round(humedad, 2)
    else:
        humedad = None
        print("Error: La humedad no es un número.")
        return
    bateria = params["devicepower:0"]["battery"]["percent"]
    if isinstance(bateria,int) or isinstance(bateria,float):
        bateria = round(bateria, 2)
    else:
        bateria = None
        print("Error: La batería no es un número.")
        return
    lista = [temperatura, humedad, bateria]
    atributos_dict = {}
    for i in range(3, len(sys.argv)):
        key= sys.argv[i]
        atributos_dict[key] = lista[i-3]
        # print(f"Data: {atributos_dict}")

    dispositivo_service = dispositivoService()
    dispositivo_service.almacenarMedicion(atributos_dict, id)

    for clave, valor in atributos_dict.items():
        print(f"{clave}:{valor}", end="|")


# Llama a la función principal si el script se ejecuta de manera independiente
if __name__ == "__main__":
    main()