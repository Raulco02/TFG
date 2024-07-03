class dispositivoService{
    async getDispositivos() {
        const response = await fetch('http://localhost:5000/dispositivo/getAll', {
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

      async getDispositivosTemperatura() {
        const response = await fetch('http://localhost:5000/dispositivo/getAllTemperatura', {
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

    async getDispositivosAtributo(id: string) {
        const url = `http://localhost:5000/dispositivo/getAll/${id}`;
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

      async getDispositivo(id: string) {
        const url = `http://localhost:5000/dispositivo/get/${id}`;
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

      async getAllAtributos() {
        const url = `http://localhost:5000/dispositivo/getAllAtributos`;
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

      async createDispositivo(data: any) {
        console.log('datos a enviar',data)
        const response = await fetch('http://localhost:5000/dispositivo/create', {
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

      async editDispositivo(data: any) {
        console.log('datos a enviar',data)
        const response = await fetch('http://localhost:5000/dispositivo/edit', {
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

      async deleteDispositivo(id: string) {
        const url = `http://localhost:5000/dispositivo/delete/${id}`;
        const response = await fetch(url, {
          method: 'DELETE',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
          },
        });
        if (!response.ok) {
          throw new Error(response.error);
        }
        return response.json();
      }

      async getValoresSensor(id: string) {
        const url = `http://localhost:5000/historico/${id}`;
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

      async getValoresSensores(atributos: [string], fechaInicio: string, fechaFin: string, dispositivos: [string]) {
        console.log(atributos, fechaInicio, fechaFin, dispositivos);
        if (!dispositivos || !fechaFin || !fechaInicio || !atributos) {
          throw new Error('Se deben proporcionar los ids de los dispositivos, las fechas de inicio y fin y los atributos a consultar');
        }
    
        const url = new URL('http://localhost:5000/historico/lista');
        atributos.forEach(id => url.searchParams.append('atributo', id));
        dispositivos.forEach(id => url.searchParams.append('id', id));
        url.searchParams.append('fecha_inicio', fechaInicio);
        url.searchParams.append('fecha_fin', fechaFin);
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
}
export default new dispositivoService();