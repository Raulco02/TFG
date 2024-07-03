// Formulario.js
import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from "react-router-dom";
import { useForm, Controller } from 'react-hook-form';
import { Button, MenuItem, TextField, Box, Grid, IconButton, Typography } from '@mui/material';
import { ArrowForward, Close, Add } from '@mui/icons-material';
import { Comparadores, Acciones } from '../../resources/enums/enums';
import dispositivoService from '../../services/dispositivoService';
import reglaService from '../../services/reglaService';

const FormularioRegla = ({regla = null, onClose, theme}) => {
  const { handleSubmit, setValue, control, formState: { errors } } = useForm();
  const [dispositivos, setDispositivos] = useState([]);
  const [atributos, setAtributos] = useState([]);
  const [disparadores, setDisparadores] = useState([{ id: Date.now() }]);
  const [condiciones, setCondiciones] = useState([{ id: Date.now() + 1 }]);
  const [acciones, setAcciones] = useState([{ id: Date.now() + 2 }]);

  // const location = useLocation();
  const navigate = useNavigate();

  // const onClose = () => {
  //   navigate("/reglas");
  // };

  useEffect(() => { //Arreglar los índices
    if(regla){
      console.log("Regla:", regla)
      setValue("nombre", regla.nombre);
      let index_c = 0;
      let index_d = 0;
      Object.values(regla.criterios).forEach((criterio, index) => {
        console.log("Criterio",criterio, index, )
        const indice = criterio.tipo === "d" ? index_d : index_c;
        const nombre_tipo = criterio.tipo === "d" ? "disparador" : "condicion";
        console.log(`disp_${nombre_tipo}_${indice}`, criterio.dispositivo_id)
        setValue(`disp_${nombre_tipo}_${indice}`, criterio.dispositivo_id);
        setValue(`atr_${nombre_tipo}_${indice}`, criterio.atributo_id);
        setValue(`comp_${nombre_tipo}_${indice}`, criterio.comparador);
        setValue(`val_${nombre_tipo}_${indice}`, criterio.valor);
        if(criterio.tipo === "d"){
          index_d++;
        } else if (criterio.tipo === "c"){
          index_c++;
        }
    });
    
    // Iterar sobre las acciones
    Object.values(regla.acciones).forEach((accion, index) => {
        console.log("Accion",accion, index)
        const nombre_accion = accion.accion_id === 1 ? Acciones.Set : "";
        setValue(`disp_accion_${index}`, accion.dispositivo_id);
        setValue(`atr_accion_${index}`, accion.atributo_id);
        setValue(`accion_${index}`, nombre_accion);
        // Agregar un valor ficticio para 'valor_accion' si no existe
        setValue(`val_accion_${index}`, accion.valor_accion || '');
    });
    }
  }, [regla]);

  const onSubmit = async (data) => {
    const criterios = [];
    const acciones = [];

    // Transformar los datos de disparadores y condiciones
    Object.keys(data).forEach(key => {
        const match = key.match(/(disp|atr|comp|val)_(disparador|condicion)_(\d+)/);
        if (match) {
            const [_, field, tipo, index] = match;
            const criterioIndex = criterios.findIndex(criterio => criterio.index === index && criterio.tipo === tipo[0]);
            if (criterioIndex === -1) {
                criterios.push({
                    tipo: tipo === "disparador" ? "d" : "c",
                    [`${field === "disp" ? "dispositivo_id" : field === "atr" ? "atributo_id" : field === "comp" ? "comparador" : "valor"}`]: field === "val" ? Number(data[key]) : data[key],
                    index
                });
            } else {
                criterios[criterioIndex][`${field === "disp" ? "dispositivo_id" : field === "atr" ? "atributo_id" : field === "comp" ? "comparador" : "valor"}`] = field === "val" ? Number(data[key]) : data[key];
            }
        }
    });

    // Transformar los datos de acciones
    Object.keys(data).forEach(key => { //No cojo el valor de accion_id
      const match = key.match(/(disp|atr|accion|valor)_(accion)_(\d+)/);
      if (match) {
          const [_, field, tipo, index] = match;
          const accionIndex = acciones.findIndex(accion => accion.index === index);
          if (accionIndex === -1) {
              acciones.push({
                  [`${field === "disp" ? "dispositivo_id" : field === "atr" ? "atributo_id" : field === "accion" ? "accion_id" : "valor_accion"}`]: field === "valor" ? Number(data[key]) : field === "accion" ? Number(data[key]) : data[key],
                  index
              });
          } else {
              acciones[accionIndex][`${field === "disp" ? "dispositivo_id" : field === "atr" ? "atributo_id" : field === "accion" ? "accion_id" : "valor_accion"}`] = field === "valor" ? Number(data[key]) : field === "accion" ? Number(data[key]) : data[key];
          }
      }else{
        const partes = key.split("_");
        if(partes[0] === "accion"){
          const accionIndex = acciones.findIndex(accion => accion.index === partes[1]);
          if(accionIndex !== -1){
            if(data[key] === Acciones.Set){
              acciones[accionIndex]["accion_id"] = 1;
            }
          }
        } else if(partes[0] === "val"){
          const accionIndex = acciones.findIndex(accion => accion.index === partes[2]);
          if(accionIndex !== -1){
            acciones[accionIndex]["valor_accion"] = data[key];
          }
        }
      }
  });

    // Eliminar el campo "index" de los objetos en criterios y acciones
    criterios.forEach(criterio => {
        delete criterio.index;
    });
    acciones.forEach(accion => {
        delete accion.index;
    });

    // Crear el objeto transformado
    const objetoTransformado = {
        nombre: data.nombre,
        criterios,
        acciones
    };

    console.log(objetoTransformado);

    // Realizar la llamada a la API con el objeto transformado
    if (regla === null){
      await reglaService.createRegla(objetoTransformado);
    }

    // Redirigir o realizar otra acción tras el envío del formulario
    // navigate("/reglas");
};


  useEffect(() => {
    async function getDispositivos() {
      try {
        const respuesta = await dispositivoService.getDispositivos();
        setDispositivos(respuesta);
      } catch (error) {
        console.error("Error:", error);
      }
    }
    getDispositivos();
  }, []);

  const addDisparador = () => {
    setDisparadores([...disparadores, { id: Date.now() }]);
  };

  const removeDisparador = (id) => {
    setDisparadores(disparadores.filter(disparador => disparador.id !== id));
  };

  const addCondicion = () => {
    setCondiciones([...condiciones, { id: Date.now() }]);
  };

  const removeCondicion = (id) => {
    setCondiciones(condiciones.filter(condicion => condicion.id !== id));
  };

  const addAccion = () => {
    setAcciones([...acciones, { id: Date.now() }]);
  };

  const removeAccion = (id) => {
    setAcciones(acciones.filter(accion => accion.id !== id));
  };

  return (
    <Box className="formulario" sx={{ padding: 2, backgroundColor: theme.palette.background.paper, color: theme.palette.primary.text }}>
      <form onSubmit={handleSubmit(onSubmit)}>
        <Grid container spacing={2}>
          <Grid item xs={12}>
          <Typography variant="h5" gutterBottom>
              Regla
          </Typography>
          </Grid>
          <Grid item xs={12}>
            <Controller
              name="nombre"
              control={control}
              defaultValue={regla?.nombre || ''}
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
          <Typography variant="h6" gutterBottom>
              Disparadores
          </Typography>
          <Typography variant="body" gutterBottom>
              Elabora las condiciones que dispararán la regla. Puedes añadir tantos disparadores como necesites. Se relacionarán entre ellos con un or.
          </Typography>
          </Grid>
          {disparadores.map((disparador, index) => (
            <React.Fragment key={disparador.id}>
              <Grid item xs={12}>
                <Typography variant="h6" gutterBottom>
                    Disparador {index + 1}
                </Typography>
              </Grid>
              <Grid item xs={12} md={5.5} lg={2.75}>
                <Controller
                  name={`disp_disparador_${index}`}
                  control={control}
                  defaultValue={""}
                  rules={{ required: 'Este campo es requerido' }}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Dispositivo disparador"
                      select
                      fullWidth
                      error={!!errors[`disp_disparador_${index}`]}
                      helperText={errors[`disp_disparador_${index}`] && errors[`disp_disparador_${index}`].message}
                      onChange={(e) => {
                        setValue(`disp_disparador_${index}`, e.target.value);
                        setAtributos(dispositivos.find((dispositivo) => dispositivo.id === e.target.value)?.atributos || []);
                      }}
                    >
                      {dispositivos.map((dispositivo) => (
                        <MenuItem key={dispositivo.id} value={dispositivo.id}>
                          {dispositivo.nombre}
                        </MenuItem>
                      ))}
                    </TextField>
                  )}
                />
              </Grid>
              <Grid item xs={12} md={5.5} lg={2.75}>
                <Controller
                  name={`atr_disparador_${index}`}
                  control={control}
                  defaultValue={""}
                  rules={{ required: 'Este campo es requerido' }}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Atributo disparador"
                      select
                      fullWidth
                      error={!!errors[`atr_disparador_${index}`]}
                      helperText={errors[`atr_disparador_${index}`] && errors[`atr_disparador_${index}`].message}
                    >
                      {atributos.map((atributo) => (
                        <MenuItem key={atributo.id} value={atributo.id}>
                          {atributo.nombre_atributo}
                        </MenuItem>
                      ))}
                    </TextField>
                  )}
                />
              </Grid>
              <Grid item xs={12} md={5.5} lg={2.75}>
                <Controller
                  name={`comp_disparador_${index}`}
                  control={control}
                  defaultValue={""}
                  rules={{ required: 'Este campo es requerido' }}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Comparador disparador"
                      select
                      fullWidth
                      error={!!errors[`comp_disparador_${index}`]}
                      helperText={errors[`comp_disparador_${index}`] && errors[`comp_disparador_${index}`].message}
                    >
                      {Object.values(Comparadores).map((comparador) => (
                        <MenuItem key={comparador} value={comparador}>
                          {comparador}
                        </MenuItem>
                      ))}
                    </TextField>
                  )}
                />
              </Grid>
              <Grid item xs={12} md={5.5} lg={2.75}>
                <Controller
                  name={`val_disparador_${index}`}
                  control={control}
                  defaultValue={""}
                  rules={{ required: 'Este campo es requerido' }}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Valor disparador"
                      fullWidth
                      error={!!errors[`val_disparador_${index}`]}
                      helperText={errors[`val_disparador_${index}`] && errors[`val_disparador_${index}`].message}
                    />
                  )}
                />
              </Grid>
              <Grid item xs={1}>
                <IconButton onClick={() => removeDisparador(disparador.id)}>
                  <Close />
                </IconButton>
              </Grid>
            </React.Fragment>
          ))}

          <Grid item xs={12} md={5.5} lg={6}>
            <Button variant="contained" fullWidth onClick={addDisparador} startIcon={<Add />}>
              Añadir disparador
            </Button>
          </Grid>
          <Grid item xs={false} md={6.5} lg={6}/>

          <Grid item xs={12}>
          <Typography variant="h6" gutterBottom>
              Condiciones
          </Typography>
          <Typography variant="body" gutterBottom>
              Elabora las condiciones que complementarán a los disparadores. Puedes añadir tantas condiciones como necesites. Se relacionarán entre ellos con un or, y con los disparadores con un and.
          </Typography>
          </Grid>
          {condiciones.map((condicion, index) => (
            <React.Fragment key={condicion.id}>
              <Grid item xs={12}>
                <Typography variant="h6" gutterBottom>
                    Condición {index + 1}
                </Typography>
              </Grid>
              <Grid item xs={12} md={5.5} lg={2.75}>
                <Controller
                  name={`disp_condicion_${index}`}
                  control={control}
                  defaultValue={""}
                  rules={{ required: 'Este campo es requerido' }}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Dispositivo condición"
                      select
                      fullWidth
                      error={!!errors[`disp_condicion_${index}`]}
                      helperText={errors[`disp_condicion_${index}`] && errors[`disp_condicion_${index}`].message}
                      onChange={(e) => {
                        setValue(`disp_condicion_${index}`, e.target.value);
                        setAtributos(dispositivos.find((dispositivo) => dispositivo.id === e.target.value)?.atributos || []);
                        }}
                      >
                        {dispositivos.map((dispositivo) => (
                          <MenuItem key={dispositivo.id} value={dispositivo.id}>
                            {dispositivo.nombre}
                          </MenuItem>
                        ))}
                      </TextField>
                    )}
                  />
                </Grid>
                <Grid item xs={12} md={5.5} lg={2.75}>
                  <Controller
                    name={`atr_condicion_${index}`}
                    control={control}
                    defaultValue={""}
                    rules={{ required: 'Este campo es requerido' }}
                    render={({ field }) => (
                      <TextField
                        {...field}
                        label="Atributo condición"
                        select
                        fullWidth
                        error={!!errors[`atr_condicion_${index}`]}
                        helperText={errors[`atr_condicion_${index}`] && errors[`atr_condicion_${index}`].message}
                      >
                        {atributos.map((atributo) => (
                          <MenuItem key={atributo.id} value={atributo.id}>
                            {atributo.nombre_atributo}
                          </MenuItem>
                        ))}
                      </TextField>
                    )}
                  />
                </Grid>
                <Grid item xs={12} md={5.5} lg={2.75}>
                  <Controller
                    name={`comp_condicion_${index}`}
                    control={control}
                    defaultValue={""}
                    rules={{ required: 'Este campo es requerido' }}
                    render={({ field }) => (
                      <TextField
                        {...field}
                        label="Comparador condición"
                        select
                        fullWidth
                        error={!!errors[`comp_condicion_${index}`]}
                        helperText={errors[`comp_condicion_${index}`] && errors[`comp_condicion_${index}`].message}
                      >
                        {Object.values(Comparadores).map((comparador) => (
                          <MenuItem key={comparador} value={comparador}>
                            {comparador}
                          </MenuItem>
                        ))}
                      </TextField>
                    )}
                  />
                </Grid>
                <Grid item xs={12} md={5.5} lg={2.75}>
                  <Controller
                    name={`val_condicion_${index}`}
                    control={control}
                    defaultValue={""}
                    rules={{ required: 'Este campo es requerido' }}
                    render={({ field }) => (
                      <TextField
                        {...field}
                        label="Valor condición"
                        fullWidth
                        error={!!errors[`val_condicion_${index}`]}
                        helperText={errors[`val_condicion_${index}`] && errors[`val_condicion_${index}`].message}
                      />
                    )}
                  />
                </Grid>
                <Grid item xs={1}>
                  <IconButton onClick={() => removeCondicion(condicion.id)}>
                    <Close />
                  </IconButton>
                </Grid>
              </React.Fragment>
            ))}

            <Grid item xs={12} md={5.5} lg={6}>
              <Button variant="contained" fullWidth onClick={addCondicion} startIcon={<Add />}>
                Añadir condición
              </Button>
            </Grid>
            <Grid item xs={0} md={6.5} lg={6}/>

          <Grid item xs={12}>
          <Typography variant="h6" gutterBottom>
              Actuaciones
          </Typography>
          <Typography variant="body" gutterBottom>
              Elabora las actuaciones que se realizarán cuando se dispare la regla. Puedes añadir tantas actuaciones como necesites.
          </Typography>
          </Grid>

            {acciones.map((accion, index) => (
            <React.Fragment key={accion.id}>
              <Grid item xs={12}>
                <Typography variant="h6" gutterBottom>
                    Actuación {index + 1}
                </Typography>
              </Grid>
              <Grid item xs={12} md={5.5} lg={2.75}>
                <Controller
                  name={`disp_accion_${index}`}
                  control={control}
                  defaultValue={""}
                  rules={{ required: 'Este campo es requerido' }}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Dispositivo actuación"
                      select
                      fullWidth
                      error={!!errors[`disp_accion_${index}`]}
                      helperText={errors[`disp_accion_${index}`] && errors[`disp_accion_${index}`].message}
                      onChange={(e) => {
                        setValue(`disp_accion_${index}`, e.target.value);
                        setAtributos(dispositivos.find((dispositivo) => dispositivo.id === e.target.value)?.atributos || []);
                        }}
                      >
                        {dispositivos.map((dispositivo) => (
                          <MenuItem key={dispositivo.id} value={dispositivo.id}>
                            {dispositivo.nombre}
                          </MenuItem>
                        ))}
                      </TextField>
                    )}
                  />
                </Grid>
                <Grid item xs={12} md={5.5} lg={2.75}>
                  <Controller
                    name={`atr_accion_${index}`}
                    control={control}
                    defaultValue={""}
                    rules={{ required: 'Este campo es requerido' }}
                    render={({ field }) => (
                      <TextField
                        {...field}
                        label="Atributo actuación"
                        select
                        fullWidth
                        error={!!errors[`atr_accion_${index}`]}
                        helperText={errors[`atr_accion_${index}`] && errors[`atr_accion_${index}`].message}
                      >
                        {atributos.map((atributo) => (
                          <MenuItem key={atributo.id} value={atributo.id}>
                            {atributo.nombre_atributo}
                          </MenuItem>
                        ))}
                      </TextField>
                    )}
                  />
                </Grid>
                <Grid item xs={12} md={5.5} lg={2.75}>
                  <Controller
                    name={`accion_${index}`}
                    control={control}
                    defaultValue={""}
                    rules={{ required: 'Este campo es requerido' }}
                    render={({ field }) => (
                      <TextField
                        {...field}
                        label="Actuación"
                        select
                        fullWidth
                        error={!!errors[`accion_${index}`]}
                        helperText={errors[`accion_${index}`] && errors[`accion_${index}`].message}
                      >
                        {Object.values(Acciones).map((accion) => (
                          <MenuItem key={accion} value={accion}>
                            {accion}
                          </MenuItem>
                        ))}
                      </TextField>
                    )}
                  />
                </Grid>
                <Grid item xs={12} md={5.5} lg={2.75}>
                  <Controller
                    name={`val_accion_${index}`}
                    control={control}
                    defaultValue={""}
                    rules={{ required: 'Este campo es requerido' }}
                    render={({ field }) => (
                      <TextField
                        {...field}
                        label="Valor actuación"
                        fullWidth
                        error={!!errors[`val_accion_${index}`]}
                        helperText={errors[`val_accion_${index}`] && errors[`val_accion_${index}`].message}
                      />
                    )}
                  />
                </Grid>
                <Grid item xs={1}>
                  <IconButton onClick={() => removeAccion(accion.id)}>
                    <Close />
                  </IconButton>
                </Grid>
              </React.Fragment>
            ))}

            <Grid item xs={12} md={5.5} lg={6}>
              <Button variant="contained" fullWidth onClick={addAccion} startIcon={<Add />}>
                Añadir acción
              </Button>
            </Grid>
            <Grid item xs={12} md={6.5} lg={6}/>
            {/* SE ME MUEVE EL CANCELAR AL HACERLO PEQUEÑO. VER COMO COLOCAR */}
            <Grid item xs={6} md={5.5} lg={6}>
              <Button variant="contained" fullWidth onClick={onClose} endIcon={<Close />}>
                Cancelar
              </Button>
            </Grid>
            <Grid item xs={6} md={5.5} lg={6}>
              <Button type="submit" variant="contained" fullWidth endIcon={<ArrowForward />}>
                Guardar
              </Button>
            </Grid>
          </Grid>
        </form>
      </Box>
    );
  };

  export default FormularioRegla;
