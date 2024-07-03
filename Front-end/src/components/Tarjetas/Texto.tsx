import React from 'react';

const Texto = ({ contenido }) => {
  return (
    <div className='atributo-card'>
      {contenido !== null ? (
        <div style={
          {
            // display: 'flex',
            // flexDirection: 'column',
            // justifyContent: 'center',
            // alignItems: 'center'
            padding: '6%',
          }
        }>
          {contenido}
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default Texto;
