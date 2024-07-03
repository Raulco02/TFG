import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import PropTypes from "prop-types";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Button,
  useTheme,
  Popover,
} from "@mui/material";
import {
  AddCircleOutline as AddCircleOutlineIcon,
} from "@mui/icons-material";
import dispositivoService from "../services/dispositivoService";
import dashboardService from "../services/dashboardService";
import { getIconComponent } from "../utils/iconUtils";
import { IconName } from "../resources/enums/enums";
import Formulario from "./Formularios/Formulario";
import InfoBox from "./InfoBox";
import integracionService from "../services/integracionService";
import grupoService from "../services/grupoService";
import reglaService from "../services/reglaService";
import FormularioDispositivo from "./Formularios/FormularioDispositivo";
import FormularioIntegraciones from "./Formularios/FormularioIntegraciones";
import FormularioGrupos from "./Formularios/FormularioGrupos";
import FormularioRegla from "./Formularios/FormularioRegla";
import FormularioTipos from "./Formularios/FormularioTipos";
import FormularioAlerta from "./Formularios/FormularioAlerta";
import userService from "../services/userService";
import FormularioUsuario from "./Formularios/FormularioUsuario";

function Lista({ opcion }) {
  const [data, setData] = useState([]);
  const [items, setItems] = useState({});
  const [selectedItem, setSelectedItem] = useState({});
  const [editandoItem, setEditandoItem] = useState(null);
  const [mostrandoFormulario, setMostrandoFormulario] = useState(false);
  const [isAdding, setIsAdding] = useState(false);
  const [anchorEl, setAnchorEl] = useState(null);
  const [eliminandoItem, setEliminandoItem] = useState(false);
  const [isSmallScreen, setIsSmallScreen] = useState(window.innerWidth < 768);

useEffect(() => {
  const handleResize = () => {
    setIsSmallScreen(window.innerWidth < 768);
  };

  window.addEventListener("resize", handleResize);

  return () => {
    window.removeEventListener("resize", handleResize);
  };
}, []);

  const theme = useTheme();
  const navigate = useNavigate();

  const transformListsToObjects = (input) => {
    const arrayToObject = (arr) => {
      return arr.reduce((acc, item) => {
        acc[item.id] = transformListsToObjects(item);
        return acc;
      }, {});
    };

    for (const key in input) {
      if (Array.isArray(input[key])) {
        input[key] = arrayToObject(input[key]);
      } else if (typeof input[key] === "object" && input[key] !== null) {
        input[key] = transformListsToObjects(input[key]);
      }
    }

    return input;
  };

  const editarItem = (item) => {
    console.log("Editando item:", item);
    setEditandoItem(item);
    setMostrandoFormulario(true);
    setIsAdding(false);
  };

  const closeEditandoItem = () => {
    setEditandoItem(null);
    setMostrandoFormulario(false);
    setIsAdding(false);
  };

  const confirmarEliminarItem = async (item) => {
    setEliminandoItem(true);
  };

  const eliminarItem = async (item) => { //Tengo que recargar cada vez que elimino un item (o lo edito o lo añado)
    console.log("Eliminando item:", item);
    try {
      switch (opcion) {
        case "dispositivos":
          await dispositivoService.deleteDispositivo(item.id);
          alert("Dispositivo eliminado correctamente");
          break;
        case "dashboards":
          await dashboardService.deleteDashboard(item.id);
          break;
        case "integraciones":
          await integracionService.deleteIntegracion({ id: item.id });
          break;
        case "usuarios":
          await userService.deleteUsuario(item.id);
          break;
        case "grupos":
          await grupoService.deleteGrupo(item.id);
          break;
        case "reglas":
          await reglaService.deleteRegla(item.id);
          break;
        case "alertas":
          await reglaService.deleteRegla(item.id);
          break;
        default:
          break;
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Error al eliminar el elemento");
    } finally {
      setEliminandoItem(false);
    }
  };

  const onSubmitEditandoItem = async (data) => {
    try {
      data.id = editandoItem.id;
      const response = await dashboardService.editDashboard(data); // Ajusta esto según el tipo de elemento que se edita
      console.log("Item editado:", response);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setEditandoItem(null);
      setMostrandoFormulario(false);
    }
  };

  const onSubmitCreandoItem = async (data) => {
    try {
      const response = await dashboardService.createDashboard(data); // Ajusta esto según el tipo de elemento que se crea
      console.log("Item creado:", response);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setEditandoItem(null);
      setMostrandoFormulario(false);
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      
      let response;
      try{
      switch (opcion) {
        case "dispositivos":
          response = await dispositivoService.getDispositivos();
          break;
        case "dashboards":
          response = await dashboardService.getDashboards();
          break;
        case "integraciones":
          response = await integracionService.getIntegraciones();
          break;
        case "grupos":
          response = await grupoService.getGrupos();
          break;
        case "reglas":
          response = await reglaService.getReglas();
          break;
        case "alertas":
          response = await reglaService.getAlertas();
          break;
        case "tipos":
          response = await integracionService.getTipos();
          break;
        case "usuarios":
          response = await userService.getUsuarios();
          console.log("Usuarios:", response);
          break;
        default:
          break;
      }
    }catch (error) {
      console.error("Error:", error);
      alert("Error al obtener los datos");
      setData(null)
    }
      const transformedItemsObject = response.reduce((acc, item) => {
        acc[item.id] = transformListsToObjects(item);
        return acc;
      }, {});
      setItems(transformedItemsObject);
      let formattedData;
      switch (opcion) {
        case "dispositivos":
          formattedData = response.map((item) => ({
            Id: item.id,
            Nombre: item.nombre,
            Integracion: item.integracion,
            Topic: item.topic,
            Icono: getIconComponent(item.icono),
            Editar: (
              <Button
                variant="contained"
                color="primary"
                onClick={() => editarItem(item)}
              >
                {getIconComponent(IconName.Edit)}
              </Button>
            ),
            Eliminar: (
              <Button
                variant="contained"
                color="secondary"
                onClick={() => confirmarEliminarItem(item)}
              >
                {getIconComponent(IconName.Delete)}
              </Button>
            ),
          }));
          break;
        case "dashboards":
          formattedData = response.map((item) => ({
            Id: item.id,
            Nombre: item.nombre,
            Icono: getIconComponent(item.icono),
            Editar: (
              <Button
                variant="contained"
                color="primary"
                onClick={() => editarItem(item)}
              >
                {getIconComponent(IconName.Edit)}
              </Button>
            ),
            Eliminar: (
              <Button
                variant="contained"
                color="secondary"
                onClick={() => confirmarEliminarItem(item)}
              >
                {getIconComponent(IconName.Delete)}
              </Button>
            ),
          }));
          break;
        case "integraciones":
          formattedData = response.map((item) => ({
            Id: item.id,
            Nombre: item.nombre,
            Script: item.script,
            Editar: (
              <Button
                variant="contained"
                color="primary"
                onClick={() => editarItem(item)}
              >
                {getIconComponent(IconName.Edit)}
              </Button>
            ),
            Eliminar: (
              <Button
                variant="contained"
                color="secondary"
                onClick={() => confirmarEliminarItem(item)}
              >
                {getIconComponent(IconName.Delete)}
              </Button>
            ),
          }));
          break;
        case "grupos":
          formattedData = response.map((item) => ({
            Id: item.id,
            Nombre: item.nombre,
            Icono: getIconComponent(item.icono),
            Editar: (
              <Button
                variant="contained"
                color="primary"
                onClick={() => editarItem(item)}
              >
                {getIconComponent(IconName.Edit)}
              </Button>
            ),
            Eliminar: (
              <Button
                variant="contained"
                color="secondary"
                onClick={() => confirmarEliminarItem(item)}
              >
                {getIconComponent(IconName.Delete)}
              </Button>
            ),
          }));
          break;
        case "reglas":
          console.log("Reglas", response)
          formattedData = response.map((item) => ({
            Id: item.id,
            Nombre: item.nombre,
            Editar: (
              <Button
                variant="contained"
                color="primary"
                onClick={() => editarItem(item)}
              >
                {getIconComponent(IconName.Edit)}
              </Button>
            ),
            Eliminar: (
              <Button
                variant="contained"
                color="secondary"
                onClick={() => confirmarEliminarItem(item)}
              >
                {getIconComponent(IconName.Delete)}
              </Button>
            ),
          }));
          break;
        case "alertas":
          formattedData = response.map((item) => ({
            Id: item.id,
            Nombre: item.nombre,
            Editar: (
              <Button
                variant="contained"
                color="primary"
                onClick={() => editarItem(item)}
              >
                {getIconComponent(IconName.Edit)}
              </Button>
            ),
            Eliminar: (
              <Button
                variant="contained"
                color="secondary"
                onClick={() => confirmarEliminarItem(item)}
              >
                {getIconComponent(IconName.Delete)}
              </Button>
            ),
          }));
          break;
        case "tipos":
          formattedData = response.map((item) => ({
            Id: item.id,
            Nombre: item.nombre,
            Editar: (
              <Button
                variant="contained"
                color="primary"
                onClick={() => editarItem(item)}
              >
                {getIconComponent(IconName.Edit)}
              </Button>
            ),
            Eliminar: (
              <Button
                variant="contained"
                color="secondary"
                onClick={() => confirmarEliminarItem(item)}
              >
                {getIconComponent(IconName.Delete)}
              </Button>
            ),
          }));
          break;
        case "usuarios":
          formattedData = response.map((item) => ({
            Id: item.id,
            Nombre: item.nombre,
            Correo: item.correo,
            Editar: (
              <Button
                variant="contained"
                color="primary"
                onClick={() => editarItem(item)}
              >
                {getIconComponent(IconName.Edit)}
              </Button>
            ),
            Eliminar: (
              <Button
                variant="contained"
                color="secondary"
                onClick={() => confirmarEliminarItem(item)}
              >
                {getIconComponent(IconName.Delete)}
              </Button>
            ),
          }));
          break;
        default:
          break;
      }
      console.log("Data:", formattedData);
      setData(formattedData);
    };

    fetchData();
  }, [opcion]);

  if (data === null) {
    return <div>Error al obtener los datos</div>;
  }

  let columns;
  if (data.length === 0) {
    //return <div>Otros</div>;
    columns = [];
  } else{
  columns = Object.keys(data[0]);
}
  const adding = () => {
    setEditandoItem(null);
    setMostrandoFormulario(true);
    setIsAdding(true);
  };

  const handleFilaClick = (row) => () => {
    console.log("Editando item:", items[row.Id]);
    setEditandoItem(items[row.Id]);
    setMostrandoFormulario(true);
    setIsAdding(false);
    // setSelectedItem(items[row.Id]);
    // setAnchorEl(document.body);
  };

  const handleClose = () => {
    setSelectedItem({});
    setAnchorEl(null);
  };

  return (
    <div style={{ width: "100%", maxHeight: "100%", display: "flex", flexDirection: "column"  }}>
      <Button
        onClick={() => {
          if (mostrandoFormulario) {
            setMostrandoFormulario(false);
            setEditandoItem(null);
          } else {
            navigate("/config");
          }
        }}
        style={{
          marginBottom: "1rem",
          display: "flex",
          alignItems: "center",
          backgroundColor: theme.palette.primary.main,
          color: theme.palette.primary.contrastText,
          cursor: "pointer",
          width: "fit-content",
        }}
      >
        {getIconComponent(IconName.Back)}
        <span>Volver</span>
      </Button>

      <div style={{ display: "flex", width: "100%", maxHeight: "100%", overflow:"hidden" }}>
        <div
          style={{
            width: mostrandoFormulario ? isSmallScreen ? "0%": "33%" : "100%",
            marginRight: editandoItem || isAdding ? "2%" : "",
            overflow: "hidden",
            display: "flex",
            flexDirection: "column",
          }}
        >
          <TableContainer component={Paper} style={{ maxHeight: "100%", overflow:"auto" }}>
            <Table stickyHeader>
              <TableHead>
                <TableRow style={{backgroundColor: "white"}}>
                  {columns.map((column) => (
                    <TableCell key={column} style={{ fontWeight: "bold", backgroundColor: theme.palette.background.paper, color: theme.palette.primary.text }}>
                      {column}
                    </TableCell>
                  ))}
                </TableRow>
              </TableHead>
              <TableBody>
                {data.map((row, rowIndex) => (
                  <TableRow
                    key={rowIndex}
                    onClick={handleFilaClick(row)}
                    sx={{ backgroundColor: theme.palette.background.paper, color: theme.palette.primary.text }}
                    style={{ transition: "background-color 0.3s ease" }}
                    onMouseOver={(e) => {
                      e.currentTarget.style.backgroundColor = theme.palette.background.list;
                      e.currentTarget.style.cursor = "pointer";
                    }}
                    onMouseOut={(e) => {
                      e.currentTarget.style.backgroundColor = "";
                      e.currentTarget.style.cursor = "";
                    }}
                  >
                    {columns.map((column, colIndex) => (
                      <TableCell key={colIndex} sx={{color: theme.palette.primary.text}}>{row[column]}</TableCell>
                    ))}
                  </TableRow>
                ))}
                {/* <TableRow style={{alignItems:"center"}}>
                <Button
              onMouseOver={(e) => {
                e.currentTarget.style.backgroundColor = "#f0f0f0";
                e.currentTarget.style.cursor = "pointer";
              }}
              onMouseOut={(e) => {
                e.currentTarget.style.backgroundColor = "";
                e.currentTarget.style.cursor = "";
              }}
              sx={{
                display: "flex",
                width: "100%",
                alignItems: "center",
                justifyContent: "center",
                backgroundColor: "white",
                // '&::before': {
                //   content: "''",
                //   flex: 1,
                //   borderBottom: `1px solid ${theme.palette.primary.main}`,
                //   marginRight: '8px',
                // },
                // '&::after': {
                //   content: "''",
                //   flex: 1,
                //   borderBottom: `1px solid ${theme.palette.primary.main}`,
                //   marginLeft: '8px',
                // },
              }}
              onClick={adding}
            >
              <AddCircleOutlineIcon />
            </Button>

                </TableRow> */}
              </TableBody>
            </Table>
          </TableContainer>
          {(!mostrandoFormulario && !(opcion === "dashboards" && data.length === 5)) && (
            <Button
              onMouseOver={(e) => {
                e.currentTarget.style.backgroundColor = theme.palette.background.list;
                e.currentTarget.style.cursor = "pointer";
              }}
              onMouseOut={(e) => {
                e.currentTarget.style.backgroundColor = "";
                e.currentTarget.style.cursor = "";
              }}
              sx={{
                display: "flex",
                width: "100%",
                alignItems: "center",
                justifyContent: "center",
                backgroundColor: theme.palette.background.paper,
                // '&::before': {
                //   content: "''",
                //   flex: 1,
                //   borderBottom: `1px solid ${theme.palette.primary.main}`,
                //   marginRight: '8px',
                // },
                // '&::after': {
                //   content: "''",
                //   flex: 1,
                //   borderBottom: `1px solid ${theme.palette.primary.main}`,
                //   marginLeft: '8px',
                // },
              }}
              onClick={adding}
            >
              <AddCircleOutlineIcon sx={{color: theme.palette.primary.text}}/>
            </Button>
          )}
        </div>
        {mostrandoFormulario && (
          <div style={{ width: isSmallScreen ? "100%" : "67%", maxHeight: "100%", overflowY: "auto" }}>
            {/* <Button
            onClick={() => setMostrandoFormulario(false)}
            style={{ marginBottom: "1rem", display: "flex", alignItems: "center", backgroundColor: theme.palette.primary.main, color: theme.palette.primary.contrastText, cursor: "pointer"}}
          >
            {getIconComponent(IconName.Back)}
            <span>Volver</span>
          </Button> */}
            {opcion === "dashboards" && !isAdding && (
              <Formulario
                onClose={closeEditandoItem}
                submit={onSubmitEditandoItem}
                icono={editandoItem ? editandoItem.icono : ""}
                nombre={editandoItem ? editandoItem.nombre : ""}
                popover={false}
                theme = {theme}
              />
            )}
            {opcion === "dashboards" && isAdding && (
              <Formulario
                onClose={closeEditandoItem}
                submit={onSubmitCreandoItem}
                popover={false}
                theme = {theme}
              />
            )}
            {opcion === "dispositivos" && (
              <FormularioDispositivo
                dispositivo={editandoItem}
                onClose={closeEditandoItem}
                theme = {theme}
              />
            )}
            {opcion === "integraciones" && (
              <FormularioIntegraciones
                integracion={editandoItem}
                onClose={closeEditandoItem}
                theme={theme}
              />
            )}
            {opcion === "grupos" && (
              <FormularioGrupos
                grupo={editandoItem}
                onClose={closeEditandoItem}
                theme = {theme}
              />
            )}
            {opcion === "reglas" && (
              <FormularioRegla
                regla={editandoItem}
                onClose={closeEditandoItem}
                theme = {theme}
              />
            )}
            {opcion === "alertas" && (
              <FormularioAlerta
                regla={editandoItem}
                onClose={closeEditandoItem}
                theme = {theme}
              />
            )}
            {opcion === "tipos" && (
              <FormularioTipos
                tipo={editandoItem}
                onClose={closeEditandoItem}
                theme = {theme}
              />
            )}
            {opcion === "usuarios" && (
              <FormularioUsuario
                usuario={editandoItem}
                onClose={closeEditandoItem}
                theme = {theme}
              />
            )}
          </div>
        )}
        <Popover
          open={eliminandoItem}
          anchorEl={anchorEl}
          onClose={handleClose}
          anchorOrigin={{
            vertical: "center",
            horizontal: "center",
          }}
          transformOrigin={{
            vertical: "center",
            horizontal: "center",
          }}
        >
          <div style={{ padding: "1rem" }}>
            <h3>¿Estás seguro de que quieres eliminar este elemento?</h3>
            <Button
              variant="contained"
              color="primary"
              onClick={() => {
                console.log("Eliminando item:", editandoItem);
                eliminarItem(editandoItem);
                setEliminandoItem(false);
              }}
            >
              Sí
            </Button>
            <Button
              variant="contained"
              color="secondary"
              onClick={() => {
                setEliminandoItem(false);
              }}
            >
              No
            </Button>
          </div>
        </Popover>
        {/* <InfoBox info={selectedItem} anchorEl={anchorEl} onClose={handleClose} /> */}
      </div>
    </div>
  );
}

