import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Atributo = ({ idSensor, nombreAtributo }) => {
  const [atributoValor, setAtributoValor] = useState(null);

  useEffect(() => {
    const fetchAtributo = async () => {
      try {
        const response = await axios.get(`http://localhost:5000/sensor/last/${idSensor}`);
        const atributos = response.data.attributes;
        setAtributoValor(atributos[nombreAtributo]);
      } catch (error) {
        console.error('Error fetching attribute:', error);
      }
    };
    fetchAtributo();
  }, [idSensor, nombreAtributo]);

  return (
    <div className='atributo-card'>
      {atributoValor !== null ? (
        <div>
          <h3>{nombreAtributo}</h3>
          <p>{atributoValor}</p>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default Atributo;
