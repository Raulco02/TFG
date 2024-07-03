    # def _update_state(self, data):
    #     self._state = int(data[11]) * 256 + int(data[12])
    #     self._attributes['Temperature'] = (int(data[1]) * 256 + int(data[2]))/10
    #     self._attributes['Humidity'] = int(data[4]) 
    #     self._attributes['Light'] = (int(data[6]) *256 + int(data[7])) 
    #     self._attributes['Motion'] = int(data[9]) 
    #     self._attributes['CO2'] = int(data[11]) * 256 + int(data[12])
    #     self._attributes['Vdd'] = int(data[14]) * 256 + int(data[15])
    #     self.schedule_update_ha_state()
import sys
import json
import base64
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
print("Directorio actual:", current_dir)
config_file_absolute = os.path.join(current_dir, '..')
print("Ruta anterior", config_file_absolute)
sys.path.append(config_file_absolute)
print(sys.path)
from App.services.mongo_dispositivo_service import dispositivoService

# Función principal que procesa los argumentos y realiza el procesamiento del xml
def main():
    print("En Lora.py")
    if len(sys.argv) < 4:
        print("Error: Se requieren más argumentos. <msg> <nombre> <atributos>")
        return
    
    for i in range(0, len(sys.argv)):
        print(f"Argumento {i}: {sys.argv[i]}")  

    # Cargar el objeto JSON del primer argumento
    try:
        msg_json = json.loads(sys.argv[1])
        print(f"Mensaje JSON: {msg_json}")
    except json.JSONDecodeError:
        print("Error: El primer argumento no es un JSON válido.")
        return
    
    try:
        nombre = sys.argv[2]
        print(f"Nombre: {nombre}")
    except Exception as e:
        print(f"Error: El segundo argumento no es un nombre válido. {e}")
        return
    
    # Acceder a los datos dentro del objeto JSON
    # Ejemplo de cómo acceder a los datos:
    data = msg_json.get('data', '')
    data = base64.b64decode(data)
    # data = int.from_bytes(data, byteorder='big')
    co2 = int(data[11]) * 256 + int(data[12])
    Temperatura = (int(data[1]) * 256 + int(data[2]))/10
    Humedad = int(data[4]) 
    Luz = (int(data[6]) *256 + int(data[7])) 
    Presencia = int(data[9]) 
    Bateria = int(data[14]) * 256 + int(data[15])
    lista = [Temperatura, Humedad, Bateria, co2, Presencia, Luz]
    atributos = {}
    for i in range(3, len(sys.argv)):
        key= sys.argv[i]
        atributos[key] = lista[i-3]
        print(f"Data: {atributos}")

    dispositivoService.almacenarMedicion(atributos, nombre)

# Llama a la función principal si el script se ejecuta de manera independiente
if __name__ == "__main__":
    main()