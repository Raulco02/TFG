import threading
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from App.services.usuario_service import usuarioService
from App.services.mysql_dispositivo_service import mysql_dispositivoService
from App.motor_reglas.rules_list import RulesList
from App.motor_reglas.rules_eval import RulesEval

class MotorReglas(threading.Thread):
    """
    Descripción:
    Clase que representa el motor de ejecución de reglas. Gestiona la evaluación y ejecución de reglas y alertas basadas en eventos.
    """
    def __init__(self):
        """
        Inicializa el MotorReglas con configuraciones predeterminadas.
        """
        super().__init__()
        self.daemon = True
        self.running = True
        self.rules = None
        self.rules_eval_dict = None
        self.last_execution_time = {}
        self.last_evaluated_triggers = {}
        self.last_evaluated_conditions = {}
        self.rules_list = RulesList()
        self.rules_eval = RulesEval()
        self.rules_list.daemon = True
        self.rules_eval.daemon = True
        self.rules_list.start()
        self.rules_eval.start()
        
        ##¿Crear y lanzar aqui los otros dos hilos?

    def run(self):
        while self.running:
            self.set_rules()
            self.rules_eval.set_rules(self.rules)
            self.set_rules_eval_dict()
            if self.rules and self.rules != [] and self.rules_eval_dict and self.rules_eval_dict != {}:
                self.check_rules()
            time.sleep(1)  # Espera 1 segundo antes de volver a ejecutar

    def set_rules_eval_dict(self):
        self.rules_eval_dict = self.rules_eval.get_rules_eval_dict() #Parentesis?

    def stop(self):
        self.running = False
        self.rules_list.stop()
        self.rules_eval.stop()
        self.rules_list.join()
        self.rules_eval.join()
        #¿Les hago el join?

    def set_rules(self):
        self.rules = self.rules_list.get_rules_list() #Parentesis?

    def check_rules(self): ##Revisar lo de los triggers y demás
        for rule in self.rules:
            current_time = time.time()
            if current_time - self.last_execution_time.get(rule['id'], 0) > 60: #¿Mayor tiempo? ¿Solo una vez hasta que cambie?
                rules_eval = self.rules_eval.get_rules_eval_dict() #Parentesis?
                rule_id = rule['id']
                print(f"Regla {rule_id}:")
                print(f"rules:{self.rules}")
                print(f"rules_eval: {rules_eval}")
                print(f"rules_eval[rule]: {rules_eval[rule['id']]}")
                print(f"last_execution_time:", self.last_execution_time)
                if rule_id in rules_eval and rules_eval[rule['id']] == True:
                    try:
                        print('Ejecutando acción...', rule['id'] ,rule['action'])
                        exec(rule['action'])
                    except Exception as e:
                        print(f"Error al ejecutar la acción de la regla {rule['id']}: {e}")
                    finally:
                        self.last_execution_time[rule['id']] = time.time()

    def alert(self, texto, id_regla):
        regla = next(rule for rule in self.rules if rule['id'] == id_regla)

        usuario = usuarioService.obtener_usuario_por_id(regla['user'])
        email = usuario['correo']
        print(f"Enviando alerta a {email}...")

        smtp_server = 'smtp-mail.outlook.com'
        smtp_port = 587
        sender_email = 'prueba_smartesi@outlook.com'
        password = 'Contrasena'

        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = email
        message['Subject'] = 'Alerta de seguridad Smart ESI'

        body = f'Alerta Smart ESI: {texto}'
        message.attach(MIMEText(body, 'plain'))

        # Enviar el correo electrónico
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, email, message.as_string())
        print(f"Alerta: {texto}, ID regla: {id_regla}, ID usuario: {regla['user']}")


# # rule_engine.py
# import threading
# import time
# import smtplib
# import signal
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from App.services.regla_service import reglaService
# from App.services.mysql_dispositivo_service import mysql_dispositivoService
# from App.services.usuario_service import usuarioService

