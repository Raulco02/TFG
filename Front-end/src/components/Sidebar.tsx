import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Drawer, List, ListItemButton, ListItemIcon, ListItemText, Divider, Typography, Box, IconButton } from '@mui/material';
import SettingsIcon from '@mui/icons-material/Settings';
import AddIcon from '@mui/icons-material/Add';
import LogoutIcon from '@mui/icons-material/Logout';
import MenuIcon from '@mui/icons-material/Menu';
import { Dashboard } from '../resources/Interfaces/interfaces';
import { getIconComponent } from '../utils/iconUtils';
import userService from '../services/userService';

interface SidebarProps {
  dashboards: Dashboard[];
  setSelectedDashboard: (dashboard: Dashboard) => void;
  crearDashboard: () => void;
  className?: string;
  drawerOpen: boolean;
  toggleDrawer: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ dashboards, setSelectedDashboard, crearDashboard, className, drawerOpen, toggleDrawer }) => {
  const navigate = useNavigate();

  const showCreateDashboardButton = dashboards.length < 5;

  const handleLogOut = async () => {
    try {
      await userService.logout();
      navigate("/");
    } catch (error) {
      console.error("Error al cerrar sesión:", error);
    }
  };

  return (
    <Box sx={{ display: 'flex' }} className={className}>
      <Drawer
        anchor="left"
        open={drawerOpen}
        variant="permanent"
        sx={{
          width: drawerOpen ? 240 : 56,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: drawerOpen ? 240 : 56,
            boxSizing: 'border-box',
            backgroundColor: 'primary.main', // Cambia el color de fondo del Drawer
            color: 'primary.contrastText',  // Cambia el color del texto del Drawer
          },
        }}
      >
        <Box sx={{ display: 'flex', alignItems: 'center', cursor: 'pointer', padding: drawerOpen ? '5px' : '0', justifyContent: 'left', backgroundColor: 'background.paper' }}>
          <IconButton onClick={toggleDrawer} sx={{ margin: 1, color: 'primary.secondaryText' }}>
            <MenuIcon />
          </IconButton>

          {drawerOpen && (
            <>
              <img
                src="logo-sin-fondo.png"
                alt="Logo Smart ESI"
                style={{ marginRight: drawerOpen ? '10px' : '0', width: '35px', height: '35px' }}
                onClick={() => { navigate('/dashboard') }}
              />
              <Typography
                variant="h6"
                component="div"
                onClick={() => { navigate('/dashboard') }}
                sx={{
                  padding: '10px',
                  borderRadius: '5px',
                  textAlign: 'center',
                  color: 'primary.secondaryText',  // Cambia el color del texto
                }}
              >
                SmartESI
              </Typography>
            </>
          )}
        </Box>
        <Divider />
        <List>
          {dashboards.map((item, index) => (
            <ListItemButton key={index} onClick={() => { setSelectedDashboard(item); navigate('/dashboard') }} sx={{ color: 'primary.contrastText' }}>
              <ListItemIcon sx={{ color: 'primary.contrastText' }}>{getIconComponent(item.icono)}</ListItemIcon>
              {drawerOpen && <ListItemText primary={item.nombre} />}
            </ListItemButton>
          ))}
          {showCreateDashboardButton && (
            <ListItemButton onClick={crearDashboard} sx={{ color: 'primary.contrastText' }}>
              <ListItemIcon sx={{ color: 'primary.contrastText' }}>
                <AddIcon />
              </ListItemIcon>
              {drawerOpen && <ListItemText primary="Crear dashboard" />}
            </ListItemButton>
          )}
          <Divider />
          <ListItemButton onClick={() => navigate("/config")} sx={{ color: 'primary.contrastText' }}>
            <ListItemIcon sx={{ color: 'primary.contrastText' }}>
              <SettingsIcon />
            </ListItemIcon>
            {drawerOpen && <ListItemText primary="Configuración" />}
          </ListItemButton>
          <ListItemButton onClick={handleLogOut} sx={{ color: 'primary.contrastText' }}>
            <ListItemIcon sx={{ color: 'primary.contrastText' }}>
              <LogoutIcon />
            </ListItemIcon>
            {drawerOpen && <ListItemText primary="Cerrar sesión" />}
          </ListItemButton>
        </List>
      </Drawer>
    </Box>
  );
};

export default Sidebar;
