import React, { useState, useRef, useEffect } from "react";
import { getIconComponent } from "../../utils/iconUtils";
//¿No preocuparme por grupo?¿Cambiar implementacion de tarjeta grupo para que me de el nombre del grupo?¿Pasar booleana grupo y preguntar por nombre de grupo?
const Estado = ({
  valor,
  nombreAtributo,
  nombreDispositivo,
  iconos,
  unidad,
  grupo,
  icono_grupo,
  id_grupo,
  theme
}) => {
  const [columnsClass, setColumnsClass] = useState("one-column");
  

  console.log("Estado", valor, nombreAtributo, nombreDispositivo, unidad);
  const uno =
    !Array.isArray(valor) &&
    !Array.isArray(nombreAtributo) &&
    !Array.isArray(nombreDispositivo) &&
    !Array.isArray(unidad);

  const containerRef = useRef(null);

  useEffect(() => {
    const updateColumnsClass = (entry) => {
      const parentWidth = entry.contentRect.width; // Obtiene el ancho del contenedor padre
      if (parentWidth >= 1000) {
        // 100% width is around 1000px
        setColumnsClass("three-columns");
      } else if (parentWidth >= 500) {
        // 66% width is around 500px
        setColumnsClass("two-columns");
      } else {
        setColumnsClass("one-column");
      }
    };

    const resizeObserver = new ResizeObserver((entries) => {
      for (let entry of entries) {
        updateColumnsClass(entry);
      }
    });

    if (containerRef.current) {
      resizeObserver.observe(containerRef.current);
    }

    return () => {
      if (containerRef.current) {
        resizeObserver.unobserve(containerRef.current);
      }
    };
  }, []);

  if (uno) {
    return (
      <div className="atributo-card" key="estado-card">
        {valor !== null ? (
          <div style={{ padding: "6%" }}>
            <h3 style={{ fontSize: "1em" }}>
              {nombreAtributo + " " + nombreDispositivo}
            </h3>
            <p style={{ fontSize: "inherit" }}>
              {valor}
              {" " + unidad}
            </p>
          </div>
        ) : (
          <p>Loading...</p>
        )}
      </div>
    );
  }
  const varios =
    Array.isArray(valor) &&
    Array.isArray(nombreAtributo) &&
    Array.isArray(nombreDispositivo) &&
    Array.isArray(unidad) &&
    valor.length === nombreAtributo.length &&
    nombreAtributo.length === nombreDispositivo.length &&
    nombreDispositivo.length === unidad.length;

  if (!varios) {
    return <p>Error: Los props deben ser listas de la misma longitud</p>;
  }

  return (
    <>
  {grupo !== null && (
    <div style={{ 
      position: "fixed", 
      top: "2%", 
      left: "2%", 
      zIndex: "10", 
      backgroundColor: theme.palette.background.default, 
      borderRadius: "10px",
      padding: "10px", 
      boxShadow: "0 2px 4px rgba(0, 0, 0, 0.1)", 
      width: "94%", 

    }}>
      <div style={{ display: "flex", alignItems: "center" }}>
        <h3 style={{ fontSize: "1em", margin: 0 }}>Grupo</h3>
        <p style={{ fontSize: "inherit", margin: "0 0 0 10px" }}>{grupo}</p>
        {getIconComponent(icono_grupo)}
      </div>
    </div>
  )}
  <div
    ref={containerRef}
    id="estado-container"
    className={`atributo-container ${columnsClass}`}
    style={{ marginTop: grupo !== null ? "calc(2% + 30px)" : 0 }} // Ajusta el margen top para evitar solapamientos
  >
    {valor.map((value, index) => (
      <div className="atributo-card" key={index}>
        {value !== null ? (
          <div style={{ padding: "6%" }}>
            <h3 style={{ fontSize: "1em" }}>
              {nombreAtributo[index] + " " + nombreDispositivo[index]}
            </h3>
            <p style={{ fontSize: "inherit" }}>
              {value}
              {" " + unidad[index]}
            </p>
          </div>
        ) : (
          <p>Loading...</p>
        )}
      </div>
    ))}
  </div>
</>
  );
};

export default Estado;
