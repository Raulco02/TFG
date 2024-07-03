import React, { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { useForm, Controller } from "react-hook-form";
import { Button, MenuItem, TextField, Box, Grid } from "@mui/material";
import { ArrowForward, Close } from "@mui/icons-material";
import integracionService from "../../services/integracionService";
import dispositivoService from "../../services/dispositivoService";

const FormularioDispositivo = ({ dispositivo=null, onClose, theme }) => {
  const {
    handleSubmit,
    setValue,
    getValues,
    control,
    formState: { errors },
  } = useForm();
  const [integraciones, setIntegraciones] = useState([]);
  const [selectedIntegracion, setSelectedIntegracion] = useState(null);
  const [atributosActuables, setAtributosActuables] = useState([]);
  const [prev_id, setPrev_id] = useState("");

  const navigate = useNavigate();
  const location = useLocation();
  // const { dispositivo } = location.state || {};

  useEffect(() => {
    async function fetchIntegraciones() {
      try {
        const respuesta = await integracionService.getIntegraciones();
        setIntegraciones(respuesta);
        console.log("Integraciones fetched:", respuesta);

        if (dispositivo) {
          console.log("Dispositivo:", dispositivo);
          setValue("id", dispositivo.id);
          setPrev_id(dispositivo.id);
          setValue("nombre", dispositivo.nombre);
          setValue("topic", dispositivo.topic);
          setValue("ubicacion", dispositivo.ubicacion);

          const selectedIntegracion = respuesta.find(
            (integracion) => integracion.nombre === dispositivo.integracion
          );
          if (selectedIntegracion) {
            console.log('selectedIntegracion:', selectedIntegracion);
            setSelectedIntegracion(selectedIntegracion);
            setValue("integraciones", selectedIntegracion.id);
            console.log('integraciones:', getValues("integraciones"));
            //setAtributosActuables(
              const atributosActuablesIntegracion = selectedIntegracion.atributos.filter((item) => item.actuable === "true")
            //);
            console.log(dispositivo.atributos);
// Filtrar los atributos del dispositivo que coincidan con los atributos actuables de la integración
          const atributosActuablesDispositivo = atributosActuablesIntegracion.map((atributoIntegracion) => {
            const idIntegracion = parseInt(atributoIntegracion.id); // Convertir el ID de cadena a número
            return dispositivo.atributos[idIntegracion]//dispositivo.atributos.find((atributoDispositivo) => atributoDispositivo.id === idIntegracion);
          }).filter(Boolean);

          console.log('atributosActuablesIntegracion:', atributosActuablesIntegracion);
          console.log('atributosActuablesDispositivo:', atributosActuablesDispositivo);
          // Establecer los atributos actuables del dispositivo
          setAtributosActuables(atributosActuablesDispositivo);
            if(atributosActuablesDispositivo.length !== 0){
              for (let i = 0; i < atributosActuablesDispositivo.length; i++) {
                setValue(`topic_${atributosActuablesDispositivo[i].nombre}`, atributosActuablesDispositivo[i]['topic-actuacion']);
                setValue(`plantilla_${atributosActuablesDispositivo[i].nombre}`, atributosActuablesDispositivo[i].plantilla);
              }
            }
            console.log('atributosActuables:', atributosActuables);
          }
        }
      } catch (error) {
        console.error("Error fetching integraciones:", error);
      }
    }

    fetchIntegraciones();
  }, [dispositivo, setValue]);

  const transformarObjeto = (data) => {
    let topics_actuacion = [];
    let plantillas_actuacion = [];

    if (atributosActuables.length !== 0) {
      atributosActuables.forEach((atributo) => {
        const topicKey = `topic_${atributo.nombre}`;
        const plantillaKey = `plantilla_${atributo.nombre}`;

        if (data[topicKey]) {
          topics_actuacion.push(data[topicKey]);
        }

        if (data[plantillaKey]) {
          plantillas_actuacion.push(data[plantillaKey]);
        }
      });
    }

    const objetoTransformado = {
      prev_id: prev_id,
      id: data.id,
      nombre: data.nombre,
      nombre_integracion: selectedIntegracion ? selectedIntegracion.nombre : "",
      topic: data.topic,
      ubicacion: data.ubicacion,
      topics_actuacion: topics_actuacion,
      plantillas_actuacion: plantillas_actuacion,
    };

    return objetoTransformado;
  };

  const onSubmit = async (data) => {
    if(dispositivo === null){
      try {
        console.log("data:", data);
        const objetoTransformado = transformarObjeto(data);
        console.log("Objeto transformado:", objetoTransformado);
        const response = await dispositivoService.createDispositivo(
          objetoTransformado
        );
        console.log("Integración creada:", response);
        onClose();
      } catch (error) {
        console.error("Error creando integración:", error);
      } finally {
        // onClose();
      }
    }else{
      try {
        console.log("data:", data);
        const objetoTransformado = transformarObjeto(data);
        console.log("Objeto transformado:", objetoTransformado);
        const response = await dispositivoService.editDispositivo(
          objetoTransformado
        );
        console.log("Integración editada:", response);
        onClose();
      } catch (error) {
        console.error("Error editando integración:", error);
      } finally {
        // onClose();
      }
    }

  };

  // const onClose = () => {
  //   navigate("/dispositivos");
  // };

  return (
    <Box className="formulario" sx={{ padding: 2, backgroundColor: theme.palette.background.paper, color: theme.palette.primary.text }}>
      <form onSubmit={handleSubmit(onSubmit)}>
        <Grid container spacing={5}>
          <Grid item xs={6}>
            <Controller
              name="id"
              control={control}
              defaultValue={dispositivo ? dispositivo.id : ""}
              rules={{ required: "Este campo es requerido" }}
              render={({ field }) => (
                <TextField
                  {...field}
                  label="ID Dispositivo"
                  fullWidth
                  error={!!errors.id}
                  helperText={errors.id && errors.id.message}
                />
              )}
            />
          </Grid>
          <Grid item xs={6}>
            <Controller
              name="nombre"
              control={control}
              defaultValue={dispositivo ? dispositivo.nombre : ""}
              rules={{ required: "Este campo es requerido" }}
              render={({ field }) => (
                <TextField
                  {...field}
                  label="Nombre dispositivo"
                  fullWidth
                  error={!!errors.nombre}
                  helperText={errors.nombre && errors.nombre.message}
                />
              )}
            />
          </Grid>
          <Grid item xs={4}>
            <Controller
              name="integraciones"
              control={control}
              rules={{ required: "Este campo es requerido" }}
              defaultValue={selectedIntegracion ? selectedIntegracion.id : ""}
              render={({ field }) => (
                <TextField
                  {...field}
                  select
                  label="Integración a la que pertenece el dispositivo"
                  fullWidth
                  onChange={(e) => {
                    const selectedIntegracion = integraciones.find(
                      (integracion) => integracion.id === e.target.value
                    );
                    setSelectedIntegracion(selectedIntegracion);
                    setValue("integraciones", e.target.value);
                    setAtributosActuables(
                      selectedIntegracion.atributos.filter(
                        (item) => item.actuable === "true"
                      )
                    );
                    console.log('selectedIntegracion:', selectedIntegracion);
                  }}
                  error={!!errors.integraciones}
                  helperText={errors.integraciones && errors.integraciones.message}
                >
                  {integraciones.map((integracion) => (
                    <MenuItem key={integracion.id} value={integracion.id}>
                      {integracion.nombre}
                    </MenuItem>
                  ))}
                </TextField>
              )}
            />
          </Grid>
          <Grid item xs={4}>
            <Controller
              name="ubicacion"
              control={control}
              defaultValue={dispositivo ? dispositivo.ubicacion : ""}
              rules={{ required: "Este campo es requerido" }}
              render={({ field }) => (
                <TextField
                  {...field}
                  label="Ubicación del dispositivo"
                  fullWidth
                  error={!!errors.topic}
                  helperText={errors.topic && errors.topic.message}
                />
              )}
            />
          </Grid>
          <Grid item xs={4}>
            <Controller
              name="topic"
              control={control}
              defaultValue={dispositivo ? dispositivo.topic : ""}
              rules={{ required: "Este campo es requerido" }}
              render={({ field }) => (
                <TextField
                  {...field}
                  label="Topic MQTT de publicación de los datos"
                  fullWidth
                  error={!!errors.topic}
                  helperText={errors.topic && errors.topic.message}
                />
              )}
            />
          </Grid>
          {atributosActuables.length !== 0 &&
            atributosActuables.map((atributo) => (
              <React.Fragment key={atributo.id}>
                <Grid item xs={6}>
                  <Controller
                    name={`topic_${atributo.nombre}`}
                    control={control}
                    rules={{ required: "Este campo es requerido" }}
                    render={({ field }) => (
                      <TextField
                        {...field}
                        label={`Topic de actuación ${atributo.nombre}`}
                        fullWidth
                        error={!!errors[`topic_${atributo.nombre}`]}
                        helperText={
                          errors[`topic_${atributo.nombre}`] &&
                          errors[`topic_${atributo.nombre}`].message
                        }
                      />
                    )}
                  />
                </Grid>
                <Grid item xs={6}>
                  <Controller
                    name={`plantilla_${atributo.nombre}`}
                    control={control}
                    rules={{ required: "Este campo es requerido" }}
                    render={({ field }) => (
                      <TextField
                        {...field}
                        label={`Plantilla Jinja2 del mensaje ${atributo.nombre}`}
                        fullWidth
                        error={!!errors[`plantilla_${atributo.nombre}`]}
                        helperText={
                          errors[`plantilla_${atributo.nombre}`] &&
                          errors[`plantilla_${atributo.nombre}`].message
                        }
                      />
                    )}
                  />
                </Grid>
              </React.Fragment>
            ))}
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

export default FormularioDispositivo;

// // Formulario.js
// import React, { useState, useEffect } from "react";
// import { useNavigate, useLocation } from "react-router-dom";
// import { useForm, Controller, set, get } from "react-hook-form";
// import {
//   Button,
//   MenuItem,
//   TextField,
//   Popover,
//   Box,
//   Grid,
//   Checkbox,
// } from "@mui/material";
// import { ArrowForward, CheckBox, Close } from "@mui/icons-material";
// import { getIconComponent } from "../../utils/iconUtils";
// import { IconName } from "../../resources/enums/enums";
// import integracionService from "../../services/integracionService";
// import dispositivoService from "../../services/dispositivoService";

// const FormularioDispositivo = () => {
//   const {
//     handleSubmit,
//     setValue,
//     getValues,
//     control,
//     formState: { errors },
//   } = useForm();
//   const [numAtributos, setNumAtributos] = useState(0);
//   const [integraciones, setIntegraciones] = useState([]);
//   const [selectedIntegracion, setSelectedIntegracion] = useState({
//     id: "",
//     nombre: "",
//     atributos: [],
//   });
//   const [atributosActuables, setAtributosActuables] = useState([]);

//   const navigate = useNavigate();

//   const location = useLocation();
//   const { dispositivo } = location.state || {};

//   useEffect(() => {
//     if (dispositivo) {
//       console.log("Dispositivo:", dispositivo);
//       setValue("id", dispositivo.id);
//       setValue("nombre", dispositivo.nombre);
//       //setValue("integraciones", dispositivo.integracion);
//       setValue("topic", dispositivo.topic);
//       // setSelectedIntegracion({
//       //   id: dispositivo.integracion_id,
//       //   nombre: dispositivo.nombre_integracion,
//       //   atributos: dispositivo.atributos,
//       // });
//       if(integraciones.length !== 0){
//         const selectedIntegracion = integraciones.find(
//           (integracion) => integracion.nombre === dispositivo.integracion
//         );
//         setSelectedIntegracion({
//           id: selectedIntegracion.id,
//           nombre: selectedIntegracion.nombre,
//           atributos: selectedIntegracion.atributos,
//         });
//         setValue("integraciones", selectedIntegracion.id);
//         setAtributosActuables(
//           dispositivo.atributos.filter((item) => item.actuable === "true")
//         );
//       }
//     }
//   }, [dispositivo]);

//   useEffect(() => {
//     async function getIntegraciones() {
//       try {
//         const respuesta = await integracionService.getIntegraciones();
//         setIntegraciones(respuesta);
//         console.log("respuesta", respuesta);
//         console.log("integraciones", integraciones); // Should log the updated value
//         if(dispositivo.integracion){
//           const selectedIntegracion = integraciones.find(
//             (integracion) => integracion.nombre === dispositivo.integracion
//           );
//           console.log('Dispositivo integracion', dispositivo.integracion, 'selected', selectedIntegracion);
//           setSelectedIntegracion({
//             id: selectedIntegracion.id,
//             nombre: selectedIntegracion.nombre,
//             atributos: selectedIntegracion.atributos,
//           });
//           setValue("integraciones", selectedIntegracion.id);
//           console.log(getValues("integraciones"));
//           setAtributosActuables(
//             dispositivo.atributos.filter((item) => item.actuable === "true")
//           );
//         }
//       } catch (error) {
//         console.error("Error fetching integraciones:", error);
//       }
//     }

//     getIntegraciones();
//   }, []);

//   const transformarObjeto = (data) => {
//     let topics_actuacion = [];
//     let plantillas_actuacion = [];
  
//     // Si hay atributos actuales, extraer los valores de los campos de texto
//     if (atributosActuables.length !== 0) {
//       atributosActuables.forEach((atributo) => {
//         const topicKey = `topic_${atributo.nombre}`;
//         const plantillaKey = `plantilla_${atributo.nombre}`;
  
//         // Agregar el valor del campo de texto del topic a la lista de topics_actuacion
//         if (data[topicKey]) {
//           topics_actuacion.push(data[topicKey]);
//         }
  
//         // Agregar el valor del campo de texto de la plantilla a la lista de plantillas_actuacion
//         if (data[plantillaKey]) {
//           plantillas_actuacion.push(data[plantillaKey]);
//         }
//       });
//     }
  
//     // Crear el objeto transformado
//     const objetoTransformado = {
//       id: data.id,
//       nombre: data.nombre,
//       nombre_integracion: selectedIntegracion.nombre,
//       topic: data.topic,
//       topics_actuacion: topics_actuacion,
//       plantillas_actuacion: plantillas_actuacion,
//     };
  
//     return objetoTransformado;
//   };

//   const onSubmit = async (data) => {
//     try {
//       console.log("data:", data);
//       const objetoTransformado = transformarObjeto(data);
//       console.log("Objeto transformado:", objetoTransformado);
//       const response = await dispositivoService.createDispositivo(
//         objetoTransformado
//       );
//       console.log("Integración creada:", response);
//       onClose();
//     } catch (error) {
//       console.error("Error creando integración:", error);
//     } finally {
//       // onClose();
//     }
//   };

//   const onClose = () => {
//     navigate("/dispositivos");
//   };

//   return (
//     <Box sx={{ padding: 2 }}>
//       <form onSubmit={handleSubmit(onSubmit)}>
//         <Grid container spacing={5}>
//           <Grid item xs={6}>
//             <Controller
//               name="id"
//               control={control}
//               rules={{ required: "Este campo es requerido" }}
//               render={({ field }) => (
//                 <TextField
//                   {...field}
//                   label="ID Dispositivo"
//                   fullWidth
//                   error={!!errors.id}
//                   helperText={errors.id && errors.id.message}
//                 />
//               )}
//             />
//           </Grid>
//           <Grid item xs={6}>
//             <Controller
//               name="nombre"
//               control={control}
//               rules={{ required: "Este campo es requerido" }}
//               render={({ field }) => (
//                 <TextField
//                   {...field}
//                   label="Nombre dispositivo"
//                   fullWidth
//                   error={!!errors.nombre}
//                   helperText={errors.nombre && errors.nombre.message}
//                 />
//               )}
//             />
//           </Grid>
//           <Grid item xs={6}>
//             <Controller
//               name="integraciones"
//               control={control}
//               rules={{ required: "Este campo es requerido" }}
//               render={({ field }) => (
//                 <TextField
//                   {...field}
//                   select
//                   label="Integración a la que pertenece el dispositivo"
//                   fullWidth
//                   onChange={(e) => {
//                     const selectedIntegracion = integraciones.find(
//                       (integracion) => integracion.id === e.target.value
//                     );
//                     setSelectedIntegracion({
//                       id: selectedIntegracion.id,
//                       nombre: selectedIntegracion.nombre,
//                       atributos: selectedIntegracion.atributos,
//                     });
//                     setValue("integraciones", e.target.value);
//                     setAtributosActuables(
//                       selectedIntegracion.atributos.filter(
//                         (item) => item.actuable === "true"
//                       )
//                     );
//                   }}
//                   error={!!errors.nombre}
//                   helperText={errors.nombre && errors.nombre.message}
//                 >
//                   {integraciones.map((integracion) => (
//                     <MenuItem key={integracion.id} value={integracion.id}>
//                       {integracion.nombre}
//                     </MenuItem>
//                   ))}
//                 </TextField>
//               )}
//             />
//           </Grid>
//           <Grid item xs={6}>
//             <Controller
//               name="topic"
//               control={control}
//               rules={{ required: "Este campo es requerido" }}
//               render={({ field }) => (
//                 <TextField
//                   {...field}
//                   label="Topic MQTT de publicación de los datos"
//                   fullWidth
//                   error={!!errors.topic}
//                   helperText={errors.topic && errors.topic.message}
//                 />
//               )}
//             />
//           </Grid>
//           {atributosActuables.length !== 0 &&
//             atributosActuables.map((atributo, index) => (
//               <React.Fragment key={atributo.id}>
//                 <Grid item xs={6}>
//                   <Controller
//                     name={`topic_${atributo.nombre}`}
//                     control={control}
//                     rules={{ required: "Este campo es requerido" }}
//                     render={({ field }) => (
//                       <TextField
//                         {...field}
//                         label={`Topic de actuación ${atributo.nombre}`}
//                         fullWidth
//                         error={!!errors[`topic_${atributo.nombre}`]}
//                         helperText={
//                           errors[`topic_${atributo.nombre}`] &&
//                           errors[`topic_${atributo.nombre}`].message
//                         }
//                       />
//                     )}
//                   />
//                 </Grid>
//                 <Grid item xs={6}>
//                   <Controller
//                     name={`plantilla_${atributo.nombre}`}
//                     control={control}
//                     rules={{ required: "Este campo es requerido" }}
//                     render={({ field }) => (
//                       <TextField
//                         {...field}
//                         label={`Plantilla Jinja2 del mensaje ${atributo.nombre}`}
//                         fullWidth
//                         error={!!errors[`plantilla_${atributo.nombre}`]}
//                         helperText={
//                           errors[`plantilla_${atributo.nombre}`] &&
//                           errors[`plantilla_${atributo.nombre}`].message
//                         }
//                       />
//                     )}
//                   />
//                 </Grid>
//               </React.Fragment>
//             ))}
//           <Grid item xs={6}>
//             <Button
//               variant="contained"
//               fullWidth
//               onClick={onClose}
//               endIcon={<Close />}
//             >
//               Cancelar
//             </Button>
//           </Grid>
//           <Grid item xs={6}>
//             <Button
//               type="submit"
//               variant="contained"
//               fullWidth
//               endIcon={<ArrowForward />}
//             >
//               Guardar
//             </Button>
//           </Grid>
//         </Grid>
//       </form>
//     </Box>
//   );
// };

// export default FormularioDispositivo;
