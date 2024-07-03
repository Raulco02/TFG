import React, { useState, useEffect } from "react";
import "./Login.css";
import userService from "../../services/userService";
import { useNavigate } from "react-router-dom";
import { TextField } from "@mui/material";
import { FieldValue, FieldValues, useForm } from "react-hook-form";

const Code: React.FC = () => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate();

  const handleCode = async (data: FieldValues) => {
    try {
      const code = data.code as string;
      const response = await userService.sendSecurityCode( code );
      if(response.error){
        setErrorMessage(response.error);
        return;
      }
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
          onSubmit={handleSubmit(handleCode)}
        >
          <TextField
            label="Code"
            id="code"
            {...register("code", { required: true })}
            error={!!errors.email}
            helperText={
              errors.email && errors.email.type === "required"
                ? "Este campo no puede estar vacío"
                : null
            }
          ></TextField>
          {/*errors.email && (
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
      </div>
    </div>
  );
};

export default Code;
