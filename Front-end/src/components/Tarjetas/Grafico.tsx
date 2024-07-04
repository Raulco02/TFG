import React, { useState, useEffect } from 'react';
import { TipoGrafico, TiempoGrafico } from '../../resources/enums/enums';
import dispositivoService from '../../services/dispositivoService';
import SensorChart from './GraficoPrueba';
import dayjs from 'dayjs';

const Grafico = ({ item }) => {
    const [tipo, setTipo] = useState(TipoGrafico.Lineal);
    const [tiempoGrafico, setTiempoGrafico] = useState(TiempoGrafico.Dia);
    const [idAtributo, setIdAtributo] = useState();
    const [nombreAtributo, setNombreAtributo] = useState('');
    const [idDispositivos, setIdDispositivos] = useState([]);
    const [nombreDispositivo, setNombreDispositivo] = useState();
    const [fechaInicio, setFechaInicio] = useState();
    const [fechaFin, setFechaFin] = useState();
    const [unidad, setUnidad] = useState('');
    const [data, setData] = useState([]);

    useEffect(() => {
        console.log("Item del grafico: ", item);

        const tiempoGraficoAct = item['tiempo-grafico'];
        console.log("Tiempo grafico: ", tiempoGraficoAct);

        const idAtributoAct = [item['id-atributo'][0]];
        const unidadAct = item['unidades'];
        const idDispositivosAct = item['id-dispositivo'];
        const nombreAtributoAct = item['nombre-atributo'];
        const nombreDispositivoAct = item['nombre-dispositivo'];
        const tipoAct = item['tipo-grafico'];
        const fechaInicioAct = obtenerMarcaDeTiempo(tiempoGraficoAct);
        const fechaFinAct = formatearFecha(new Date());

        setTiempoGrafico(tiempoGraficoAct);
        setIdAtributo(idAtributoAct);
        setIdDispositivos(idDispositivosAct || []);
        setNombreAtributo(nombreAtributoAct[0]);
        setNombreDispositivo(nombreDispositivoAct);
        setFechaInicio(fechaInicioAct);
        setFechaFin(fechaFinAct);
        setUnidad(unidadAct);
        setTipo(tipoAct);

        console.log("Tipo de grafico: ", tipoAct);

        const fetchData = async () => {
            try {
                console.log('Fetching data with params:', { fechaInicioAct, fechaFinAct, idDispositivosAct, nombreAtributoAct });
                const response = await dispositivoService.getValoresSensores(nombreAtributoAct, fechaInicioAct, fechaFinAct, idDispositivosAct);
                console.log('Raw data fetched:', response);
                const formattedSensorData = formatSensorData(response, nombreAtributoAct[0]);
                console.log('Formatted sensor data:', formattedSensorData);
                setData(formattedSensorData);
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };
        fetchData();
    }, []);

    const formatearFecha = (fecha) => {
        return dayjs(fecha).format('DD-MM-YYYY HH:mm:ss');
    };

    const obtenerMarcaDeTiempo = (valor) => {
        const ahora = new Date();
        console.log("Ahora: ", formatearFecha(ahora))
        console.log("Valor: ", valor)
        let marcaDeTiempo;
        switch (valor) {
            case TiempoGrafico.Dia:
                marcaDeTiempo = new Date(ahora.getTime() - 24 * 60 * 60 * 1000);
                break;
            case TiempoGrafico.Semana:
                marcaDeTiempo = new Date(ahora.getTime() - 7 * 24 * 60 * 60 * 1000);
                break;
            case TiempoGrafico.Mes:
                marcaDeTiempo = new Date(ahora.getTime() - 30 * 24 * 60 * 60 * 1000);
                break;
            case TiempoGrafico.TMeses:
                marcaDeTiempo = new Date(ahora.getTime() - 90 * 24 * 60 * 60 * 1000);
                break;
            case TiempoGrafico.Anio:
                marcaDeTiempo = new Date(ahora.setFullYear(ahora.getFullYear() - 1));
                break;
            default:
                marcaDeTiempo = ahora;
                break;
        }
        console.log("Marca de tiempo: ", formatearFecha(marcaDeTiempo));
        return formatearFecha(marcaDeTiempo);
    };

    const formatSensorData = (data, nAtributo) => {
        const formattedData = [];
        data.forEach(entry => {
            const { timestamp, attributes, dispositivo } = entry;
            console.log(nAtributo)
            if (attributes && attributes[nAtributo] !== undefined) {
                console.log(nAtributo, attributes[nAtributo]);
                formattedData.push({
                    timestamp: dayjs(timestamp).format('YYYY-MM-DDTHH:mm:ss[Z]'),
                    dispositivo: dispositivo,
                    value: attributes[nAtributo]
                });
            } else {
                console.warn(`El atributo ${nAtributo} no está definido en: `, entry);
            }
        });
        return formattedData;
    };

    useEffect(() => {
        console.log("Tipo antes de renderizar SensorChart: ", tipo);
        console.log("Data antes de renderizar SensorChart: ", data);
        console.log("unidad antes", unidad[0])
    }, [tipo, data, unidad]);

    return (
        <div style={{height:"100%", width:"100%", padding:"6%"}}>
            <div style={{fontWeight: "bold"}}>{nombreAtributo}</div>
            <SensorChart data={data} tipo={tipo} tiempoGrafico={tiempoGrafico} unidad={unidad[0]} />
        </div>
    );
};

export default Grafico;
