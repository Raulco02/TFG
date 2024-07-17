import hashlib
import uuid

class Usuario:
    """
    Descripción:
    Clase que representa un usuario en la aplicación.
    """
    def __init__(self, nombre, correo, password):
        """
        Descripción:
        Inicializa una instancia de Usuario con un nombre, correo, password y le genera un id y un rol_id que por defecto será 2.

        Retorna:
        No hay retorno explícito.
        """
        self.id = str(uuid.uuid4())
        self.nombre = nombre
        self.correo = correo
        self.password = self._hash_password(password)  # Almacena la contraseña codificada
        self.rol_id = 2  # Por defecto, el rol es 2 (usuario)

    def _hash_password(self, password):
        """
        Descripción:
        Codifica la contraseña del usuario usando el algoritmo SHA-256

        Retorna:
        Retorna la contraseña codificada.
        """
        return hashlib.sha256(password.encode()).hexdigest()