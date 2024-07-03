// Formulario.js
import React, { useState, useEffect } from "react";
import { useForm, Controller, set } from "react-hook-form";
import { useNavigate, useLocation } from "react-router-dom";
import {
  Button,
  MenuItem,
  TextField,
  Box,
  Grid,
  Checkbox,
  Typography
} from "@mui/material";
import { ArrowForward, Close } from "@mui/icons-material";
import Editor from "./Editor";
import integracionService from "../../services/integracionService";
import { createIntegracionData, Atributo } from "../../resources/Interfaces/interfaces";
import { IconName } from "../../resources/enums/enums";
import { getIconComponent } from "../../utils/iconUtils";

// import { javascript } from '@codemirror/lang-javascript';
// import { act } from "react-dom/test-utils";

const FormularioIntegraciones = ({integracion = null, onClose, theme}) => {
  const {
    handleSubmit,
    setValue,
    control,
    formState: { errors },
  } = useForm();
  const [numAtributos, setNumAtributos] = useState(0);
  const [tipo, setTipo] = useState("Sensor");
  const [actuables, setActuables] = useState([]);
  const [codigo, setCodigo] = useState("");
  const [nombreOriginal, setNombreOriginal] = useState("");
  const [tipos, setTipos] = useState([]);

  const navigate = useNavigate();

  // const location = useLocation();
  // const { integracion } = location.state || {};

  useEffect(() => {
    getTipos();
    if (integracion) {
      console.log("Integración a editar:", integracion);
      setValue("nombre", integracion.nombre);
      setNombreOriginal(integracion.nombre);
      setValue("tipo", integracion.tipo);
      let actuador = false;
      let actuablesTemp = [];
      setValue("atributos", Object.entries(integracion.atributos).length);
      setValue("nombre_archivo", integracion.script);
      setNumAtributos(Object.entries(integracion.atributos).length);
      setTipo(integracion.tipo);
      const atributos = integracion.atributos;
      console.log('atributos',atributos)
      let i=0;
      Object.entries(atributos).forEach(([id, atributo]) => {
      // for (const [id, atributo] in Object.entries(atributos)) {
        console.log("atributo",id,atributo)
        console.log("atributo",atributo.nombre)
        setValue(`atributo_${i}`, atributo.nombre);
        setValue(`unidad_${i}`, atributo.unidades);
        setValue(`icono_${i}`, atributo.icono)
        setValue(`tipo_${i}`, atributo.tipo);
        setValue(`ls_${i}`, atributo.limite_superior);
        setValue(`li_${i}`, atributo.limite_inferior);
        if (atributo.actuable === "true") {
          actuador = true;
          console.log("actuables en el if",actuables)
          console.log("nombre atributo",atributo.nombre)
          actuablesTemp.push(i);
        }
        i++;
      });
      setActuables(actuablesTemp);
      console.log("Actuables",actuables)
      if (actuador) {
        setValue("tipo", "Actuador");
        setTipo("Actuador");
      }else{
        setValue("tipo", "Sensor");
        setTipo("Sensor");
      }
      setCodigo(integracion.codigo);
      setValue("codigo", integracion.codigo);
    }
  }, [integracion]);

  const getTipos = async () => {
    try {
      const response = await integracionService.getTipos();
      console.log("Tipos de integraciones:", response);
      setTipos(response);
    } catch (error) {
      console.error("Error:", error);
    }
  }

  // useEffect(() => {
  //   setCodigo('print("Hello, World!")');
  //   setValue("codigo", 'print("Hello, World!")');
  //   console.log(codigo)
  // }, []);

  useEffect(() => {
    console.log("codigo", codigo);
    setValue("codigo", codigo);
  }, [codigo]);

  // const onClose = () => {
  //   navigate("/config");
  // };

  const transformarObjeto = (entrada): createIntegracionData => {
    const atributos: Atributo[] = [];
    console.log("actuables", actuables)
    for (let i = 0; i < entrada.atributos; i++) {
        const atributo: Atributo = {
            nombre: entrada[`atributo_${i}`],
            unidades: entrada[`unidad_${i}`],
            actuable: actuables.includes(i) ? true : false,
            tipo: entrada[`tipo_${i}`],
        };
        console.log('Atributo.tipo',atributo.tipo)
        if (entrada[`icono_${i}`]) { atributo.icono = entrada[`icono_${i}`]; }
        if (entrada[`ls_${i}`]) { atributo.limite_superior = Number(entrada[`ls_${i}`]); }
        if (entrada[`li_${i}`]) { atributo.limite_inferior = Number(entrada[`li_${i}`]); }
        atributos.push(atributo);
    }

    const salida: createIntegracionData = {
        prev_nombre: nombreOriginal,
        nombre: entrada.nombre,
        nombre_script: entrada.nombre_archivo,
        script: entrada.codigo,
        tipo_dispositivo: entrada.tipo,
        atributos: atributos
    };

    return salida;
};
  const onSubmit = async (data) => {
    if (integracion === null){
    try{
      console.log('data:', data)
      const objetoTransformado = transformarObjeto(data);
      console.log("Objeto transformado:", objetoTransformado);
      const response = await integracionService.createIntegracion(objetoTransformado);
      console.log("Integración creada:", response);
      if(response.code === 200){
        alert("Integración creada exitosamente");
      }
      onClose();
    }catch(error){
      console.error("Error creando integración:", error);
      alert(error)
    }
    finally{
      //onClose();
    }
  }else{
    try{
      console.log('data:', data)
      const objetoTransformado = transformarObjeto(data);
      console.log("Objeto transformado:", objetoTransformado);
      const response = await integracionService.editIntegracion(objetoTransformado);
      console.log("Integración actualizada:", response);
      if(response.code === 200){
        alert("Integración actualizada exitosamente");
      }
      onClose();
    }catch(error){
      console.error("Error actualizando integración:", error);
      alert(error)
    }
    finally{
      //onClose();
    }
  }
};

  const handleAtributosChange = (e) => {
    const value = parseInt(e.target.value);
    setNumAtributos(value);
  };
  const handleTipoChange = (e) => {
    const value = e.target.value;
    if (tipo === "Actuador") {
      setActuables([]);
    }
    setTipo(value);
  };

  const handleCheckboxChange = (index) => {
    const updatedActuables = [...actuables];
    if (updatedActuables.includes(index)) {
      // Si el checkbox ya está marcado, lo desmarcamos y eliminamos su índice de actuables
      const indexToRemove = updatedActuables.indexOf(index);
      updatedActuables.splice(indexToRemove, 1);
    } else {
      // Si el checkbox no está marcado, lo marcamos y agregamos su índice a actuables
      updatedActuables.push(index);
    }
    setActuables(updatedActuables);
  };

  const onCodeMirrorChange = (value) => {
    console.log('codigo',codigo);
    console.log('value',value);
    setCodigo(value);
  };

  const iconOptions = Object.values(IconName).map((iconName) => ({
    value: iconName,
    label: (
      <Box sx={{ display: 'flex', alignItems: 'center' }}>
        <Box sx={{ marginRight: 1 }}>{getIconComponent(iconName)}</Box>
        <span>{iconName}</span>
      </Box>
    ),
  }));

  //   useEffect(() => {
  //     if (icono && nombre) {
  //       setValue('icono', icono);
  //       setValue('nombre', nombre);
  //     }
  //   }, [icono, nombre]);

  return (
      <Box className="formulario" sx={{ padding: 2, backgroundColor: theme.palette.background.paper, color: theme.palette.primary.text }}>
        <form onSubmit={handleSubmit(onSubmit)}>
          <Grid container spacing={5}>
          <Grid item xs={12}>
            <Typography variant="h5" gutterBottom>
                Integración
            </Typography>
          </Grid>
            <Grid item xs={6}>
              <Controller
                name="nombre"
                control={control}
                rules={{ required: "Este campo es requerido" }}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Nombre integración"
                    fullWidth
                    error={!!errors.nombre}
                    helperText={errors.nombre && errors.nombre.message}
                    sx={{ backgroundColor: theme.palette.background.default, borderRadius: '5px' }}
                    InputProps={{
                      sx: { color: theme.palette.primary.text }
                    }}
                    InputLabelProps={{
                      sx: { color: theme.palette.primary.text } // Cambia esto al color que desees para la etiqueta
                    }}
                  />
                )}
              />
            </Grid>
            <Grid item xs={6}>
              <Controller
                name="tipo"
                control={control}
                rules={{ required: "Este campo es requerido" }}
                render={({ field }) => (
                  <TextField
                    {...field}
                    select
                    label="Tipo de dispositivos de la integración"
                    fullWidth
                    error={!!errors.atributos}
                    helperText={errors.atributos && errors.atributos.message}
                    value={field.value || ""} // Ensure value is defined
                    onChange={(e) => {
                      field.onChange(e);
                      handleTipoChange(e); // Update numAtributos state
                    }}
                  >
                    {["Sensor", "Actuador"].map((option) => (
                      <MenuItem key={option} value={option}>
                        {option}
                      </MenuItem>
                    ))}
                  </TextField>
                )}
              />
            </Grid>
            <Grid item xs={6}>
              <Controller
                name="nombre_archivo"
                control={control}
                rules={{ required: "Este campo es requerido" }}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Nombre del archivo Python de la integración"
                    fullWidth
                    error={!!errors.nombre}
                    helperText={errors.nombre && errors.nombre.message}
                  />
                )}
              />
            </Grid>
            <Grid item xs={6}>
              <Controller
                name="atributos"
                control={control}
                rules={{ required: "Este campo es requerido" }}
                render={({ field }) => (
                  <TextField
                    {...field}
                    select
                    label="Numero de atributos de los dispositivos a integrar"
                    fullWidth
                    error={!!errors.atributos}
                    helperText={errors.atributos && errors.atributos.message}
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
              <>
                <Grid item xs={12}>
                  <Typography variant="h5" gutterBottom>
                    Atributo {index + 1}
                  </Typography>
                </Grid>
                <Grid item xs={tipo === "Sensor" ? 5 : 4} key={"atributo_"+index}>
                  <Controller
                    name={`atributo_${index}`}
                    control={control}
                    rules={{ required: "Este campo es requerido" }}
                    render={({ field }) => (
                      <TextField
                        {...field}
                        label={`Nombre atributo ${index + 1}`}
                        fullWidth
                        error={!!errors[`atributo_${index}`]}
                        helperText={
                          errors[`atributo_${index}`] &&
                          errors[`atributo_${index}`].message
                        }
                      />
                    )}
                  />
                </Grid>
                <Grid item xs={tipo === "Sensor" ? 5 : 4} key={"icono_"+index}>
                  <Controller
                    name={`icono_${index}`}
                    control={control}
                    rules={{
                      required: "Este campo es requerido",
                      maxLength: { message: "No puede tener más de 5 caracteres" },
                    }}
                    render={({ field }) => (
                      <TextField
                        {...field}
                        label={`Icono ${index + 1}`}
                        fullWidth
                        select
                        error={!!errors[`icono_${index}`]}
                        helperText={
                          errors[`icono_${index}`] &&
                          errors[`icono_${index}`].message
                        }
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
                <Grid item xs={tipo === "Sensor" ? 2 : 2} key={"unidad_"+index}>
                  <Controller
                    name={`unidad_${index}`}
                    control={control}
                    rules={{
                      required: "Este campo es requerido",
                      maxLength: { value: 5, message: "No puede tener más de 5 caracteres" },
                    }}
                    render={({ field }) => (
                      <TextField
                        {...field}
                        label={`Unidad ${index + 1}`}
                        fullWidth
                        error={!!errors[`unidad_${index}`]}
                        helperText={
                          errors[`unidad_${index}`] &&
                          errors[`unidad_${index}`].message
                        }
                      />
                    )}
                  />
                </Grid>
                {tipo === "Actuador" && (
                  <Grid item xs={2} container alignItems="center">
                    <Checkbox
                      id={`actuable${index}`}
                      name={`actuable_${index}`}
                      checked={actuables.includes(index)}
                      onChange={() => handleCheckboxChange(index)}
                    />
                    <label htmlFor={`actuable_${index}`}>Actuable</label>
                  </Grid>
                )}
                <Grid item xs={4} key={"tipo_"+index}>
                  <Controller
                    name={`tipo_${index}`}
                    control={control}
                    rules={{required: "Este campo es requerido"}}
                    render={({ field }) => (
                      <TextField
                        {...field}
                        select
                        label={`Tipo ${index + 1}`}
                        fullWidth
                        error={!!errors[`tipo_${index}`]}
                        helperText={
                          errors[`tipo_${index}`] &&
                          errors[`tipo_${index}`].message
                        }
                      >
                        {tipos.map((option) => (
                          <MenuItem key={option.id} value={option.nombre}>
                            {option.nombre}
                          </MenuItem>
                        ))}
                      </TextField>
                    )}
                  />
                </Grid>
                <Grid item xs={4} key={"li_"+index}>
                  <Controller
                    name={`li_${index}`}
                    control={control}
                    rules={{required: "Este campo es requerido"}}
                    render={({ field }) => (
                      <TextField
                        {...field}
                        label={`Límite inferior ${index + 1}`}
                        value={field.value || ""}
                        fullWidth
                        error={!!errors[`li_${index}`]}
                        helperText={
                          errors[`li_${index}`] &&
                          errors[`li_${index}`].message
                        }
                      />
                    )}
                  />
                </Grid>
                <Grid item xs={4} key={"ls_"+index}>
                  <Controller
                    name={`ls_${index}`}
                    control={control}
                    rules={{required: "Este campo es requerido"}}
                    render={({ field }) => (
                      <TextField
                        {...field}
                        label={`Límite superior ${index + 1}`}
                        value={field.value || ""}
                        fullWidth
                        error={!!errors[`ls_${index}`]}
                        helperText={
                          errors[`ls_${index}`] &&
                          errors[`ls_${index}`].message
                        }
                      />
                    )}
                  />
                </Grid>
                <Grid item xs={12}>
                  <Typography variant="body2" gutterBottom>
                    Los límites son variables opcionales que indican el rango de valores adecuados para el atributo.
                  </Typography>
                </Grid>
                {/* {actuables.includes(index) && tipo === "Actuador" && (
                  <>
                    <Grid item xs={5}>
                      <Controller
                        name={`topic_${index}`}
                        control={control}
                        rules={{ required: "Este campo es requerido" }}
                        render={({ field }) => (
                          <TextField
                            {...field}
                            label={`Topic de actuación ${index + 1}`}
                            fullWidth
                            error={!!errors[`topic_${index}`]}
                            helperText={
                              errors[`topic_${index}`] &&
                              errors[`topic_${index}`].message
                            }
                          />
                        )}
                      />
                    </Grid>
                    <Grid item xs={5}>
                      <Controller
                        name={`plantilla_${index}`}
                        control={control}
                        rules={{ required: "Este campo es requerido" }}
                        render={({ field }) => (
                          <TextField
                            {...field}
                            label={`Plantilla Jinja2 del mensaje ${index + 1}`}
                            fullWidth
                            error={!!errors[`plantilla_${index}`]}
                            helperText={
                              errors[`plantilla_${index}`] &&
                              errors[`plantilla_${index}`].message
                            }
                          />
                        )}
                      />
                    </Grid>
                  </>
                )} */}
              </>
            ))}
            <Grid item xs={12}>
              <Typography variant="h5" gutterBottom>
                Código de la integración
              </Typography>
            </Grid>
            <Grid item xs={12}>
              <Editor codigo={codigo} setCodigo={setCodigo}/>
            </Grid>
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
  );
};

export default FormularioIntegraciones;
