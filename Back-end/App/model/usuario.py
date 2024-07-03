import hashlib
import uuid

class Usuario:
    def __init__(self, nombre, correo, password):
        self.id = str(uuid.uuid4())
        self.nombre = nombre
        self.correo = correo
        self.password = self._hash_password(password)  # Almacena la contraseña codificada
        self.rol_id = 2  # Por defecto, el rol es 2 (usuario)

    def _hash_password(self, password):
        # Función para codificar la contraseña utilizando el algoritmo SHA-256
        return hashlib.sha256(password.encode()).hexdigest()