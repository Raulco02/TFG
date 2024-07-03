import { createTextCard } from '../resources/Interfaces/interfaces';

class tarjetaService{
    async createTexto(data: createTextCard) {
        try {
            const response = await fetch('http://localhost:5000/tarjeta/create_texto', {
              method: 'POST',
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
      async createImagen(data: createTextCard) {
        try {
            const response = await fetch('http://localhost:5000/tarjeta/create_imagen', {
              method: 'POST',
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
      async createEstado(data: createTextCard) {
        console.log('Envio',data)
        try {
            const response = await fetch('http://localhost:5000/tarjeta/create_estado', {
              method: 'POST',
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

      async createGrafico(data: createTextCard) {
        try {
            const response = await fetch('http://localhost:5000/tarjeta/create_grafico', {
              method: 'POST',
              credentials: 'include',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify(data),
            });
      
            if (response.ok) {
              // Lógica para manejar la respuesta exitosa
              console.log('Tarjeta creado exitosamente');
              return response.json();
            } else {
              throw new Error('Error al crear el Tarjeta:' + response.status.toString());
            }
          } catch (error) {
            // Manejo de errores de red u otros errores
            console.log('Error al crear el Tarjeta', error);
            throw new Error('Error al crear el Tarjeta:' + error); //No se esto
          }
      }

      async createTermostato(data: createTextCard) {
        try {
            const response = await fetch('http://localhost:5000/tarjeta/create_termostato', {
              method: 'POST',
              credentials: 'include',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify(data),
            });
      
            if (response.ok) {
              // Lógica para manejar la respuesta exitosa
              console.log('Tarjeta creado exitosamente');
              return response.json();
            } else {
              throw new Error('Error al crear el Tarjeta:' + response.status.toString());
            }
          } catch (error) {
            // Manejo de errores de red u otros errores
            console.log('Error al crear el Tarjeta', error);
            throw new Error('Error al crear el Tarjeta:' + error); //No se esto
          }
      }

      async createPlano(data: createTextCard) {
        try {
            const response = await fetch('http://localhost:5000/tarjeta/create_plano', {
              method: 'POST',
              credentials: 'include',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify(data),
            });
      
            if (response.ok) {
              // Lógica para manejar la respuesta exitosa
              console.log('Tarjeta creado exitosamente');
              return response.json();
            } else {
              throw new Error('Error al crear el Tarjeta:' + response.status.toString());
            }
          } catch (error) {
            // Manejo de errores de red u otros errores
            console.log('Error al crear el Tarjeta', error);
            throw new Error('Error al crear el Tarjeta:' + error); //No se esto
          }
      }

      async createTarjetaGrupo(data: createTextCard) {
        try {
            const response = await fetch('http://localhost:5000/tarjeta/create_tarjeta_grupo', {
              method: 'POST',
              credentials: 'include',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify(data),
            });
      
            if (response.ok) {
              // Lógica para manejar la respuesta exitosa
              console.log('Tarjeta creado exitosamente');
              return response.json();
            } else {
              throw new Error('Error al crear el Tarjeta:' + response.status.toString());
            }
          } catch (error) {
            // Manejo de errores de red u otros errores
            console.log('Error al crear el Tarjeta', error);
            throw new Error('Error al crear el Tarjeta:' + error); //No se esto
          }
      }

      async getTarjetas(id_seccion){
        try {
          const response = await fetch('http://localhost:5000/tarjeta/get/'+id_seccion, {
            method: 'GET',
            credentials: 'include',
            headers: {
              'Content-Type': 'application/json',
            },
          });
    
          if (response.ok) {
            // Lógica para manejar la respuesta exitosa
            const responseData = await response.json();
            console.log('Tarjeta creada exitosamente');
            return responseData;
          } else {
            throw new Error('Error al crear el Tarjeta:' + response.status.toString());
          }
        } catch (error) {
          // Manejo de errores de red u otros errores
          console.log('Error al crear el Tarjeta', error);
          throw new Error('Error al crear el Tarjeta:' + error); //No se esto
        }
      }

      async sendTemperaturaTermostato(data){
        try {
          const response = await fetch('http://localhost:5000/tarjeta/set_temperatura', {
            method: 'PUT',
            credentials: 'include',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
          });
    
          if (response.ok) {
            // Lógica para manejar la respuesta exitosa
            console.log('Tarjeta creado exitosamente');
            return response.json();
          } else {
            throw new Error('Error al crear el Tarjeta:' + response.status.toString());
          }
        } catch (error) {
          // Manejo de errores de red u otros errores
          console.log('Error al crear el Tarjeta', error);
          throw new Error('Error al crear el Tarjeta:' + error); //No se esto
        }
      }
}

export default new tarjetaService();