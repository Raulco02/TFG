import { Anexo_B_1_enum, Planta_Baja_enum, Planta_1_enum, Planta_2_enum } from "./enum_planos";

export type Anexo_B_1_type = Anexo_B_1_enum.Aula_A1_1 | Anexo_B_1_enum.Aula_A1_2 | Anexo_B_1_enum.Pasillo_A1 | Anexo_B_1_enum.Aula_A2_1 | Anexo_B_1_enum.Aula_A2_2 | Anexo_B_1_enum.Pasillo_A2;

export type Planta_Baja_type = Planta_Baja_enum.Salon_De_Actos | Planta_Baja_enum.Salon_De_Grados | Planta_Baja_enum.Aula_F0_1;

export type Planta_1_type = Planta_1_enum.LD1 | Planta_1_enum.LD2 | Planta_1_enum.LD3 | Planta_1_enum.Aula_F1_1;

export type Planta_2_type = Planta_2_enum.LD4;