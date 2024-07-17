import hashlib
from App.model.seccionDAO import seccionDAO
from App.model.tarjetaDAO import tarjetaDAO
from App.model.seccion import Seccion
from App.model.tarjeta import Tarjeta
from App.helpers.tarjetas import tarjetasHelper

class seccionService:
    """
    Descripción:
    Servicio para gestionar secciones y tarjetas asociadas a los dashboards en la aplicación.
    """
    def obtener_secciones(id_dashboard):
        """
        Descripción:
        Obtiene todas las secciones asociadas a un dashboard específico desde la base de datos.

        Parámetros:
        id_dashboard (int): ID del dashboard para el cual se obtienen las secciones.

        Retorna:
        list: Lista de secciones asociadas al dashboard.

        Excepciones:
        None
        """
        seccion_dao = seccionDAO()
        seccion_data = seccion_dao.obtener_secciones(id_dashboard)
        print("seccion DATA:", seccion_data)
        seccions=[]
        if seccion_data is None:
            return None
        for seccion in seccion_data:
            seccions.append({"id": seccion[0], "nombre": seccion[1], "icono": seccion[2], "layout": seccion[3], "numFilas": seccion[4]})
        print("seccions:", seccions)
        return seccions
    
    def obtener_seccion(id_seccion):
        """
        Descripción:
        Obtiene una sección específica junto con las tarjetas asociadas desde la base de datos.

        Parámetros:
        id_seccion (int): ID de la sección que se desea obtener.

        Retorna:
        dict: Información de la sección incluyendo sus tarjetas asociadas.

        Excepciones:
        None
        """
        tarjeta_dao = tarjetaDAO()
        seccion_dao = seccionDAO()
        seccion_data = seccion_dao.obtener_seccion(id_seccion)
        tarjeta_data = tarjeta_dao.obtener_tarjetas_seccion(id_seccion)
        if tarjeta_data is None:
            tarjeta_data = []
        lista_tarjetas = tarjetasHelper.generar_lista_tarjetas(tarjeta_data, tarjeta_dao)#seccionService.generar_lista_tarjetas(tarjeta_data, tarjeta_dao)
        print("seccion DATA:", seccion_data)
        seccions=[]
        if seccion_data is None:
            return None
        seccions.append({"id": seccion_data[0], "nombre": seccion_data[1], "icono": seccion_data[2], "layout": seccion_data[3], "numFilas": seccion_data[4], "tarjetas": lista_tarjetas})
        print("seccion:", seccions)
        return seccions
    
    def comprobar_seccion(id_seccion, id_usuario):
        """
        Descripción:
        Verifica si una sección específica pertenece a un usuario.

        Parámetros:
        id_seccion (int): ID de la sección que se desea verificar.
        id_usuario (int): ID del usuario propietario de la sección.

        Retorna:
        bool: True si la sección pertenece al usuario, False en caso contrario.

        Excepciones:
        None
        """
        seccion_dao = seccionDAO()
        existe = seccion_dao.comprobar_seccion(id_seccion, id_usuario)
        return existe
    
    def obtener_secciones_usuario(dashboards):
        """
        Descripción:
        Obtiene todas las secciones de múltiples dashboards junto con sus tarjetas asociadas.

        Parámetros:
        dashboards (list): Lista de dashboards de los cuales se obtendrán las secciones.

        Retorna:
        list: Lista de dashboards con sus respectivas secciones y tarjetas.

        Excepciones:
        None
        """
        seccion_dao = seccionDAO()
        tarjeta_dao = tarjetaDAO()
        print('DASHBOARDS:', dashboards)
        for dashboard in dashboards:
            print("Entra")
            secciones=[]
            seccion_data = seccion_dao.obtener_secciones(dashboard['id'])
            if seccion_data is None:
                print('Es aquí')
                break
            print(dashboard['id'])
            for seccion in seccion_data:
                print(seccion[0])
                tarjetas = tarjeta_dao.obtener_tarjetas_seccion(seccion[0])
                tarjetas_lista = tarjetasHelper.generar_lista_tarjetas(tarjetas, tarjeta_dao)#seccionService.generar_lista_tarjetas(tarjetas, tarjeta_dao)
                secciones.append({"id": seccion[0], "nombre": seccion[1], "icono": seccion[2], "layout": seccion[3], "numFilas": seccion[4], "tarjetas": tarjetas_lista})
            print('a')
            dashboard['secciones'] = secciones
        return dashboards
    
    def obtener_secciones_dashboard(id_dashboard):
        """
        Descripción:
        Obtiene todas las secciones asociadas a un dashboard específico desde la base de datos.

        Parámetros:
        id_dashboard (int): ID del dashboard para el cual se obtienen las secciones.

        Retorna:
        list: Lista de secciones asociadas al dashboard.

        Excepciones:
        None
        """
        seccion_dao = seccionDAO()
        seccion_data = seccion_dao.obtener_secciones(id_dashboard)
        secciones=[]
        if seccion_data is None:
            return None
        for seccion in seccion_data:
            secciones.append({"id": seccion[0], "nombre": seccion[1], "icono": seccion[2], "layout": seccion[3], "numFilas": seccion[4]})
        return secciones
    
    # def generar_lista_tarjetas(tarjetas, tarjeta_dao):
    #     print(tarjetas)
    #     tarjeta={}
    #     tarjetas_lista=[]
    #     #tarjetas = seccion[4]
    #     if tarjetas is None:
    #         tarjetas = []
    #     for tarj in tarjetas: #Hacer método para comprobaciones de que las tarjetas estén de forma correcta
    #         if(tarj[1] == 'Estado' or tarj[1] == 'Termostato'):
    #             print('TUPLA', tarj)
    #             tarjeta = Tarjeta(tarj[1], tarj[2], tarj[7], tarj[3], tarj[4], tarj[5], tarj[6], tarj[11], tarj[8], tarj[9], tarj[10], tarj[14], tarj[12], tarj[13])
    #         elif(tarj[1] == 'Grafico'):
    #             print('TUPLA', tarj)
    #             print('TARJETA GRAFICO',tarj)
    #             tarjeta = Tarjeta(tarj[1], tarj[2], tarj[7], tarj[3], tarj[4], tarj[5], tarj[6], tarj[11], tarj[8], tarj[9], tarj[10], tarj[14], tarj[12], tarj[13])
    #         elif(tarj[1] == 'Grupo'):
    #             print('TUPLA', tarj)
    #             i=0
    #             for t in tarj:
    #                 print(t,i)
    #                 i+=1
    #             tarjeta = Tarjeta(tarj[1], tarj[2], tarj[7], tarj[3], tarj[4], tarj[5], tarj[6], tarj[11], tarj[14], tarj[15], tarj[16], tarj[17], tarj[12], tarj[13], tarj[8][0], tarj[9][0], tarj[10][0])
    #         else:
    #             print('Dentro del else')
    #             tarjeta = Tarjeta(tarj[1], tarj[2], tarj[7], tarj[3], tarj[4], tarj[5], tarj[6])
    #             print('Despues de crear tarjeta en else')

    #         print('Tarjeta:', tarjeta.tipo)
    #         print('Aqui llega')
    #         print('Tarjeta', tarjeta.tipo, tarjeta.posicion, tarjeta.contenido, tarjeta.imagen, tarjeta.id_dispositivo, tarjeta.id_atributo, tarjeta.tipo_grafico, tarjeta.tiempo_grafico, tarjeta.id_seccion, tarjeta.valor, tarjeta.nombre_atributo, tarjeta.unidades, tarjeta.icono)
    #         tarjeta_data = tarjeta_dao.obtener_tarjeta_tipo(tarjeta)#{"id": tarj[0], "tipo": tarj[1], "posicion": tarj[2], "dimensiones": tarj[3], "contenido": tarj[4], "imagen": tarj[5], "id-dispositivo": tarj[6], "id-atributo": tarj[7], "tipo-grafico": tarj[8], "tiempo-grafico": tarj[9], "id-seccion": tarj[10]}
    #         tarjeta_data['id'] = tarj[0]
    #         print('Tarjeta data:', tarjeta_data)
    #         tarjetas_lista.append(tarjeta_data)
    #     print('Tarjetas lista:', tarjetas_lista)
    #     return tarjetas_lista
    
    def crear_seccion_por_dashboard_id(nombre, icono, layout, dashboard_id):
        """
        Descripción:
        Crea una nueva sección asociada a un dashboard específico en la base de datos.

        Parámetros:
        nombre (str): Nombre de la nueva sección.
        icono (str): Icono de la nueva sección.
        layout (str): Layout de la nueva sección.
        dashboard_id (int): ID del dashboard al cual se asociará la nueva sección.

        Retorna:
        dict: Información de la sección creada.

        Excepciones:
        None
        """
        print('ID DASHBOARD en DAO:', dashboard_id)
        seccion_dao = seccionDAO()
        seccion = Seccion(nombre, icono, layout)
        seccion_data = seccion_dao.crear_seccion_por_usuario_id(seccion, dashboard_id)
        return seccion_data
    
    def editar_seccion(id, nombre, icono, layout, dashboard_id):
        """
        Descripción:
        Edita una sección existente en la base de datos.

        Parámetros:
        id (int): ID de la sección que se desea editar.
        nombre (str): Nuevo nombre de la sección.
        icono (str): Nuevo icono de la sección.
        layout (str): Nuevo layout de la sección.
        dashboard_id (int): ID del dashboard al cual pertenece la sección.

        Retorna:
        dict: Información de la sección editada.

        Excepciones:
        None
        """
        seccion_dao = seccionDAO()
        seccion_data = seccion_dao.editar_seccion(id, nombre, icono, layout, dashboard_id)
        return seccion_data
    
    def obtener_dashboard_por_seccion(id_seccion):
        """
        Descripción:
        Obtiene el dashboard al cual pertenece una sección específica.

        Parámetros:
        id_seccion (int): ID de la sección de la cual se desea obtener el dashboard.

        Retorna:
        dict: Información del dashboard al cual pertenece la sección.

        Excepciones:
        None
        """
        seccion_dao = seccionDAO()
        seccion_data = seccion_dao.obtener_dashboard_por_seccion(id_seccion)
        print("DASHBOARD DATA:", seccion_data)
        dash = seccion_data[0]
        return dash
    
    def subir_numero_filas(id_seccion):
        """
        Descripción:
        Aumenta el número de filas de una sección en la base de datos.

        Parámetros:
        id_seccion (int): ID de la sección a la cual se desea aumentar el número de filas.

        Retorna:
        bool: True si se aumentó el número de filas exitosamente.

        Excepciones:
        None
        """
        seccion_dao = seccionDAO()
        seccion_data = seccion_dao.subir_numero_filas(id_seccion)
        return seccion_data
    
    