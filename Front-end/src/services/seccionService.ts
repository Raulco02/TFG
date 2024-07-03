import { createSeccion } from "../resources/Interfaces/interfaces";

class seccionService{
  async getSeccion(id) {
    try {
      const response = await fetch(`http://localhost:5000/seccion/get/${id}`, {
        method: 'GET',
        credentials: 'include',
      });

      if (response.ok) {
        // Lógica para manejar la respuesta exitosa
        const responseData = await response.json();
        console.log('Secciones obtenidas exitosamente', responseData);
        return responseData;
      } else {
        throw new Error('Error al obtener las secciones:' + response.status.toString());
      }
    } catch (error) {
      // Manejo de errores de red u otros errores
      console.log('Error al obtener las secciones', error);
      throw new Error('Error al obtener las secciones:' + error); //No se esto
    }
  }
      async createSeccion(data: createSeccion) {
        try {
            const response = await fetch('http://localhost:5000/seccion/create', {
              method: 'POST',
              credentials: 'include',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify(data),
            });
      
            if (response.ok) {
              // Lógica para manejar la respuesta exitosa
              const responseData = await response.json();
              console.log('Sección creada exitosamente', responseData);
              return responseData;
            } else {
              throw new Error('Error al crear la sección:' + response.status.toString());
            }
          } catch (error) {
            // Manejo de errores de red u otros errores
            console.log('Error al crear la sección', error);
            throw new Error('Error al crear la sección:' + error); //No se esto
          }
      }

      async subirFilas(data){
        try {
          console.log('data:', data);
          const response = await fetch('http://localhost:5000/seccion/num_filas_up', {
            method: 'PUT',
            credentials: 'include',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
          });
    
          if (response.ok) {
            // Lógica para manejar la respuesta exitosa
            console.log('Dashboard creado exitosamente');
            return response.json();
          } else {
            throw new Error('Error al crear el Dashboard:' + response.status.toString());
          }
        } catch (error) {
          // Manejo de errores de red u otros errores
          console.log('Error al crear el Dashboard', error);
          throw new Error('Error al crear el Dashboard:' + error); //No se esto
        }
      }

}

export default new seccionService();