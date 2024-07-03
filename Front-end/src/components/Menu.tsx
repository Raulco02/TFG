import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Sidebar from "./Sidebar";
import Seccionbar from "./Seccionbar";
import "../App.css";
import { IconButton } from '@mui/material';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { CssBaseline, Popover, Button, Typography } from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import CloseIcon from '@mui/icons-material/Close';
import { Dashboard, Seccion, User, createForm, createSeccionForm, createSeccion } from "../resources/Interfaces/interfaces";
import { getDatos } from "../utils/userUtils";
import dashboardService from "../services/dashboardService";
import seccionService from "../services/seccionService";
import Formulario from "./Formularios/Formulario";
import FormularioSeccion from "./Formularios/FormularioSeccion";
import { Layouts } from "../resources/enums/enums";
import clsx from 'clsx';

type MenuProps = {
  children: React.ReactNode;
  setSelectedSeccion: (seccion: Seccion | null) => void;
  selectedSeccion: Seccion | null;
  setItems: (items: any) => void;
  editando: boolean;
  setEditando: (editando: boolean) => void;
  showSeccionbar?: boolean;
};

const Menu: React.FC<MenuProps> = ({ children, setSelectedSeccion, selectedSeccion, setItems, editando, setEditando, showSeccionbar, popoverMessage, setPopoverMessage, popoverOpen, setPopoverOpen }) => {
  const [perfil, setPerfil] = useState<User | null>(null);
  const [dashboards, setDashboards] = useState<Dashboard[]>([]);
  const [selectedDashboard, setSelectedDashboard] = useState<Dashboard | null>(null);
  const [creandoDashboard, setCreandoDashboard] = useState(false);
  const [secciones, setSecciones] = useState<Seccion[]>([]);
  const [creandoSeccion, setCreandoSeccion] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);
  const [drawerOpen, setDrawerOpen] = useState(true);
  const [theme, setTheme] = useState<'light' | 'dark'>('light');
  const navigate = useNavigate();

  useEffect(() => {
    async function obtenerPerfil() {
      const datos = await getDatos();
      if (!datos?.usuario) {
        navigate("/");
      }
      setPerfil(datos.usuario);
      setIsAdmin(datos.usuario.rol === 1);
      setDashboards(datos.dashboards);
      setSelectedDashboard(datos.dashboards[0]);
      console.log("Dashboards", datos)
      setSecciones(datos.dashboards[0].secciones);
      setSelectedSeccion(datos.dashboards[0].secciones[0]);
      setItems(datos.dashboards[0].secciones[0].tarjetas);
    }
    obtenerPerfil();
  }, []);

  useEffect(() => {
    setSecciones(selectedDashboard?.secciones || []);
    if (selectedDashboard?.secciones !== undefined) {
      setSelectedSeccion(selectedDashboard?.secciones[0]);
      setItems(selectedDashboard?.secciones[0].tarjetas || []);
    } else {
      setSelectedSeccion(null);
      setItems([]);
    }
    setEditando(false);
  }, [selectedDashboard]);

  // useEffect(() => {
  //   if (selectedSeccion) {
  //     setItems(selectedSeccion.tarjetas);
  //   }
  // }, [selectedSeccion]);

  const crearDashboard = () => setCreandoDashboard(true);
  const crearSeccion = () => setCreandoSeccion(true);
  const handleCloseForm = () => {
    setCreandoDashboard(false);
    setCreandoSeccion(false);
  };

  const onSubmitFormDashboard = async (data: createForm) => { //datos no es la variable que busco
    try {
      const response = await dashboardService.createDashboard(data);
      const id_dashboard = response["datos"]["id_dashboard"];
      const datos = await dashboardService.getDashboard(id_dashboard);
      //const datos = await dashboardService.getDashboards();
      console.log(datos);
      console.log(datos[datos.length - 1]);
      console.log(datos[datos.length - 1].secciones);
      console.log(datos[datos.length - 1].secciones[0].tarjetas);
      setDashboards([...dashboards, datos[0]]);
      setSelectedDashboard(datos[0]);
      setSecciones(datos[0].secciones);
      setSelectedSeccion(datos[0].secciones[0]);
      setItems(datos[0].secciones[0].tarjetas);
      setPopoverMessage(response.message); // Suponiendo que la respuesta tiene un campo `message`
      setPopoverOpen(true);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setCreandoDashboard(false);
    }
  };

  const onSubmitFormSeccion = async (data: createSeccionForm) => {
    try {
      let layoutType = Layouts.Grid;
      if (data.layout === 'Card') layoutType = Layouts.Card;
      if (data.layout === 'Sidebar') layoutType = Layouts.Sidebar;
      const datos: createSeccion = {
        nombre: data.nombre,
        layout: layoutType,
        dashboard_id: selectedDashboard?.id || "",
      };
      const response = await seccionService.createSeccion(datos);
      const dashboard = await dashboardService.getDashboard(selectedDashboard?.id || "");
      setSecciones(dashboard.secciones);
      setSelectedSeccion(dashboard.secciones[dashboard.secciones.length - 1]); // Tengo el id, debe haber una forma de obtener el objeto seccion
      //const seccion = await seccionService.getSeccion(response.id);
      setItems(dashboard.secciones[dashboard.secciones.length - 1].tarjetas);

      setPopoverMessage(response.message); // Suponiendo que la respuesta tiene un campo `message`
      setPopoverOpen(true);
      
      //Ver como hacer que si la respuesta es 200 se añada sin recargar la pagina y se muestren mensajes 
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setCreandoSeccion(false);
    }
  };

  const toggleEdicion = () => setEditando(!editando);
  const toggleDrawer = () => setDrawerOpen(!drawerOpen);

  // Define los temas claro y oscuro
  const themeClaro = createTheme({
    palette: {
      mode: 'light', // Modo claro
      primary: {
        main: '#1976d2',  // Color principal
        contrastText: '#fff',  // Color del texto en elementos con el color principal
        secondaryText: '#1976d2',
        text: '#000',  // Color del texto en elementos con el color principal
      },
      opposite: {
        main: '#f5f5f5',  // Color opuesto
        contrastText: '#1976d2',  // Color del texto en elementos con el color opuesto
      },
      secondary: {
        main: '#dc004e',  // Color secundario
        contrastText: '#fff',  // Color del texto en elementos con el color secundario
      },
      background: {
        default: '#f5f5f5',  // Color de fondo de la aplicación
        paper: '#fff',  // Color de fondo de los elementos
        list: '#f0f0f0'
      },
    },
  });
  const themeOscuro = createTheme({
    palette: {
      primary: {
        main: '#1d2262',  // Color principal
        contrastText: '#fff',  // Color del texto en elementos con el color principal
        secondaryText: '#fff',
        text: '#fff',
        button: '#dc004e'
      },
      secondary: {
        main: '#dc004e',  // Color secundario
        contrastText: '#fff',  // Color del texto en elementos con el color secundario
      },
      opposite: {
        main: '#fff',  // Color opuesto
        contrastText: '#1d2262',  // Color del texto en elementos con el color opuesto
      },
      config: {
        main: '#fff'
      },
      background: {
        default: '#242424',  // Color de fondo de la aplicación
        paper: '#333',
        list: '#222'
      },
    },
    components: {
      MuiTextField: {
        styleOverrides: {
          root: {
            backgroundColor: '#242424', // Color de fondo predeterminado para los TextField
            borderRadius: '5px',
          },
          input: {
            color: '#ffffff', // Color del texto dentro del TextField
            '&::placeholder': {
              color: '#fffff', // Color del placeholder dentro del TextField
            },
          },
          // focused: {
          //   borderColor: '#f50057 !important', // Color del borde cuando el TextField está enfocado
          // },
        },
      },
      MuiInputLabel: {
        styleOverrides: {
          root: {
            color: '#DDDDDD', // Cambiar color de la etiqueta
          },
        },
      },
      MuiInputBase: {
        styleOverrides: {
          root: {
            backgroundColor: '#242424', // Cambiar color de fondo del input
            borderColor: '#ffffff', // Cambiar color del borde del input
            color: '#ffffff'
          },
        },
      },
      MuiSelect: {
        styleOverrides: {
          root: {
            color: 'white',
          },
        },
      },
    },
  });
    // Función para detectar el tema del navegador
    const detectarTemaNavegador = () => {
      if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        setTheme('dark');
      } else {
        setTheme('light');
      }
    };
  
    // Detectar el tema del navegador al cargar el componente
    useEffect(() => {
      detectarTemaNavegador();
    }, []);

    useEffect(() => {
      const handleResize = () => {
        if ((window.innerWidth <= 768 && drawerOpen) || (window.screen.width <= 768 && drawerOpen)) {
          setDrawerOpen(false);
        } else if ((window.innerWidth > 768 && !drawerOpen) || window.screen.width > 768 && !drawerOpen) {
          setDrawerOpen(true);
        }
      };
      //handleResize();
      window.addEventListener('resize', handleResize);
      return () => {
        window.removeEventListener('resize', handleResize);
      };
    }, [drawerOpen]);

    const temaActual = theme === 'light' ? themeClaro : themeOscuro;

    const handleAceptarClick = () => {
      setPopoverOpen(false);
      // Puedes realizar acciones adicionales al aceptar el mensaje, si es necesario
    };

  return (
    <ThemeProvider theme={temaActual}>
      <CssBaseline />
      <div className={clsx('menu-container', { 'sidebar-compact': !drawerOpen, 'no-seccionbar': !showSeccionbar })}>
        <Sidebar
          dashboards={dashboards}
          setSelectedDashboard={setSelectedDashboard}
          crearDashboard={crearDashboard}
          className="sidebar"
          drawerOpen={drawerOpen}
          toggleDrawer={toggleDrawer}
        />
        { showSeccionbar && (
        <Seccionbar
          secciones={secciones}
          setSelectedSeccion={setSelectedSeccion}
          crearSeccion={crearSeccion}
          editarSeccion={crearSeccion}
          setItems={setItems}
          className="seccionbar"
          editando={editando}
        />
        )}
        <div className={clsx('info-section', { 'no-seccionbar': !showSeccionbar })}>
          {React.Children.map(children, (child) => {
            if (React.isValidElement(child)) {
              return React.cloneElement(child, { isAdmin, theme: temaActual });
            }
            return child;
          })}
          { showSeccionbar && (
          <IconButton
            onClick={toggleEdicion}
            sx={{
              position: 'absolute',
              bottom: 16,
              right: 16,
              width: '50px',
              height: '50px',
              backgroundColor: temaActual.palette.primary.main,
              color: temaActual.palette.primary.contrastText,
              '&:hover': { backgroundColor: '#3B92E9' },
            }}
          >
            {editando ? <CloseIcon /> : <EditIcon />}
          </IconButton>
          )}
        </div>
        {creandoDashboard && <Formulario onClose={handleCloseForm} submit={onSubmitFormDashboard} />}
        {creandoSeccion && <FormularioSeccion onClose={handleCloseForm} submit={onSubmitFormSeccion} />}
        <Popover
      open={popoverOpen}
      onClose={() => setPopoverOpen(false)}
      anchorOrigin={{
        vertical: 'center',
        horizontal: 'center',
      }}
      transformOrigin={{
        vertical: 'top',
        horizontal: 'center',
      }}
    >
      <div style={{ width: '300px', height: '150px', padding: '20px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center'  }}>
        <Typography>{popoverMessage}</Typography>
        <Button onClick={handleAceptarClick} variant="contained" color="primary" style={{ marginTop: '10px' }}>
          Aceptar
        </Button>
      </div>
    </Popover>
      </div>
    </ThemeProvider>
  );
};

export default Menu;
