import hashlib
from App.model.grupoDAO import grupoDAO
from App.model.mysql_dispositivoDAO import mysql_dispositivoDAO

class grupoService:    
    def obtener_grupos_por_id_usuario(id):
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
        grupo_dao = grupoDAO()
        if grupo_icono is None:
            grupo_icono = "default"
        grupo = {"nombre": grupo_nombre, "icono": grupo_icono}
        grupo_dao.crear_grupo_por_usuario_id(grupo, id_usuario, dispositivos)
        return True