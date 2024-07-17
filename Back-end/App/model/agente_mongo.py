import pymongo

class Agente:
    """
    Descripción:
    Clase que maneja operaciones CRUD básicas en una colección MongoDB utilizando pymongo.
    """
    def __init__(self, db_host, db_port, db_name, collection_name, user, password):
        """
        Inicializa una instancia de Agente para interactuar con una colección en MongoDB.

        Parámetros:
        - db_host (str): Dirección IP o nombre de host del servidor MongoDB.
        - db_port (int): Puerto del servidor MongoDB.
        - db_name (str): Nombre de la base de datos MongoDB.
        - collection_name (str): Nombre de la colección dentro de la base de datos.
        - user (str): Nombre de usuario para autenticación en MongoDB.
        - password (str): Contraseña del usuario para autenticación en MongoDB.
        """
        self.client = pymongo.MongoClient(host=db_host, port=int(db_port), username=user, password=password)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        print(db_host, db_port, db_name, collection_name)

    def insertar_documento(self, documento):
        """
        Descripción:
        Inserta un nuevo documento en la colección.

        Parámetros:
        - documento (dict): Documento a ser insertado en la colección.

        Retorna:
        No hay retorno explícito.

        Excepciones:
        pymongo.errors.PyMongoError: Error al insertar el documento en la colección.
        """
        self.collection.insert_one(documento)
    
    def buscar_documento(self, filtro, sort=None):
        """
        Descripción:
        Busca y devuelve un documento basado en el filtro proporcionado.

        Parámetros:
        - filtro (dict): Filtro para buscar el documento en la colección.
        - sort (dict): Opcional. Especifica el orden de clasificación del documento.

        Retorna:
        - dict: Documento encontrado que cumple con el filtro especificado.

        Excepciones:
        pymongo.errors.PyMongoError: Error al buscar el documento en la colección.
        """
        if sort is not None:
            return self.collection.find_one(filter=filtro, sort=sort)
        else:
            return self.collection.find_one(filter=filtro)

    def buscar_documentos(self, filtro, campos=None):
        """
        Descripción:
        Busca y devuelve múltiples documentos basados en el filtro y campos especificados.

        Parámetros:
        - filtro (dict): Filtro para buscar los documentos en la colección.
        - campos (list): Opcional. Lista de campos a incluir en los documentos devueltos.

        Retorna:
        - pymongo.cursor.Cursor: Cursor iterable con los documentos encontrados que cumplen con el filtro.

        Excepciones:
        pymongo.errors.PyMongoError: Error al buscar los documentos en la colección.
        """
        print(campos)
        incluir={}
        if campos is None or campos == []:
            campos = ["dispositivo", "timestamp", "attributes"]
            for campo in campos:
                incluir[campo] = 1
        else:
            campos.append("dispositivo")
            campos.append("timestamp")
            for campo in campos:
                if campo != "dispositivo" and campo != "timestamp":
                    campo = "attributes."+campo
                incluir[campo] = 1


        print(incluir)
        return(self.collection.find(filtro, incluir))

    def actualizar_documento(self, filtro, nuevo_valor):
        """
        Descripción:
        Actualiza un documento en la colección basado en el filtro proporcionado.

        Parámetros:
        - filtro (dict): Filtro para encontrar el documento a actualizar.
        - nuevo_valor (dict): Nuevos valores a ser aplicados al documento encontrado.

        Retorna:
        No hay retorno explícito.

        Excepciones:
        pymongo.errors.PyMongoError: Error al actualizar el documento en la colección.
        """
        self.collection.update_one(filtro, {"$set": nuevo_valor})

    def eliminar_documento(self, filtro):
        """
        Descripción:
        Elimina un documento de la colección basado en el filtro proporcionado.

        Parámetros:
        - filtro (dict): Filtro para encontrar el documento a eliminar.

        Retorna:
        No hay retorno explícito.

        Excepciones:
        pymongo.errors.PyMongoError: Error al eliminar el documento de la colección.
        """
        self.collection.delete_one(filtro)