# running = True
# class motorReglas:
#     def __init__(self):
#         # self.rules = []
#         # #self.acciones_pendientes = {}
#         # self.rules = self.load_rules()
#         # self.last_execution_time = {}
#         signal.signal(signal.SIGINT, self.parar)
#         signal.signal(signal.SIGTERM, self.parar)
#         self.corriendo = True

#         self.rules = []
#         self.device_values_cache = {}
#         self.last_execution_time = {}
#         self.last_evaluated_triggers = {}
#         self.last_evaluated_conditions = {}
#         self.lock = threading.Lock()
#         self.stop_event = threading.Event()
#         self.load_rules()
#         # self.schedule_periodic_device_value_update()
#         # self.schedule_periodic_rule_reload()
#         self.device_value_update_thread = threading.Thread(target=self.schedule_periodic_device_value_update)
#         self.rule_reload_thread = threading.Thread(target=self.schedule_periodic_rule_reload)
#         self.rule_check_thread = threading.Thread(target=self.check_rules)
#         self.start_threads()
#         print(self.rules)

#     def parar(self, signum, frame):
#         self.corriendo = False
#         self.stop_event.set()
#         global running
#         running = False
#         print("Running", running)
#         print("Corriendo", self.corriendo)
    
#     def start_threads(self):
#         self.device_value_update_thread.start()
#         self.rule_reload_thread.start()
#         self.rule_check_thread.start()

#     def stop(self):
#         print("En stop")
#         self.stop_event.set()
#         global running
#         running = False
#         print("Running", running)
#         self.device_value_update_thread.join(timeout=10)
#         print("Hilo de actualización de valores de dispositivos detenido.")
#         self.rule_reload_thread.join(timeout=10)
#         print("Hilo de recarga de reglas detenido.")
#         self.rule_check_thread.join(timeout=10)
#         print("Hilo de verificación de reglas detenido.")
#         print("Motor de reglas detenido.")

#     def schedule_periodic_rule_reload(self):
#         #threading.Timer(60, self.reload_rules).start()
#         try:
#             global running
#             while running:
#                 # print("Recargando reglas...", not self.stop_event.is_set())
#                 # print(f"Reglas actuales: {self.rules}")
#                 # print(f"Última ejecución de reglas: {self.last_execution_time}")
#                 with self.lock:
#                     self.rules = self.load_rules()
#                 self.stop_event.wait(10)
#         except Exception as e:
#             print(f"Error al recargar reglas: {e}")
#             #self.schedule_periodic_rule_reload()

#     def schedule_periodic_device_value_update(self):
#         #threading.Timer(10, self.update_device_values).start()
#         try:
#             while running:
#                 # print("Actualizando valores de dispositivos...", not self.stop_event.is_set())
#                 # print(f"Reglas actuales: {self.rules}")
#                 # print(f"Última ejecución de reglas: {self.last_execution_time}")
#                 with self.lock:
#                     self.device_values_cache = self.load_device_values()
#                     print(f"Valores de dispositivos actualizados: {self.device_values_cache}")
#                 self.stop_event.wait(10)
#         except Exception as e:
#             print(f"Error al actualizar valores de dispositivos: {e}")
#             #self.schedule_periodic_device_value_update()

#     # def reload_rules(self):
#     #     with self.lock:
#     #         self.rules = self.load_rules()
#     #     self.schedule_periodic_rule_reload()

#     def update_device_values(self):
#         with self.lock:
#             self.device_values_cache = self.load_device_values()
#             print(f"Valores de dispositivos actualizados: {self.device_values_cache}")
#         self.schedule_periodic_device_value_update()
    
#     def load_device_values(self):
#         # Implementa la lógica para cargar los valores de los dispositivos desde la base de datos
#         device_values = mysql_dispositivoService().obtener_todos_los_valores()
#         device_values_dict = {}
#         for device_value in device_values:
#             device_id = device_value['dispositivo_id']
#             attribute_id = device_value['atributo_id']
#             value = device_value['valor']
#             if device_id not in device_values_dict:
#                 device_values_dict[device_id] = {}
#             device_values_dict[device_id][attribute_id] = value
#         return device_values_dict

