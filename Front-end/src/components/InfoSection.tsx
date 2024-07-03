import React from 'react';
import Aulas from './Aulas';
import Energia from './Energia';
import Iluminacion from './Iluminacion';
import Principal from './Principal';
import { EnumSecciones } from '../resources/enums/enums';

interface InfoSectionProps {
  selectedSection: EnumSecciones;
}

const InfoSection: React.FC<InfoSectionProps> = ({ selectedSection }) => {
  const nombres = ['Botón 1', 'Botón 2', 'Botón 3', 'Botón 4']; // Puedes agregar más nombres según sea necesario
  switch (selectedSection) {
    case EnumSecciones.Principal:
      return <Principal botones={nombres}/>;
    case EnumSecciones.Iluminacion:
      return <Iluminacion />;
    case EnumSecciones.Energia:
      return <Energia />;
    case EnumSecciones.Aulas:
      return <Aulas />;
    default:
      return <div>Información de la sección: {selectedSection}</div>;
  }
};

export default InfoSection;