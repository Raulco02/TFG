import React from "react";
import {
  Grid,
  Card,
  CardContent,
  CardActionArea,
  Typography,
  useTheme,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import { styled } from '@mui/system';
import DevicesIcon from '@mui/icons-material/Devices';
import DevicesOtherIcon from '@mui/icons-material/DevicesOther';
import GroupsIcon from '@mui/icons-material/Groups';
import DashboardIcon from '@mui/icons-material/Dashboard';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import AlertIcon from '@mui/icons-material/NotificationImportant';
import RuleIcon from '@mui/icons-material/Rule';
import IntegrationIcon from '@mui/icons-material/IntegrationInstructions';

const CardContentStyled = styled(CardContent)(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  padding: theme.spacing(3),
}));

const IconStyled = styled('div')(({ theme }) => ({
  marginRight: theme.spacing(2),
}));

const CardActionAreaStyled = styled(CardActionArea)({
  height: "100%",
  width: "100%",
});

const Config = ({ isAdmin }) => {
  const navigate = useNavigate();
  const theme = useTheme();

  const menuItems = [
    { text: "Perfil", icon: <AccountCircleIcon />, onClick: () => navigate("/cuenta", {state: true}) },
    { text: "Dashboards", icon: <DashboardIcon />, onClick: () => navigate("/dashboards") },
    { text: "Grupos de dispositivos", icon: <DevicesOtherIcon  />, onClick: () => navigate("/grupos") },
    { text: "Alertas", icon: <AlertIcon />, onClick: () => navigate("/alertas") },
  ];

  const adminItems = [
    { text: "Dispositivos", icon: <DevicesIcon />, onClick: () => navigate("/dispositivos") },
    { text: "Gestión de usuarios", icon: <GroupsIcon />, onClick: () => navigate("/usuarios") },
    { text: "Reglas", icon: <RuleIcon />, onClick: () => navigate("/reglas") },
    { text: "Integraciones", icon: <IntegrationIcon />, onClick: () => navigate("/integraciones") },
    { text: "Tipos de atributos", icon: <DevicesIcon />, onClick: () => navigate("/tipos-atributos")}
  ];
//No funciona el overflow, no se como hacerlo
  return (
    <div style={{overflow:"auto", padding:"2px"}}> 
    <Grid container spacing={3}>
      {menuItems.map((item, index) => (
        <Grid item xs={12} md={4} key={index}>
          <Card sx={{backgroundColor: theme.palette.background.paper, height: "100%"}}>
            <CardActionAreaStyled onClick={item.onClick}>
              <CardContentStyled>
                <IconStyled sx={{color: theme.palette.primary.secondaryText}}>{item.icon}</IconStyled>
                <div>
                  <Typography variant="h6" gutterBottom sx={{color: theme.palette.primary.secondaryText}}>
                    {item.text}
                  </Typography>
                  <Typography variant="body2" sx={{color: theme.palette.primary.secondaryText}}>
                    {`Administrar ${item.text.toLowerCase()}`}
                  </Typography>
                </div>
              </CardContentStyled>
            </CardActionAreaStyled>
          </Card>
        </Grid>
      ))}
      {isAdmin && adminItems.map((item, index) => (
        <Grid item xs={12} md={4} key={index}>
          <Card sx={{backgroundColor: theme.palette.background.paper}}>
            <CardActionAreaStyled onClick={item.onClick}>
              <CardContentStyled>
                <IconStyled sx={{color: theme.palette.primary.secondaryText}}>{item.icon}</IconStyled>
                <div>
                  <Typography variant="h6" gutterBottom sx={{color: theme.palette.primary.secondaryText}}>
                    {item.text}
                  </Typography>
                  <Typography variant="body2" sx={{color: theme.palette.primary.secondaryText}}>
                    {`Administrar ${item.text.toLowerCase()}`}
                  </Typography>
                </div>
              </CardContentStyled>
            </CardActionAreaStyled>
          </Card>
        </Grid>
      ))}
    </Grid>
    </div>
  );
};

export default Config;
