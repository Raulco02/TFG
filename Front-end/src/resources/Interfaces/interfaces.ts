import { IconName, Layouts, Tarjetas } from '../enums/enums';

export interface User {
    id: string;
    nombre: string;
    correo: string;
    password: string;
}

export interface LoginData {
    correo: string;
    password: string;
}

export interface RegisterData {
  nombre: string;
  correo: string;
  pwd1: string;
  pwd2: string;
}

export interface Dashboard {
    id: string;
    icono: IconName;
    nombre: string;
    secciones: [] | null;
}

export interface createForm {
    nombre: string;
    icono: IconName;
}

export interface createSeccionForm {
    nombre: string;
    layout: 'Card' | 'Grid' | 'Sidebar';
}

export interface createCardForm {
    tipo: Tarjetas;
    id_seccion: string;
    contenido: string | null; 
    imagen: string | null; //Revisar tipo
    dispositivo: string | null; //Hacer enum de dispositivos?
    atributo: string | null; //Hacer enum de atributos?
    unidad: string | null; //Hacer enum de unidades
    tipo_grafico: string | null; //Hacer enum de tipos de graficos
    tiempo_grafico: string | null; //Hacer enum de tiempos de graficos
    id_atributo: number | null;
    id_dispositivo: string | null;
    posicion: '0x0' | '0x1' | '0x2' | '1x0' | '1x1' | '1x2' | '2x0' | '2x1' | '2x2';
    filas: number;
    columnas: number;

}

export interface Seccion {
    id: string;
    nombre: string;
    icono: IconName;
    layout: Layouts;
    tarjetas: [] | null;
}

export interface createSeccion {
    dashboard_id: string;
    nombre: string;
    layout: Layouts;
}

export interface Tarjeta {
    tipo: Tarjetas;
    contenido: string | null;
    dispositivo: string | null;
    atributo: string | null;
    unidad: string | null;
    tipo_grafico: string | null;
    posicion: string;

}

export interface columnaLista {
   id: string;//'name' | 'code' | 'population' | 'size' | 'density';
   label: string;
   minWidth?: number;
   align?: 'right';
   format?: (value: number) => string;
}

export interface Atributo {
    nombre: string;
    unidades: string;
    actuable: "true" | "false";
}

export interface createIntegracionData {
    nombre: string;
    nombre_script: string;
    script: string;
    atributos: Atributo[];
    
}