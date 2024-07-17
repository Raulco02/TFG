import hashlib
from App.model.grupoDAO import grupoDAO
from App.model.mysql_dispositivoDAO import mysql_dispositivoDAO

class grupoService:
    """
    Descripción:
    Servicio para gestionar operaciones relacionadas con grupos y dispositivos.
    """
    def obtener_grupos_por_id_usuario(id):
        """
        Descripción:
        Obtiene todos los grupos asociados a un usuario específico.

        Parámetros:
        id (int): El ID del usuario cuyos grupos se desean obtener.

        Retorna:
        list: Lista de diccionarios con los datos de los grupos asociados al usuario especificado.

        Excepciones:
        Exception: Captura y maneja cualquier excepción que ocurra al intentar obtener los grupos.
        """
        grupo_dao = grupoDAO()
        grupo_data = grupo_dao.obtener_grupos_por_id_usuario(id)
        print("grupo DATA:", grupo_data)
        grupos=[]
        if grupo_data is not None:
            for grupo in grupo_data:
                grupos.append({"id": grupo[0], "nombre": grupo[1], "icono": grupo[2]})
            print("grupos:", grupos)
        return grupos
    
    def obtener_dispositivo_por_grupo(id_grupo, id_usuario):
        """
        Descripción:
        Obtiene los dispositivos asociados a un grupo específico de un usuario.

        Parámetros:
        id_grupo (int): El ID del grupo cuyos dispositivos se desean obtener.
        id_usuario (int): El ID del usuario propietario del grupo.

        Retorna:
        list: Lista de diccionarios con los datos de los dispositivos asociados al grupo especificado.

        Excepciones:
        ValueError: Si no se encuentra el grupo para el usuario especificado.
        Exception: Captura y maneja cualquier excepción que ocurra al intentar obtener los dispositivos.
        """
        grupo_dao = grupoDAO()
        grupos_usuario = grupo_dao.obtener_grupos_por_id_usuario(id_usuario)
        print("Grupos usuario:", grupos_usuario)
        dispositivos = []
        if grupos_usuario is not None:
            for grupo in grupos_usuario:
                print("Grupo:", grupo, "ID:", id_grupo, "ID GRUPO:", grupo[0])
                if grupo[0] == id_grupo:
                    ids_dispositivos = grupo_dao.obtener_ids_dispositivos_por_grupo(id_grupo)
                    for id_dispositivo in ids_dispositivos:
                        dispositivo = mysql_dispositivoDAO().obtener_dispositivo_por_id(id_dispositivo[0])
                        if dispositivo is not None:
                            dispositivos.append(dispositivo[0])
                    return dispositivos
                        
        raise ValueError("No se encontró el grupo")
    
    def crear_grupo_por_usuario_id(grupo_nombre, grupo_icono, id_usuario, dispositivos):
        """
        Descripción:
        Crea un nuevo grupo para un usuario específico y asocia dispositivos al grupo.

        Parámetros:
        grupo_nombre (str): El nombre del nuevo grupo.
        grupo_icono (str): El icono del nuevo grupo (opcional, valor por defecto es "default").
        id_usuario (int): El ID del usuario para el cual se crea el grupo.
        dispositivos (list): Lista de IDs de dispositivos que se desean asociar al grupo.

        Retorna:
        bool: True si el grupo fue creado exitosamente, False en caso contrario.

        Excepciones:
        Exception: Captura y maneja cualquier excepción que ocurra al intentar crear el grupo.
        """
        grupo_dao = grupoDAO()
        if grupo_icono is None:
            grupo_icono = "default"
        grupo = {"nombre": grupo_nombre, "icono": grupo_icono}
        grupo_dao.crear_grupo_por_usuario_id(grupo, id_usuario, dispositivos)
        return True