import threading
import time
from App.services.regla_service import reglaService 

class RulesList(threading.Thread):
    def __init__(self):
        super().__init__()
        self.rules_list = []
        self.running = True  # Bandera para controlar la ejecución del hilo
        self.rules = None  # Objeto que se recibirá en cada ejecución
        #self.valores_dispositivos = {}

    def run(self):
        while self.running:
            self.rules = [] #Para que no se repitan las reglas. Habría que ver que se actualicen en vez de borrar y reemplazar siempre
            reglas = reglaService.obtener_reglas() ##En lugar de añadir rules habría que ver que no coincidan, y si no lo hacen, añadirlas
            if not reglas:
                self.rules = []
                continue
            for regla in reglas:
                disparadores = []
                condiciones = []
                valores_dispositivos = []

                for criterio in regla['criterios']:
                    if criterio['tipo'] == 'd':
                        disparadores.append(criterio)
                    elif criterio['tipo'] == 'c':
                        condiciones.append(criterio)
                    valores_dispositivos.append({"dispositivo_id":criterio['dispositivo_id'], "atributo_id": criterio['atributo_id']})

                # Generar las sentencias para todos los disparadores
                sentencias_disparadores = [self.generar_sentencia_criterio(disparador) for disparador in disparadores]
                sentencias_condiciones = [self.generar_sentencia_criterio(condicion) for condicion in condiciones]
                acciones = [self.generar_sentencia_accion(accion, regla['id']) for accion in regla['acciones']]

                # Unir las sentencias con 'or'
                disparador_final = " or ".join(sentencias_disparadores)
                condicion_final = " or ".join(sentencias_condiciones)
    
                for accion in acciones:
                    self.add_rule(
                        id=regla['id'],
                        user=regla['usuario'],
                        trigger=disparador_final,
                        condition=condicion_final,
                        action=accion,
                        valores_dispositivos=valores_dispositivos
                    )
            time.sleep(60)

    def generar_sentencia_criterio(self, criterio):
        dispositivo_id = criterio['dispositivo_id']
        atributo_id = criterio['atributo_id']
        comparador = criterio['comparador']
        valor = criterio['valor']

        #print(f"Dispositivo: {dispositivo_id}, Atributo: {atributo_id}, Comparador: {comparador}, Valor: {valor}")

        #valor_dispositivo = mysql_dispositivoService().obtener_valor(dispositivo_id, atributo_id)

        return f"/{dispositivo_id}-{atributo_id}/ {comparador} {valor}"
    
    def generar_sentencia_accion(self, accion, id_regla):
        dispositivo_id = accion['dispositivo_id']
        atributo_id = accion['atributo_id']
        valor = accion['valor_accion']
        nombre_accion = accion['nombre']
        if nombre_accion.lower() == "set":
            return f"mysql_dispositivoService().set_valor('{dispositivo_id}', {atributo_id}, {valor})"  
        return f"self.alert('{valor}', {id_regla})"
    
    def add_rule(self, id, user, trigger, condition, action, valores_dispositivos):
        if not any(r['id'] == id for r in self.rules_list):
            print(f"Adding rule, id:{id}, user:{user}, trigger:{trigger}, condition:{condition}, action:{action}, valores_dispositivos:{valores_dispositivos}")
            self.rules_list.append({
                'id': id,
                'user': user,
                'trigger': trigger,
                'condition': condition,
                'action': action,
                'valores_dispositivos': valores_dispositivos
            })

    def get_rules_list(self):
        return self.rules_list

    def stop(self):
        self.running = False

    # def set_rules(self, rules): #EL QUE
    #     self.rules = rules
