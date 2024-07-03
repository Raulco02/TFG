import React, { useState, useEffect } from 'react';
import PlanoFacultad from './plano';
import Plano from './Tarjetas/Plano';
import { Planos } from '../resources/enums/enums';
import axios from 'axios'; 
import { useInterval } from '../hooks/useInterval';
import CircularProgress from '@mui/material/CircularProgress';

// Mejorar lógica del loader

const Principal = ({ botones }) => {
  const [temperaturas, setTemperaturas] = useState<any>({}); // Define estado para almacenar las temperaturas
  
  useEffect(() => {
    setTemperaturas(null);
    // Realiza la consulta HTTP al montar el componente
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:5000/sensor/es/ERSCO2-1,ERSCO2-2');
        // Extrae las temperaturas de los primeros 7 objetos de la respuesta
        const temps = response.data.map((obj: any) => ({
          sensor: obj.sensor,
          temperatura: obj.attributes.Temperatura
        }));
        setTemperaturas(temps); // Actualiza el estado con las temperaturas extraídas
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    fetchData();
  }, []);
  // Estado para almacenar el índice del botón seleccionado
  const [botonSeleccionado, setBotonSeleccionado] = useState(0);

  // Función para cambiar el botón seleccionado
  const handleBotonClick = async (index) => {
    setBotonSeleccionado(index);
    try{
      let response;
      if(index === 0){
        response = await axios.get('http://localhost:5000/sensor/es/ERSCO2-1,ERSCO2-2');
      }else if(index === 1){
        response = await axios.get('http://localhost:5000/sensor/es/ERSCO2-1,Shelly1,Shelly2,Temperatura');
      }else if(index === 2){
        response = await axios.get('http://localhost:5000/sensor/es/Temperatura,Shelly1,Shelly2,ERSCO2-2');
      }else if(index === 3){
        // response = await axios.get('http://localhost:5000/sensor/es/ERSCO2-7,ERSCO2-8');
      }
      // Extrae las temperaturas de los primeros 7 objetos de la respuesta
      let temps;
      if (response !== undefined){
        temps = response.data.map((obj) => ({
          sensor: obj.sensor,
          temperatura: obj.attributes.Temperatura
        }));
        console.log(temperaturas);
      }else{
        temps = null;
      }
      setTemperaturas(temps); // Actualiza el estado con las temperaturas extraídas
      console.log(temperaturas);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
      // Función para avanzar al siguiente botón
  const avanzarSiguienteBoton = () => {
    const siguienteBoton = (botonSeleccionado + 1) % botones.length; // Calcula el índice del siguiente botón
    handleBotonClick(siguienteBoton); // Llama a la función para hacer clic en el siguiente botón
  };

  // Llama a la función para avanzar al siguiente botón cada 30 segundos
  useInterval(() => {
    avanzarSiguienteBoton();
  }, 30000);

  return (
    <div>
      {/* Mostrar botones */}
      <div style={{ marginBottom: '20px' }}>
        {botones.map((nombre, index) => (
          <button
            key={index}
            onClick={() => handleBotonClick(index)}
            style={{ marginRight: '10px', backgroundColor: index === botonSeleccionado ? 'blue' : 'gray', color: 'white' }}
          >
            {nombre}
          </button>
        ))}
      </div>
      <Plano plano={Planos.Anexo_B_1}/>
      {/* <PlanoFacultad temperaturas={temperaturas} /> */}
      {/* Mostrar componente dependiendo del botón seleccionado */}
      {/* {temperaturas !== null && <PlanoFacultad temperaturas={temperaturas} />} */}
      {/* {temperaturas === null && <CircularProgress />}     */}
      </div>
  );
};
export default Principal;