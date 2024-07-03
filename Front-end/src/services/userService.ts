import { LoginData, RegisterData } from "../resources/Interfaces/interfaces";

class userService {
  async login(data: LoginData) {
    try {
      const response = await fetch('http://localhost:5000/usuario/login', {
        method: 'PUT',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });
      console.log(data);

      if (response.ok) {
        // Lógica para manejar la respuesta exitosa
        console.log('Inicio de sesión exitoso');
      } else {
        // Lógica para manejar la respuesta de error
        console.error('Error al iniciar sesión');
      }
      return response.json();
    } catch (error) {
      // Manejo de errores de red u otros errores
      console.error('Error de red:', error);
    }
  }

  async sendSecurityCode(code: string) {
    try {
      const response = await fetch('http://localhost:5000/usuario/codigo', {
        method: 'PUT',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({'codigo': code}),
      });
      console.log(code);

      if (response.ok) {
        // Lógica para manejar la respuesta exitosa
        console.log('Inicio de sesión exitoso');
      } else {
        // Lógica para manejar la respuesta de error
        console.error('Error al iniciar sesión');
      }
      return response.json();
    } catch (error) {
      // Manejo de errores de red u otros errores
      console.error('Error de red:', error);
    }
  }

  async register(data: RegisterData) {
    try {
      const response = await fetch('http://localhost:5000/usuario/registrar', {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (response.ok) {
        // Lógica para manejar la respuesta exitosa
        console.log('Registro exitoso');
        return response.json();
      } else {
        // Lógica para manejar la respuesta de error
        console.error('Error al registrarse:');
      }
    } catch (error) {
      // Manejo de errores de red u otros errores
      console.error('Error de red:', error);
    }
  }

  async editUsuario(data: any) {
    try {
      const response = await fetch('http://localhost:5000/usuario/edit', {
        method: 'PUT',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (response.ok) {
        // Lógica para manejar la respuesta exitosa
        console.log('Usuario editado exitosamente');
        return response.json();
      } else {
        // Lógica para manejar la respuesta de error
        console.error('Error al editar usuario:');
      }
    } catch (error) {
      // Manejo de errores de red u otros errores
      console.error('Error de red:', error);
    }
  }

  async deleteUsuario(id: string) {
    try {
      const response = await fetch(`http://localhost:5000/usuario/delete/${id}`, {
        method: 'DELETE',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        // Lógica para manejar la respuesta exitosa
        console.log('Usuario eliminado exitosamente');
        return response.json();
      } else {
        // Lógica para manejar la respuesta de error
        console.error('Error al eliminar usuario:');
      }
    } catch (error) {
      // Manejo de errores de red u otros errores
      console.error('Error de red:', error);
    }
  }


  async obtenerPerfil() {
    try {
      const response = await fetch('http://localhost:5000/usuario/perfil', {
        method: 'GET',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        // Lógica para manejar la respuesta exitosa
        console.log('Perfil obtenido');
      } else {
        if (response.status === 404)
          throw new Error('Error 404: Not found');
        else if (response.status === 403)
          throw new Error('Error 403: Forbidden');
        else
          console.error('Error al obtener perfil:');
      }
      return response.json();
    } catch (error) {
      // Manejo de errores de red u otros errores
      console.error('Error de red:', error);
    }
  }

  async obtenerDatos(){
    try {
      const response = await fetch('http://localhost:5000/usuario/datos', {
        method: 'GET',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        // Lógica para manejar la respuesta exitosa
        console.log('Datos obtenidos');
      } else {
        if (response.status === 404)
          throw new Error('Error 404: Not found');
        else if (response.status === 401)
          throw new Error('Error 401: Unauthorized');
        else
          console.error('Error al obtener datos:');
      }
      return response.json();
    } catch (error) {
      // Manejo de errores de red u otros errores
      console.error('Error de red:', error);
    }
  }

  async getUsuario(){
    try {
      const response = await fetch('http://localhost:5000/usuario/get_usuario', {
        method: 'GET',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        // Lógica para manejar la respuesta exitosa
        console.log('Usuario obtenido');
      } else {
        if (response.status === 404)
          throw new Error('Error 404: Not found');
        else if (response.status === 401)
          throw new Error('Error 401: Unauthorized');
        else
          console.error('Error al obtener usuario:');
      }
      return response.json();
    } catch (error) {
      // Manejo de errores de red u otros errores
      console.error('Error de red:', error);
    }
  }

  async logout() {
    const response = await fetch('http://localhost:5000/usuario/logout', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (response.ok) {
      // Lógica para manejar la respuesta exitosa
      console.log('Logout exitoso');
      return response.json();
    } else {
      // Lógica para manejar la respuesta de error
      console.error('Error al cerrar sesión');
      throw new Error("Error al cerrar sesión");
    }
  }

  async getUsuarios() {
    try {
      const response = await fetch('http://localhost:5000/usuario/getAll', {
        method: 'GET',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        // Lógica para manejar la respuesta exitosa
        console.log('Usuarios obtenidos');
      } else {
        // Lógica para manejar la respuesta de error
        console.error('Error al obtener usuarios:');
      }
      return response.json();
    } catch (error) {
      // Manejo de errores de red u otros errores
      console.error('Error de red:', error);
    }
  }
}

export default new userService();