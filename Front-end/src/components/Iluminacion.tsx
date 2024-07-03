import Atributo from "./atributo";

const Iluminacion = () => {
  const atributos = [
    { idSensor: "ERSCO2-1", nombreAtributo: "Temperatura" },
    { idSensor: "ERSCO2-1", nombreAtributo: "CO2" },
    { idSensor: "ERSCO2-1", nombreAtributo: "Humedad" },
    { idSensor: "ERSCO2-1", nombreAtributo: "Luz" },
    { idSensor: "ERSCO2-1", nombreAtributo: "Presencia" },
    { idSensor: "ERSCO2-1", nombreAtributo: "Batería" }
  ];

  return (
    <div className="atributo-grid">
      {/* Utiliza el método map para crear dinámicamente los componentes Atributo */}
      {atributos.map((atributo, index) => (
        <Atributo 
          key={index} 
          idSensor={atributo.idSensor} 
          nombreAtributo={atributo.nombreAtributo} 
        />
      ))}
    </div>
  );
};

export default Iluminacion;