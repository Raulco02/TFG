import React, { useState, useEffect } from "react";
import InfoSection from "./components/InfoSection";
import {
  BrowserRouter as Router,
  Route,
  Routes,
  useNavigate
} from "react-router-dom";
import { Seccion } from "./resources/Interfaces/interfaces";
import Login from "./components/Login/Login";
//import Menu from './components/menuBORRAR';
import Register from "./components/Register/Register";
import "./App.css";
import Menu from "./components/Menu";
import Config from "./components/Config";
import Texto from "./components/Tarjetas/Texto";
import Grafico from "./components/Tarjetas/Grafico";
import SeccionGrid from "./components/SeccionGrid";
import Lista from "./components/Lista";
import Principal from "./components/Principal";
import Code from "./components/Login/Code";
import FormularioIntegraciones from "./components/Formularios/FormularioIntegraciones";
import Editor from "./components/Formularios/Editor";
import FormularioDispositivo from "./components/Formularios/FormularioDispositivo";
import FormularioGrupo from "./components/Formularios/FormularioGrupos";
import FormularioRegla from "./components/Formularios/FormularioRegla";
import SensorChart from "./components/Tarjetas/GraficoPrueba";
import { TiempoGrafico, TipoGrafico } from "./resources/enums/enums";
import FormularioUsuario from "./components/Formularios/FormularioUsuario";
import FormularioAlerta from "./components/Formularios/FormularioAlerta";

