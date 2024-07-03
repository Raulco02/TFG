import { createForm } from "../resources/Interfaces/interfaces";

class dashboardService{
    async getDashboards() {
        const response = await fetch('http://localhost:5000/dashboard/', {
        method: 'GET',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
        },
        });
        console.log(response);
        if (!response.ok) {
        throw new Error('Error 404: Not found');
        }
        return response.json();
      }

    async getDashboard(id){
        try {
            const response = await fetch(`http://localhost:5000/dashboard/get/${id}`, {
              method: 'GET',
              credentials: 'include',
              headers: {
                'Content-Type': 'application/json',
              },
            });
      
            if (response.ok) {
              // Lógica para manejar la respuesta exitosa
              console.log('Dashboard obtenido exitosamente');
              return response.json();
            } else {
              throw new Error('Error al obtener el Dashboard:' + response.status.toString());
            }
          } catch (error) {
            // Manejo de errores de red u otros errores
            console.log('Error al obtener el Dashboard', error);
            throw new Error('Error al obtener el Dashboard:' + error); //No se esto
          }
    }

      async createDashboard(data: createForm) {
        try {
            const response = await fetch('http://localhost:5000/dashboard/create', {
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
              console.log('Dashboard creado exitosamente');
              return responseData;
            } else {
              throw new Error('Error al crear el Dashboard:' + response.status.toString());
            }
          } catch (error) {
            // Manejo de errores de red u otros errores
            console.log('Error al crear el Dashboard', error);
            throw new Error('Error al crear el Dashboard:' + error); //No se esto
          }
      }

      async editDashboard(data) {
        try {
            const response = await fetch('http://localhost:5000/dashboard/edit', {
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

      async deleteDashboard(id) {
        try{
            const response = await fetch(`http://localhost:5000/dashboard/delete/${id}`, {
                method: 'DELETE',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            if(response.ok){
                console.log('Dashboard eliminado exitosamente');
                return response.json();
            } else {
                throw new Error('Error al eliminar el Dashboard:' + response.status.toString());
            }
        } catch(error){
            console.log('Error al eliminar el Dashboard', error);
            throw new Error('Error al eliminar el Dashboard:' + error);
        }
      }

}

export default new dashboardService();