import React, { useEffect, useState } from "react";
import { useNavigate } from 'react-router-dom';
import userService from '../services/userService';
import User from '../resources/Interfaces/interfaces'
import InfoSection from "./InfoSection";
import "../App.css";


const Menu: React.FC = () => {
  const [selectedSection, setSelectedSection] = useState("principal");
  const [perfil, setPerfil] = useState<User | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    async function obtenerPerfil() {
      const datos = await userService.obtenerPerfil();
      console.log("Datos: ", datos);
      if(datos === undefined){
        navigate('/');
      }
      setPerfil(datos);
    }
    obtenerPerfil();
  }, []);

  const handleSectionChange = (section) => {
    setSelectedSection(section);
  };

  const checkLogin = (id:string) => {
    if (id === "") {
      navigate("/");
    }
  }

  const handleLogout = async () => {
    sessionStorage.removeItem("httpId");
    await userService.logout();
    navigate("/");
  }

  const handleSidebar = () => {
    navigate("/sidebar");
  }

  return (
    <div className="app">
      <div className="grid-container">
        <div className="left-column">
          <button onClick={() => handleSectionChange("principal")}>
            Principal
          </button>
          <button onClick={() => handleSectionChange("iluminacion")}>
            ERSCO2-1
          </button>
          <button onClick={() => handleSidebar()}>
            Sidebar
          </button>
          <button onClick={() => handleLogout()}>Logout</button>
          {perfil && <label>Nombre: {perfil.nombre}</label>}
          <div className="empty-row"> {/* Última fila vacía */} </div>
        </div>
        <div className="right-column">
          <InfoSection selectedSection={selectedSection} />
        </div>
      </div>
    </div>
  );
};

export default Menu;
