from App.model.agente_mysql import agente_mysql
from App.exceptions.duplicate import duplicateIntegracionException
from App.exceptions.duplicate import duplicateAtributoException
import mysql.connector
import os

class IntegracionDAO:
    def __init__(self):
        self.agent = agente_mysql()

    def conectar(self):
        try:
            self.agent.connect()
        except Exception as ex:
            print(f"Error al conectar con la base de datos: {ex}")

    def desconectar(self):
        try:
            print('Desconectando', self.agent.connection.is_connected())
            self.agent.disconnect()
        except Exception as ex:
            print('Desconectando', self.agent.connection.is_connected())
            print(f"Error al desconectar de la base de datos: {ex}")

    def obtener_integraciones(self): #Me lo ha arreglao chatgpt, comprobar
        try:
            self.conectar()
            query = """
                SELECT 
                    i.id AS id_integracion,
                    i.nombre AS nombre_integracion,
                    i.script AS script_integracion,
                    GROUP_CONCAT(a.id SEPARATOR ', ') AS id_atributos,
                    GROUP_CONCAT(a.nombre SEPARATOR ', ') AS nombre_atributos,
                    GROUP_CONCAT(a.unidades SEPARATOR ', ') AS unidades_atributos,
                    GROUP_CONCAT(a.actuable SEPARATOR ', ') AS atributo_actuable,
                    GROUP_CONCAT(a.icono SEPARATOR ', ') AS iconos_atributos,
                    GROUP_CONCAT(t.nombre SEPARATOR ', ') AS tipo_atributos,
                    GROUP_CONCAT(a.limite_superior SEPARATOR ', ') AS limite_superior,
                    GROUP_CONCAT(a.limite_inferior SEPARATOR ', ') AS limite_inferior
                FROM
                    integraciones i
                JOIN
                    `integraciones-atributos` ia ON i.id = ia.idintegracion
                JOIN
                    atributos a ON ia.idatributo = a.id
                JOIN
                    tipos_atributos t ON a.tipo = t.id
                GROUP BY
                    i.id;
            """
            result = self.agent.read_records_by_query(query, None)
            #print("Integraciones", result)
            integraciones = []
            for row in result:
                ids_atributos = row[3].split(", ") if row[3] else []
                nombres_atributos = row[4].split(", ") if row[4] else []
                unidades_atributos = row[5].split(", ") if row[5] else []
                actuable_atributos = row[6].split(", ") if row[6] else []
                iconos_atributos = row[7].split(", ") if row[7] else []
                tipos_atributos = row[8].split(", ") if row[8] else []
                limite_superior_atributos = row[9].split(", ") if row[9] else []
                limite_inferior_atributos = row[10].split(", ") if row[10] else []

                num_atributos = len(ids_atributos)
                atributos = []

                for i in range(num_atributos):
                    atributo = {
                        "id": ids_atributos[i] if i < len(ids_atributos) else "Null",
                        "nombre": nombres_atributos[i] if i < len(nombres_atributos) else "Null",
                        "unidades": unidades_atributos[i] if i < len(unidades_atributos) else "Null",
                        "actuable": actuable_atributos[i] if i < len(actuable_atributos) else "Null",
                        "icono": iconos_atributos[i] if i < len(iconos_atributos) else "Null",
                        "tipo": tipos_atributos[i] if i < len(tipos_atributos) else "Null",
                        "limite_superior": limite_superior_atributos[i] if i < len(limite_superior_atributos) else "Null",
                        "limite_inferior": limite_inferior_atributos[i] if i < len(limite_inferior_atributos) else "Null"
                    }
                    atributos.append(atributo)
                
                contenido = ""
                try:
                    current_dir = os.path.dirname(os.path.abspath(__file__))
                    print("Directorio actual:", current_dir)
                    nombre_archivo = current_dir + "/../../Dispositivos/" + row[2] + ".py"
                    with open(nombre_archivo, 'r') as archivo:
                        contenido = archivo.read()
                except FileNotFoundError:
                    print(f"El archivo {nombre_archivo} no existe.")
                except IOError:
                    print(f"Error al leer el archivo {nombre_archivo}.")
                    raise

                integraciones.append({
                    "id": row[0],
                    "nombre": row[1],
                    "script": row[2],
                    "codigo": contenido,
                    "atributos": atributos
                })
                #print("Integraciones:", integraciones)
            self.desconectar()
            return integraciones
        except Exception as ex:
            print(f"Error al obtener todas las integraciones: {ex}")
            return None

    
    def obtener_integracion(self, nombre_integracion): #La consulta tiene ls repe y le falta icono
        try:
            self.conectar()
            query = """
                SELECT 
                    i.id AS id_integracion,
                    i.nombre AS nombre_integracion,
                    i.script AS script_integracion,
                    i.tipo_dispositivo AS tipo_dispositivo,
                    GROUP_CONCAT(a.id SEPARATOR ', ') AS id_atributos,
                    GROUP_CONCAT(a.nombre SEPARATOR ', ') AS nombre_atributos,
                    GROUP_CONCAT(a.unidades SEPARATOR ', ') AS unidades_atributos,
                    GROUP_CONCAT(a.actuable SEPARATOR ', ') AS actuable_atributos,
                    GROUP_CONCAT(t.nombre SEPARATOR ', ') AS tipo_atributos
                FROM
                    integraciones i
                JOIN
                    `integraciones-atributos` ia ON i.id = ia.idintegracion
                JOIN
                    atributos a ON ia.idatributo = a.id
                JOIN
                    tipos_atributos t ON a.tipo = t.id
                WHERE
                    i.nombre = %s
                GROUP BY
                    i.id;
            """
            result = self.agent.read_records_by_query(query, (nombre_integracion,))
            integracion = {}
            print(nombre_integracion)
            print(result)
            for row in result:
                ids_atributos = row[4].split(", ")
                nombres_atributos = row[5].split(", ")
                unidades_atributos = row[6].split(", ")
                actuable_atributos = row[7].split(", ")
                tipos_atributos = row[8].split(", ")
                atributos = []
                contenido = ""
                for i in range(len(ids_atributos)):
                    atributos.append({
                        "id": ids_atributos[i],
                        "nombre": nombres_atributos[i],
                        "unidades": unidades_atributos[i],
                        "actuable": actuable_atributos[i],
                        "tipo": tipos_atributos[i]
                    })
                try:
                    current_dir = os.path.dirname(os.path.abspath(__file__))
                    print("Directorio actual:", current_dir)
                    nombre_archivo=current_dir+"/../../Dispositivos/"+row[2]+".py"
                    with open(nombre_archivo, 'r') as archivo:
                        contenido = archivo.read()
                    print(contenido)
                except FileNotFoundError:
                    print(f"El archivo {nombre_archivo} no existe.")
                except IOError:
                    print(f"Error al leer el archivo {nombre_archivo}.")
                    raise
                integracion = {
                    "id": row[0],
                    "nombre": row[1],
                    "script": row[2],
                    "tipo_dispositivo": row[3],
                    "atributos": atributos,
                }
            self.desconectar()
            return integracion
        except Exception as ex:
            self.desconectar()
            print(f"Error al obtener los atributos de la integracion {nombre_integracion}: {ex}")
            return None
        
    def obtener_tipos(self):
        try:
            self.conectar()
            query = """
                SELECT 
                    id,
                    nombre
                FROM
                    tipos_atributos
            """
            result = self.agent.read_records_by_query(query, None)
            tipos = []
            for row in result:
                tipos.append({
                    "id": row[0],
                    "nombre": row[1]
                })
            self.desconectar()
            return tipos
        except Exception as ex:
            print(f"Error al obtener los tipos de atributos: {ex}")
            return None
        
    def crear_integracion(self, integracion, atributos): ##Comprobar si las transacciones funcionan
        try:
            self.conectar()
            self.agent.start_transaction()

            integracion_id = self.agent.create_record("integraciones", {"nombre": integracion.nombre, "script": integracion.nombre_script, "tipo_dispositivo": integracion.tipo_dispositivo})
            print('Integracion creada, id:', integracion_id)

            for atributo in atributos:
                try:
                    if atributo["actuable"] == "true" and integracion.tipo_dispositivo == "s":
                        raise ValueError("El tipo de dispositivo no coincide con los atributos actuables.")
                    tipo_atributo = self.agent.read_records('tipos_atributos', f"nombre = '{atributo['tipo']}'")
                    if tipo_atributo == []:
                        self.agent.rollback_transaction()
                        raise ValueError("El tipo de atributo no existe.")
                    atributo["tipo"] = tipo_atributo[0][0]
                    atributo_id = self.agent.create_record("atributos", atributo)  # Controlar que si ya existe, busque el id
                    if not atributo_id:
                        self.agent.rollback_transaction()
                        raise ValueError("Error al crear el atributo. Los atributos proporcionados contienen campos desconocidos.")
                    #print(atributo_id)
                except mysql.connector.Error as ex: 
                    if "Duplicate entry" in str(ex) and "atributos.nombre_UNIQUE" in str(ex):
                        print("Atributo ya existente, buscando id...")
                        atributo_bbdd = self.agent.read_records('atributos', 'nombre = "' + atributo["nombre"] + '"')[0]
                        atributo_actuable = atributo_bbdd[3]
                        if atributo_actuable != atributo["actuable"]:
                            print('Es actuable',atributo_actuable, atributo["actuable"])
                            raise duplicateAtributoException()
                        atributo_id = atributo_bbdd[0]
                        print('Atributo ya existente, id:', atributo_id)
                        print(atributo["nombre"])
                    elif "Data too long" in str(ex) and 'unidades' in str(ex):
                        self.agent.rollback_transaction()
                        raise ValueError("Las unidades no pueden tener más de 5 caracteres")
                    elif "Unknown column" in str(ex):
                        self.agent.rollback_transaction()
                        raise ValueError("Los atributos proporcionados contienen campos desconocidos")
                        
                try: #Era un intento de controlar que no me metan dos veces el mismo atributo en la misma integracion
                    self.agent.create_record("integraciones-atributos", {
                        "idintegracion": integracion_id,
                        "idatributo": atributo_id
                    })
                except mysql.connector.Error as ex:
                    if "Duplicate entry" in str(ex) and "integraciones-atributos.PRIMARY" in str(ex):
                        print("NO SE")
                        self.agent.rollback_transaction()
                        raise duplicateAtributoException("Estás incluyendo un atributo repetido")
                    
            self.agent.commit_transaction()
            self.desconectar()
            return integracion_id
        except Exception as ex:
            print(ex)
            self.agent.rollback_transaction()
            self.desconectar()
            if "Duplicate entry" in str(ex) and "integraciones.nombre_UNIQUE" in str(ex):
                raise duplicateIntegracionException() from ex
            else:
                raise

    def edit_integracion(self, prev_nombre, integracion, atributos): ##CREO que funciona, REVISAR
        try:
            self.conectar()
            self.agent.start_transaction()
            integracion_bbdd = self.agent.update_record("integraciones", {"nombre": integracion.nombre, "script": integracion.nombre_script, "tipo_dispositivo": integracion.tipo_dispositivo}, f"nombre = '{prev_nombre}'")
            if not integracion_bbdd:
                self.agent.rollback_transaction()
                raise ValueError("No se ha encontrado la integración a editar.")
            atributos_integracion = self.agent.read_records('integraciones-atributos', f"idintegracion = '{str(integracion_bbdd[0][0])}'")
            if atributos_integracion == []:
                self.agent.rollback_transaction()
                raise ValueError("No se han encontrado los atributos de la integración a editar.")
            ids_atributos_integracion = [{"atributo":atributo[1], "encontrado":False} for atributo in atributos_integracion]
            for atributo_integracion in ids_atributos_integracion:
                atributo_completo = self.agent.read_records('atributos', f"id = '{atributo_integracion['atributo']}'")
                if atributo_completo==[]:
                    self.agent.rollback_transaction()
                    raise ValueError("No se encontrar un atributo de la integración a editar.")
                atributo_integracion["nombre"] = atributo_completo[0][1]
                atributo_integracion["actuable"] = atributo_completo[0][3]
            print('Atributos de la integracion:', atributos_integracion)
            
            print('Integracion editada:', integracion_bbdd)
            print('Atributos de la integracion:', atributos_integracion)
            print('Ids de los atributos de la integracion:', ids_atributos_integracion)

            for atributo in atributos:
                encontrado = False
                try:
                    if atributo["actuable"] == "true" and integracion.tipo_dispositivo == "s":
                        self.agent.rollback_transaction()
                        raise ValueError("El tipo de dispositivo no coincide con los atributos actuables.")
                    print(atributo)
                    for id_atributo in ids_atributos_integracion:
                        if id_atributo["encontrado"]:
                            continue
                        print("Atributo a buscar", id_atributo["nombre"], atributo["nombre"], id_atributo["actuable"], atributo["actuable"], id_atributo["encontrado"])
                        if id_atributo["nombre"] == atributo["nombre"] and id_atributo["actuable"] == atributo["actuable"] and id_atributo["encontrado"] == False:
                            tipo_atributo = self.agent.read_records('tipos_atributos', f"nombre = '{atributo['tipo']}'")
                            if tipo_atributo == []:
                                self.agent.rollback_transaction()
                                raise ValueError("El tipo de atributo no existe.")
                            atributo["tipo"] = tipo_atributo[0][0]
                            atributo_act = self.agent.update_record("atributos", atributo, f"id = '{id_atributo['atributo']}'")
                            print("El atributo que se actualiza es este", atributo_act)
                            if atributo_act is None:
                                print('Atributo no encontrado', id_atributo["nombre"])
                                continue
                            id_atributo["encontrado"] = True
                            encontrado = True
                            print("Atributo encontrado", id_atributo)
                            break
                      # Controlar que si ya existe, busque el id
                    print('Atributo editado:', atributo)
                    print('Encontrado:', encontrado)
                    if not encontrado:
                        tipo_atributo = self.agent.read_records('tipos_atributos', f"nombre = '{atributo['tipo']}'")
                        if tipo_atributo == []:
                            self.agent.rollback_transaction()
                            raise ValueError("El tipo de atributo no existe.")
                        atributo["tipo"] = tipo_atributo[0][0]
                        atributo_id = self.agent.create_record("atributos", atributo)
                        if not atributo_id:
                            self.agent.rollback_transaction()
                            raise ValueError("Error al crear el atributo. Los atributos proporcionados contienen campos desconocidos.")
                        self.agent.create_record("integraciones-atributos", {
                            "idintegracion": integracion_bbdd[0][0],
                            "idatributo": atributo_id
                        })
                except mysql.connector.Error as ex: 
                    if "Duplicate entry" in str(ex) and "atributos.nombre_UNIQUE" in str(ex):
                        atributo_bbdd = self.agent.read_records('atributos', 'nombre = "' + atributo["nombre"] + '"')[0]
                        atributo_actuable = atributo_bbdd[3]
                        if atributo_actuable != atributo["actuable"]:
                            print('Es actuable',atributo_actuable, atributo["actuable"])
                            self.agent.rollback_transaction()
                            raise duplicateAtributoException()
                        atributo_id = atributo_bbdd[0]
                        try:
                            self.agent.create_record("`integraciones-atributos`", {
                                "idintegracion": integracion_bbdd[0][0],
                                "idatributo": atributo_id
                            })
                        except mysql.connector.Error as ex:
                            if "Duplicate entry" in str(ex) and "integraciones-atributos.PRIMARY" in str(ex):
                                print('Atributo ya existente en la integracion', atributo["nombre"])
                    elif "Data too long" in str(ex) and 'unidades' in str(ex):
                        self.agent.rollback_transaction()
                        raise ValueError("Las unidades no pueden tener más de 5 caracteres")
                    elif "Unknown column" in str(ex):
                        self.agent.rollback_transaction()
                        raise ValueError("Los atributos proporcionados contienen campos desconocidos")
                    else:
                        self.agent.rollback_transaction()
                        raise
                # try: #Era un intento de controlar que no me metan dos veces el mismo atributo en la misma integracion
                #     self.agent.create_record("integraciones-atributos", {
                #         "idintegracion": integracion_bbdd['id'],
                #         "idatributo": atributo_id
                #     })
                # except mysql.connector.Error as ex:
                #     if "Duplicate entry" in str(ex) and "integraciones-atributos.PRIMARY" in str(ex):
                #         self.agent.rollback_transaction()
                #         raise duplicateAtributoException()
            for id_atributo in ids_atributos_integracion:
                if not id_atributo["encontrado"]:
                    print('Borrando', id_atributo['atributo'])
                    self.agent.delete_record("`integraciones-atributos`", f"idintegracion = {integracion_bbdd[0][0]} AND idatributo = {id_atributo['atributo']}")    
            self.agent.commit_transaction()
            self.desconectar()
            return True
        except Exception as ex:
            print(ex)
            self.agent.rollback_transaction()
            self.desconectar()
            if "Duplicate entry" in str(ex) and "integraciones.nombre_UNIQUE" in str(ex):
                raise duplicateIntegracionException() from ex
            else:
                raise

    def obtener_scripts(self):
        try:
            self.conectar()
            query = """
                SELECT 
                    script
                FROM
                    integraciones
            """
            result = self.agent.read_records_by_query(query, None)
            scripts = []
            for row in result:
                scripts.append(row[0])
            self.desconectar()
            return scripts
        except Exception as ex:
            print(f"Error al obtener todos los scripts: {ex}")
            return None
        
    def obtener_script_integracion(self, nombre_integracion):
        try:
            self.conectar()
            query = """
                SELECT 
                    nombre
                FROM
                    integraciones
                WHERE
                    script = %s
            """
            result = self.agent.read_records_by_query(query, (nombre_integracion,))
            script = ""
            print('Result:', result)
            for row in result:
                script = row[0]
            self.desconectar()
            return script
        except Exception as ex:
            print(f"Error al obtener el script de la integracion {nombre_integracion}: {ex}")
            return None
        

    def eliminar_integracion(self, id):
        try:
            self.conectar()
            self.agent.start_transaction()
            integracion = self.agent.delete_record("integraciones", f"id = {id}")
            if not integracion:
                self.agent.rollback_transaction()
                raise ValueError("No se ha encontrado la integración a eliminar.")
            #self.agent.delete_record("`integraciones-atributos`", f"idintegracion = {id}")
            self.agent.commit_transaction()
            self.desconectar()
            return True
        except Exception as ex:
            print(f"Error al eliminar la integración {id}: {ex}")
            self.agent.rollback_transaction()
            self.desconectar()
            raise
            

