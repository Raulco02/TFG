// Formulario.js
import React, { useEffect } from 'react';
import { useForm, Controller, set } from 'react-hook-form';
import { Button, MenuItem, TextField, Popover, Box, Grid } from '@mui/material';
import { ArrowForward, Close } from '@mui/icons-material';
import { getIconComponent } from '../../utils/iconUtils';
import { Layouts } from '../../resources/enums/enums';

const FormularioSeccion = ({onClose, submit, layout=null, nombre=null}) => {
  const { handleSubmit, setValue, control, formState: { errors } } = useForm();

  const onSubmit = submit;

  const layoutptions = Object.keys(Layouts).map((layout) => ({
    value: layout,
    label: (
      <Box sx={{ display: 'flex', alignItems: 'center' }}>
        <span>{layout}</span>
      </Box>
    ),
  }));

  useEffect(() => {
    if (layout && nombre) {
      setValue('layout', layout);
      setValue('nombre', nombre);
    }
  }, [layout, nombre]);

  return (
    <Popover open={true} anchorOrigin={{ vertical: 'center', horizontal: 'center' }} transformOrigin={{ vertical: 'center', horizontal: 'center' }}>
      <Box sx={{ padding: 2 }}>
        <form onSubmit={handleSubmit(onSubmit)}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <Controller
                name="layout"
                control={control}
                rules={{ required: 'Este campo es requerido' }}
                render={({ field }) => (
                  <TextField
                    {...field}
                    select
                    label="Layout"
                    fullWidth
                    error={!!errors.layout}
                    helperText={errors.layout && errors.layout.message}
                  >
                    {layoutptions.map((option) => (
                      <MenuItem key={option.value} value={option.value}>
                        {option.label}
                      </MenuItem>
                    ))}
                  </TextField>
                )}
              />
            </Grid>
            <Grid item xs={12}>
              <Controller
                name="nombre"
                control={control}
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
    </Popover>
  );
};

export default FormularioSeccion;
