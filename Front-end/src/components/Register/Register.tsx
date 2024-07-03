import React, { useState } from 'react';
import './Register.css'; 
import userService from '../../services/userService';
import { useNavigate } from 'react-router-dom';
import { TextField } from "@mui/material";
import { FieldValue, FieldValues, useForm } from "react-hook-form";

const Register: React.FC = () => {
    const navigate = useNavigate();
    const {
      register,
      handleSubmit,
      formState: { errors },
      watch,
    } = useForm();
    const [errorMessage, setErrorMessage] = useState("");
    
    const password = watch("pwd1");
    
    const confirmPasswordValidation = (value: string) =>
      value === password || "Las contraseñas no coinciden";

    const handleSignup = async(data: FieldValues) => {
            try {
              const nombre = data.nombre as string;
              const correo = data.correo as string;
              const pwd1 = data.pwd1 as string;
              const pwd2 = data.pwd2 as string;
              await userService.register({ nombre, correo, pwd1, pwd2 });
              //onSignup(id); // Ver si es necesario
              //console.log(id.httpId); 
              //sessionStorage.setItem('httpId', id.httpId);
              navigate('/');
            } catch (error) {
              console.error('Error al registrarse:', error);
            }
      };

  return (
    <div className="signup-container">
      <div className="background-image"></div>
      <div className="signup-form">
        <div className="avatar-container">
          <img className="avatar" src="/logo.png" alt="Avatar-Smart-Esi" />
        </div>
        <form
          style={{ display: "flex", flexDirection: "column" }}
          onSubmit={handleSubmit(handleSignup)}
        >
          <TextField
            label="Nombre de usuario"
            id="nombre"
            {...register("nombre", { required: true, minLength: 2 })}
            error={!!errors.nombre}
            helperText={
              errors.nombre && errors.nombre.type === "required"
                ? "Este campo no puede estar vacío"
                : errors.nombre && errors.nombre.type === "pattern"
                ? "Por favor, introduce un correo electrónico válido"
                : errors.nombre && errors.nombre.type === "minLength"
                ? "El nombre debe tener al menos 2 caracteres"
                : null
            }
          ></TextField>

          <TextField
            label="Email"
            id="correo"
            style={{ marginTop: "1rem" }}
            {...register("correo", { required: true, pattern: /^\S+@\S+$/i })}
            error={!!errors.correo}
            helperText={
              errors.correo && errors.correo.type === "required"
                ? "Este campo no puede estar vacío"
                : errors.correo && errors.correo.type === "pattern"
                ? "Por favor, introduce un correo electrónico válido"
                : null
            }
          ></TextField>
          {/*errors.email && (
            <span style={{ color: "red" }}>
              Este campo no puede estar vacío
            </span>
          )*/}

          <TextField
            type="password"
            style={{ marginTop: "1rem" }}
            label="Contraseña"
            id="pwd1"
            {...register("pwd1", { required: true, minLength: 8 })}
            error={!!errors.pwd1}
            helperText={
              errors.pwd1 && errors.pwd1.type === "required"
                ? "Este campo no puede estar vacío"
                : errors.pwd1 && errors.pwd1.type === "minLength"
                ? "La contraseña debe tener al menos 8 caracteres"
                : null
            }
          />

          <TextField
            type="password"
            style={{ marginTop: "1rem" }}
            label="Confirmar Contraseña"
            id="pwd2"
            {...register("pwd2", { required: true, minLength: 8, validate: confirmPasswordValidation })}
            error={!!errors.pwd2}
            helperText={
              errors.pwd2 && errors.pwd2.type === "required"
                ? "Este campo no puede estar vacío"
                : errors.pwd2 && errors.pwd2.type === "minLength"
                ? "La contraseña debe tener al menos 8 caracteres"
                : errors.pwd2 && errors.pwd2.type === "validate"
                ? "Las contraseñas no coinciden"
                : null
            }
          />
          {/*errors.password && (
            <span style={{ color: "red" }}>
              Este campo no puede estar vacío
            </span>
          )*/}

          {errorMessage && (
            <div
              style={{
                backgroundColor: "red",
                color: "white",
                padding: "10px",
                borderRadius: "5px",
                marginTop: "1rem",
              }}
            >
              {errorMessage}
            </div>
          )}

          <button
            style={{ marginTop: "1rem" }}
            type="submit"
            className="signup-button"
          >
            Registrarse
          </button>
        </form>
      </div>
    </div>
  );
};

export default Register;
