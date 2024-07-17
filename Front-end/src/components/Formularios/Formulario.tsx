// Formulario.js
import React, { useEffect } from 'react';
import { useForm, Controller } from 'react-hook-form';
import { Button, MenuItem, TextField, Popover, Box, Grid } from '@mui/material';
import { ArrowForward, Close } from '@mui/icons-material';
import { getIconComponent } from '../../utils/iconUtils';
import { IconName } from '../../resources/enums/enums';

const Formulario = ({onClose, submit, icono = null, nombre = null, popover = true, theme}) => {
  const { handleSubmit, setValue, control, formState: { errors } } = useForm();

  const onSubmit = submit;

  const iconOptions = Object.values(IconName).map((iconName) => ({
    value: iconName,
    label: (
      <Box sx={{ display: 'flex', alignItems: 'center' }}>
        <Box sx={{ marginRight: 1 }}>{getIconComponent(iconName)}</Box>
        <span>{iconName}</span>
      </Box>
    ),
  }));

  useEffect(() => {
    if (icono && nombre) {
      console.log('icono:', icono, 'nombre:', nombre)
      setValue('icono', icono);
      setValue('nombre', nombre);
    }
  }, [icono, nombre, setValue]);

  const formContent = (
    <Box className={!popover ? 'formulario' : ''} sx={{ padding: 2, backgroundColor: theme.palette.background.paper }}>
      <form onSubmit={handleSubmit(onSubmit)}>
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <Controller
              name="icono"
              control={control}
              defaultValue={icono || ''}
              rules={{ required: 'Este campo es requerido' }}
              render={({ field }) => (
                <TextField
                  {...field}
                  select
                  label="Icono"
                  fullWidth
                  error={!!errors.icono}
                  style={{ color: theme.palette.text.primary }}
                  helperText={errors.icono && errors.icono.message}
                >
                  {iconOptions.map((option) => (
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

export default Formulario;
