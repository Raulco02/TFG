import hashlib
from App.model.reglaDAO import reglaDAO
from App.model.mysql_dispositivoDAO import mysql_dispositivoDAO

class reglaService:
    """
    Descripción:
    Servicio para gestionar reglas y alertas relacionadas con dispositivos y usuarios en la aplicación.
    """
    def obtener_reglas_por_id_usuario(id):
        """
        Descripción:
        Obtiene las reglas asociadas a un usuario específico desde la base de datos.

        Parámetros:
        id (int): El ID del usuario para el cual se obtienen las reglas.

        Retorna:
        list: Lista de reglas asociadas al usuario.

        Excepciones:
        None
        """
        regla_dao = reglaDAO()
        regla_data = regla_dao.obtener_reglas_por_id_usuario(id)
        # print("regla DATA:", regla_data)
        # reglas=[]
        # if regla_data is not None:
        #     criterios_data = []
        #     acciones_data = []
        #     for regla in regla_data:
        #         print("regla:", regla)
        #         criterios = regla[1]
        #         print("criterios:", criterios)
        #         i=0
        #         for criterio in criterios:
        #             print(i)
        #             print(criterio)
        #             print(criterio[i])
        #             criterios_data.append({"id": criterio[i][0], "atributo_id": criterio[i][2], "dispositivo_id": criterio[i][3], "valor": criterio[i][4], "comparador": criterio[i][5], "tipo": criterio[i][6]})
        #             i+=1
        #         print("criterios_data:", criterios_data)
        #         acciones = regla[2]
        #         print("acciones:", acciones)
        #         i=0
        #         for accion in acciones:
        #             acciones_data.append({"id": accion[i][0], "atributo_id": accion[i][2], "dispositivo_id": accion[i][3], "accion_id": accion[i][4]})
        #             i+=1
        #         reglas.append({"id": regla[0], "nombre": regla[1], "icono": regla[2], "criterios": criterios, "acciones": acciones})
        #     print("reglas:", reglas)
        if regla_data is not None:
            return regla_data
        return None
    
    def obtener_alertas_por_id_usuario(id):
        """
        Descripción:
        Obtiene las alertas asociadas a un usuario específico desde la base de datos.

        Parámetros:
        id (int): El ID del usuario para el cual se obtienen las alertas.

        Retorna:
        list: Lista de alertas asociadas al usuario.

        Excepciones:
        None
        """
        regla_dao = reglaDAO()
        regla_data = regla_dao.obtener_reglas_por_id_usuario(id, True)
        if regla_data is not None:
            return regla_data
        return None
    
    def obtener_dispositivo_por_regla(id_regla, id_usuario):
        """
        Descripción:
        Obtiene los dispositivos asociados a una regla específica de un usuario desde la base de datos.

        Parámetros:
        id_regla (int): El ID de la regla para la cual se obtienen los dispositivos.
        id_usuario (int): El ID del usuario propietario de la regla.

        Retorna:
        list: Lista de dispositivos asociados a la regla.

        Excepciones:
        ValueError: Si no se encuentra la regla especificada.
        """
        regla_dao = reglaDAO()
        reglas_usuario = regla_dao.obtener_reglas_por_id_usuario(id_usuario)
        print("reglas usuario:", reglas_usuario)
        dispositivos = []
        if reglas_usuario is not None:
            for regla in reglas_usuario:
                print("regla:", regla, "ID:", id_regla, "ID regla:", regla[0])
                if regla[0] == id_regla:
                    ids_dispositivos = regla_dao.obtener_ids_dispositivos_por_regla(id_regla)
                    for id_dispositivo in ids_dispositivos:
                        dispositivo = mysql_dispositivoDAO().obtener_dispositivo_por_id(id_dispositivo[0])
                        if dispositivo is not None:
                            dispositivos.append(dispositivo[0])
                    return dispositivos
                        
        raise ValueError("No se encontró el regla")
    
    def obtener_reglas():
        """
        Descripción:
        Obtiene todas las reglas almacenadas en la base de datos.

        Parámetros:
        None

        Retorna:
        list: Lista de todas las reglas almacenadas.

        Excepciones:
        None
        """
        regla_dao = reglaDAO()
        reglas = regla_dao.obtener_reglas()
        return reglas   
    
    def crear_regla_por_usuario_id(nombre, id_usuario, criterios, acciones, alerta=False):
        """
        Descripción:
        Crea una nueva regla o alerta para un usuario específico en la base de datos.

        Parámetros:
        nombre (str): Nombre de la regla o alerta a crear.
        id_usuario (int): ID del usuario para el cual se crea la regla.
        criterios (list): Lista de criterios que definen la condición de la regla.
        acciones (list): Lista de acciones a ejecutar cuando se cumple la regla.
        alerta (bool, opcional): Indica si la regla es una alerta (por defecto False).

        Retorna:
        bool: True si la regla fue creada exitosamente.

        Excepciones:
        None
        """
        regla_dao = reglaDAO()
        print("En creando alerta service")
        regla = {"nombre": nombre,"id_usuario": id_usuario, "criterios": criterios, "acciones": acciones}
        print("Objeto alerta creado", regla)
        regla_dao.crear_regla_por_usuario_id(regla, alerta)
        return True
    
    def eliminar_regla_por_id(regla_id, usuario_id):
        """
        Descripción:
        Elimina una regla específica de un usuario desde la base de datos.

        Parámetros:
        regla_id (int): ID de la regla que se desea eliminar.
        usuario_id (int): ID del usuario propietario de la regla.

        Retorna:
        bool: True si la regla fue eliminada exitosamente.

        Excepciones:
        None
        """
        regla_dao = reglaDAO()
        regla_dao.eliminar_regla_por_id(regla_id, usuario_id)
        return True