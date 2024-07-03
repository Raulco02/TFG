import React from 'react';
//Hay que ajustar que la imagen se quede en el tamaño correcto
const Imagen = ({ enlace }) => {

  return (
    <div className='atributo-card'>
      {enlace !== null ? (
        <div style={{ padding: "6%" }}>
            <img src={enlace} alt="Imagen" className='imagen-ajustada'/>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default Imagen;
