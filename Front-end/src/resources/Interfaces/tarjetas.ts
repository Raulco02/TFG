import { Tarjetas, TipoGrafico, TiempoGrafico, Posiciones } from '../enums/enums';

export interface tarjetaTexto {
    tipo: Tarjetas.Texto;
    id_seccion: string;
    contenido: string | null; 
    posicion: Posiciones;
}

export interface tarjetaImagen {
    tipo: Tarjetas.Imagen;
    id_seccion: string; 
    posicion: Posiciones;
    imagen: string | null;
}

export interface tarjetaEstado {
    tipo: Tarjetas.Estado;
    id_seccion: string;
    posicion: Posiciones;
    id_dispositivo: string;
    id_atributo: string;
}

export interface tarjetaGrafico {
    tipo: Tarjetas.Grafico;
    id_seccion: string;
    posicion: Posiciones;
    id_dispositivos: [string];
    id_atributos: [string];
    tipo_grafico: TipoGrafico;
    tiempo_grafico: TiempoGrafico;
}

export interface tarjetaTermostato {
    tipo: Tarjetas.Termostato;
    id_seccion: string;
    posicion: Posiciones;
    id_dispositivo: string;
    id_atributo: string;
}

export interface tarjetaPlano {
    tipo: Tarjetas.Plano;
    id_seccion: string;
    posicion: Posiciones;
}

export interface tarjetaGrupo {
    tipo: Tarjetas.Grupo;
    id_seccion: string;
    posicion: Posiciones;
    id_grupo: string;
}

export type TypeTarjetas = tarjetaTexto | tarjetaImagen | tarjetaEstado | tarjetaGrafico | tarjetaPlano | tarjetaGrupo | tarjetaTermostato;