import userService from "../services/userService";
import { useNavigate } from "react-router-dom";

export const logout = async () => { //Ver como hacer lo del navigate
    //Si hay algo en sessionStorage lo tengo que quitar
    await userService.logout();
    navigate("/");
}

export const getPerfil = async () => {
    try{
        const datos = await userService.obtenerPerfil();
        console.log("Datos: ", datos);
        return datos;
    }catch(error){
        console.error("Error al obtener perfil:", error);
    }

}

export const getDatos = async () => {
    try{
        const datos = await userService.obtenerDatos();
        console.log("Datos: ", datos);
        return datos;
    }catch(error){
        console.error("Error al obtener datos:", error);
    }
}