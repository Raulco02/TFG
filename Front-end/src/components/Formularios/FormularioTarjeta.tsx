import React, { useState, useEffect } from "react";
import { useForm, Controller } from "react-hook-form";
import {
  Button,
  MenuItem,
  TextField,
  Popover,
  Box,
  Grid,
  FormControlLabel,
  Checkbox,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
} from "@mui/material";
import { ArrowForward, Close } from "@mui/icons-material";
import { Tarjetas } from "../../resources/enums/enums";
import dispositivoService from "../../services/dispositivoService";
import grupoService from "../../services/grupoService";

const FormularioTarjeta = ({ onClose, submit, editingItem }) => {
  const {
    handleSubmit,
    control,
    setValue,
    getValues,
    formState: { errors },
  } = useForm();
  const [dispositivos, setDispositivos] = useState([]);
  const [atributos, setAtributos] = useState([]);
  const [dispositivosObj, setDispositivosObj] = useState({});
  const [atributosObj, setAtributosObj] = useState({});
  const [grupos, setGrupos] = useState([]);
  const [tipo, setTipo] = useState("");
  const [numAtributos, setNumAtributos] = useState(0);
  const [prevNumAtributos, setPrevNumAtributos] = useState(0);
  const [selectedDispositivos, setSelectedDispositivos] = useState([]);
  const [editando, setEditando] = useState(false);

  // useEffect(() => {
  //   if(typeof editingItem === 'object' && tipo === Tarjetas.Estado){
  //     console.log('Dispositivos en use effect', dispositivos)
  //     if(editingItem['id-dispositivo'].length === numAtributos){
  //       for (let i = 0; i < editingItem['id-dispositivo'].length; i++) {
  //         dispositivoChange(editingItem['nombre-dispositivo'][i], i);
  //       }
  //     }
  //   }
  // }, [numAtributos]);

  useEffect(() => {
    console.log("Editing item:", editingItem);
    console.log("Editing:", typeof editingItem !== "object" ? false : true);
    setEditando(typeof editingItem !== "object" ? false : true);
  }, [editingItem]);
  //DAR VALORES SI SE ESTA EDITANDO
  useEffect(() => {
    console.log("editando", editando);
    if (editando && editingItem !== null) {
      setValue("tipo", editingItem.tipo);
      setTipo(editingItem.tipo);
      if (editingItem.tipo === Tarjetas.Texto) {
        setValue("contenido", editingItem.contenido);
      }
      if (editingItem.tipo === Tarjetas.Imagen) {
        setValue("imagen", editingItem.imagen);
      }

      if (editingItem.tipo === Tarjetas.Estado) {
        if (typeof editingItem["id-dispositivo"] !== "object") {
          setValue("atributos", 1);
          setNumAtributos(1);
        } else {
          setValue("atributos", editingItem["id-dispositivo"].length);
          setNumAtributos(editingItem["id-dispositivo"].length);
        }
        //Hacer otro useEffect con dispositivos o numAtributos de dependencia creo
      }

      if (editingItem.tipo === Tarjetas.Termostato) {
        console.log("En el if");
        setValue("dispositivo", editingItem["nombre-dispositivo"]);
        getDispositivosTemperatura();
        // setValue('atributo', editingItem['nombre-atributo']) //UseEffect, esperar a que tenga atributos cargados y entonces si
      }
      if (editingItem.tipo === Tarjetas.Grafico) {
        console.log("En el if");
        getAtributos();
      }
      if (editingItem.tipo === Tarjetas.Estado) {
        console.log("En el if");
        getDispositivos();
      }
      if (editingItem.tipo === Tarjetas.Termostato) {
        console.log("En el if");
        getDispositivosTemperatura();
      }
      if (editingItem.tipo === Tarjetas.Grafico) {
        console.log("En el if");
        getAtributos();
      }
      if (editingItem.tipo === Tarjetas.Grupo) {
        console.log("En el if");
        getGrupos();
      }
    }
  }, [editingItem, editando]);

  useEffect(() => {
    if (tipo === Tarjetas.Termostato && typeof editingItem === "object") {
      dispositivoChange(getValues("dispositivo"), 0);
    } else if (tipo === Tarjetas.Estado && typeof editingItem === "object") {
      for (let i = 0; i < numAtributos; i++) {
        // setValue(`id_dispositivo${i}`, editingItem['id-dispositivo'][i]);
        setValue(`dispositivo_${i}`, editingItem["nombre-dispositivo"][i]);
        dispositivoChange(editingItem["nombre-dispositivo"][i], i);
      }
    }
  }, [dispositivos]);

  useEffect(() => {
    if (tipo === Tarjetas.Estado && editando && typeof editingItem === "object" && editingItem && !(editingItem.nativeEvent instanceof Event)) {
      console.log("Atributos:", atributosObj);
      console.log("Dispositivos:", dispositivosObj);
      console.log("Editing item:", editingItem);
      for (let i = 0; i < numAtributos; i++) {
        setValue(`id_atributo${i}`, editingItem["id-atributo"][i]);
        setValue(`atributo_${i}`, editingItem["nombre-atributo"][i]);
      }
    }
  }, [dispositivosObj]);

  useEffect(() => {
    if (tipo === Tarjetas.Termostato && typeof editingItem === "object") {
      setValue("atributo", editingItem["nombre-atributo"]);
      setValue("id_atributo", editingItem["id-atributo"]);
    }
  }, [atributos]);

  useEffect(() => {}, [tipo]);

  useEffect(() => {
    if(editando){
      const newDispositivosObj = { ...dispositivosObj };
      const newAtributosObj = { ...atributosObj };
      if (numAtributos > prevNumAtributos) {
        for (let i = prevNumAtributos; i < numAtributos; i++) {
          newDispositivosObj[`dispositivo_${i}`] = "";
          newAtributosObj[`atributo_${i}`] = "";
        }
      } else if (numAtributos < prevNumAtributos) {
        for (let i = 0; i < numAtributos; i++) {
          if (newDispositivosObj[`dispositivo_${i}`] !== undefined)
            delete newDispositivosObj[`dispositivo_${i}`];
          if (newAtributosObj[`atributo_${i}`] !== undefined)
            delete newAtributosObj[`atributo_${i}`];
        }
      }

      setDispositivosObj(newDispositivosObj);
      setAtributosObj(newAtributosObj);
    }
  }, [numAtributos]);

  useEffect(() => {
    console.log("Selected Dispositivos:", selectedDispositivos);
    setValue("dispositivos", selectedDispositivos);
  }, [selectedDispositivos]);

  const onSubmit = submit;

  const tiempo_grafico = ["24h", "7d", "30d", "90d", "365d"];
  const tipo_grafico = ["Lineal", "Barra", "Circular"];

  const handleTipoChange = (event) => {
    setValue("tipo", event.target.value);
    setTipo(event.target.value);
    console.log(event.target.value);
    if (event.target.value === Tarjetas.Estado) {
      console.log("En el if");
      getDispositivos();
    }
    if (event.target.value === Tarjetas.Termostato) {
      console.log("En el if");
      getDispositivosTemperatura();
    }
    if (event.target.value === Tarjetas.Grafico) {
      console.log("En el if");
      getAtributos();
    }
    if (event.target.value === Tarjetas.Grupo) {
      console.log("En el if");
      getGrupos();
    }
  };

  const handleImagenChange = (event) => {
    setValue("imagen", event.target.files[0].name);
  };

  const handleDispositivoChange = (event, index) => {
    dispositivoChange(event.target.value, index);
  };

  const dispositivoChange = (nombre_dispositivo, index) => {
    console.log("Handle dispositivo activado", nombre_dispositivo);
    const selectedDispositivo = dispositivos.find(
      (dispositivo) => dispositivo.nombre === nombre_dispositivo
    );
    console.log("Dispositivos:", dispositivos);
    console.log(
      "Selected Dispositivo en dispositivo change:",
      selectedDispositivo
    );
    if (selectedDispositivo) {
      if (tipo !== Tarjetas.Termostato) {
        console.log("id dispositivo:", selectedDispositivo.id);
        setValue(`id_dispositivo${index}`, selectedDispositivo?.id);
        setDispositivosObj((prevDispositivosObj) => {
          const updatedDispositivosObj = {
            ...prevDispositivosObj,
            [`dispositivo_${index}`]: selectedDispositivo.id,
          };
          console.log("Updated dispositivosObj:", updatedDispositivosObj);
          return updatedDispositivosObj;
        });
        setAtributosObj((prevAtributosObj) => {
          const updatedAtributosObj = {
            ...prevAtributosObj,
            [`atributo_${index}`]: selectedDispositivo.atributos.map(
              (atributo) => ({
                id: atributo.id,
                nombre_atributo: atributo.nombre_atributo,
              })
            ),
          };
          console.log("Updated atributosObj:", updatedAtributosObj);
          return updatedAtributosObj;
        });
      } else {
        console.log("Dispositivo selected", selectedDispositivo);
        setValue("id_dispositivo", selectedDispositivo.id);
        const listaAtributos = selectedDispositivo.atributos.map(
          (atributo) => ({
            id: atributo.id,
            nombre_atributo: atributo.nombre_atributo,
          })
        );
        console.log("Dispositivo selected atributos", listaAtributos);
        setAtributos(listaAtributos);
      }
      console.log("Dispositivo selected", selectedDispositivo);
      console.log("DispositivosObj", dispositivosObj);
      console.log("AtributosObj", atributosObj);
    }
  };

  const handleAtributoChange = (event, index) => {
    console.log("Atributos", atributosObj);
    console.log("Event", event.target.value);
    if (tipo !== Tarjetas.Termostato) {
      const selectedAtributo = atributosObj[`atributo_${index}`].find(
        (atributo) => atributo.nombre_atributo === event.target.value
      );
      console.log("Atributo:", selectedAtributo);
      if (selectedAtributo)
        setValue(`id_atributo${index}`, selectedAtributo.id);
    } else {
      const selectedAtributo = atributos.find(
        (atributo) => atributo.nombre_atributo === event.target.value
      );
      if (selectedAtributo) setValue("id_atributo", selectedAtributo.id);
    }
  };

  const handleAtributosChange = (e) => {
    const value = parseInt(e.target.value);
    console.log("Atributos:", value);
    setPrevNumAtributos(numAtributos);
    setValue("atributos", value);
    setNumAtributos(value);
  };

  const handleAtributoGraficoChange = (e) => {
    const { id, nombre } = JSON.parse(e.target.value);
    setValue("atributo_grafico", JSON.stringify({ id, nombre }));
    setValue("id_atributo", id);
    getDispositivosAtributo(id);
  };

  const handleCheckboxChange = (event, dispositivoId) => {
    if (event.target.checked) {
      setSelectedDispositivos([...selectedDispositivos, dispositivoId]);
    } else {
      setSelectedDispositivos(
        selectedDispositivos.filter((id) => id !== dispositivoId)
      );
    }
  };

  async function getDispositivos() {
    try {
      const dispositivos = await dispositivoService.getDispositivos();
      setDispositivos(dispositivos);
      console.log("Dispositivos:", dispositivos);
    } catch (error) {
      console.error("Error fetching devices:", error);
    }
  }

  async function getDispositivosTemperatura() {
    try {
      const dispositivos =
        await dispositivoService.getDispositivosTemperatura();
      setDispositivos(dispositivos);
      console.log("Dispositivos:", dispositivos);
    } catch (error) {
      console.error("Error fetching devices:", error);
    }
  }

  async function getAtributos() {
    try {
      const atributos = await dispositivoService.getAllAtributos();
      setAtributos(atributos);
      console.log("Atributos:", atributos);
      console.log("AtributosObj:", atributosObj);
    } catch (error) {
      console.error("Error fetching devices:", error);
    }
  }

  async function getDispositivosAtributo(id) {
    try {
      const dispositivos = await dispositivoService.getDispositivosAtributo(id);
      setDispositivos(dispositivos);
      console.log("Dispositivos:", dispositivos);
    } catch (error) {
      console.error("Error fetching attributes:", error);
    }
  }

  async function getGrupos() {
    try {
      const grupos = await grupoService.getGrupos();
      setGrupos(grupos);
      console.log("Grupos:", grupos);
    } catch (error) {
      console.error("Error fetching groups:", error);
    }
  }

  return (
    <Popover
      open={true}
      anchorEl={document.body}
      anchorOrigin={{ vertical: "center", horizontal: "center" }}
      transformOrigin={{ vertical: "center", horizontal: "center" }}
    >
      <Box sx={{ padding: 2 }}>
        <form onSubmit={handleSubmit(onSubmit)}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <Controller
                name="tipo"
                control={control}
                defaultValue=""
                render={({ field }) => (
                  <TextField
                    {...field}
                    select
                    label="Tipo"
                    fullWidth
                    onChange={handleTipoChange}
                  >
                    {Object.values(Tarjetas).map((tarjeta) => (
                      <MenuItem key={tarjeta} value={tarjeta}>
                        {tarjeta}
                      </MenuItem>
                    ))}
                  </TextField>
                )}
              />
            </Grid>
            {getValues("tipo") === Tarjetas.Texto && (
              <Grid item xs={12}>
                <Controller
                  name="contenido"
                  control={control}
                  defaultValue=""
                  render={({ field }) => (
                    <TextField {...field} label="Contenido" fullWidth />
                  )}
                />
              </Grid>
            )}
            {getValues("tipo") === Tarjetas.Imagen && (
              <Grid item xs={12}>
                {/* Agregar el campo para subir imágenes */}
                <Controller
                  name="image"
                  control={control}
                  defaultValue=""
                  render={({ field }) => (
                    <>
                      <input
                        {...field}
                        type="file"
                        accept="image/*"
                        onChange={handleImagenChange}
                      />
                    </>
                  )}
                />
              </Grid>
            )}
            {/* Termostato igual tendría que mantenerse solo con un atributo, ir a GitHub */}
            {getValues("tipo") === Tarjetas.Estado && (
              <>
                <Grid item xs={12}>
                  <Controller
                    name="atributos"
                    control={control}
                    rules={{ required: "Este campo es requerido" }}
                    render={({ field }) => (
                      <TextField
                        {...field}
                        select
                        label="Numero de atributos a controlar"
                        fullWidth
                        error={!!errors.atributos}
                        helperText={
                          errors.atributos && errors.atributos.message
                        }
                        value={field.value || ""} // Ensure value is defined
                        onChange={(e) => {
                          field.onChange(e);
                          handleAtributosChange(e); // Update numAtributos state
                        }}
                      >
                        {[1, 2, 3, 4, 5, 6, 7, 8, 9].map((option) => (
                          <MenuItem key={option} value={option}>
                            {option}
                          </MenuItem>
                        ))}
                      </TextField>
                    )}
                  />
                </Grid>
                {[...Array(numAtributos)].map((_, index) => (
                  <React.Fragment key={index}>
                    <Grid item xs={6}>
                      {/* Agregar dropdown para dispositivos */}
                      <Controller
                        name={`dispositivo_${index}`}
                        control={control}
                        defaultValue=""
                        render={({ field }) => (
                          <TextField
                            {...field}
                            select
                            label={`Dispositivo ${index + 1}`}
                            fullWidth
                            onChange={(e) => {
                              field.onChange(e);
                              handleDispositivoChange(e, index);
                            }}
                          >
                            {dispositivos.map((dispositivo) => (
                              <MenuItem
                                key={dispositivo.id}
                                value={dispositivo.nombre}
                              >
                                {dispositivo.nombre}
                              </MenuItem>
                            ))}
                          </TextField>
                        )}
                      />
                    </Grid>
                    <Grid item xs={6}>
                      {/* Agregar dropdown para atributos */}
                      <Controller
                        name={`atributo_${index}`}
                        control={control}
                        defaultValue=""
                        render={({ field }) => (
                          <TextField
                            {...field}
                            select
                            label={`Atributo ${index + 1}`}
                            fullWidth
                            onChange={(e) => {
                              field.onChange(e);
                              handleAtributoChange(e, index);
                            }}
                          >
                            {(atributosObj[`atributo_${index}`] || []).map(
                              (atributo) => (
                                <MenuItem
                                  key={atributo.id}
                                  value={atributo.nombre_atributo}
                                >
                                  {atributo.nombre_atributo}
                                </MenuItem>
                              )
                            )}
                          </TextField>
                        )}
                      />
                    </Grid>
                  </React.Fragment>
                ))}
              </>
            )}
            {getValues("tipo") === Tarjetas.Termostato && (
              <>
                <Grid item xs={6}>
                  {/* Agregar dropdown para dispositivos */}
                  <Controller
                    name="dispositivo"
                    control={control}
                    defaultValue=""
                    render={({ field }) => (
                      <TextField
                        {...field}
                        select
                        label="Dispositivo"
                        fullWidth
                        onChange={(e) => {
                          field.onChange(e);
                          handleDispositivoChange(e);
                        }}
                      >
                        {dispositivos.map((dispositivo) => (
                          <MenuItem
                            key={dispositivo.id}
                            value={dispositivo.nombre}
                          >
                            {dispositivo.nombre}
                          </MenuItem>
                        ))}
                      </TextField>
                    )}
                  />
                </Grid>
                <Grid item xs={6}>
                  {/* Agregar dropdown para atributos */}
                  <Controller
                    name="atributo"
                    control={control}
                    defaultValue=""
                    render={({ field }) => (
                      <TextField
                        {...field}
                        select
                        label="Atributo"
                        fullWidth
                        onChange={(e) => {
                          field.onChange(e);
                          handleAtributoChange(e);
                        }}
                      >
                        {atributos.map((atributo) => (
                          <MenuItem
                            key={atributo.id}
                            value={atributo.nombre_atributo}
                          >
                            {atributo.nombre_atributo}
                          </MenuItem>
                        ))}
                      </TextField>
                    )}
                  />
                </Grid>
              </>
            )}
            {getValues("tipo") === Tarjetas.Grupo && (
              <Grid item xs={12}>
                {/* Agregar dropdown para grupos */}
                <Controller
                  name="grupo"
                  control={control}
                  defaultValue=""
                  render={({ field }) => (
                    <TextField 
                      {...field}
                      select 
                      label="Grupo" 
                      fullWidth
                      onChange={(e) => {
                        field.onChange(e);
                        console.log("Grupo seleccionado",e.target.value)
                        setValue("id_grupo", e.target.value);
                      }}
                      >
                      {grupos.map((grupo) => (
                        <MenuItem key={grupo.id} value={grupo.id}>
                          {grupo.nombre}
                        </MenuItem>
                      ))}
                    </TextField>
                  )}
                />
              </Grid>
            )}
            {getValues("tipo") === Tarjetas.Grafico && (
              <>
                <Grid item xs={4}>
                  {/* Agregar dropdown para tiempo */}
                  <Controller
                    name="tiempoGrafico"
                    control={control}
                    defaultValue=""
                    render={({ field }) => (
                      <TextField {...field} select label="Tiempo" fullWidth>
                        {tiempo_grafico.map((tiempo) => (
                          <MenuItem key={tiempo} value={tiempo}>
                            {tiempo}
                          </MenuItem>
                        ))}
                      </TextField>
                    )}
                  />
                </Grid>
                <Grid item xs={4}>
                  {/* Agregar dropdown para tipo de gráfico */}
                  <Controller
                    name="tipoGrafico"
                    control={control}
                    defaultValue=""
                    render={({ field }) => (
                      <TextField
                        {...field}
                        select
                        label="Tipo de Gráfico"
                        fullWidth
                      >
                        {tipo_grafico.map((tipo) => (
                          <MenuItem key={tipo} value={tipo}>
                            {tipo}
                          </MenuItem>
                        ))}
                      </TextField>
                    )}
                  />
                </Grid>
                <Grid item xs={4}>
                  {/* Agregar dropdown para atributo */}
                  <Controller
                    name="atributo_grafico"
                    control={control}
                    defaultValue=""
                    render={({ field }) => (
                      <TextField
                        {...field}
                        select
                        label="Atributo a controlar"
                        onChange={handleAtributoGraficoChange}
                        fullWidth
                      >
                        {atributos.map((atributo) => (
                          <MenuItem
                            key={atributo.id}
                            value={JSON.stringify({
                              id: atributo.id,
                              nombre: atributo.nombre,
                            })}
                          >
                            {atributo.nombre}
                          </MenuItem>
                        ))}
                      </TextField>
                    )}
                  />
                </Grid>
                {/* Mostrar lista de dispositivos con checkboxes */}
                <Grid item xs={12}>
                  <List>
                    {dispositivos.map((dispositivo) => (
                      <ListItem
                        key={dispositivo.id}
                        dense
                        button
                        onClick={() =>
                          handleCheckboxChange(
                            {
                              target: {
                                checked: !selectedDispositivos.includes(
                                  dispositivo.id
                                ),
                              },
                            },
                            dispositivo.id
                          )
                        }
                      >
                        <ListItemIcon>
                          <Checkbox
                            edge="start"
                            checked={selectedDispositivos.includes(
                              dispositivo.id
                            )}
                            tabIndex={-1}
                            disableRipple
                          />
                        </ListItemIcon>
                        <ListItemText primary={dispositivo.nombre} />
                      </ListItem>
                    ))}
                  </List>
                </Grid>
              </>
            )}
            <Grid item xs={6}>
              <Button
                variant="contained"
                fullWidth
                onClick={onClose}
                endIcon={<Close />}
              >
                Cancelar
              </Button>
            </Grid>
            <Grid item xs={6}>
              <Button
                type="submit"
                variant="contained"
                fullWidth
                endIcon={<ArrowForward />}
              >
                Guardar
              </Button>
            </Grid>
          </Grid>
        </form>
      </Box>
    </Popover>
  );
};

export default FormularioTarjeta;
