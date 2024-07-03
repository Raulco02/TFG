import React, { useRef, useState, useEffect } from "react";
import {
  Tarjetas,
  Posiciones,
  Layouts,
} from "../resources/enums/enums";
import { createCardForm } from "../resources/Interfaces/interfaces";
import {
  TypeTarjetas,
  tarjetaTexto,
  tarjetaEstado,
  tarjetaGrafico,
  tarjetaImagen,
  tarjetaPlano
} from "../resources/Interfaces/tarjetas";
import Texto from "./Tarjetas/Texto";
import Imagen from "./Tarjetas/Imagen";
import Estado from "./Tarjetas/Estado";
import FormularioTarjeta from "./Formularios/FormularioTarjeta";
import AddCircleOutlineIcon from "@mui/icons-material/AddCircleOutline";
import EditIcon from "@mui/icons-material/Edit";
import { set } from "react-hook-form";
import tarjetaService from "../services/tarjetaService";
import dispositivoService from "../services/dispositivoService";
import Termostato from "./Tarjetas/Termostato";
import Grafico from "./Tarjetas/Grafico";
import { Button, useTheme } from "@mui/material";
import seccionService from "../services/seccionService";
import PlanosComponent from "./Tarjetas/Plano";

const SeccionGrid = ({
  items,
  editando = false,
  id_seccion,
  layout,
  numFilas,
  setPopoverOpen,
  setPopoverMessage,
  setItems
}) => {
  const [hoveredCell, setHoveredCell] = useState(null);
  const [mostrandoFormulario, setMostrandoFormulario] = useState(false);
  const [posicion, setPosicion] = useState<Posiciones>(null);
  const [numeroFilas, setNumeroFilas] = useState(3);
  const [filaNueva, setFilaNueva] = useState(false);
  const [celdaVacia, setCeldaVacia] = useState(null);
  const [selectedItem, setSelectedItem] = useState(null);

  const theme = useTheme();

  useEffect(() => {
    modifyItems();
    console.log("Items: ", items);
  }, [items]);

  useEffect(() => {
    setNumeroFilas(numFilas);
  }, [numFilas]);

  useEffect(() => {
    if (editando) {
      const celda = findPrimeraCeldaVacia();
      if (celda) {
        setCeldaVacia(celda);
      } else {
        const nuevaFila = numeroFilas + 1;
        setNumeroFilas(nuevaFila);
        setFilaNueva(true);
        setCeldaVacia(`$${nuevaFila - 1}x0`);
      }
    } else {
      setCeldaVacia(null);
      if (filaNueva === true) setNumeroFilas(numeroFilas - 1);
      setFilaNueva(false);
    }
  }, [editando, items, numeroFilas, id_seccion, layout]);

  useEffect(() => {
    console.log("celda vacia", celdaVacia);
  }, [celdaVacia]);

  const findPrimeraCeldaVacia = () => { //No se si la parte de layout === Layouts.Card y Layouts.Sidebar estan bien
    if (layout === Layouts.Card) {
      const cellIsEmpty = items.every((item) => item.posicion !== "0x0");
      if (cellIsEmpty) {
        return "0x0";
      }
    }
    else if (layout === Layouts.Sidebar) {
      for (let i = 0; i < 2; i++) {
        for (let j = 0; j < numeroFilas; j++) {
          const cellIsEmpty = items.every(
            (item) => item.posicion !== `${j}x${i}`
          );
          if (cellIsEmpty) {
            return `${j}x${i}`;
          }
        }
      }
    }
    else if(layout === Layouts.Grid){
      for (let i = 0; i < numeroFilas; i++) {
        for (let j = 0; j < 3; j++) {
          const cellIsEmpty = items.every(
            (item) => item.posicion !== `${i}x${j}`
          );
          if (cellIsEmpty) {
            return `${i}x${j}`;
          }
        }
      }
    }
    return null;
  };

  const modifyItems = async () => {
    for (const item of items) {
      if (item.tipo === Tarjetas.Estado || item.tipo === Tarjetas.Termostato) {
        console.log("Item:", item);
        const id_dispositivo = item["id-dispositivo"];
        try {
          console.log("ID dispositivo:", id_dispositivo);
          const dispositivo = await getDispositivo(id_dispositivo);
          if (dispositivo.length > 0 && dispositivo[0].atributos) {
            const attribute = dispositivo[0].atributos.find(
              (atributo) => atributo["nombre-atributo"] === item.atributo
            );
            if (attribute) {
              item.atributo = attribute;
            } else {
              console.error(
                `No se encontró el atributo '${item.atributo}' para el dispositivo '${item["id-dispositivo"]}'`
              );
            }
          } else {
            console.error(
              "No se encontraron atributos para el dispositivo",
              dispositivo
            );
          }
        } catch (error) {
          console.error("Error fetching device:", error);
        }
        console.log("Item:", item);
      }
    }
  };

  const handleCellClick = (row, col) => {
    console.log(`Celda clickeada: ${row} - ${col}`);
    console.log(`Editando: ${editando}`);
    const nuevaPosicion = `${row}x${col}`;

    // Verificar si la posición es válida
    //if (Object.values(Posiciones).includes(nuevaPosicion as Posiciones)) {
    setPosicion(nuevaPosicion); // VER SI HAY ALGUNA FORMA DE SOLUCIONAR ESTO
    //} else {
    //console.error('La posición proporcionada no es válida');
    //}
    setMostrandoFormulario(true);
  };

  const handleEditButtonClick = (id) => {
    console.log(`Botón de edición clickeado en la celda ${id}`);
  };

  const generateGrid = () => {
    const grid = [];
    if (layout === Layouts.Grid) {
      for (let i = 0; i < numeroFilas; i++) {
        const row = [];
        for (let j = 0; j < 3; j++) {
          row.push(<Cell key={`${i}-${j}`} row={i} col={j} theme={theme}/>);
        }
        grid.push(row);
      }
    } else if (layout === Layouts.Card) {
      const row = [];
      row.push(<Cell key={`0-0`} row={0} col={0} theme={theme}/>);
      grid.push(row);
    } else if (layout === Layouts.Sidebar) {
      for (let i = 0; i < 2; i++) {
        const col = [];
        if (i === 0) {
          col.push(<Cell key={`0-${i}`} row={0} col={i} theme={theme}/>);
        } else {
          for (let j = 0; j < numeroFilas; j++) {
            col.push(<Cell key={`${j}-${i}`} row={j} col={i} theme={theme} />);
          }
        }
        grid.push(col);
      }
    }
    return grid;
  };

  async function getDispositivo(id_dispositivo: string) {
    console.log("ID dispositivo:", id_dispositivo);
    try {
      const dispositivo = await dispositivoService.getDispositivo(
        id_dispositivo
      );
      return dispositivo;
    } catch (error) {
      console.error("Error fetching", id_dispositivo, "devices:", error);
    }
  }
  const handleSubmit = async (data: createCardForm) => {
    console.log("Datos del formulario:", data);
    console.log("", id_seccion);
    console.log("POSICION", posicion);
    const dimension = `${data.filas}x${data.columnas}`;
    if (filaNueva === true) {
      try {
        await seccionService.subirFilas({ id: id_seccion }); //Esto sube las filas pero si hay error se queda subido
      } catch (error) {
        console.error("Error:", error);
      }
    }
    let datos: TypeTarjetas;
    try{
    switch (data.tipo) {
      case Tarjetas.Texto:
        datos = {
          tipo: data.tipo,
          id_seccion: id_seccion,
          posicion: posicion,
          contenido: data.contenido,
        };
        console.log("Datos", datos);
        tarjetaService.createTexto(datos);
        break;
      case Tarjetas.Imagen:
        console.log("Imagen");
        console.log(data.imagen);
        datos = {
          tipo: data.tipo,
          id_seccion: id_seccion,
          posicion: posicion,
          imagen: data.imagen,
        };
        console.log("Datos", datos);
        tarjetaService.createImagen(datos);
        break;
      case Tarjetas.Estado:
        console.log("Data de crear estado", data);
        console.log("Dispositivo", data.dispositivo);
        console.log(data.id_atributo);
        console.log(data.id_dispositivo);
        const id_dispositivo = [];
        const id_atributo = [];
        for (let i = 0; i < data.atributos; i++) {
          const dispositivoKey = `id_dispositivo${i}`;
          const atributoKey = `id_atributo${i}`;

          if (Object.prototype.hasOwnProperty.call(data, dispositivoKey)) {
            id_dispositivo.push(data[dispositivoKey]);
          }

          if (Object.prototype.hasOwnProperty.call(data, atributoKey)) {
            id_atributo.push(data[atributoKey]);
          }
        }
        datos = {
          tipo: data.tipo,
          id_seccion: id_seccion,
          posicion: posicion,
          id_dispositivo: id_dispositivo,
          id_atributo: id_atributo,
        };
        console.log("Datos", datos);
        tarjetaService.createEstado(datos);
        break;
      case Tarjetas.Termostato:
        console.log("Termostato");
        datos = {
          tipo: data.tipo,
          id_seccion: id_seccion,
          posicion: posicion,
          id_dispositivo: data.id_dispositivo,
          id_atributo: data.id_atributo,
        };
        console.log("Datos", datos);
        tarjetaService.createTermostato(datos);
        break;
      case Tarjetas.Grafico:
        console.log("Grafico");
        datos = {
          tipo: data.tipo,
          id_seccion: id_seccion,
          posicion: posicion,
          id_dispositivos: data.dispositivos,
          id_atributo: data.id_atributo,
          tipo_grafico: data.tipoGrafico,
          tiempo_grafico: data.tiempoGrafico,
        };
        console.log("Datos", datos);
        tarjetaService.createGrafico(datos);
        break;
      case Tarjetas.Plano:
        console.log("Plano");
        datos = {
          tipo: data.tipo,
          id_seccion: id_seccion,
          posicion: posicion,
        };
        console.log("Datos", datos);
        tarjetaService.createPlano(datos);
        break;
      case Tarjetas.Grupo:
        console.log("Grupo");
        datos = {
          tipo: data.tipo,
          id_seccion: id_seccion,
          posicion: posicion,
          id_grupo: data.id_grupo,
        };
        console.log("Datos", datos);
        tarjetaService.createTarjetaGrupo(datos);
        break;
      default:
        console.log("Error");
        break;
      }
      setPopoverMessage("Tarjeta creada exitosamente");
      setPopoverOpen(true);
      console.log("ID seccion", id_seccion)
      const newItems = await tarjetaService.getTarjetas(id_seccion);
      setItems(newItems);
      console.log("Items:", newItems);
    }catch (error) {
      console.error("Error:", error);
      setPopoverMessage("Error al crear la tarjeta", error);
      setPopoverOpen(true);
    }
    setMostrandoFormulario(false);
  };

  const handleClose = () => {
    setMostrandoFormulario(false);
  };

  const Cell = ({ row, col, theme }) => {
    const [filas, setFilas] = useState(1);
    const [columnas, setColumnas] = useState(1);
    const [isSmall, setIsSmall] = useState(false); //Controlar el tipo de celda que es, si es pequeña de grid o de sidebar

    useEffect(() => {
      if (layout === Layouts.Sidebar) {
        setFilas(numeroFilas);
        setColumnas(1);
      } else if (layout === Layouts.Card) {
        setFilas(3);
        setColumnas(3);
      } else {
        setFilas(1);
        setColumnas(1);
        setIsSmall(true);
      }
    }, [layout]);

    useEffect(() => {
      if (!editando && hoveredCell) {
          setHoveredCell(null);
      }
    }, [editando]);

    const cellIsEmpty = items.every(
      (item) => item.posicion !== `${row}x${col}`
    );

    const handleMouseEnter = () => {
      if (editando) {
        setHoveredCell({ row, col });
      }
    };

    const handleMouseLeave = () => {
      if (editando) {
        setHoveredCell(null);
      }
    };

    const handleClick = () => {
      handleCellClick(row, col);
    };

    const handleEditClick = (item) => {
      console.log('Item a editar:', item);
      handleEditButtonClick(item.id);
      setSelectedItem(item);
      setMostrandoFormulario(true);
    };

    const esPrimeraCeldaVacia = celdaVacia === `${row}x${col}`;

    return (
      <div
        style={{
          // border: editando ? "1px solid black" : "",
          margin: "10px",
          minHeight: layout === Layouts.Grid ? "95%" : "95%",
          minWidth: layout === Layouts.Grid ? "95%" : "98%",
          height: layout === Layouts.Grid ? "95%" : "95%",
          width: layout === Layouts.Grid ? "95%" : "95%",
          // height: "176.33px",
          // width: "425.33px",
          transition: "transform 0.2s",
          transform:
            hoveredCell && hoveredCell.row === row && hoveredCell.col === col
              ? "scale(1.05)"
              : "scale(1)",
          overflow: "hidden",
          gridRow:
            (layout === Layouts.Grid && window.innerWidth <= 768)
              ? (row === 0) ? `${row + 1 + col} / span ${filas}` : `${(row*3) + 1 + col} / span ${filas}`
              : (layout === Layouts.Sidebar && window.innerWidth <= 768)
              ? `${row + col + 1} / span ${1}`
              : ((layout === Layouts.Sidebar && window.innerWidth > 768 && col === 0) || layout === Layouts.Card)
              ? `${row + 1} / span ${filas}`
              : `${row + 1} / span ${1}`,
          gridColumn:
            (layout === Layouts.Grid && window.innerWidth <= 768)
              ? `${1} / span ${columnas}`
              : (layout === Layouts.Sidebar && window.innerWidth <= 768) 
              ? `${1} / span ${1}`
              : (layout === Layouts.Sidebar && window.innerWidth > 768 && col === 0)
              ? `${col + 1} / span ${columnas}`
              : `${col + 1} / span ${1}`,
          // gridRow: `${row + 1} / span ${filas}`,
          // gridColumn: `${col + 1} / span ${columnas}`,
        }}
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
        onClick={handleClick}
      >
        {items.map((item) => {
          const [itemRow, itemCol] = item.posicion.split("x").map(Number);
         
          //
          if (itemRow === row && itemCol === col) {
            return (
              <div
                key={item.id}
                className="custom-scrollbar"
                style={{
                  width: "auto",
                  height: "100%",
                  borderRadius: "10px", // Ajusta el valor según el redondeo que desees
                  boxShadow: "0 0 10px rgba(0, 0, 0, 0.1)", // Ajusta el valor según la sombra deseada
                  // padding: "10px", // Ajusta el valor según el espacio interno deseado
                  backgroundColor: theme.palette.background.paper, // Ajusta el valor según el color deseado
                  color: theme.palette.primary.text, // Ajusta el valor según el color deseado
                  overflowY: item.tipo === Tarjetas.Estado || Tarjetas.Grupo ? "auto" : "hidden",
                  //margin: "5px", // Ajusta el valor según el espacio entre tarjetas deseado
                }}
              >
                {item.tipo === Tarjetas.Texto ? (
                  <Texto contenido={item.contenido} />
                ) : item.tipo === Tarjetas.Imagen ? (
                  <Imagen enlace={item.imagen} />
                ) : (item.tipo === Tarjetas.Estado || item.tipo === Tarjetas.Grupo) ? (
                  <Estado
                    valor={item.valor}
                    nombreAtributo={item["nombre-atributo"]}
                    nombreDispositivo={item["nombre-dispositivo"]}
                    iconos={item.iconos}
                    unidad={item.unidades}
                    grupo={item.tipo === Tarjetas.Grupo ? item.grupo : null}
                    icono_grupo={item.tipo === Tarjetas.Grupo ? item['icono-grupo'] : null}
                    id_grupo={item.tipo === Tarjetas.Grupo ? item['id-grupo'] : null}
                    theme={theme}

                  />
                ) : item.tipo === Tarjetas.Termostato ? (
                  <Termostato
                    valorInicial={item.valor}
                    nombreAtributo={item["nombre-atributo"]}
                    nombreDispositivo={item["nombre-dispositivo"]}
                    idDispositivo={item["id-dispositivo"]}
                    idAtributo={item["id-atributo"]}
                    unidad={item.unidades}
                    theme={theme}
                  />
                ) : item.tipo === Tarjetas.Grafico ? (
                  <Grafico item={item} />
                ) : // <div>
                //   <p>Grafico</p>
                // </div>
                item.tipo === Tarjetas.Plano ? (
                  <PlanosComponent isSmall={isSmall} theme={theme}/>
                ) : // <div>
                //   <p>Grafico</p>
                // </div>
                null}
                {!cellIsEmpty && editando && (
                  <div
                    style={{
                      textAlign: "center",
                      position: "absolute",
                      bottom: "8px",
                      right: "8px",
                      display: "flex",
                      gap: "8px",
                    }}
                  >
                    <button
                      onClick={() => handleEditClick(item)}
                      style={{ color: "white", backgroundColor: "grey" }}
                    >
                      <EditIcon />
                    </button>
                  </div>
                )}
              </div>
            );
          }
          return null;
        })}
        {editando && cellIsEmpty && esPrimeraCeldaVacia && (
          <div
            onClick={handleEditClick}
            style={{
              textAlign: "center",
              width: "100%",
              height: "100%",
              borderRadius: "10px", // Ajusta el valor según el redondeo que desees
              boxShadow: "0 0 10px rgba(0, 0, 0, 0.1)", // Ajusta el valor según la sombra deseada
              padding: "10px", // Ajusta el valor según el espacio interno deseado
              backgroundColor: theme.palette.background.paper,
            }}
          >
            <div
              style={{
                position: "absolute",
                bottom: "8px",
                right: "8px",
                display: "flex",
                gap: "8px",
              }}
            >
              <button
                onClick={handleEditClick}
                style={{ color: "white", backgroundColor: "grey" }}
              >
                <AddCircleOutlineIcon />
              </button>
            </div>
          </div>
        )}
      </div>
    );
  };

  const grid = generateGrid();

  // const onMasFilasClick = async () => {
  //   try{
  //     await seccionService.subirFilas({"id": id_seccion})
  //   }catch (error) {
  //     console.error("Error:", error);
  //   }
  // };
  const generateFilasString = () => {
    let filasString;
    console.log("Numero de filas", numeroFilas)
    if(layout === Layouts.Grid && window.innerWidth < 768){
      filasString = Array(numeroFilas*3).fill("33%").join(" ");
    }
    else if(layout === Layouts.Sidebar && window.innerWidth < 768){
      filasString = Array(numeroFilas).fill("33%").join(" ");
    }
    else{
      filasString = Array(numeroFilas).fill("33%").join(" ");
    }
    return filasString;
  };

  return (
    <div style={{ width: "100%", height: "100%" }}>
      {editando && mostrandoFormulario && (
        <div style={{ textAlign: "center" }}>
          <FormularioTarjeta submit={handleSubmit} onClose={handleClose} editingItem={selectedItem} />
        </div>
      )}
      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            (layout === Layouts.Grid && window.innerWidth > 768)
              ? "1fr 1fr 1fr"
              : layout === Layouts.Card
              ? "1fr"
              : (layout === Layouts.Sidebar && window.innerWidth > 768)
              ? "66% 33%"
              : "1fr",
          gridTemplateRows: generateFilasString(), //layouts === Layouts.Sidebar ? "1fr 1fr 1fr" : "1fr 1fr 1fr",
          width: "100%",
          height: "100%",
        }}
      >
        {grid.map((row, rowIndex) => (
          <React.Fragment key={rowIndex}>
            {row.map((cell, colIndex) => (
              <React.Fragment key={`${rowIndex}-${colIndex}`}>
                {cell}
              </React.Fragment>
            ))}
          </React.Fragment>
        ))}

        {/* {editando && (
          <Button
          sx={{
            display: 'flex',
            gridColumn: 'span 3',
            alignItems: 'center',
            justifyContent: 'center',
            '&::before': {
              content: "''",
              flex: 1,
              borderBottom: '1px solid #1976D2',
              marginRight: '8px',
            },
            '&::after': {
              content: "''",
              flex: 1,
              borderBottom: '1px solid #1976D2',
              marginLeft: '8px',
            },
          }}
          onClick={onMasFilasClick}
        >
          <AddCircleOutlineIcon />
        </Button>
        )} */}
      </div>
    </div>
  );
};

export default SeccionGrid;