#     def load_rules(self):
#         reglas = reglaService.obtener_reglas()
#         if not reglas:
#             return []
#         for regla in reglas:
#             disparadores, condiciones = (
#                 [criterio for criterio in regla['criterios'] if criterio['tipo'] == 'd'],
#                 [criterio for criterio in regla['criterios'] if criterio['tipo'] == 'c']
#             )

#             # Generar las sentencias para todos los disparadores
#             sentencias_disparadores = [self.generar_sentencia_criterio(disparador) for disparador in disparadores]
#             sentencias_condiciones = [self.generar_sentencia_criterio(condicion) for condicion in condiciones]
#             acciones = [self.generar_sentencia_accion(accion, regla['id']) for accion in regla['acciones']]

#             # Unir las sentencias con 'and'
#             disparador_final = " or ".join(sentencias_disparadores)
#             condicion_final = " or ".join(sentencias_condiciones)
                  
#         # self.add_rule(
#         #         trigger=lambda: self.check_trigger(regla['criterios']),
#         #         condition=lambda: self.check_condition(regla['criterios']),
#         #         action=lambda: self.execute_action(regla['acciones'])
#         #     )    
#             for accion in acciones:
#                 self.add_rule(
#                     id=regla['id'],
#                     user=regla['usuario'],
#                     trigger=disparador_final,
#                     condition=condicion_final,
#                     action=accion
#                 )
#         return self.rules

#     def generar_sentencia_criterio(self, criterio):
#         dispositivo_id = criterio['dispositivo_id']
#         atributo_id = criterio['atributo_id']
#         comparador = criterio['comparador']
#         valor = criterio['valor']

#         print(f"Dispositivo: {dispositivo_id}, Atributo: {atributo_id}, Comparador: {comparador}, Valor: {valor}")

#         #valor_dispositivo = mysql_dispositivoService().obtener_valor(dispositivo_id, atributo_id)
        
#         valor_dispositivo = self.device_values_cache.get(dispositivo_id, {}).get(atributo_id)

#         return f"{valor_dispositivo} {comparador} {valor}"

#     def generar_sentencia_accion(self, accion, id_regla):
#         dispositivo_id = accion['dispositivo_id']
#         atributo_id = accion['atributo_id']
#         valor = accion['valor_accion']
#         nombre_accion = accion['nombre']
#         if nombre_accion.lower() == "set":
#             return f"mysql_dispositivoService().set_valor('{dispositivo_id}', {atributo_id}, {valor})"  
#         return f"self.alert('{valor}', {id_regla})"
    
#     def alert(self, texto, id_regla):
#         regla = next(rule for rule in self.rules if rule['id'] == id_regla)

#         usuario = usuarioService.obtener_usuario_por_id(regla['user'])
#         email = usuario['correo']
#         print(f"Enviando alerta a {email}...")

#         smtp_server = 'smtp-mail.outlook.com'
#         smtp_port = 587
#         sender_email = 'prueba_smartesi@outlook.com'
#         password = 'Contrasena'

#         message = MIMEMultipart()
#         message['From'] = sender_email
#         message['To'] = email
#         message['Subject'] = 'Alerta de seguridad Smart ESI'

#         body = f'Alerta Smart ESI: {texto}'
#         message.attach(MIMEText(body, 'plain'))

#         # Enviar el correo electrónico
#         with smtplib.SMTP(smtp_server, smtp_port) as server:
#             server.starttls()
#             server.login(sender_email, password)
#             server.sendmail(sender_email, email, message.as_string())
#         print(f"Alerta: {texto}, ID regla: {id_regla}, ID usuario: {regla['user']}")
#         # Ver como compruebo si ya he ejecutado esta acción
#         # reglaService.eliminar_regla_por_id(id_regla)
#         # self.rules = self.load_rules()
#         # if not self.acciones_pendientes.get(id_regla):
#         #     self.acciones_pendientes[id_regla] = texto
#         # elif texto not in self.acciones_pendientes.get(id_regla):
#         #     self.acciones_pendientes[id_regla].append(texto)
#         # print(f"Acciones pendientes: {self.acciones_pendientes}")
    
