import React, { useState, useEffect } from 'react';
import { TextField, Button, IconButton, Typography, Grid } from '@mui/material';
import { Add as AddIcon, Remove as RemoveIcon } from '@mui/icons-material';
import tarjetaService from '../../services/tarjetaService';

const Termostato = ({ valorInicial, nombreAtributo, nombreDispositivo, idDispositivo, idAtributo, unidad, theme }) => {
  const [valor, setValor] = useState(valorInicial);
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

  const handleInputChange = (e) => {
    const newValue = e.target.value;
    const regex = /^[0-9]{2}\.[0-9]$/; // RegEx para el formato DU.d
    if (regex.test(newValue)) {
      setValor(newValue);
    }
  };

  const incrementar = () => {
    let newValue = parseFloat(valor) + 0.1;
    newValue = newValue.toFixed(1).toString();
    if (/^[0-9]{2}\.[0-9]$/.test(newValue)) {
      setValor(newValue);
    }
  };

  const disminuir = () => {
    let newValue = parseFloat(valor) - 0.1;
    newValue = newValue.toFixed(1).toString();
    if (/^[0-9]{2}\.[0-9]$/.test(newValue)) {
      setValor(newValue);
    }
  };

  const setTemperatura = async () => {
    console.log(valor);
    const sendTemperatura = await tarjetaService.sendTemperaturaTermostato({
        id_dispositivo: idDispositivo,
        id_atributo: idAtributo,
        valor: valor,
     });
    console.log(sendTemperatura);
  };

  return (
    <div className='atributo-card' style={{ height: '100%', width: '100%', padding: '4%' }}>
      {valor !== null ? (
        <div style={{ height: '100%', width: '100%'}}>
              <h3 style={{ fontSize: "1em" }}>
                {nombreAtributo + " " + nombreDispositivo}
              </h3>
          {/* <Typography variant="h6" style={{ marginBottom: '1em' }}>{`${nombreAtributo} ${nombreDispositivo}`}</Typography> */}
          <Grid container alignItems="center" spacing={0}>
            <Grid item xs={6} md={10} lg={6}>
              <TextField
                fullWidth
                type="text"
                value={valor}
                onChange={handleInputChange}
                sx={{ color: theme.palette.primary.text, backgroundColor: theme.palette.background.default, borderRadius: '5px' }}
                InputProps={{
                  sx: { color: theme.palette.primary.text }
                }}
                InputLabelProps={{
                  sx: { color: theme.palette.primary.text }
                }}
              />
            </Grid>
            <Grid item xs={2} md={2} xl={2}>
              <IconButton onClick={incrementar}>
                <AddIcon sx={{color: theme.palette.primary.text}}/>
              </IconButton>
              <IconButton onClick={disminuir}>
                <RemoveIcon sx={{color: theme.palette.primary.text}}/>
              </IconButton>
            </Grid>
            <Grid item xs={2} md={12} lg={2}>
              <Button
                variant="contained"
                color="primary"
                onClick={setTemperatura}
                style={{ height: '100%', textTransform: 'capitalize' }}
              >
                Establecer
              </Button>
            </Grid>
          </Grid>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default Termostato;
