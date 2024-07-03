import React, { useState } from "react";

const Aula = ({ x, y, ancho, alto, temperatura, onClick }) => {
    let color;
  if (temperatura < 18.1) {
    color = "blue";
  } else if (temperatura >= 18.1 && temperatura < 25) {
    color = "green";
  } else{
    color = "red";
  }
  // Calculamos la posición del centro del rectángulo
  const centroX = x + (ancho || 48) / 2;
  const centroY = y + (alto || 48) / 2;

  return (
    <g>
      <rect
        x={x}
        y={y}
        width={ancho || 48}
        height={alto || 48}
        fill={color}
        onClick={onClick}
      />
      <text
        x={centroX}
        y={centroY + 6} // Ajustamos la posición del texto para que esté centrado verticalmente
        textAnchor="middle"
        fill="white"
        fontSize="12"
      >
        {temperatura}°C
      </text>
    </g>
  );
};

export default Aula;