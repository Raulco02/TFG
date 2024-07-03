from jinja2 import Template, TemplateSyntaxError, UndefinedError
from App.model.mysql_dispositivoDAO import mysql_dispositivoDAO
from App.model.integracionDAO import IntegracionDAO
from App.model.mysql_dispositivo import mysql_dispositivo
from App.helpers.escritorXML import EscritorXML
from App.services.tarjeta_service import tarjetaService

class mysql_dispositivoService:
    integracionDAO = IntegracionDAO()
    escritor = EscritorXML()
    def obtener_dispositivos(self):
        dispositivoDAO = mysql_dispositivoDAO()
        dispositivos = dispositivoDAO.obtener_dispositivos()
        return dispositivos
    
    def obtener_dispositivos_temperatura(self):
        dispositivoDAO = mysql_dispositivoDAO()
        dispositivos = dispositivoDAO.obtener_dispositivos_temperatura()
        return dispositivos
    
    def obtener_dispositivos_por_atributo(self, atributo):
        dispositivoDAO = mysql_dispositivoDAO()
        dispositivos = dispositivoDAO.obtener_dispositivos_por_atributo(atributo)
        return dispositivos

    def obtener_dispositivo_por_id(self, id):
        dispositivoDAO = mysql_dispositivoDAO()
        dispositivo = dispositivoDAO.obtener_dispositivo_por_id(id)
        return dispositivo

    def crear_dispositivo(self, dispositivo, valores_actuales): ##ESTO HAY QUE CAMBIARLO
        dispositivoDAO = mysql_dispositivoDAO()
        dispositivoDAO.crear_dispositivo(dispositivo)
        valores = []
        self.obtener_atributos()
        ids_atributos = [atributo['id'] for atributo in self.atributos if atributo['nombre'] in dispositivo.atributos]
        print(f"IDs de atributos: {ids_atributos}")
        if len(ids_atributos) == len(valores_actuales):
            for i in range(len(valores_actuales)):
                valores.append({
                    'id-dispositivo': dispositivo.id,
                    'id-atributo': ids_atributos[i],
                    'valor': valores_actuales[i]
                })
        dispositivoDAO.valores_actuales(valores)
    
    def crear_dispositivo_http(self, id, nombre, topic, nombre_integracion, ubicacion, topics_actuacion=None, plantillas_actuacion=None):
        #dispositivo = mysql_dispositivo(id, nombre, topic, nombre_integracion)
        dispositivoDAO = mysql_dispositivoDAO()
        print(nombre_integracion)
        integracion = self.integracionDAO.obtener_integracion(nombre_integracion)  # Asegúrate de que esto devuelve lo esperado
        if integracion is None or integracion == [] or integracion == {}:
            raise ValueError("La integración no existe.")
        print('integracion',integracion)
        # Extrae la lista de atributos
        atributos = integracion["atributos"]
        
        # Contar los atributos actuables
        print('Antes de lo del count')
        atributos_actuables_count = sum(1 for atributo in atributos if atributo["actuable"] == "true")
        print(integracion["tipo_dispositivo"], atributos_actuables_count, topics_actuacion, integracion)
        if (integracion["tipo_dispositivo"] == "a" and atributos_actuables_count == 0) or (integracion["tipo_dispositivo"] == "s" and atributos_actuables_count > 0):
            raise ValueError("El tipo de dispositivo no coincide con los atributos actuables.")

        # Verifica que topics_actuacion no sea None y tenga la longitud correcta
        if (integracion["tipo_dispositivo"] == "a") and (topics_actuacion is not None and plantillas_actuacion is not None and atributos_actuables_count > 0):
            print('TOPICS ACTUACION', topics_actuacion, atributos_actuables_count)
            if len(topics_actuacion) != atributos_actuables_count and len(plantillas_actuacion) != atributos_actuables_count:
                raise ValueError("El número de topics_actuacion y de plantillas_actuacion debe coincidir con el número de atributos actuables.")
            
            # Empareja topics_actuacion y atributos actuables
            actuable_index = 0
            # index = 0
            # indexes = []
            for atributo in atributos:
                try:
                    if atributo["actuable"] == "true":
                        atributo["topic"] = topics_actuacion[actuable_index]
                        if self.validate_template(plantillas_actuacion[actuable_index]) is False:
                            print('plantilla', plantillas_actuacion[actuable_index])
                            raise ValueError("La plantilla de actuación no es válida, debe ser una plantilla Jinja2.")
                        atributo["plantilla"] = plantillas_actuacion[actuable_index]
                        actuable_index += 1
                except IndexError:
                    raise ValueError("El número de topics_actuacion y de plantillas_actuacion debe coincidir con el número de atributos actuables.")
                    # indexes.append(index)
                # index+=1
            print('Atributos', atributos)
            # print('Indexes', indexes)
            print('Atributos antes de modificar', integracion['atributos'])
            # for indice in indexes:
            #     integracion["atributos"][indice] = atributos[indice]
        elif (integracion["tipo_dispositivo"] == "s") and ((topics_actuacion is not None and topics_actuacion != []) or (plantillas_actuacion is not None and plantillas_actuacion != [])):
            raise ValueError("El tipo de dispositivo es sensor y se han enviado topics de actuacion o plantillas de actuacion.")

        print('Antes de esto')
        self.escritor.verificar_y_crear_xml(id, nombre, topic, integracion, ubicacion)  ##Si hay excepciones aquí qué pasa
        print('XML ESCRITO')
        #id_atributos = [atributo['id'] for atributo in integracion['atributos']]
        dispositivoDAO.crear_dispositivo_http(id, nombre, topic, integracion, ubicacion) ##REALMENTE QUIERO ALMACENAR TODO ESTO EN BBDD
        print('BBDD')
        return True
    
    def edit_dispositivo_http(self, prev_id, id, nombre, topic, nombre_integracion, ubicacion, topics_actuacion=None, plantillas_actuacion=None):
        #dispositivo = mysql_dispositivo(id, nombre, topic, nombre_integracion)
        dispositivoDAO = mysql_dispositivoDAO()
        print(nombre_integracion)
        integracion = self.integracionDAO.obtener_integracion(nombre_integracion)  # Asegúrate de que esto devuelve lo esperado
        if integracion is None or integracion == [] or integracion == {}:
            raise ValueError("La integración no existe.")
        # Extrae la lista de atributos
        atributos = integracion["atributos"]
        
        # Contar los atributos actuables
        atributos_actuables_count = sum(1 for atributo in atributos if atributo["actuable"] == "true")
        print(integracion["tipo_dispositivo"], atributos_actuables_count, topics_actuacion, integracion)
        if (integracion["tipo_dispositivo"] == "a" and atributos_actuables_count == 0) or (integracion["tipo_dispositivo"] == "s" and atributos_actuables_count > 0):
            raise ValueError("El tipo de dispositivo no coincide con los atributos actuables.")

        # Verifica que topics_actuacion no sea None y tenga la longitud correcta
        if (integracion["tipo_dispositivo"] == "a") and (topics_actuacion is not None and plantillas_actuacion is not None and atributos_actuables_count > 0):
            print('TOPICS ACTUACION', topics_actuacion, atributos_actuables_count)
            if len(topics_actuacion) != atributos_actuables_count and len(plantillas_actuacion) != atributos_actuables_count:
                raise ValueError("El número de topics_actuacion y de plantillas_actuacion debe coincidir con el número de atributos actuables.")
            
            # Empareja topics_actuacion y atributos actuables
            actuable_index = 0
            # index = 0
            # indexes = []
            for atributo in atributos:
                try:
                    if atributo["actuable"] == "true":
                        atributo["topic"] = topics_actuacion[actuable_index]
                        if self.validate_template(plantillas_actuacion[actuable_index]) is False:
                            print('plantilla', plantillas_actuacion[actuable_index])
                            raise ValueError("La plantilla de actuación no es válida, debe ser una plantilla Jinja2.")
                        atributo["plantilla"] = plantillas_actuacion[actuable_index]
                        actuable_index += 1
                except IndexError:
                    raise ValueError("El número de topics_actuacion y de plantillas_actuacion debe coincidir con el número de atributos actuables.")
                    # indexes.append(index)
                # index+=1
            print('Atributos', atributos)
            # print('Indexes', indexes)
            print('Atributos antes de modificar', integracion['atributos'])
            # for indice in indexes:
            #     integracion["atributos"][indice] = atributos[indice]
        elif (integracion["tipo_dispositivo"] == "s") and ((topics_actuacion is not None and topics_actuacion != []) or (plantillas_actuacion is not None and plantillas_actuacion != [])):
            raise ValueError("El tipo de dispositivo es sensor y se han enviado topics de actuacion o plantillas de actuacion.")

        print('Antes de esto')
        self.escritor.editar_xml(prev_id, id, nombre, topic, integracion) 
        print('XML ESCRITO')
        #id_atributos = [atributo['id'] for atributo in integracion['atributos']]
        dispositivoDAO.edit_dispositivo_http(prev_id, id, nombre, topic, integracion, ubicacion) ##REALMENTE QUIERO ALMACENAR TODO ESTO EN BBDD
        print('BBDD')
        return True
    
    def eliminar_dispositivo(self, id):
        dispositivoDAO = mysql_dispositivoDAO()
        dispositivoDAO.eliminar_dispositivo(id)
        return True

    def valores_actuales(self, valores):
        dispositivoDAO = mysql_dispositivoDAO()
        dispositivoDAO.valores_actuales(valores)

    def valores_actuales_xml(self, valores):
        dispositivoDAO = mysql_dispositivoDAO()
        dispositivoDAO.valores_actuales_xml(valores)

    def obtener_valor(self, dispositivo_id, atributo_id):
        dispositivoDAO = mysql_dispositivoDAO()
        valor = dispositivoDAO.obtener_valor(dispositivo_id, atributo_id)
        return valor

    def obtener_atributos(self):
        dispositivoDAO = mysql_dispositivoDAO()
        atributos = dispositivoDAO.obtener_atributos()
        self.atributos = atributos
        return atributos
    
    def obtener_tipo_atributo(self, atributo_id):
        dispositivoDAO = mysql_dispositivoDAO()
        tipo = dispositivoDAO.obtener_tipo_atributo(atributo_id)
        return tipo

    def validate_template(self, template_string):
        try:
            Template(template_string)
            return True
        except (TemplateSyntaxError, UndefinedError):
            return False
        
    def set_valor(self, dispositivo_id, atributo_id, valor):
        dispositivoDAO = mysql_dispositivoDAO()
        tipo = dispositivoDAO.obtener_tipo_atributo(atributo_id)
        print("tipo", tipo)
        
        if tipo.lower() == 'termostato':
            print("Es termostato")
            tarjetaService.setTemperatura(dispositivo_id, atributo_id, valor)

    def obtener_todos_los_valores(self):
        dispositivoDAO = mysql_dispositivoDAO()
        valores = []
        valores_bbdd = dispositivoDAO.obtener_todos_los_valores()
        for valor in valores_bbdd:
            valores.append({
                'dispositivo_id': valor[0],
                'atributo_id': valor[1],
                'valor': float(valor[2]) if valor[2] is not None else None
            })
        return valores
    
    def obtener_valores_dispositivos_atributos(self, dispositivos_atributos):
        dispositivoDAO = mysql_dispositivoDAO()
        valores = []
        valores_bbdd = dispositivoDAO.obtener_valores_dispositivos_atributos(dispositivos_atributos)
        for valor in valores_bbdd:
            valores.append({
                'dispositivo_id': valor[0],
                'atributo_id': valor[1],
                'valor': float(valor[2]) if valor[2] is not None else None
            })
        print('Valores:', valores)
        return valores
            

    # def actualizar_dispositivo(self, dispositivo):
    #     dispositivoDAO = mysql_dispositivoDAO()
    #     dispositivoDAO.actualizar_dispositivo(dispositivo)

    # def eliminar_dispositivo(self, id):
    #     dispositivoDAO = mysql_dispositivoDAO()
    #     dispositivoDAO.eliminar_dispositivo(id)