import React, { useEffect, useState } from "react";
import { Planos, Espacios } from "../../resources/enums/enums";
import { useInterval } from "../../hooks/useInterval";
import dispositivoService from "../../services/dispositivoService";
import { Button, IconButton, Popover, Tooltip, useTheme } from "@mui/material";
import { getIconComponent } from "../../utils/iconUtils";
import InfoBox from "../InfoBox";

import Anexo_B_1 from "../Planos/Anexo_B_1";
import {
  Anexo_B_1_enum,
  Anexo_B_1_Espacios,
  Anexo_B_2_Espacios,
  Planta_Baja_enum,
  Planta_1_enum,
  Planta_2_enum,
} from "../Planos/enum_planos";

// Importa los SVGs
import Fermin_Caballero_B from "../../assets/Fermin_Caballero_B.svg";
import Fermin_Caballero_1 from "../../assets/Fermin_Caballero_1.svg";
import Fermin_Caballero_2 from "../../assets/Fermin_Caballero_2.svg";
import Fermin_Caballero_3 from "../../assets/Fermin_Caballero_3.svg";
import Anexo_A_B from "../../assets/Anexo_A_B.svg";
import Anexo_A_1 from "../../assets/Anexo_A_1.svg";
import Anexo_B_B from "../../assets/Anexo_B_B.svg";
//import { ReactComponent as Anexo_B_1} from '../../assets/Anexo_B_1.svg';
import Anexo_B_2 from "../../assets/Anexo_B_2.svg";
import { get, set } from "react-hook-form";
import PlanoPopover from "./PlanoPopover";
import Planta_Baja from "../Planos/Planta_Baja";
import Planta_1 from "../Planos/Planta_1";
import Planta_2 from "../Planos/Planta_2";
import { render } from "react-dom";

// Define las props del componente
// interface PlanosProps {
//   plano: Planos;
// }

// Mapea los valores del enum a los archivos SVG
// const planosMap: Record<Planos, string> = {
//   [Planos.Fermin_Caballero_B]: Fermin_Caballero_B,
//   [Planos.Fermin_Caballero_1]: Fermin_Caballero_1,
//   [Planos.Fermin_Caballero_2]: Fermin_Caballero_2,
//   [Planos.Anexo_A_B]: Anexo_A_B,
//   [Planos.Anexo_A_1]: Anexo_A_1,
//   [Planos.Anexo_B_B]: Anexo_B_B,
//   [Planos.Anexo_B_1]: Anexo_B_1,
//   [Planos.Anexo_B_2]: Anexo_B_2,
// };

