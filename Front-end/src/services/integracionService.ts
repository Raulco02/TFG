class integracionService{
    async getIntegraciones() {
        const response = await fetch('http://localhost:5000/integracion/', {
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

      async getTipos() {
        const response = await fetch('http://localhost:5000/integracion/tipos', {
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

      async createIntegracion(data: any) {
        console.log('datos a enviar',data)
        const response = await fetch('http://localhost:5000/integracion/add', {
          method: 'POST',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
        });
        if (!response.ok) {
          throw new Error(response.error);
        }
        return response.json();
      }

      async editIntegracion(data: any){
        console.log('datos a enviar',data)
        const response = await fetch('http://localhost:5000/integracion/edit', {
          method: 'PUT',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
        });
        if (!response.ok) {
          throw new Error(response.error);
        }
        return response.json();
      }

      async deleteIntegracion(data: any){
        console.log('datos a enviar',data)
        const response = await fetch('http://localhost:5000/integracion/delete', {
          method: 'DELETE',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
        });
        if (!response.ok) {
          throw new Error(response.error);
        }
        return response.json();
      }
}

export default new integracionService();