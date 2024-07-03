import React, { useRef, useEffect, useState } from "react";
import { getIconComponent } from "../utils/iconUtils";
import { IconName, Layouts } from "../resources/enums/enums";
import FormularioSeccion from "./Formularios/FormularioSeccion";
import { AppBar, Button, IconButton } from "@mui/material";
import ArrowBackIosIcon from '@mui/icons-material/ArrowBackIos';
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import { get } from "react-hook-form";

const Seccionbar = ({
  secciones = [],
  setSelectedSeccion,
  crearSeccion,
  setItems,
  className,
  editando = false
}) => {
  const containerRef = useRef(null);
  const [showScrollLeft, setShowScrollLeft] = useState(false);
  const [showScrollRight, setShowScrollRight] = useState(false);
  const [editandoSeccion, setEditandoSeccion] = useState(false);
  const [seccionEditada, setSeccionEditada] = useState({'layout': '', 'nombre': ''});

  useEffect(() => {
    const updateScrollButtons = () => {
      if (containerRef.current) {
        const { scrollLeft, scrollWidth, clientWidth } = containerRef.current;
        setShowScrollLeft(scrollLeft > 0);
        setShowScrollRight(scrollLeft + clientWidth < scrollWidth);
      }
    };

    updateScrollButtons();
    window.addEventListener("resize", updateScrollButtons);
    containerRef.current.addEventListener("scroll", updateScrollButtons);

    return () => {
      window.removeEventListener("resize", updateScrollButtons);
      if (containerRef.current) {
        containerRef.current.removeEventListener("scroll", updateScrollButtons);
      }
    };
  }, [secciones]);

  const handleScrollRight = () => {
    if (containerRef.current) {
      containerRef.current.scrollBy({ left: 200, behavior: 'smooth' });
    }
  };

  const handleScrollLeft = () => {
    if (containerRef.current) {
      containerRef.current.scrollBy({ left: -200, behavior: 'smooth' });
    }
  };

  const showCreateSeccionButton = secciones.length < 10;
  const createSeccionButton = getIconComponent(IconName.Add);

  const editarSeccion = (seccion) => () => {
    console.log("Editando sección", seccion);
    console.log("Layout de la sección", seccion.layout);
    console.log(Layouts.Grid);
    const layout = seccion.layout;
    if(layout === Layouts.Grid) setSeccionEditada({'layout': "Grid", 'nombre': seccion.nombre});
    if(layout === Layouts.Card) setSeccionEditada({'layout': "Card", 'nombre': seccion.nombre});
    if(layout === Layouts.Sidebar) setSeccionEditada({'layout': "Sidebar", 'nombre': seccion.nombre});
    setEditandoSeccion(true);
  };

  const handleCloseEdit = () => {
    setEditandoSeccion(false);
    setSeccionEditada({'layout': '', 'nombre': ''});
  };

  const onSubmitEditSeccion = (data) => {
    console.log("Sección editada", data); //HAY QUE ENVIARLO
    setEditandoSeccion(false);
    setSeccionEditada({'layout': '', 'nombre': ''});
  };

  console.log(showScrollRight, "Show Scroll Right")

  return (
    <AppBar position="static" className={className}>
      <div className="seccionbar-container">
        {showScrollLeft && (
          <Button className="scroll-button left" onClick={handleScrollLeft}>
            <ArrowBackIosIcon sx={{color:'white'}}/>
          </Button>
        )}
        <div className="seccionbar-content" ref={containerRef}>
          {secciones.map((result, index) => (
            <>
            <Button
              key={index}
              color="inherit"
              onClick={() => { setSelectedSeccion(result); setItems(result.tarjetas); }}
              style={{ whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', minWidth: 'max-content' }}
            >
              {result.nombre}
            </Button>
            {editando && (<IconButton color="inherit" onClick={editarSeccion(result)}>{getIconComponent(IconName.Edit)}</IconButton>)}
            </>
          ))}
          {showCreateSeccionButton && editando && (
            <IconButton color="inherit" onClick={crearSeccion}>
              {createSeccionButton}
            </IconButton>
          )}
        </div>
        {showScrollRight && (
          <Button className="scroll-button right" onClick={handleScrollRight}>
            <ArrowForwardIosIcon sx={{color: 'white'}}/>
          </Button>
        )}
        {editandoSeccion && (
          <FormularioSeccion onClose={handleCloseEdit} submit={onSubmitEditSeccion} layout={seccionEditada.layout} nombre={seccionEditada.nombre}/>
        )}
      </div>
    </AppBar>
  );
};

export default Seccionbar;
