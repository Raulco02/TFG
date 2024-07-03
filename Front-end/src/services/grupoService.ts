class grupoService{
    async getGrupos() {
        const response = await fetch('http://localhost:5000/grupo/', {
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

    async getGrupo(id: string) {
        const url = `http://localhost:5000/grupo/${id}/dispositivos`;
        const response = await fetch(url, {
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
    
    async createGrupo(data: any) {
        console.log('datos a enviar',data)
        const response = await fetch('http://localhost:5000/grupo/create', {
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
}
export default new grupoService();