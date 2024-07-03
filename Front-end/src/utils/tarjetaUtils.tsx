import React from 'react';
import { Tarjetas } from '../resources/enums/enums';
import { Tarjeta } from '../resources/Interfaces/interfaces';
import { Grid, Button } from '@mui/material';

export const getTarjetaComponent = (tarjeta: Tarjeta): React.ReactNode => {
    switch (tarjeta.tipo) {
        case Tarjetas.Texto: //Hacer componente por cada tarjeta
            return <div> Tarjeta Texto </div>;
        case Tarjetas.Grafico:
            return <div> Tarjeta Gráfico </div>;
        case Tarjetas.Imagen:
            return <div> Tarjeta Imagen </div>;
        case Tarjetas.Estado:
            return <div> Tarjeta Estado </div>;
        case Tarjetas.Termostato:
            return <div> Tarjeta Termostato </div>;
        default:
            return null;
    }
};