Lista.propTypes = {
  opcion: PropTypes.string.isRequired,
};

export default Lista;

// import React, { useEffect, useState } from 'react';
// import { useNavigate } from "react-router-dom";
// import PropTypes from 'prop-types';
// import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';
// import dispositivoService from '../services/dispositivoService';
// import dashboardService from '../services/dashboardService';
// import { getIconComponent } from '../utils/iconUtils';
// import { Button } from '@mui/material';
// import { IconName } from '../resources/enums/enums';
// import { set } from 'react-hook-form';
// import Formulario from './Formularios/Formulario';
// import InfoBox from './InfoBox';
// import integracionService from '../services/integracionService';
// import grupoService from '../services/grupoService';
// import reglaService from '../services/reglaService';

// function Lista({ opcion }) {
//   const [data, setData] = useState([]);
//   const [items, setItems] = useState({});
//   const [selectedItem, setSelectedItem] = useState({});
//   const [editandoDashboard, setEditandoDashboard] = useState(false);
//   const [itemEditado, setItemEditado] = useState({});
//   const [anchorEl, setAnchorEl] = useState<HTMLElement | null>(null);

//   const navigate = useNavigate();

//   const transformListsToObjects = (input) => {
//     // Helper function to transform an array to an object using `id` as key
//     const arrayToObject = (arr) => {
//         return arr.reduce((acc, item) => {
//             acc[item.id] = transformListsToObjects(item);
//             return acc;
//         }, {});
//     };

