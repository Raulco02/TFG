import React, { useState, useEffect } from 'react';
import { useForm, Controller } from 'react-hook-form';
import { useNavigate, useLocation } from "react-router-dom";
import { Button, MenuItem, TextField, Popover, Box, Grid, IconButton, Typography } from '@mui/material';
import { ArrowForward, Close, Add, Remove } from '@mui/icons-material';
import grupoService from '../../services/grupoService';
import dispositivoService from '../../services/dispositivoService';
import { IconName } from '../../resources/enums/enums';
import { getIconComponent } from '../../utils/iconUtils';

const FormularioGrupo = ({ grupo = null, onClose, popover = false, theme }) => {
  const { handleSubmit, setValue, control, watch, formState: { errors } } = useForm();
  const [dispositivosGrupo, setDispositivosGrupo] = useState([]);
  const [opcionesDispositivos, setOpcionesDispositivos] = useState([]);
  const navigate = useNavigate();

  const onSubmit = async (data) => {
    console.log('Dispositivos grupo:', dispositivosGrupo);
    data.dispositivos = dispositivosGrupo.map(d => ({ id: d.id }));
    console.log('data:', data);
  };

  useEffect(() => {
    async function getDispositivosGrupo() {
      try {
        if (grupo) {
          const respuesta = await grupoService.getGrupo(grupo.id);
          console.log("Respuesta del grupo:", respuesta);
          setValue('nombre', grupo.nombre);
          setValue('icono', grupo.icono);
          if (respuesta) {
            const dispositivos = respuesta.map((dispositivo) => ({
              id: dispositivo.id,
              nombre: dispositivo.nombre
            }));
            setDispositivosGrupo(dispositivos);
            setOpcionesDispositivos(prevOpciones =>
              prevOpciones.filter(opcion => !dispositivos.some(d => d.id === opcion.id))
            );
          }
        }
      } catch (error) {
        console.error("Error:", error);
      }
    }
    getDispositivosGrupo();
  }, [grupo, setValue]);

  useEffect(() => {
    async function getDispositivos() {
      try {
        const respuesta = await dispositivoService.getDispositivos();
        console.log("Respuesta a dispositivos:", respuesta);
        setOpcionesDispositivos(respuesta.filter(opcion => !dispositivosGrupo.some(d => d.id === opcion.id)));
      } catch (error) {
        console.error("Error:", error);
      }
    }
    getDispositivos();
    console.log('Dispositivos grupo:', dispositivosGrupo);
  }, [dispositivosGrupo]);

  const handleAddDevice = () => {
    setDispositivosGrupo([...dispositivosGrupo, { id: '', nombre: '' }]);
  };

  const handleRemoveDevice = (index) => {
    const dispositivoRemovido = dispositivosGrupo[index];
    const newDispositivosGrupo = dispositivosGrupo.filter((_, i) => i !== index);
    setDispositivosGrupo(newDispositivosGrupo);

    if (dispositivoRemovido && dispositivoRemovido.id) {
      setOpcionesDispositivos([...opcionesDispositivos, dispositivoRemovido]);
    }
  };

  const dispositivos = watch('dispositivos') || [];

  const iconOptions = Object.values(IconName).map((iconName) => ({
    value: iconName,
    label: (
      <Box sx={{ display: 'flex', alignItems: 'center' }}>
        <Box sx={{ marginRight: 1 }}>{getIconComponent(iconName)}</Box>
        <span>{iconName}</span>
      </Box>
    ),
  }));

  const formContent = (
    <Box className={!popover ? 'formulario' : ''} sx={{ padding: 2, backgroundColor: theme.palette.background.paper, color: theme.palette.primary.text }}>
      <form onSubmit={handleSubmit(onSubmit)}>
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <Typography variant="h5" gutterBottom>
                Grupo
            </Typography>
          </Grid>
          <Grid item xs={12}>
            <Controller
              name="nombre"
              control={control}
              defaultValue={grupo?.nombre || ''}
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
          <Grid item xs={12}>
            <Controller
              name="icono"
              control={control}
              defaultValue={grupo?.icono || ''}
              rules={{ required: 'Este campo es requerido' }}
              render={({ field }) => (
                <TextField
                  {...field}
                  select
                  label="Icono"
                  fullWidth
                  error={!!errors.icono}
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
          {dispositivosGrupo.map((device, index) => (
            <Grid item xs={12} key={device.id || index} container spacing={2} alignItems="center">
              <Grid item xs={10}>
                <Controller
                  name={`dispositivos[${index}].id`}
                  control={control}
                  defaultValue={device.id}
                  rules={{ required: 'Este campo es requerido', validate: value => value.trim() !== '' || 'Este campo no puede estar vacío' }}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      select
                      label="Seleccione un dispositivo"
                      fullWidth
                      value={field.value || ''}
                      onChange={(e) => {
                        field.onChange(e);
                        const nuevoDispositivoNombre = e.target.value;
                        const nuevoDispositivo = opcionesDispositivos.find(d => d.nombre === nuevoDispositivoNombre);

                        if (!nuevoDispositivo) {
                          console.log('No se encontró el dispositivo');
                          return;
                        }

                        const newDispositivosGrupo = [...dispositivosGrupo];
                        newDispositivosGrupo[index] = nuevoDispositivo;
                        setDispositivosGrupo(newDispositivosGrupo);

                        setOpcionesDispositivos(opcionesDispositivos.filter(d => d.id !== nuevoDispositivo.id));
                        setValue(`dispositivos[${index}].id`, nuevoDispositivoNombre);
                      }}
                      error={!!errors.dispositivos && !!errors.dispositivos[index]?.id}
                      helperText={errors.dispositivos && errors.dispositivos[index]?.id && errors.dispositivos[index]?.id.message}
                    >
                      {[ ...(dispositivosGrupo[index].id ? [dispositivosGrupo[index]] : []),
                        ...opcionesDispositivos].map((opcion) => (
                        <MenuItem key={opcion.id} value={opcion.id}>
                          {opcion.id}
                        </MenuItem>
                      ))}
                    </TextField>
                  )}
                />
              </Grid>
              <Grid item xs={2}>
                <IconButton onClick={() => handleRemoveDevice(index)}>
                  <Remove />
                </IconButton>
              </Grid>
            </Grid>
          ))}
          {opcionesDispositivos.length > 0 && (
            <Grid item xs={12}>
              <Button variant="outlined" fullWidth onClick={handleAddDevice} startIcon={<Add />}>
                Añadir dispositivo
              </Button>
            </Grid>
          )}
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

export default FormularioGrupo;