#     def add_rule(self, id, user, trigger, condition, action):
#         self.rules.append({
#             'id': id,
#             'user': user,
#             'trigger': trigger,
#             'condition': condition,
#             'action': action
#         })

#     def check_rules(self):
#         try:
#             global running
#             while running:
#                 print("Verificando reglas...", running, self.corriendo)
#                 # print(f"Reglas actuales: {self.rules}")
#                 # print(f"Última ejecución de reglas: {self.last_execution_time}")
#                 for rule in self.rules:
#                     current_time = time.time()
#                     if current_time - self.last_execution_time.get(rule['id'], 0) > 60:
#                         try:
#                             trigger_eval = eval(rule['trigger'])
#                             condition_eval = eval(rule['condition'])
#                         except Exception as e:
#                             print(f"Error al evaluar la regla {rule['id']}: {e}")
#                             print(f"Trigger: {rule['trigger']}")
#                             print(f"Condition: {rule['condition']}")
#                             self.last_evaluated_triggers[rule['id']] = False
#                             self.last_evaluated_conditions[rule['id']] = False
#                             continue
                        
#                         # Comparar con los resultados anteriores
#                         if (rule['id'] not in self.last_evaluated_triggers or 
#                             self.last_evaluated_triggers[rule['id']] != trigger_eval or
#                             self.last_evaluated_conditions[rule['id']] != condition_eval):

#                             print(self.last_evaluated_triggers)
#                             print(self.last_evaluated_conditions)
                            
#                             # Actualizar los resultados almacenados
#                             self.last_evaluated_triggers[rule['id']] = trigger_eval
#                             self.last_evaluated_conditions[rule['id']] = condition_eval
                            
#                             # Ejecutar la acción si el trigger y la condición son verdaderos
#                             if trigger_eval and condition_eval:
#                                 try:
#                                     exec(rule['action'])
#                                 except Exception as e:
#                                     print(f"Error al ejecutar la acción de la regla {rule['id']}: {e}")
#                                 finally:
#                                     self.last_execution_time[rule['id']] = time.time()
#                 self.stop_event.wait(1)
#         except Exception as e:
#             print(f"Error al verificar reglas: {e}")
#             #self.check_rules()


#     # def check_rules(self):
#     #     while True:
#     #         # print("Verificando reglas...")
#     #         # print(self.rules)
#     #         for rule in self.rules:
#     #             current_time = time.time()
#     #             print(f"Última ejecución de la regla {rule['id']}: {self.last_execution_time.get(rule['id'], 0)}")
#     #             if current_time - self.last_execution_time.get(rule['id'], 0) > 60:
#     #                 print(f"Verificando regla {rule}...")
#     #                 # print(f"Acciones pendientes: {self.acciones_pendientes}")
#     #                 print(f"Trigger: {rule['trigger']}")
#     #                 print(f"Condition: {rule['condition']}")
#     #                 trigger_eval = eval(rule['trigger'])
#     #                 print(f"Trigger eval: {trigger_eval}")
#     #                 condition_eval = eval(rule['condition'])
#     #                 print(f"Condition eval: {condition_eval}")
#     #                 if trigger_eval and condition_eval:
#     #                     print(rule['id'])
#     #                     print(rule['action'])
#     #                     exec(rule['action'])
#     #                     self.last_execution_time[rule['id']] = time.time()

#     #                     # if self.acciones_pendientes.get(rule['id']):
#     #                     #     print(f"Acciones pendientes: {self.acciones_pendientes.get(rule['id'])}")
#     #                     #     for accion in self.acciones_pendientes[rule['id']]:
#     #                     #         print(f"Ejecutando acción: {accion}")
#     #                     #         #exec(accion)
#     #                     #     self.acciones_pendientes[rule['id']] = []
#     #                     time.sleep(1)
#     #             # if rule['trigger']() and rule['condition']():
#     #             #     rule['action']()
#     #         time.sleep(1)  # Tiempo de espera entre cada verificación de reglas
#     #         self.rules = self.load_rules()