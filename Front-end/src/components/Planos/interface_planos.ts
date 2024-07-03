import { Planos } from "../../resources/enums/enums";
import { Anexo_B_1_type, Planta_Baja_type, Planta_1_type, Planta_2_type } from "./type_planos";

export interface PlanosInterface {
    Valores: { [key: string]: string }; // Esta parte parece estar bien
}

export interface Anexo_B_1_iface {
    contenido: { [key in Anexo_B_1_type]: string };
    plano: Planos.Anexo_B_1 | Planos.Anexo_B_2;
    popover: boolean;
}

export interface Planta_Baja_iface {
    contenido: { [key in Planta_Baja_type]: string };
    popover: boolean;
}

export interface Planta_1_iface {
    contenido: { [key in Planta_1_type]: string };
    popover: boolean;
}

export interface Planta_2_iface {
    contenido: { [key in Planta_2_type]: string };
    popover: boolean;
}
