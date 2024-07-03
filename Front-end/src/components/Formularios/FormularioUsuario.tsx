import React, { useState, useEffect } from "react";
import { useForm, Controller } from "react-hook-form";
import { useLocation, useNavigate } from "react-router-dom";
import { IconName } from "../../resources/enums/enums";
import { getIconComponent } from "../../utils/iconUtils";
import { Button, TextField, Box, Grid, Typography } from "@mui/material";
import { ArrowForward, Close } from "@mui/icons-material";
import userService from "../../services/userService";

const FormularioUsuario = ({ usuario = null, onClose, theme }) => {
  const {
    handleSubmit,
    setValue,
    control,
    formState: { errors },
    watch,
  } = useForm();

  const [prevId, setPrevId] = useState("");
  const [user, setUser] = useState(null);

  const location = useLocation();
  const navigate = useNavigate();

  const isAdministrarCuenta = location.state;

  useEffect(() => {
    if (usuario) {
      setValue("nombre", usuario.nombre);
      setValue("correo", usuario.correo);
      setPrevId(usuario.id);
    }
  }, [usuario, setValue]);

  useEffect(() => {
    if (isAdministrarCuenta) {
        getUsuario();
    }
  }, [isAdministrarCuenta]);

  useEffect(() => {
    if (user) {
      setValue("nombre", user.nombre);
      setValue("correo", user.correo);
      setPrevId(user.id);
    }
  }, [user, setValue]);

  const getUsuario = async () => {
    try {
      const response = await userService.obtenerPerfil();
      console.log("Usuario obtenido:", response);
      setUser(response)
    } catch (error) {
      console.error("Error obteniendo usuario:", error);
      setUser(null)
    }
  };

  const onSubmit = async (data) => {
    if (data.password !== data.confirmPassword) {
      alert("Las contraseñas no coinciden");
      return;
    }

    const objetoTransformadoCrear = {
      id: prevId,
      nombre: data.nombre,
      correo: data.correo,
      pwd1: data.password,
      pwd2: data.confirmPassword,
    };

    const objetoTransformadoEditar = {
        id: prevId,
        nuevo_nombre: data.nombre,
        nuevo_correo: data.correo,
        nueva_password: data.password,
    }

    try {
      if (usuario === null && user === null) {
        const response = await userService.register(objetoTransformadoCrear);
        console.log("Usuario creado:", response);
      } else {
        const response = await userService.editUsuario(objetoTransformadoEditar);
        console.log("Usuario editado:", response);
      }
      if(isAdministrarCuenta){
        navigate("/config");
      } else{
        onClose();
      }
    } catch (error) {
      console.error("Error guardando usuario:", error);
    }
  };

  return (
    <Box className="formulario" sx={{ padding: 2, backgroundColor: theme.palette.background.paper, color: theme.palette.primary.text }}>
      <form onSubmit={handleSubmit(onSubmit)}>
        <Grid container spacing={3}>
          {isAdministrarCuenta && (
            <>
            <Grid item xs={12}>
                <Typography variant="h6" gutterBottom >
                    Editar perfil
                </Typography>
            </Grid>
            </>
          )}
          {!isAdministrarCuenta && (
            <>
            <Grid item xs={12}>
                <Typography variant="h6" gutterBottom >
                    {usuario ? "Editar usuario" : "Crear usuario"}
                </Typography>
            </Grid>
            </>
          )}
          <Grid item xs={12}>
            <Controller
              name="nombre"
              control={control}
              defaultValue={usuario ? usuario.nombre : ""}
              rules={{ required: "Este campo es requerido" }}
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
              name="correo"
              control={control}
              defaultValue={usuario ? usuario.correo : ""}
              rules={{ 
                required: "Este campo es requerido",
                pattern: {
                  value: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/,
                  message: "Correo electrónico inválido"
                }
              }}
              render={({ field }) => (
                <TextField
                  {...field}
                  label="Correo"
                  fullWidth
                  error={!!errors.correo}
                  helperText={errors.correo && errors.correo.message}
                />
              )}
            />
          </Grid>
          <Grid item xs={6}>
            <Controller
              name="password"
              control={control}
              defaultValue=""
              rules={{ required: "Este campo es requerido", minLength: { value: 8, message: "La contraseña debe tener al menos 8 caracteres"}}}
              render={({ field }) => (
                <TextField
                  {...field}
                  type="password"
                  label="Contraseña"
                  fullWidth
                  error={!!errors.password}
                  helperText={errors.password && errors.password.message}
                />
              )}
            />
          </Grid>
          <Grid item xs={6}>
            <Controller
              name="confirmPassword"
              control={control}
              defaultValue=""
              rules={{ 
                required: "Este campo es requerido",
                minLength: { value: 8, message: "La contraseña debe tener al menos 8 caracteres"},
                validate: value =>
                  value === watch('password') || "Las contraseñas no coinciden"
              }}
              render={({ field }) => (
                <TextField
                  {...field}
                  type="password"
                  label="Confirmar Contraseña"
                  fullWidth
                  error={!!errors.confirmPassword}
                  helperText={errors.confirmPassword && errors.confirmPassword.message}
                />
              )}
            />
          </Grid>
          <Grid item xs={6}>
            <Button
              variant="contained"
              fullWidth
              onClick={() => {if(isAdministrarCuenta){navigate("/config")}else{onClose}}}
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

export default FormularioUsuario;
