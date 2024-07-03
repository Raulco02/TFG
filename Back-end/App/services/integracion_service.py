import os
from App.model.integracionDAO import IntegracionDAO
from App.model.integracion import Integracion 

class integracionService:
    def comprobar_script(script): ##En el editar igual hay que comprobarlo con todos los ficheros
        integracion_dao = IntegracionDAO()
        integracion_data = integracion_dao.obtener_scripts()
        if script in integracion_data:
            return True
        return False
    
    def comprobar_script_valido(script, nombre_integracion):
        integracion_dao = IntegracionDAO()
        integracion_data = integracion_dao.obtener_script_integracion(script)####HAY QUE COMPROBAR ESTE METODO INTERIOR
        print('integracion_data:', integracion_data)
        if nombre_integracion == integracion_data:
            print(script, nombre_integracion,'si')
            return True
        script_en_uso = integracionService.comprobar_script(script)
        if script_en_uso:
            print(script, nombre_integracion,'no')
            return False
        else:
            print(script, nombre_integracion,'si')
            return True
        
    
    def eliminar_scripts():
        integracion_dao = IntegracionDAO()
        integracion_data = integracion_dao.obtener_scripts()
        
        directorio = ".\\Dispositivos"
        archivos_en_directorio = [f for f in os.listdir(directorio) if f.endswith('.py')]
        print('Archivos en directorio:', archivos_en_directorio)

        for archivo in archivos_en_directorio:
            nombre_archivo = os.path.splitext(archivo)[0]
            if nombre_archivo not in integracion_data:
                ruta_archivo = os.path.join(directorio, archivo)
                print("Se va a eliminar el siguiente archivo:", ruta_archivo)
                os.remove(ruta_archivo)
        
        return True

    def obtener_integraciones():
        integracion_dao = IntegracionDAO()
        integracion_data = integracion_dao.obtener_integraciones()
        #print("integracion DATA:", integracion_data)
        return integracion_data
    
    def obtener_tipos():
        integracion_dao = IntegracionDAO()
        tipos_data = integracion_dao.obtener_tipos()
        print("Tipos DATA:", tipos_data)
        return tipos_data
    
    def crear_integracion(nombre, nombre_script, script, atributos):
        if not integracionService.comprobar_script(nombre_script):
            integracion_dao = IntegracionDAO()
            actuable_present = any(atributo["actuable"] == "true" for atributo in atributos)
            print('Actuable present:', actuable_present)
            tipo_dispositivo = "a" if actuable_present else "s"
            print('tipo dispositivo', tipo_dispositivo)
            integracion = Integracion(nombre, nombre_script, script, tipo_dispositivo)
            print('Integracion:', integracion.tipo_dispositivo)
            integracion_data = integracion_dao.crear_integracion(integracion, atributos) ##Vigilar que ningún atributo sea actuable
            # Ruta del directorio donde se almacenarán los scripts
            directorio = ".\\Dispositivos"
            
            # Comprobamos si el directorio existe, si no, lo creamos
            if not os.path.exists(directorio):
                os.makedirs(directorio)
            
            # Ruta completa del archivo
            ruta_archivo = os.path.join(directorio, nombre_script + ".py")
            
            # Escribir el contenido en el archivo
            with open(ruta_archivo, "w") as archivo:
                archivo.write(script)

            return integracion_data
        else:
            raise ValueError("El script está en uso por otra integración")
    
    def edit_integracion(prev_nombre, nombre, nombre_script, script, atributos): 
        integracion_dao = IntegracionDAO()
        if integracionService.comprobar_script_valido(nombre_script, prev_nombre):
            actuable_present = any(atributo["actuable"] == "true" for atributo in atributos)
            print('Actuable present:', actuable_present)
            tipo_dispositivo = "a" if actuable_present else "s"
            print('tipo dispositivo', tipo_dispositivo)
            integracion = Integracion(nombre, nombre_script, script, tipo_dispositivo)
            print('Integracion:', integracion.tipo_dispositivo)
            integracion_data = integracion_dao.edit_integracion(prev_nombre, integracion, atributos) ##Vigilar que ningún atributo sea actuable
                    # Ruta del directorio donde se almacenarán los scripts
            directorio = ".\\Dispositivos"
            
            # Comprobamos si el directorio existe, si no, lo creamos
            if not os.path.exists(directorio):
                os.makedirs(directorio)
            
            # Ruta completa del archivo
            ruta_archivo = os.path.join(directorio, nombre_script + ".py")
            
            # Escribir el contenido en el archivo
            with open(ruta_archivo, "w") as archivo:
                archivo.write(script)

            integracionService.eliminar_scripts()
            return integracion_data
        else:
            raise ValueError("El script está en uso por otra integración")
        
    def eliminar_integracion(id):
        integracion_dao = IntegracionDAO()
        integracion_data = integracion_dao.eliminar_integracion(id)
        integracionService.eliminar_scripts() ###LO DE LOS SCRIPTS NO ES ASI, O SI
        return integracion_data
    