// Componente que retorna el SVG correspondiente al plano
const PlanosComponent = ({ isSmall, theme }) => {
  console.log("Es pequeño:", isSmall);
  console.log("theme plano", theme);
  const botones = [
    "Planta Baja",
    "Planta 1",
    "Planta 2",
    "Anexo B P1",
    "Anexo B P2",
  ]; // Puedes agregar más nombres según sea necesario
  const [botonSeleccionado, setBotonSeleccionado] = useState(0);
  const [iconoSeleccionado, setIconoSeleccionado] = useState(0);
  const [atributosMap, setAtributosMap] = useState({});
  const [atributoSeleccionado, setAtributoSeleccionado] = useState("");
  const [plano, setPlano] = useState(Planos.Fermin_Caballero_B);
  const [aulas, setAulas] = useState([]);
  const [contenido, setContenido] = useState({});
  const [datosAulas, setDatosAulas] = useState({});
  const [dispositivos, setDispositivos] = useState([]);
  const [atributosPlano, setAtributosPlano] = useState({});
  const [infoAula, setInfoAula] = useState({});
  const [anchorEl, setAnchorEl] = useState<HTMLElement | null>(null);
  const [numColores, setNumColores] = useState(0); // 0 para uno,1 para dos con li,2 para dos con ls,3 para tres. + gray
  const [liActual, setLiActual] = useState(null);
  const [lsActual, setLsActual] = useState(null);
  const [unidadActual, setUnidadActual] = useState("");
  const [popoverOpen, setPopoverOpen] = useState(false);
  const [popoverAnchor, setPopoverAnchor] = useState<HTMLElement | null>(null);

  // const theme = useTheme();

  //   const datosAulas = {
  //     "Aula_1": 22,
  //     "Aula_2": 19,
  //     "Pasillo": 25,
  //     // Añadir más datos según sea necesario
  //   };
  const obtenerColor = (valor: number) => {
    //Habria que guardar min y max en bbdd por atributo
    console.log("Temperatura de obtenerColor", atributoSeleccionado, valor);
    const atributo = atributosMap[atributoSeleccionado];
    let ls = null;
    let li = null;
    if (atributo) {
      setLsActual(atributo.limite_superior);
      setLiActual(atributo.limite_inferior);
      setUnidadActual(atributo.unidades);
      ls = atributo.limite_superior;
      li = atributo.limite_inferior;
    }
    if (ls !== null && li !== null) {
      setNumColores(3);
      if (valor > ls) {
        return "red";
      } else if (Number.isNaN(valor) || valor === -150) {
        console.log("Valor en color", valor, atributoSeleccionado);
        return "gray";
      } else if (valor < ls && valor > li) {
        return "green";
      } else {
        return "blue";
      }
    } else if (ls !== null) {
      setNumColores(2);
      if (valor > ls) {
        return "red";
      } else if (Number.isNaN(valor) || valor === -150) {
        return "gray";
      } else {
        return "green";
      }
    } else if (li !== null) {
      setNumColores(1);
      if (valor > li) {
        return "green";
      } else if (Number.isNaN(valor) || valor === -150) {
        return "gray";
      } else {
        return "blue";
      }
    } else {
      setNumColores(0);
      if (Number.isNaN(valor) || valor === -150) {
        return "gray";
      }
      return "green";
    }
  };

  //   useEffect(() => {
  //     const svgElement = document.getElementById('svg1');
  //     console.log(svgElement);
  //     if (svgElement) {
  //       Object.keys(datosAulas).forEach((id) => {
  //         const elemento = svgElement.getElementById(id);
  //         console.log(elemento);
  //         console.log(datosAulas[id]);
  //         if (elemento) {
  //           const temperatura = datosAulas[id];
  //           elemento.style.fill = obtenerColor(temperatura);
  //         }
  //       });
  //     }
  //   }, []);

  const handleBotonClick = (index: number) => {
    setNumColores(0);
    setBotonSeleccionado(index);
    setIconoSeleccionado(0);
    console.log("Botón seleccionado:", index);
    switch (index) {
      case 0:
        setPlano(Planos.Fermin_Caballero_B);
        setAulas(Object.values(Planta_Baja_enum));
        break;
      case 1:
        setPlano(Planos.Fermin_Caballero_1);
        setAulas(Object.values(Planta_1_enum));
        break;
      case 2:
        setPlano(Planos.Fermin_Caballero_2);
        setAulas(Object.values(Planta_2_enum));
        break;
      case 3:
        setPlano(Planos.Anexo_B_1);
        setAulas(Object.values(Anexo_B_1_Espacios));
        break;
      case 4:
        setPlano(Planos.Anexo_B_2);
        setAulas(Object.values(Anexo_B_2_Espacios));
        break;
      default:
        setPlano(Planos.Fermin_Caballero_B);
        setAulas(Object.values(Planta_Baja_enum));
        break;
    }
    console.log("Plano seleccionado:", plano);
    console.log("Aulas", aulas);
  };
  const handleIconoClick = (index: number) => {
    setIconoSeleccionado(index);
    console.log(
      "Icono seleccionado:",
      index,
      Object.keys(atributosPlano)[index]
    );
    setAtributoSeleccionado(Object.keys(atributosPlano)[index]);
  };

  useEffect(() => {
    getDispositivos();
    console.log("Plano seleccionado:", plano);
    // if (planta === '1') {
    //     setContenido({
    //         [Anexo_B_1_enum.Aula_A1_1]: 22,
    //         [Anexo_B_1_enum.Aula_A1_2]: 19,
    //         [Anexo_B_1_enum.Pasillo_A1]: 25
    //     });
    // } else if (planta === '2') {
    //     setContenido({
    //         [Anexo_B_1_enum.Aula_A2_1]: 16,
    //         [Anexo_B_1_enum.Aula_A2_2]: 19,
    //         [Anexo_B_1_enum.Pasillo_A2]: 25
    //     });
    // }
    // const svgElement = document.getElementById('svg1');
    // console.log(svgElement);
    // if (svgElement) {
    //   Object.keys(datosAulas).forEach((id) => {
    //     const elemento = svgElement.getElementById(id);
    //     console.log(elemento);
    //     console.log(datosAulas[id]);
    //     if (elemento) {
    //       const temperatura = datosAulas[id];
    //       elemento.style.fill = obtenerColor(temperatura);
    //     }
    //   });
    // }
  }, [plano]);

  // useEffect(() => {
  //   const contenidoMap = {};
  //   dispositivos.forEach((dispositivo) => {
  //     dispositivo.atributos.forEach((atributo) => {
  //       if (atributo.nombre_atributo === atributoSeleccionado) {
  //         contenidoMap[dispositivo.ubicacion] = atributo.valor;
  //       }
  //     });
  //   });
  //   //setContenido(contenidoMap);
  //   console.log("Contenido", contenidoMap);
  //   console.log("Dispositivos", dispositivos);
  //   console.log("Atributos plano", atributosPlano);
  // }, [dispositivos, atributoSeleccionado]);

  useEffect(() => {
    console.log("Atributo seleccionado", atributoSeleccionado);
    const contenidoMap = {};
    dispositivos.forEach((dispositivo) => {
      if (!aulas.includes(dispositivo.ubicacion)) return;
      if (!dispositivo.atributos) return;
      dispositivo.atributos.forEach((atributo) => {
        if (atributo.nombre_atributo === atributoSeleccionado) {
          const aula = determinarAula(dispositivo.ubicacion);
          contenidoMap[aula] = atributo.valor + atributo.unidades;
        }
      });
    });
    setContenido(contenidoMap);
    console.log("Contenido", contenidoMap);
  }, [atributoSeleccionado]);

  useEffect(() => {
    const svgElement = document.getElementById("svg1");
    console.log(svgElement);
    console.log(aulas);
    const aulaModificada = {};
    aulas.forEach((aula) => {
      aulaModificada[aula] = false;
    });
    console.log(aulaModificada);
    if (svgElement) {
      console.log("Dispositivos para color", dispositivos);
      console.log("Contenido para color", contenido);
      console.log("Atributo seleccionado para color", atributoSeleccionado);
      console.log(
        "Lo de los atributos",
        atributoSeleccionado,
        atributosPlano,
        atributosMap
      );
      console.log("Aulas en lo del color", aulas);
      aulas.forEach((id) => {
        const elemento = svgElement.getElementById(id);
        console.log("Elemento", id, elemento, contenido);
        if (elemento) {
          const valor = parseFloat(contenido[id]);
          console.log(id, elemento);
          console.log(
            "Valor para el color",
            elemento,
            valor,
            obtenerColor(valor)
          );
          elemento.style.fill = obtenerColor(valor, id);
          elemento.onclick = (event) => {
            console.log("Click", id);
            const infoAulaAct = obtenerInfoAula(id);
            console.log(infoAulaAct);
            setInfoAula(infoAulaAct);
            setAnchorEl(event.currentTarget);
          };
          const elemento_tag = id + "_tag";
          console.log("Elemento tag", elemento_tag);
          const elementoTag = svgElement.getElementById(elemento_tag);
          elementoTag.onclick = (event) => {
            console.log("Click", id);
            const infoAulaAct = obtenerInfoAula(id);
            console.log(infoAulaAct);
            setInfoAula(infoAulaAct);
            setAnchorEl(event.currentTarget);
          };
          console.log(
            valor,
            id,
            aulaModificada[id],
            obtenerColor(valor),
            elemento
          );
          aulaModificada[id] = true;
        }
      });
      // Object.keys(aulaModificada).forEach((id) => {
      //   console.log("aulaModificada", aulaModificada[id]);
      //   if (!aulaModificada[id]) return;
      //   const elemento = svgElement.getElementById(id);
      //   if (elemento && !aulaModificada[id]) {
      //     elemento.style.fill = obtenerColor(-150);
      //   }
      // });
      // console.log("Despues", aulaModificada);
    }
  }, [contenido]);

  const determinarAula = (ubicacion: string) => {
    switch (ubicacion) {
      case Espacios.Aula_A1_1:
        return Anexo_B_1_enum.Aula_A1_1;
      case Espacios.Aula_A1_2:
        return Anexo_B_1_enum.Aula_A1_2;
      case Espacios.Pasillo_A1:
        return Anexo_B_1_enum.Pasillo_A1;
      case Espacios.Aula_A2_1:
        return Anexo_B_1_enum.Aula_A2_1;
      case Espacios.Aula_A2_2:
        return Anexo_B_1_enum.Aula_A2_2;
      case Espacios.Pasillo_A2:
        return Anexo_B_1_enum.Pasillo_A2;
      case Espacios.LD1:
        return Planta_1_enum.LD1;
      case Espacios.LD2:
        return Planta_1_enum.LD2;
      case Espacios.LD3:
        return Planta_1_enum.LD3;
      case Espacios.LD4:
        return Planta_2_enum.LD4;
      case Espacios.Aula_F0_1:
        return Planta_Baja_enum.Aula_F0_1;
      case Espacios.Aula_F1_1:
        return Planta_1_enum.Aula_F1_1;
      case Espacios.Salon_De_Actos:
        return Planta_Baja_enum.Salon_De_Actos;
      case Espacios.Salon_De_Grados:
        return Planta_Baja_enum.Salon_De_Grados;
      default:
        return "null";
    }
  };

  const obtenerInfoAula = (aula: string) => {
    //Hacer componente que acepte información diccionarios y los muestre en un popover o algo así
    const infoAulaAct = {
      nombre: aula,
      dispositivos: {},
    };
    dispositivos.forEach((dispositivo) => {
      if (dispositivo.ubicacion === aula) {
        infoAulaAct.dispositivos[dispositivo.nombre] = {};
        dispositivo.atributos.forEach((atributo) => {
          dispositivo.atributos.forEach((atributo) => {
            infoAulaAct.dispositivos[dispositivo.nombre][
              atributo.nombre_atributo
            ] = atributo.valor + atributo.unidades;
          });
        });
      }
    });
    console.log(infoAulaAct);
    return infoAulaAct;
  };

  // useEffect(() => {
  //     setDatosAulas({
  //         "Aula_1": contenido[Anexo_B_1_enum.Aula_A1_1] || contenido[Anexo_B_1_enum.Aula_A2_1] || 0,
  //         "Aula_2": contenido[Anexo_B_1_enum.Aula_A1_2] || contenido[Anexo_B_1_enum.Aula_A2_2] || 0,
  //         "Pasillo": contenido[Anexo_B_1_enum.Pasillo_A1] || contenido[Anexo_B_1_enum.Pasillo_A2] || 0
  //     });
  // },[contenido]);

  // useEffect(() => {
  //     const svgElement = document.getElementById('svg1');
  //     console.log(svgElement);
  //     if (svgElement) {
  //       Object.keys(datosAulas).forEach((id) => {
  //         const elemento = svgElement.getElementById(id);
  //         console.log(elemento);
  //         console.log(datosAulas[id]);
  //         if (elemento) {
  //           const temperatura = datosAulas[id];
  //           elemento.style.fill = obtenerColor(temperatura);
  //         }
  //       });
  //     }
  // }, [datosAulas]);

  const avanzarSiguienteBoton = () => {
    const siguienteBoton = (botonSeleccionado + 1) % botones.length; // Calcula el índice del siguiente botón
    handleBotonClick(siguienteBoton); // Llama a la función para hacer clic en el siguiente botón
    handleIconoClick(0); // Resetea el índice del icono seleccionado
  };
  const avanzarSiguienteIcono = () => {
    if (iconoSeleccionado === Object.keys(atributosPlano).length - 1) {
      avanzarSiguienteBoton();
      return;
    }
    const siguienteIcono = iconoSeleccionado + 1;
    handleIconoClick(siguienteIcono);
  };
  useInterval(() => {
    avanzarSiguienteIcono();
  }, 10000);

  const getDispositivos = async () => {
    try {
      const dispositivos = await dispositivoService.getDispositivos();
      console.log("DISPOSITIVOS", dispositivos);
      dispositivos.sort((a, b) => {
        if (a.ubicacion === null) return 1;
        if (b.ubicacion === null) return -1;
        if (a.ubicacion < b.ubicacion) return -1;
        if (a.ubicacion > b.ubicacion) return 1;
        return 0;
      });
      let aulasAct = [];
      const atributosMapAct = {};
      const atributosPlanoAct = {};
      switch (plano) {
        case Planos.Fermin_Caballero_B:
          aulasAct = Object.values(Planta_Baja_enum);
          setAulas(aulasAct);
          break;
        case Planos.Fermin_Caballero_1:
          aulasAct = Object.values(Planta_1_enum);
          setAulas(aulasAct);
          break;
        case Planos.Fermin_Caballero_2:
          aulasAct = Object.values(Planta_2_enum);
          setAulas(aulasAct);
          break;
        case Planos.Anexo_B_1:
          aulasAct = Object.values(Anexo_B_1_Espacios);
          setAulas(aulasAct);
          break;
        case Planos.Anexo_B_2:
          aulasAct = Object.values(Anexo_B_2_Espacios);
          setAulas(aulasAct);
          break;
        default:
          aulasAct = Object.values(Planta_Baja_enum);
          setAulas(aulasAct);
          break;
      }
      dispositivos.forEach((dispositivo) => {
        dispositivo.atributos.forEach((atributo) => {
          if (!atributosMapAct[atributo.nombre_atributo]) {
            atributosMapAct[atributo.nombre_atributo] = {
              nombre: atributo.nombre_atributo,
              icono: atributo.icono || "null", // Usa un icono por defecto si no hay icono en el dispositivo
              limite_superior: atributo.limite_superior || null,
              limite_inferior: atributo.limite_inferior || null,
              unidades: atributo.unidades || "",
            };
          }
          console.log("Ubicacion", dispositivo.ubicacion);
          console.log("Aulas", aulas);
          console.log("Presente", aulas.includes(dispositivo.ubicacion));
          console.log(
            "Presente 2",
            !atributosPlanoAct[atributo.nombre_atributo]
          );
          if (
            !atributosPlanoAct[atributo.nombre_atributo] &&
            aulasAct.includes(dispositivo.ubicacion)
          ) {
            atributosPlanoAct[atributo.nombre_atributo] = {
              nombre: atributo.nombre_atributo,
              icono: atributo.icono || "null", // Usa un icono por defecto si no hay icono en el dispositivo
            };
          }
          console.log("Atributos plano act", atributosPlanoAct);
        });
      });
      setDispositivos(dispositivos);
      setAtributosMap(atributosMapAct);
      setAtributosPlano(atributosPlanoAct);
      console.log("Atributos plano act", atributosPlanoAct);
      setAtributoSeleccionado(Object.keys(atributosMapAct)[0]);

      console.log("Aulas", aulas);

      console.log("ATRIBUTOS ÚNICOS CON ICONOS", atributosMap);

      console.log("Dispositivos ordenados", dispositivos);
    } catch (error) {
      console.error(error);
    }
  };
  const handleClose = () => {
    setAnchorEl(null);
  };

  const mostrarPlanoEnPopover = (event) => {
    setPopoverAnchor({
      top: window.innerHeight / 2,
      left: window.innerWidth / 2,
    });
    setPopoverOpen(true);
  };

  const handlePopoverClose = () => {
    setPopoverOpen(false);
    setPopoverAnchor(null);
  };

  const widthPlano = isSmall ? "100%" : "100%";
  const heightPlano = isSmall ? "60%" : "75%";

  const renderLegend = (numColores, liActual, lsActual, unidadActual) => {
    let legendItems = [];

    switch (numColores) {
      case 0:
        legendItems = [
          { color: "green", label: "Con valor" },
          { color: "gray", label: "Sin valor" },
        ];
        break;
      case 1:
        legendItems = [
          { color: "blue", label: `Menor que ${liActual}${unidadActual}` },
          { color: "green", label: `Mayor que ${liActual}${unidadActual}` },
          { color: "gray", label: "Sin valor" },
        ];
        break;
      case 2:
        legendItems = [
          { color: "green", label: `Menor que ${lsActual}${unidadActual}` },
          { color: "red", label: `Mayor que ${lsActual}${unidadActual}` },
          { color: "gray", label: "Sin valor" },
        ];
        break;
      case 3:
        legendItems = [
          { color: "blue", label: `Menor que ${liActual}${unidadActual}` },
          {
            color: "green",
            label: `Entre ${liActual}${unidadActual} y ${lsActual}${unidadActual}`,
          },
          { color: "red", label: `Mayor que ${lsActual}${unidadActual}` },
          { color: "gray", label: "Sin valor" },
        ];
        break;
      default:
        break;
    }

    return (
      <div
        style={{
          display: "flex",
          flexDirection: "row",
          alignItems: "flex-start",
          height: "5%",
          marginBottom: "2%",
        }}
      >
        {legendItems.map((item, index) => (
          <div
            key={index}
            style={{
              display: "flex",
              alignItems: "center",
              marginBottom: "4px",
              padding: "8px",
            }}
          >
            <div
              style={{
                width: "20px",
                height: "20px",
                backgroundColor: item.color,
                marginRight: "4px",
                borderRadius: "20px",
              }}
            ></div>
            <span>{item.label}</span>
          </div>
        ))}
      </div>
    );
  };

  const renderPlano = (small, isPopover = false) => {
    return (
      <div
        style={{
          position: "relative",
          top: 0,
          left: 0,
          width: "100%",
          height: "100%",
          backgroundColor: theme.palette.background.paper,
          zIndex: 1, // Para que esté detrás del SVG
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          flexDirection: "column",
        }}
      >
        {/* Mostrar botones */}
        {!small && (
          <div style={{ marginTop: "2%", marginBottom: "2%", height: "6%" }}>
            {/* 10% */}
            {botones.map((nombre, index) => (
              <button
                key={index}
                onClick={() => handleBotonClick(index)}
                style={{
                  marginRight: "10px",
                  backgroundColor:
                    index === botonSeleccionado
                      ? theme.palette.primary.main
                      : "gray",
                  color: "white",
                }}
              >
                {nombre}
              </button>
            ))}
          </div>
        )}
        {/* Mostrar iconos */}
        {!small && (
          <div style={{ marginBottom: "2%", height: "5%" }}>
            {" "}
            {/*7%*/}
            {Object.values(atributosPlano).map((atributo, index) => (
              <Tooltip title={atributo.nombre} key={index}>
                <IconButton
                  variant="contained"
                  style={{
                    marginLeft: "10px",
                    backgroundColor:
                      index === iconoSeleccionado
                        ? theme.palette.primary.main
                        : "gray",
                    color: "white",
                  }}
                  onClick={() => handleIconoClick(index)}
                >
                  {getIconComponent(atributo.icono)}
                </IconButton>
              </Tooltip>
            ))}
          </div>
        )}
        {!small && (
          <div style={{ fontWeight: "bold", height: "5%" }}>
            {" "}
            {/* 5% */}
            {atributosPlano[atributoSeleccionado]?.nombre}{" "}
            {botones[botonSeleccionado]}
          </div>
        )}
        {small && !isPopover && (
          <div style={{ fontSize: "small", height: "10%" }}>
            Pulsa el botón "Ver plano" para una vista más detallada
          </div>
        )}
        <div style={{ width: widthPlano, height: heightPlano }}>
          {" "}
          {/* 70% */}
          {(plano === Planos.Anexo_B_1 || plano === Planos.Anexo_B_2) && (
            <Anexo_B_1 contenido={contenido} plano={plano} theme={theme} />
          )}
          {plano === Planos.Fermin_Caballero_B && (
            <Planta_Baja contenido={contenido} theme={theme} />
          )}
          {plano === Planos.Fermin_Caballero_1 && (
            <Planta_1 contenido={contenido} theme={theme} />
          )}
          {plano === Planos.Fermin_Caballero_2 && (
            <Planta_2 contenido={contenido} theme={theme} />
          )}
        </div>
        {!small && renderLegend(numColores, liActual, lsActual, unidadActual)}{" "}
        {/* 5% */}
        {small && !isPopover && (
          <div>
            <Button
              onClick={mostrarPlanoEnPopover}
              variant="contained"
              color="primary"
              style={{
                textTransform: "none",
              }}
            >
              Ver plano
            </Button>
            {/* <button onClick={mostrarPlanoEnPopover} style={{backgroundColor: theme.palette.primary.main}}>Ver plano</button> */}
          </div>
        )}
        <InfoBox info={infoAula} anchorEl={anchorEl} onClose={handleClose} />
      </div>
    );
  };

  const renderPopoverContent = () => (
    <div
      style={{
        width: "600px",
        height: "800px",
        padding: "20px",
        backgroundColor: "white",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
      }}
    >
      {renderPlano(false)}
    </div>
  );

  return (
    // {isSmall && mostrandoPopover && ( Mostrar el plano en un popover de forma que se vea grande y se pueda interactuar con él
    //   <Popover>{renderPlano()}</Popover>
    // )}
    <div style={{ height: "100%", width: "100%" }}>
      {renderPlano(isSmall)}
      <PlanoPopover
        isSmall={false}
        popoverOpen={popoverOpen}
        setPopoverOpen={setPopoverOpen}
        theme={theme}
      />

      {/* <Popover
        open={popoverOpen}
        anchorEl={popoverAnchor}
        onClose={handlePopoverClose}
        anchorOrigin={{
          vertical: 'center',
          horizontal: 'center',
        }}
        transformOrigin={{
          vertical: 'center',
          horizontal: 'center',
        }}
      >
        {renderPlano(false, true)}
      </Popover> */}
    </div>
  );

  //   <div
  //     style={{
  //       position: "relative",
  //       top: 0,
  //       left: 0,
  //       width: "100%",
  //       height: "100%",
  //       backgroundColor: "white",
  //       zIndex: 1, // Para que esté detrás del SVG
  //       display: "flex",
  //       justifyContent: "center",
  //       alignItems: "center",
  //       flexDirection: "column",
  //     }}
  //   >
  //     {/* Mostrar botones */}
  //     {!isSmall && (
  //     <div style={{ marginTop:"2%", marginBottom: "2%"  }}>{/* 20px */}
  //       {botones.map((nombre, index) => (
  //         <button
  //           key={index}
  //           onClick={() => handleBotonClick(index)}
  //           style={{
  //             marginRight: "10px",
  //             backgroundColor: index === botonSeleccionado ? "blue" : "gray",
  //             color: "white",
  //           }}
  //         >
  //           {nombre}
  //         </button>
  //       ))}
  //     </div>
  //     )}
  //     {/* Mostrar iconos */}
  //     {!isSmall && (
  //     <div
  //       style={{
  //         marginBottom: "2%", //20px
  //       }}
  //     >
  //       {Object.values(atributosPlano).map((atributo, index) => (
  //         <Tooltip title={atributo.nombre} key={index}>
  //           <IconButton
  //             variant="contained"
  //             style={{
  //               marginLeft: "10px",
  //               backgroundColor: index === iconoSeleccionado ? "blue" : "gray",
  //               color: "white",
  //             }}
  //             onClick={() => handleIconoClick(index)}
  //           >
  //             {getIconComponent(atributo.icono)}
  //           </IconButton>
  //         </Tooltip>
  //       ))}
  //     </div>
  //     )}
  //     <div style={{width: "75%", height: "75%"}}>
  //       <Anexo_B_1 contenido={contenido} plano={plano} />
  //     </div>
  //     {isSmall && (
  //       <div>
  //       <button onClick={mostrarPlanoEnPopover} style={{marginTop: "2%"}}>Siguiente</button>
  //       <p style={{marginTop: "2%"}}>Para ver el plano adecuadamente pulsa el botón</p>
  //       </div>
  //       )}
  //     <InfoBox info={infoAula} anchorEl={anchorEl} onClose={handleClose}/>
  //   </div>
  //   // <div id="svg-container" dangerouslySetInnerHTML={{ __html: planosMap[plano] }} />
  // );
};

export default PlanosComponent;