//     // Iterate over each key in the input
//     for (const key in input) {
//         if (Array.isArray(input[key])) {
//             // If the value is an array, transform it to an object
//             input[key] = arrayToObject(input[key]);
//         } else if (typeof input[key] === 'object' && input[key] !== null) {
//             // Recursively transform nested objects
//             input[key] = transformListsToObjects(input[key]);
//         }
//     }

//     return input;
// };

//   const editarDashboard = (id, icono, nombre) => {
//     setEditandoDashboard(true);
//     setItemEditado({id, icono, nombre});
//   };

//   const closeEditandoDashboard = () => {
//     setEditandoDashboard(false);
//   };

//   const onSubmitEditandoDashboard = async (data) => {
//     try {
//       data.id = itemEditado.id;
//       const response = await dashboardService.editDashboard(data);
//       console.log("Dashboard editado:", response);
//     } catch (error) {
//       console.error("Error:", error);
//     } finally {
//       setEditandoDashboard(false);
//     }
//   };

//   useEffect(() => {
//     switch (opcion) {
//       case 'dispositivos':
//         dispositivoService.getDispositivos().then((response) => {
//           const transformedItemsObject = response.reduce((acc, item) => {
//             acc[item.id] = transformListsToObjects(item);
//             return acc;
//         }, {});
//         setItems(transformedItemsObject);
//           // Procesar los datos para ajustarlos a la tabla
//           const formattedData = response.map((item) => ({
//             Id: item.id,
//             Nombre: item.nombre,
//             Icono: getIconComponent(item.icono),
//             Editar: <Button variant="contained" color="primary" onClick={() => navigate("/dispositivo-form", {state: {"dispositivo": item}})}>{getIconComponent(IconName.Edit)}</Button>
//           }));
//           setData(formattedData);
//         });
//         break;
//       case 'dashboards':

