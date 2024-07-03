import pymongo

class Agente:
    def __init__(self, db_host, db_port, db_name, collection_name, user, password):
        self.client = pymongo.MongoClient(host=db_host, port=int(db_port), username=user, password=password)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        print(db_host, db_port, db_name, collection_name)

    def insertar_documento(self, documento):
        self.collection.insert_one(documento)
    
    def buscar_documento(self, filtro, sort=None):
        if sort is not None:
            return self.collection.find_one(filter=filtro, sort=sort)
        else:
            return self.collection.find_one(filter=filtro)

    def buscar_documentos(self, filtro, campos=None):
        print(campos)
        incluir={}
        if campos is None or campos == []:
            campos = ["sensor", "timestamp", "attributes"]
            for campo in campos:
                incluir[campo] = 1
        else:
            campos.append("sensor")
            campos.append("timestamp")
            for campo in campos:
                if campo != "sensor" and campo != "timestamp":
                    campo = "attributes."+campo
                incluir[campo] = 1


        print(incluir)
        return(self.collection.find(filtro, incluir))

    def actualizar_documento(self, filtro, nuevo_valor):
        self.collection.update_one(filtro, {"$set": nuevo_valor})

    def eliminar_documento(self, filtro):
        self.collection.delete_one(filtro)
