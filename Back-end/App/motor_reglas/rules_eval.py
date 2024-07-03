import threading
import time
import re
from App.services.mysql_dispositivo_service import mysql_dispositivoService 

class RulesEval(threading.Thread):
    def __init__(self):
        super().__init__()
        self.rules_eval_dict = {}
        self.running = True  # Bandera para controlar la ejecución del hilo
        self.rules = None  # Objeto que se recibirá en cada ejecución

    def run(self):
        while self.running:
            if self.rules and self.rules != []:
                # Aquí procesas self.data_to_process según sea necesario
                print("Procesando el objeto:", self.rules)
                # Por cada regla, obtener los valores de los dispositivos y atributos
                dispositivos_atributos = []
                for regla in self.rules:
                    print(f"Regla: {regla}")
                    print(f"Dispositivo values: {regla['valores_dispositivos']}")
                    for dv in regla['valores_dispositivos']:
                        dispositivos_atributos.append((dv['dispositivo_id'], dv['atributo_id']))

                # Después de tener el valor, evaluar las reglas con el valor y guardar diccionario {regla_id: resultado}
                print(f"Dispositivos y atributos a consultar: {dispositivos_atributos}")
                device_values = mysql_dispositivoService().obtener_valores_dispositivos_atributos(dispositivos_atributos)
                for regla in self.rules:
                    print(f"Regla: {regla}")
                    disparador_final = regla['trigger']
                    condicion_final = regla['condition']

                    # Reemplazar valores en disparador_final
                    disparador_final = self.reemplazar_valores(disparador_final, device_values)

                    # Reemplazar valores en condicion_final
                    condicion_final = self.reemplazar_valores(condicion_final, device_values) #Creo que devuelve un string y a lo mejor es un problema al evaluar

                    print("Disparador, condicion,",disparador_final,condicion_final)
                    # Evaluar las expresiones lógicas
                    try:
                        disparador_valido = eval(disparador_final) #Hay que ver lo que evalua, porque el valor es string
                        condicion_valida = eval(condicion_final)
                        self.rules_eval_dict[regla['id']] = disparador_valido and condicion_valida
                        print(f"Regla {regla['id']} evaluada como {self.rules_eval_dict[regla['id']]}")
                        print(f"Disparador: {disparador_final}, Condición: {condicion_final}")
                        print(f"Evaluación: {self.rules_eval_dict[regla['id']]}")
                        print(f"Valores de dispositivos: {device_values}")
                    except Exception as e:
                        print(f"Error al evaluar la regla {regla['id']}: {e}")
                        self.rules_eval_dict[regla['id']] = False
                
                # device_values_dict = {}
                # for device_value in device_values:
                #     device_id = device_value['dispositivo_id']
                #     attribute_id = device_value['atributo_id']
                #     value = device_value['valor']
                #     if device_id not in device_values_dict:
                #         device_values_dict[device_id] = {}
                #     device_values_dict[device_id][attribute_id] = value


                self.rules = None  # Reinicia el objeto después de procesarlo. ¿Se debe reiniciar esto?
            time.sleep(10)  # Espera 10 segundos antes de volver a ejecutar

    def reemplazar_valores(self, expresion, valores):
        def reemplazar_match(match):
            dispositivo_id, atributo_id = match.group(1), int(match.group(2))
            # Buscar en la lista de diccionarios el valor correspondiente
            for val in valores:
                if val['dispositivo_id'] == dispositivo_id and val['atributo_id'] == atributo_id:
                    return str(val['valor'])
            return 'None'

        # Usar expresiones regulares para encontrar y reemplazar todos los placeholders
        return re.sub(r'/([^/]+)-(\d+)/', reemplazar_match, expresion)

    def get_rules_eval_dict(self):
        return self.rules_eval_dict

    def stop(self):
        self.running = False

    def set_rules(self, rules):
        self.rules = rules