//         dashboardService.getDashboards().then((response) => {
//           const transformedItemsObject = response.reduce((acc, item) => {
//             acc[item.id] = transformListsToObjects(item);
//             return acc;
//         }, {});
//         setItems(transformedItemsObject);          // Procesar los datos para ajustarlos a la tabla
//           const formattedData = response.map((item) => ({
//             Id: item.id,
//             Nombre: item.nombre,
//             Icono: getIconComponent(item.icono),
//             Editar: <Button variant="contained" color="primary" onClick={() => editarDashboard(item.id, item.icono, item.nombre)}>{getIconComponent(IconName.Edit)}</Button>
//           }));
//           setData(formattedData);
//         });
//         break;
//       case 'integraciones':
//         integracionService.getIntegraciones().then((response) => {
//           const transformedItemsObject = response.reduce((acc, item) => {
//             acc[item.id] = transformListsToObjects(item);
//             return acc;
//         }, {});
//         setItems(transformedItemsObject);
//           const formattedData = response.map((item) => ({
//             Id: item.id,
//             Nombre: item.nombre,
//             Script: item.script,
//             Editar: <Button variant="contained" color="primary" onClick={() => navigate("/integracion-form", {state: {"integracion": item}})}>{getIconComponent(IconName.Edit)}</Button>
//           }));
//           setData(formattedData);
//         });
//         break;
//       case 'grupos':
//         grupoService.getGrupos().then((response) => {
//           const transformedItemsObject = response.reduce((acc, item) => {
//             acc[item.id] = transformListsToObjects(item);
//             return acc;
//         }, {});
//         setItems(transformedItemsObject);
//         // Procesar los datos para ajustarlos a la tabla
//           const formattedData = response.map((item) => ({
//             Id: item.id,
//             Nombre: item.nombre,
//             Icono: getIconComponent(item.icono),
//             Editar: <Button variant="contained" color="primary" onClick={() => navigate("/grupo-form", {state: {"grupo": item}})}>{getIconComponent(IconName.Edit)}</Button>
//           }));
//           setData(formattedData);
//         });
//         break;
//       case 'reglas':
//         reglaService.getReglas().then((response) => {
//           const transformedItemsObject = response.reduce((acc, item) => {
//             acc[item.id] = transformListsToObjects(item);
//             return acc;
//         }, {});
//         setItems(transformedItemsObject);          // Procesar los datos para ajustarlos a la tabla
//           console.log(response);
//           const formattedData = response.map((item) => ({
//             Id: item.id,
//             Nombre: item.nombre,
//             // Descripción: item.descripcion,
//             Editar: <Button variant="contained" color="primary" onClick={() => navigate("/regla-form", {state: {"regla": item}})}>{getIconComponent(IconName.Edit)}</Button>
//           }));
//           setData(formattedData);
//         });
//         break;
//       default:
//         break;
//     }
//   }, [opcion]);

