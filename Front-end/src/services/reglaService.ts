class reglaService{
    async getReglas() {
        const response = await fetch('http://localhost:5000/regla/getAll', {
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
    
    async getAlertas() {
        const response = await fetch('http://localhost:5000/regla/getAllAlertas', {
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

    async createRegla(data){
        const response = await fetch('http://localhost:5000/regla/create_alerta', {
            method: 'POST',
            credentials: 'include',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
          });
    
          if (response.ok) {
            // Lógica para manejar la respuesta exitosa
            console.log('Regla creada exitosamente');
            return response.json();
          } else {
            throw new Error('Error al crear la regla:' + response.status.toString());
          }
    }

    async deleteRegla(id){
        const response = await fetch(`http://localhost:5000/regla/delete/${id}`, {
            method: 'DELETE',
            credentials: 'include',
            headers: {
              'Content-Type': 'application/json',
            },
          });
    
          if (response.ok) {
            // Lógica para manejar la respuesta exitosa
            console.log('Regla eliminada exitosamente');
            return response.json();
          } else {
            throw new Error('Error al eliminar la regla:' + response.status.toString());
          }
    }
}
export default new reglaService();