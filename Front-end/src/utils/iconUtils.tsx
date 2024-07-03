// iconUtils.ts
import React from 'react';
import HomeIcon from '@mui/icons-material/Home';
import InfoIcon from '@mui/icons-material/Info';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import DashboardIcon from '@mui/icons-material/Dashboard';
import AddCircleIcon from '@mui/icons-material/AddCircle';
import EditIcon from '@mui/icons-material/Edit';
import DoNotDisturbIcon from '@mui/icons-material/DoNotDisturb';
import DeviceThermostatIcon from '@mui/icons-material/DeviceThermostat';
import WaterDropIcon from '@mui/icons-material/WaterDrop';
import Co2Icon from '@mui/icons-material/Co2';
import Battery5BarIcon from '@mui/icons-material/Battery5Bar';
import WbIncandescentIcon from '@mui/icons-material/WbIncandescent';
import AdsClick from '@mui/icons-material/AdsClick';
import DeleteIcon from '@mui/icons-material/Delete';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';

import { IconName } from '../resources/enums/enums';

// {
//     "mover": "gnfjkdngkdsf"
// }
// icons["mover"]
export const getIconComponent = (iconName: IconName): React.ReactNode => {
    switch (iconName) {
        case IconName.Home:
            return <HomeIcon />;
        case IconName.Info:
            return <InfoIcon />;
        case IconName.AccountCircle:
            return <AccountCircleIcon />;
        case IconName.Dashboard:
            return <DashboardIcon />;
        case IconName.Add:
            return <AddCircleIcon/>;
        // Agrega más íconos según tus necesidades
        case IconName.Edit:
            return <EditIcon />;
        case IconName.Temperatura:
            return <DeviceThermostatIcon />;
        case IconName.Temperatura_Obj:
            return <AdsClick />;
        case IconName.Humedad:
            return <WaterDropIcon />;
        case IconName.Luz:
            return <WbIncandescentIcon />;
        case IconName.Bateria:
            return <Battery5BarIcon />;
        case IconName.CO2:
            return <Co2Icon />;
        case IconName.Movimiento:
            return <DoNotDisturbIcon />;
        case IconName.Delete:
            return <DeleteIcon />;
        case IconName.Back:
            return <ArrowBackIcon />;
        case IconName.Default:
            return <DoNotDisturbIcon />;
        default:
            return <DoNotDisturbIcon />;
    }
};
