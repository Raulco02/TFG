import React, { useState, useEffect } from 'react';
import { useForm, Controller } from 'react-hook-form';
import { useNavigate, useLocation } from "react-router-dom";
import { Button, MenuItem, TextField, Popover, Box, Grid, IconButton, Typography } from '@mui/material';
import { ArrowForward, Close, Add, Remove } from '@mui/icons-material';
import grupoService from '../../services/grupoService';
import dispositivoService from '../../services/dispositivoService';

const FormularioTipos = ({ tipo = null, onClose, popover = false, theme }) => {
  const { handleSubmit, setValue, control, watch, formState: { errors } } = useForm();
  const navigate = useNavigate();

  const onSubmit = async (data) => {
    console.log('data:', data);
  }


  const formContent = (
    <Box className={!popover ? 'formulario' : ''} sx={{ padding: 2, backgroundColor: theme.palette.background.paper, color: theme.palette.primary.text }}>
      <form onSubmit={handleSubmit(onSubmit)}>
        <Grid container spacing={2}>
        <Grid item xs={12}>
          <Typography variant="h5" gutterBottom>
              Tipo de atributos
          </Typography>
        </Grid>
          <Grid item xs={12}>
            <Controller
              name="nombre"
              control={control}
              defaultValue={tipo?.nombre || ''}
              rules={{ required: 'Este campo es requerido' }}
              render={({ field }) => (
                <TextField
                  {...field}
                  label="Nombre"
                  fullWidth
                  error={!!errors.nombre}
                  helperText={errors.nombre && errors.nombre.message}
                />
              )}
            />
          </Grid>
          <Grid item xs={6}>
            <Button variant="contained" fullWidth onClick={onClose} endIcon={<Close />}>
              Cancelar
            </Button>
          </Grid>
          <Grid item xs={6}>
            <Button type="submit" variant="contained" fullWidth endIcon={<ArrowForward />}>
              Guardar
            </Button>
          </Grid>
        </Grid>
      </form>
    </Box>
  );

  return (
    <>
      {popover ? (
        <Popover open={true} anchorOrigin={{ vertical: 'center', horizontal: 'center' }} transformOrigin={{ vertical: 'center', horizontal: 'center' }}>
          {formContent}
        </Popover>
      ) : (
        formContent
      )}
    </>
  );
};

export default FormularioTipos;
