import React, { useState, useEffect } from "react";
import "./Login.css";
import userService from "../../services/userService";
import { useNavigate } from "react-router-dom";
import { TextField } from "@mui/material";
import { FieldValue, FieldValues, useForm } from "react-hook-form";

const Login: React.FC<{ onLogin: (id: string) => void }> = ({ onLogin }) => {
  const [id, setId] = useState("");
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate();

  //También puedo hacer logout cada vez que se entre a login
  useEffect(() => { //Otra opción es guardar el atributo loggedin en el sessionStorage y borrarlo en el logout y comprobar eso
    async function obtenerPerfil() {
      const datos = await userService.obtenerPerfil();
      console.log("Datos: ", datos);
      if(datos.error === undefined){
        navigate('/dashboard');
      }
    }
    obtenerPerfil();
  }, []); //Estudiar el uso de useRef para que solo se ejecute una vez. Además de creación de un hook personalizado para esto
  //CHATGPT 18/04 Conversación: UseContext en React. Info importante
  const handleLogin = async (data: FieldValues) => {
    try {
      const correo = data.email as string;
      const password = data.password as string;
      const response = await userService.login({ correo, password });
      if(response.error){
        setErrorMessage(response.error);
        return;
      }
      // navigate("/code"); DESACTIVAR PARA CODIGO DE SEGURIDAD
      navigate("/dashboard");
    } catch (error) {
      console.error("Error al iniciar sesión:", error);
      setErrorMessage(
        "Error al iniciar sesión: " + error || "Error desconocido"
      );
    }
  };

  return (
    <div className="login-container">
      <div className="background-image"></div>
      <div className="login-form">
        <div className="avatar-container">
          <img className="avatar" src="/logo.png" alt="Avatar-Smart-Esi" />
        </div>
        <form
          style={{ display: "flex", flexDirection: "column" }}
          onSubmit={handleSubmit(handleLogin)}
        >
          <TextField
            label="Email"
            id="email"
            {...register("email", { required: true, pattern: /^\S+@\S+$/i })}
            error={!!errors.email}
            helperText={
              errors.email && errors.email.type === "required"
                ? "Este campo no puede estar vacío"
                : errors.email && errors.email.type === "pattern"
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
            id="password"
            {...register("password", { required: true, minLength: 8 })}
            error={!!errors.password}
            helperText={
              errors.password && errors.password.type === "required"
                ? "Este campo no puede estar vacío"
                : errors.password && errors.password.type === "minLength"
                ? "La contraseña debe tener al menos 8 caracteres"
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
            className="login-button"
          >
            Iniciar sesión
          </button>
        </form>
        <div className="form-links">
          <a href="/registrar">¿No tienes cuenta? Regístrate</a>
          <a href="#">He olvidado mi contraseña</a>
        </div>
      </div>
    </div>
  );
};

export default Login;