const App = () => {
  // const [selectedSection, setSelectedSection] = useState("principal");
  const [id, setId] = useState("");
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [selectedSeccion, setSelectedSeccion] = useState<Seccion | null>(null);
  const [items, setItems] = useState([]);
  const [editando, setEditando] = useState(false);
  const [popoverOpen, setPopoverOpen] = useState(false);
  const [popoverMessage, setPopoverMessage] = useState<string>('');

  // const handleSectionChange = (section) => {
  //   setSelectedSection(section);
  // };

  const handleLogin = (id) => {
    setId(id);
    console.log("httpId: ", id);
    setIsLoggedIn(true); // Establece isLoggedIn en true después de iniciar sesión
  };

  useEffect(() => {
    console.log("selectedSection en app", selectedSeccion);
  }, [selectedSeccion]);

  useEffect(() => {
    console.log("items", items);
  }, [items]);
  const sensorData = [
    { timestamp: '2024-05-06T12:00:00Z', value: 10, sensor: 'Sensor 1' },
    { timestamp: '2024-05-22T12:00:00Z', value: 20, sensor: 'Sensor 1' },
    { timestamp: '2024-05-07T12:00:00Z', value: 15, sensor: 'Sensor 2' },
    { timestamp: '2024-05-08T12:00:00Z', value: 15, sensor: 'Sensor 2' },
    { timestamp: '2024-06-02T12:00:00Z', value: 1, sensor: 'Sensor 2' },
    { timestamp: '2024-05-07T12:00:00Z', value: 5, sensor: 'Sensor 3' },
    { timestamp: '2024-05-08T12:00:00Z', value: 10, sensor: 'Sensor 3' },
    { timestamp: '2024-06-02T12:00:00Z', value: 7, sensor: 'Sensor 3' },
    // Añade más datos según sea necesario
  ];
  return (
    <Router>
      <div className="app">
        <Routes>
          <Route path="/" element={<Login onLogin={handleLogin} />} />
          <Route path="/code" element={<Code />} />
          <Route path="/registrar" element={<Register />} />
          <Route
            path="/dashboard"
            element={
              <Menu
                setSelectedSeccion={setSelectedSeccion}
                selectedSeccion={selectedSeccion}
                setItems={setItems}
                editando={editando}
                setEditando={setEditando}
                showSeccionbar={true}
                setPopoverOpen={setPopoverOpen}
                setPopoverMessage={setPopoverMessage}
                popoverOpen={popoverOpen}
                popoverMessage={popoverMessage}
              >
                <SeccionGrid
                  id_seccion={selectedSeccion?.id}
                  items={items}
                  editando={editando}
                  layout={selectedSeccion?.layout}
                  numFilas={selectedSeccion?.numFilas}
                  setItems={setItems}
                  setPopoverMessage={setPopoverMessage}
                  setPopoverOpen={setPopoverOpen}
                />
              </Menu>
            }
          />
          {/* <Route path="/dashboard1" element={<Menu></Menu>} />
          <Route path="/dashboard2" element={<Menu></Menu>} />
          <Route path="/dashboard3" element={<Menu></Menu>} />
          <Route path="/dashboard4" element={<Menu></Menu>} />
          <Route path="/dashboard5" element={<Menu></Menu>} /> */}
          {/* <Route path="/prueba" element={<SeccionGrid items={items} />} /> */}
          <Route
            path="/config"
            element={
              <Menu selectedSeccion={null} setSelectedSeccion={setSelectedSeccion} setItems={setItems} editando={false} setEditando={setEditando} showSeccionbar={false}>
                <Config />
              </Menu>
            }
          />
          <Route
            path="/dispositivos"
            element={
              <Menu selectedSeccion={null} setSelectedSeccion={setSelectedSeccion} setItems={setItems} editando={false} setEditando={setEditando} showSeccionbar={false}>
                <Lista opcion='dispositivos'/>
              </Menu>
            }
          />
          <Route
            path="/dashboards"
            element={
              <Menu selectedSeccion={null} setSelectedSeccion={setSelectedSeccion} setItems={setItems} editando={false} setEditando={setEditando} showSeccionbar={false}>
                <Lista opcion='dashboards'/>
              </Menu>
            }
          />
          <Route
            path="/integraciones"
            element={
              <Menu selectedSeccion={null} setSelectedSeccion={setSelectedSeccion} setItems={setItems} editando={false} setEditando={setEditando} showSeccionbar={false}>
                <Lista opcion='integraciones'/>
              </Menu>
            }
          />
          <Route
            path="/integracion-form"
            element={
              <Menu selectedSeccion={null} setSelectedSeccion={setSelectedSeccion} setItems={setItems} editando={false} setEditando={setEditando} showSeccionbar={false}>
                <FormularioIntegraciones/>
              </Menu>
            }
          />
          <Route
            path="/prueba-plano"
            element={
              <Menu selectedSeccion={null} setSelectedSeccion={setSelectedSeccion} setItems={setItems} editando={false} setEditando={setEditando} showSeccionbar={false}>
                <Principal botones={['Botón 1', 'Botón 2', 'Botón 3', 'Botón 4']}/>
              </Menu>
            }
          />
          <Route
            path="/dispositivo-form"
            element={
              <Menu selectedSeccion={null} setSelectedSeccion={setSelectedSeccion} setItems={setItems} editando={false} setEditando={setEditando} showSeccionbar={false}>
                <FormularioDispositivo/>
              </Menu>
            }
          />
          <Route
            path="/grupos"
            element={
              <Menu selectedSeccion={null} setSelectedSeccion={setSelectedSeccion} setItems={setItems} editando={false} setEditando={setEditando} showSeccionbar={false}>
                <Lista opcion='grupos'/>
              </Menu>
            }
          />
          <Route
            path="/usuarios"
            element={
              <Menu selectedSeccion={null} setSelectedSeccion={setSelectedSeccion} setItems={setItems} editando={false} setEditando={setEditando} showSeccionbar={false}>
                <Lista opcion='usuarios'/>
              </Menu>
            }
          />
          <Route
            path="/grupo-form"
            element={
              <Menu selectedSeccion={null} setSelectedSeccion={setSelectedSeccion} setItems={setItems} editando={false} setEditando={setEditando} showSeccionbar={false}>
                <FormularioGrupo/>
              </Menu>
            }
          />
          <Route
            path="/reglas"
            element={
              <Menu selectedSeccion={null} setSelectedSeccion={setSelectedSeccion} setItems={setItems} editando={false} setEditando={setEditando} showSeccionbar={false}>
                <Lista opcion='reglas'/>
              </Menu>
            }
          />
          <Route
            path="/alertas"
            element={
              <Menu selectedSeccion={null} setSelectedSeccion={setSelectedSeccion} setItems={setItems} editando={false} setEditando={setEditando} showSeccionbar={false}>
                <Lista opcion='alertas'/>
              </Menu>
            }
          />
          <Route
            path="/tipos-atributos"
            element={
              <Menu selectedSeccion={null} setSelectedSeccion={setSelectedSeccion} setItems={setItems} editando={false} setEditando={setEditando} showSeccionbar={false}>
                <Lista opcion='tipos'/>
              </Menu>
            }
          />
          <Route
            path="/cuenta"
            element={
              <Menu selectedSeccion={null} setSelectedSeccion={setSelectedSeccion} setItems={setItems} editando={true} setEditando={setEditando} showSeccionbar={false}>
                <FormularioUsuario onClose={null}/>
              </Menu>
            }
          />
          <Route
            path="/regla-form"
            element={
              <Menu selectedSeccion={null} setSelectedSeccion={setSelectedSeccion} setItems={setItems} editando={false} setEditando={setEditando} showSeccionbar={false}>
                <FormularioAlerta />
              </Menu>
            }
          />
          <Route
            path="/prueba"
            element={
              <Menu selectedSeccion={null} setSelectedSeccion={setSelectedSeccion} setItems={setItems} editando={true} setEditando={setEditando} showSeccionbar={false}>
                {/* <SensorChart data={sensorData} tipo={TipoGrafico.Lineal} tiempoGrafico={TiempoGrafico.Semana}/> */}
                <Grafico item={{
    "icono": [
        "home",
        null,
        "home",
        null
    ],
    "id": 65,
    "id-atributo": [
        1,
        1,
        1,
        1
    ],
    "id-dispositivo": [
        "Shelly2",
        "Shelly3",
        "Shelly1",
        "Shelly TRV "
    ],
    "id-seccion": "2da09a98-219d-4d97-8676-276a7371c5a9",
    "nombre-atributo": [
        "Temperatura",
        "Temperatura",
        "Temperatura",
        "Temperatura"
    ],
    "nombre-dispositivo": [
        "Shelly aula y",
        "Shelly aula z",
        "Shelly aula x",
        "Shelly trv 4"
    ],
    "posicion": "0x0",
    "tiempo-grafico": TiempoGrafico.Anio,
    "tipo": "Grafico",
    "tipo-grafico": TipoGrafico.Barra,
    "unidades": [
        "ºC",
        "ºC",
        "ºC",
        "ºC"
    ],
    "valor": [
        "19.40",
        "19.40",
        "19.40",
        "2.00"
    ]
}}/>
              </Menu>
            }
          />
          {/* <Route
            path="/prueba"
            element={
              <Menu selectedSeccion={null} setSelectedSeccion={setSelectedSeccion} setItems={setItems} editando={false} setEditando={setEditando} showSeccionbar={false}>
                <Grafico item = {{
  "icono": [
      "home",
      "home"
  ],
  "id": 63,
  "id-atributo": [
      1,
      1
  ],
  "id-dispositivo": [
      "Shelly2",
      "Shelly1"
  ],
  "id-seccion": "1",
  "nombre-atributo": [
      "Temperatura",
      "Temperatura"
  ],
  "nombre-dispositivo": [
      "Shelly aula y",
      "Shelly aula x"
  ],
  "posicion": "1x1",
  "tiempo-grafico": "30d",
  "tipo": "Grafico",
  "tipo-grafico": "Linea",
  "unidades": [
      "ºC",
      "ºC"
  ],
  "valor": [
      "19.40",
      "19.40"
  ]
}}/>
              </Menu>
            }
          /> */}
          {/* Agrega rutas para otros componentes si es necesario */}
        </Routes>
      </div>
    </Router>
  );
};

export default App;

// <div className="grid-container">
// <div className="left-column">
//   <button onClick={() => handleSectionChange('principal')}>Principal</button>
//   <button onClick={() => handleSectionChange('iluminacion')}>ERSCO2-1</button>
//   <button onClick={() => handleSectionChange('energia')}>Shelly1</button>
//   <button onClick={() => handleSectionChange('aulas')}>Aulas</button>
//   <div className="empty-row"> {/* Última fila vacía */} </div>
// </div>
// <div className="right-column">
//   <InfoSection selectedSection={selectedSection} />
// </div>
// </div>