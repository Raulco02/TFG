import Atributo from "./atributo";

const Energia = () => {
  const atributos = [
    { idSensor: "Shelly1", nombreAtributo: "Temperatura" },
    { idSensor: "Shelly1", nombreAtributo: "Humedad" },
    { idSensor: "Shelly1", nombreAtributo: "Batería" }
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

export default Energia;