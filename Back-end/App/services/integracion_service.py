import os
from App.model.integracionDAO import IntegracionDAO
from App.model.integracion import Integracion 

class integracionService:
    """
    Descripción:
    Servicio para gestionar operaciones relacionadas con integraciones de scripts y dispositivos.
    """
    def comprobar_script(script): ##En el editar igual hay que comprobarlo con todos los ficheros
        """
        Descripción:
        Comprueba si un script específico ya está en uso por alguna integración.

        Parámetros:
        script (str): El nombre del script que se desea comprobar.

        Retorna:
        bool: True si el script está en uso, False si no está en uso.

        Excepciones:
        Exception: Captura y maneja cualquier excepción que ocurra al intentar comprobar el script.
        """
        integracion_dao = IntegracionDAO()
        integracion_data = integracion_dao.obtener_scripts()
        if script in integracion_data:
            return True
        return False
    
    def comprobar_script_valido(script, nombre_integracion):
        """
        Descripción:
        Verifica si un script específico está siendo utilizado por otra integración o es válido para una integración.

        Parámetros:
        script (str): El nombre del script que se desea verificar.
        nombre_integracion (str): El nombre de la integración que se está editando.

        Retorna:
        bool: True si el script es válido para la integración especificada, False si no lo es.

        Excepciones:
        Exception: Captura y maneja cualquier excepción que ocurra al intentar verificar el script.
        """
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
        """
        Descripción:
        Elimina los scripts que no están asociados a ninguna integración desde el directorio de scripts.

        Retorna:
        bool: True si se eliminaron los scripts correctamente, False en caso contrario.

        Excepciones:
        Exception: Captura y maneja cualquier excepción que ocurra al intentar eliminar los scripts.
        """
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
        """
        Descripción:
        Obtiene todas las integraciones existentes en la base de datos.

        Retorna:
        list: Lista de diccionarios con los datos de las integraciones.

        Excepciones:
        Exception: Captura y maneja cualquier excepción que ocurra al intentar obtener las integraciones.
        """
        integracion_dao = IntegracionDAO()
        integracion_data = integracion_dao.obtener_integraciones()
        #print("integracion DATA:", integracion_data)
        return integracion_data
    
    def obtener_tipos():
        """
        Descripción:
        Obtiene todos los tipos de integraciones disponibles.

        Retorna:
        list: Lista de diccionarios con los tipos de integraciones.

        Excepciones:
        Exception: Captura y maneja cualquier excepción que ocurra al intentar obtener los tipos.
        """
        integracion_dao = IntegracionDAO()
        tipos_data = integracion_dao.obtener_tipos()
        print("Tipos DATA:", tipos_data)
        return tipos_data
    
    def crear_integracion(nombre, nombre_script, script, atributos):
        """
        Descripción:
        Crea una nueva integración de script para dispositivos y guarda el script en el directorio correspondiente.

        Parámetros:
        nombre (str): El nombre de la nueva integración.
        nombre_script (str): El nombre del script de la nueva integración.
        script (str): El contenido del script.
        atributos (list): Lista de atributos para la integración.

        Retorna:
        bool: True si la integración fue creada exitosamente, False en caso contrario.

        Excepciones:
        ValueError: Si el script está en uso por otra integración.
        Exception: Captura y maneja cualquier excepción que ocurra al intentar crear la integración.
        """
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
        """
        Descripción:
        Edita una integración existente de script para dispositivos y actualiza el script en el directorio correspondiente.

        Parámetros:
        prev_nombre (str): El nombre actual de la integración que se desea editar.
        nombre (str): El nuevo nombre de la integración.
        nombre_script (str): El nuevo nombre del script de la integración.
        script (str): El nuevo contenido del script.
        atributos (list): Lista de atributos actualizados para la integración.

        Retorna:
        bool: True si la integración fue editada exitosamente, False en caso contrario.

        Excepciones:
        ValueError: Si el nuevo nombre del script está en uso por otra integración o no es válido.
        Exception: Captura y maneja cualquier excepción que ocurra al intentar editar la integración.
        """
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
        """
        Descripción:
        Elimina una integración de script para dispositivos desde la base de datos y elimina el script correspondiente del directorio.

        Parámetros:
        id (int): El ID de la integración que se desea eliminar.

        Retorna:
        bool: True si la integración fue eliminada exitosamente, False en caso contrario.

        Excepciones:
        Exception: Captura y maneja cualquier excepción que ocurra al intentar eliminar la integración.
        """
        integracion_dao = IntegracionDAO()
        integracion_data = integracion_dao.eliminar_integracion(id)
        integracionService.eliminar_scripts() ###LO DE LOS SCRIPTS NO ES ASI, O SI
        return integracion_data
    