//   if (!data || data.length === 0) {
//     return <div>No hay datos</div>;
//   }

//   // Extrae los nombres de las columnas
//   const columns = Object.keys(data[0]);

//   const adding = () => {
//     switch (opcion) {
//       case 'dispositivos':
//         navigate("/dispositivo-form");
//         break;
//       case 'dashboards':
//         // Ver qué hacer
//         // navigate("/add-dashboard-form");
//         break;
//       case 'integraciones':
//         navigate("/integracion-form");
//         break;
//       case 'grupos':
//         navigate("/grupo-form");
//         break;
//       case 'reglas':
//         navigate("/regla-form");
//         break;
//       default:
//         break;
//     }
//   };

//   const handleFilaClick = (row) => () => {
//     console.log("Fila seleccionada:", row);
//     console.log("Items:", items);
//     setSelectedItem(items[row.Id]);
//     setAnchorEl(document.body)
//     console.log(data)
//   }

//   const handleClose = () => {
//     setSelectedItem({});
//     setAnchorEl(null);
//   }

//   return (
//     <>
//     <TableContainer component={Paper}>
//       <Table>
//         <TableHead>
//           <TableRow>
//             {columns.map((column) => (
//               <TableCell key={column} style={{ fontWeight: 'bold' }}>{column}</TableCell>
//             ))}
//           </TableRow>
//         </TableHead>
//         <TableBody>
//           {data.map((row, rowIndex) => (
//             <TableRow key={rowIndex} onClick={handleFilaClick(row)} style={{
//               transition: 'background-color 0.3s ease',
//             }}
//             onMouseOver={(e) => {
//               e.currentTarget.style.backgroundColor = '#f0f0f0';
//               e.currentTarget.style.cursor = 'pointer';
//             }}
//             onMouseOut={(e) => {
//               e.currentTarget.style.backgroundColor = '';
//               e.currentTarget.style.cursor = '';
//             }}>
//               {columns.map((column, colIndex) => (
//                 <TableCell key={colIndex}>{row[column]}</TableCell>
//               ))}
//             </TableRow>
//           ))}
//         </TableBody>
//       </Table>
//     </TableContainer>
//       {editandoDashboard && (
//         <Formulario onClose={closeEditandoDashboard} submit={onSubmitEditandoDashboard} icono={itemEditado.icono} nombre={itemEditado.nombre}/>
//       )}
//       <Button variant="contained" color="primary" onClick={() => adding()}>+</Button>
//       <InfoBox info={selectedItem} anchorEl={anchorEl} onClose={handleClose}/>
//     </>
//   );
// }

// export default Lista;
