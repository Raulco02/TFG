import os
import configparser
import mysql.connector

class agente_mysql:
    """
    Descripción:
    Clase que gestiona operaciones básicas en una base de datos MySQL utilizando mysql.connector.
    """
    def __init__(self):
        """
        Descripción:
        Inicializa una instancia de agente_mysql y carga la configuración desde el archivo secrets.cfg.

        Retorna:
        No hay retorno explícito.
        
        Excepciones:
        KeyError: Si la sección 'MYSQL' no está presente en el archivo secrets.cfg.
        """
        self.config = configparser.ConfigParser()
        # Configuración de MongoDB
        current_dir = os.path.dirname(os.path.abspath(__file__))
        print("Directorio actual:", current_dir)
        # Cargar la configuración desde el archivo secrets.cfg
        # Construir la ruta completa del archivo secrets.cfg
        self.secrets_path = os.path.join(current_dir, '..', '..\Config', 'secrets.cfg')
        print("Ruta de secrets.cfg:", self.secrets_path)
        self.config.read(self.secrets_path)
        try:
            self.host = self.config['MYSQL']['mysql_host']
            self.username = self.config['MYSQL']['mysql_username']
            self.password = self.config['MYSQL']['mysql_password']
            self.database = self.config['MYSQL']['mysql_database']
        except KeyError:
            print("Error: Configuración 'MYSQL' no encontrada en secrets.cfg")
            self.host = None
            self.username = None
            self.password = None
            self.database = None
        self.connection = None
        self.cursor = None

    def connect(self):
        """
        Descripción:
        Establece una conexión con la base de datos MySQL utilizando los parámetros de configuración cargados.

        Retorna:
        No hay retorno explícito.

        Excepciones:
        mysql.connector.Error: Error al conectar con la base de datos MySQL.
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor()
            print("Conexión exitosa a la base de datos MySQL")
        except mysql.connector.Error as err:
            print(f"Error al conectar a la base de datos MySQL: {err}")
            raise

    def disconnect(self):
        """
        Descripción:
        Establece una conexión con la base de datos MySQL utilizando los parámetros de configuración cargados.

        Retorna:
        No hay retorno explícito.

        Excepciones:
        mysql.connector.Error: Error al conectar con la base de datos MySQL.
        """
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Conexión cerrada")

    def start_transaction(self):
        """
        Descripción:
        Inicia una nueva transacción en la conexión activa.

        Retorna:
        No hay retorno explícito.

        Excepciones:
        mysql.connector.Error: Error al iniciar la transacción.
        """
        try:
            self.connection.start_transaction()
            print("Transacción iniciada")
        except mysql.connector.Error as err:
            print(f"Error al iniciar la transacción: {err}")
            raise

    def commit_transaction(self):
        """
        Descripción:
        Confirma la transacción actual en la conexión activa.

        Retorna:
        No hay retorno explícito.

        Excepciones:
        mysql.connector.Error: Error al confirmar la transacción.
        """
        try:
            self.connection.commit()
            print("Transacción confirmada")
        except mysql.connector.Error as err:
            print(f"Error al confirmar la transacción: {err}")
            raise

    def rollback_transaction(self):
        """
        Descripción:
        Revierte la transacción actual en la conexión activa.

        Retorna:
        No hay retorno explícito.

        Excepciones:
        mysql.connector.Error: Error al revertir la transacción.
        """
        try:
            self.connection.rollback()
            print("Transacción revertida")
        except mysql.connector.Error as err:
            print(f"Error al revertir la transacción: {err}")
            raise

    def execute_query(self, query, values=None):
        """
        Descripción:
        Ejecuta una consulta SQL en la base de datos utilizando los parámetros proporcionados.

        Parámetros:
        - query (str): Consulta SQL a ejecutar.
        - values (tuple): Opcional. Valores a ser pasados a la consulta SQL.

        Retorna:
        - list or None: Lista de registros devueltos por la consulta si es una consulta SELECT, o None.

        Excepciones:
        mysql.connector.Error: Error al ejecutar la consulta SQL.
        """
        try:
            print('Query en execute query:', query)
            if values:
                print('Values en execute query:', values)
                self.cursor.execute(query, values)
            else:
                self.cursor.execute(query)
            
            records = None
            if query.strip().upper().startswith("SELECT"):
                records = self.cursor.fetchall()
                
            print("Operación exitosa")
            return records
        except mysql.connector.Error as err:
            print(f"Error al ejecutar la consulta: {err}")
            raise

    def create_record(self, table, data):
        """
        Descripción:
        Crea un nuevo registro en la tabla especificada con los datos proporcionados.

        Parámetros:
        - table (str): Nombre de la tabla donde se creará el registro.
        - data (dict): Datos del nuevo registro, donde las claves son nombres de columnas y los valores son los datos.

        Retorna:
        - int or None: ID del último registro insertado si la operación fue exitosa, o None si falló.

        Excepciones:
        mysql.connector.Error: Error al ejecutar la consulta de inserción.
        """
        placeholders = ', '.join(['%s'] * len(data))
        columns = ', '.join([f"`{column}`" for column in data.keys()])
        values = tuple(data.values())
        table_name = f"`{table}`"
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        

        self.execute_query(query, values)
        return self.cursor.lastrowid

    def read_records(self, table, condition=None):
        """
        Descripción:
        Lee registros de la tabla especificada en la base de datos según la condición proporcionada.

        Parámetros:
        - table (str): Nombre de la tabla de donde se leerán los registros.
        - condition (str): Opcional. Condición para filtrar los registros a leer.

        Retorna:
        - list or None: Lista de registros leídos si la operación fue exitosa, o None si no se encontraron registros.

        Excepciones:
        mysql.connector.Error: Error al ejecutar la consulta de lectura.
        """
        table_name = f"`{table}`"
        query = f"SELECT * FROM {table_name}"
        if condition:
            query += f" WHERE {condition}"
        records = self.execute_query(query)
        return records

    def update_record(self, table, data, condition):
        """
        Descripción:
        Actualiza registros en la tabla especificada con los nuevos datos proporcionados y la condición dada.

        Parámetros:
        - table (str): Nombre de la tabla donde se actualizarán los registros.
        - data (dict): Datos actualizados, donde las claves son nombres de columnas y los valores son los nuevos datos.
        - condition (str): Condición para filtrar los registros que se actualizarán.

        Retorna:
        - list or None: Lista de registros antes de la actualización si la operación fue exitosa y se encontraron registros, o None si no se encontraron registros para actualizar.

        Excepciones:
        mysql.connector.Error: Error al ejecutar la consulta de actualización.
        """
        update_values = ', '.join([f"{key} = %s" for key in data.keys()])
        values = tuple(data.values())
        query_select = f"SELECT * FROM {table} WHERE {condition}"
        records = self.execute_query(query_select)  # Fetch the records before update

        if records:
            query_update = f"UPDATE {table} SET {update_values} WHERE {condition}"
            self.execute_query(query_update, values)
            return records  # Return the records fetched before the update
        else:
            return None

    def delete_record(self, table, condition):
        """
        Descripción:
        Elimina registros de la tabla especificada según la condición dada.

        Parámetros:
        - table (str): Nombre de la tabla de donde se eliminarán los registros.
        - condition (str): Condición para filtrar los registros que se eliminarán.

        Retorna:
        - bool: True si se eliminaron registros exitosamente, False si no se eliminaron registros.

        Excepciones:
        mysql.connector.Error: Error al ejecutar la consulta de eliminación.
        """
        query = f"DELETE FROM {table} WHERE {condition}"
        print('Query en delete:', query)
        self.execute_query(query)
        rows_affected = self.cursor.rowcount
        print('Rows affected:', rows_affected)
        return rows_affected > 0

    def read_records_by_query(self, query, params):
        """
        Descripción:
        Ejecuta una consulta SQL personalizada con parámetros.

        Parámetros:
        - query (str): Consulta SQL a ejecutar.
        - params (tuple): Parámetros para la consulta SQL.

        Retorna:
        - list or None: Lista de registros devueltos por la consulta si la operación fue exitosa, o None si no se encontraron registros.

        Excepciones:
        mysql.connector.Error: Error al ejecutar la consulta SQL personalizada.
        """
        try:
            self.cursor.execute(query, params)
            records = self.cursor.fetchall()
            return records
        except mysql.connector.Error as err:
            print(f"Error al ejecutar la consulta: {err}")
            raise



# import os
# import configparser
# import mysql.connector

# class agente_mysql:
#     def __init__(self):
#         self.config = configparser.ConfigParser()
#         # Configuración de MongoDB
#         current_dir = os.path.dirname(os.path.abspath(__file__))
#         print("Directorio actual:", current_dir)
#         # Cargar la configuración desde el archivo secrets.cfg
#         # Construir la ruta completa del archivo secrets.cfg
#         self.secrets_path = os.path.join(current_dir, '..', '..\Config', 'secrets.cfg')
#         print("Ruta de secrets.cfg:", self.secrets_path)
#         self.config.read(self.secrets_path)
#         try:
#             self.host = self.config['MYSQL']['mysql_host']
#             self.username = self.config['MYSQL']['mysql_username']
#             self.password = self.config['MYSQL']['mysql_password']
#             self.database = self.config['MYSQL']['mysql_database']
#         except KeyError:
#             print("Error: Configuración 'MYSQL' no encontrada en secrets.cfg")
#             self.host = None
#             self.username = None
#             self.password = None
#             self.database = None
#         self.connection = None
#         self.cursor = None

#     def connect(self):
#         try:
#             self.connection = mysql.connector.connect(
#                 host=self.host,
#                 user=self.username,
#                 password=self.password,
#                 database=self.database
#             )
#             self.cursor = self.connection.cursor()
#             print("Conexión exitosa a la base de datos MySQL")
#         except mysql.connector.Error as err:
#             print(f"Error al conectar a la base de datos MySQL: {err}")
#             raise

#     def disconnect(self):
#         if self.connection.is_connected():
#             self.cursor.close()
#             self.connection.close()
#             print("Conexión cerrada")

#     def start_transaction(self):
#         try:
#             self.connection.start_transaction()
#             print("Transacción iniciada")
#         except mysql.connector.Error as err:
#             print(f"Error al iniciar la transacción: {err}")
#             raise

#     def commit_transaction(self):
#         try:
#             self.connection.commit()
#             print("Transacción confirmada")
#         except mysql.connector.Error as err:
#             print(f"Error al confirmar la transacción: {err}")
#             raise

#     def rollback_transaction(self):
#         try:
#             self.connection.rollback()
#             print("Transacción revertida")
#         except mysql.connector.Error as err:
#             print(f"Error al revertir la transacción: {err}")
#             raise

#     def execute_query(self, query, values=None):
#         # Este método ejecuta una consulta SQL en la base de datos. Toma dos parámetros: query,
#         # que es la consulta SQL a ejecutar, y values, que son los valores que se deben pasar a
#         # la consulta en caso de que utilices placeholders en la consulta. Primero, verifica si
#         # se proporcionaron valores para la consulta. Si se proporcionan valores, ejecuta la
#         # consulta con los valores dados utilizando el método execute() del cursor. En caso
#         # contrario, ejecuta la consulta sin valores. Luego, realiza la confirmación de la transacción
#         # con self.connection.commit(), lo que guarda los cambios realizados en la base de datos.
#         # Si hay algún error durante la ejecución de la consulta, captura la excepción
#         # mysql.connector.Error e imprime un mensaje de error.
#         try:
#             print('Query en execute query:',query)
#             if values:
#                 print('Values en execute query:',values)
#                 self.cursor.execute(query, values)
#             else:
#                 self.cursor.execute(query)
            
#             records = self.cursor.fetchall()
#             self.connection.commit()
#             print("Operación exitosa")
#             return records
#         except mysql.connector.Error as err:
#             print(f"Error al ejecutar la consulta: {err}")
#             raise
#             return False

#     def create_record(self, table, data):
#         # Este método se utiliza para insertar un nuevo registro en la tabla especificada de la
#         # base de datos. Toma dos parámetros: table, que es el nombre de la tabla en la que se
#         # insertará el registro, y data, que es un diccionario que contiene los nombres de las
#         # columnas como claves y los valores que se insertarán en esas columnas como valores.
#         # Primero, crea una cadena de marcadores de posición para los valores utilizando la función
#         # join() para concatenar %s según la cantidad de elementos en data. Luego, crea una cadena
#         # de nombres de columna separados por comas y una tupla de valores a insertar. Después,
#         # genera la consulta SQL de inserción utilizando estos datos y llama al método execute_query()
#         # para ejecutar la consulta.
#         # placeholders = ', '.join(['%s'] * len(data))
#         # columns = ', '.join(data.keys())
#         # values = tuple(data.values())
#         # query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
#         # self.execute_query(query, values)
#         placeholders = ', '.join(['%s'] * len(data))
#         columns = ', '.join([f"`{column}`" for column in data.keys()])  # Rodear cada nombre de columna con comillas invertidas
#         values = tuple(data.values())
#         table_name = f"`{table}`"  # Rodear el nombre de la tabla con comillas invertidas
#         query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
#         #self.execute_query(query, values)
#         #####################SI DA ERROR ALGUN METODO, VOLVER A ESTE#####################
#         if self.execute_query(query, values) is not None:
#             return self.cursor.lastrowid
#         else:
#             return None

#     # def create_record_para_tabla_estado(self, table, data): ###OBVIAMENTE HAY QUE BORRAR ESTO Y UNIFICAR LOS MÉTODOS
#     #     placeholders = ', '.join(['%s'] * len(data))
#     #     columns = ', '.join([f"`{column}`" for column in data.keys()])
#     #     values = tuple(data.values())
#     #     table_name = f"`{table}`"
#     #     query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
#     #     if self.execute_query(query, values):
#     #         return self.cursor.lastrowid  # Devuelve el ID generado automáticamente
#     #     else:
#     #         return None

#     def read_records(self, table, condition=None):
#         # Este método se utiliza para recuperar registros de la tabla especificada en la base de datos.
#         # Toma dos parámetros: table, que es el nombre de la tabla de la que se recuperarán los registros,
#         # y condition, que es una condición opcional para filtrar los registros que se devolverán. Si se
#         # proporciona una condición, la consulta SQL incluirá una cláusula WHERE para filtrar los registros.
#         # Luego, llama al método execute_query() para ejecutar la consulta y devuelve todos los registros
#         # recuperados utilizando el método fetchall() del cursor.
#         table_name = f"`{table}`"
#         query = f"SELECT * FROM {table_name}"
#         #print('Condition en read_records:',condition)
#         if condition:
#             query += f" WHERE {condition}"
#         #print(query)
#         records = self.execute_query(query)
#         if records:
#             return records
#         else:
#             return None

#     def update_record(self, table, data, condition):
#         # Este método se utiliza para actualizar registros en la tabla especificada de la base de datos.
#         # Toma tres parámetros: table, que es el nombre de la tabla en la que se actualizarán los registros,
#         # data, que es un diccionario que contiene los nombres de las columnas que se actualizarán como
#         # claves y los nuevos valores como valores, y condition, que es una condición que indica qué
#         # registros se deben actualizar. Primero, crea una cadena de asignaciones para las columnas y
#         # valores nuevos utilizando la función join(). Luego, crea una tupla de valores a actualizar. Después,
#         # genera la consulta SQL de actualización utilizando estos datos y llama al método execute_query()
#         # para ejecutar la consulta.
#         update_values = ', '.join([f"{key} = %s" for key in data.keys()])
#         values = tuple(data.values())
#         query = f"UPDATE {table} SET {update_values} WHERE {condition}"
#         return self.execute_query(query, values)

#     def delete_record(self, table, condition):
#         # Este método se utiliza para eliminar registros de la tabla especificada en la base de datos. Toma
#         # dos parámetros: table, que es el nombre de la tabla de la que se eliminarán los registros, y 
#         # condition, que es una condición que indica qué registros se deben eliminar. La consulta SQL generada
#         # incluirá una cláusula WHERE con esta condición para filtrar los registros que se eliminarán. Luego,
#         # llama al método execute_query() para ejecutar la consulta y realizar la eliminación de los registros.
#         query = f"DELETE FROM {table} WHERE {condition}"
#         self.execute_query(query)

#     def read_records_by_query(self, query, params):
#         try:
#             self.cursor.execute(query, params)
#             records = self.cursor.fetchall()
#             return records
#         except mysql.connector.Error as err:
#             print(f"Error al ejecutar la consulta: {err}")
#             raise