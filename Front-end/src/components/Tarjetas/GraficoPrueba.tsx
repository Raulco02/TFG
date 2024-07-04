// src/components/dispositivoChart.tsx

import React, { useEffect } from 'react';
import { ResponsiveContainer, LineChart, BarChart, PieChart, Pie, Cell, Bar, Line, XAxis, YAxis, Tooltip, CartesianGrid, Legend } from 'recharts';
import dayjs from 'dayjs';
import { TipoGrafico, TiempoGrafico } from '../../resources/enums/enums';

interface dispositivoData {
  timestamp: string;
  value: number;
  dispositivo: string;
}

interface dispositivoChartProps {
  data: dispositivoData[];
  tipo: TipoGrafico;
  tiempoGrafico: TiempoGrafico;
  unidad?: string;
}

// Paleta de colores predefinida
const colors = [
  "#8884d8", "#82ca9d", "#ffc658", "#ff8042", "#8dd1e1",
  "#d0ed57", "#a4de6c", "#d0ed57", "#ffc0cb", "#b0e0e6"
];

const dispositivoChart: React.FC<dispositivoChartProps> = ({ data, tipo, tiempoGrafico, unidad='' }) => {
  useEffect(() => {
    console.log("Data: ", data);
    console.log("Tipo: ", tipo);
    console.log("Tiempo grafico: ", tiempoGrafico);
  }, [data, tipo, tiempoGrafico]);
  const endDate = dayjs();
  let unit: 'hour' | 'day' | 'month';
  let length: number;
  let format: string;

  switch (tiempoGrafico) {
    case TiempoGrafico.Dia:
      unit = 'hour';
      length = 24;
      format = 'YYYY-MM-DD HH';
      break;
    case TiempoGrafico.Semana:
      unit = 'day';
      length = 7;
      format = 'YYYY-MM-DD';
      break;
    case TiempoGrafico.Mes:
      unit = 'day';
      length = 30;
      format = 'YYYY-MM-DD';
      break;
    case TiempoGrafico.TMeses:
      unit = 'day';
      length = 90;
      format = 'YYYY-MM-DD';
      break;
    case TiempoGrafico.Anio:
      unit = 'month';
      length = 12;
      format = 'YYYY-MM';
      break;
  }

  const dates = Array.from({ length }, (_, i) => endDate.subtract(i, unit).format(format)).reverse();

  const dispositivos = Array.from(new Set(data.map(d => d.dispositivo)));

  const dispositivoMap: { [key: string]: { [key: string]: number[] } } = {};
  dates.forEach(date => {
    dispositivoMap[date] = {};
    dispositivos.forEach(dispositivo => {
      dispositivoMap[date][dispositivo] = [];
    });
  });

  data.forEach(({ timestamp, value, dispositivo }) => {
    const date = dayjs(timestamp).format(format);
    if (dispositivoMap[date]) {
      dispositivoMap[date][dispositivo].push(value);
    }
  });

  const chartData = dates.map(date => {
    const entry: { date: string; [key: string]: number | null } = { date };
    dispositivos.forEach(dispositivo => {
      const values = dispositivoMap[date][dispositivo];
      entry[dispositivo] = values.length ? values.reduce((a, b) => a + b, 0) / values.length : null;
    });
    return entry;
  });

  const dispositivoColors = dispositivos.reduce<{ [key: string]: string }>((acc, dispositivo, index) => {
    acc[dispositivo] = colors[index % colors.length];
    return acc;
  }, {});

  const tooltipFormatter = (value: number) => `${value.toFixed(2)} ${unidad}`;

  const renderLineChart = () => (
    <ResponsiveContainer height='100%' width='100%'>
      <LineChart data={chartData}>
    {/* <LineChart width={1000} height={500} data={chartData}> */}
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="date" />
      <YAxis label={{ value: unidad, angle: -90, position: 'insideLeft' }}/>
      <Tooltip formatter={tooltipFormatter}/>
      <Legend />
      {dispositivos.map(dispositivo => (
        <Line
          key={dispositivo}
          type="monotone"
          dataKey={dispositivo}
          stroke={dispositivoColors[dispositivo]}
          activeDot={{ r: 8 }}
          connectNulls={true}
        />
      ))}
    </LineChart>
    </ResponsiveContainer>
  );

  const renderBarChart = () => (
    <ResponsiveContainer height="100%" width="100%">
      <BarChart data={chartData}> 
    {/* <BarChart width={1000} height={500} data={chartData}> */}
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="date" />
      <YAxis label={{ value: unidad, angle: -90, position: 'insideLeft' }}/>
      <Tooltip formatter={tooltipFormatter}/>
      <Legend />
      {dispositivos.map(dispositivo => (
        <Bar key={dispositivo} dataKey={dispositivo} fill={dispositivoColors[dispositivo]} />
      ))}
    </BarChart>
    </ResponsiveContainer>
  );

  const renderPieChart = () => {
    const pieData = dispositivos.map(dispositivo => {
      const total = chartData.reduce((sum, entry) => sum + (entry[dispositivo] || 0), 0);
      return { name: dispositivo, value: total };
    });

    return (
      <PieChart width={500} height={500}>
        <Pie
          data={pieData}
          dataKey="value"
          nameKey="name"
          cx="50%"
          cy="50%"
          outerRadius={200}
          fill="#8884d8"
          label
        >
          {pieData.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
          ))}
        </Pie>
        <Tooltip formatter={tooltipFormatter}/>
        <Legend />
      </PieChart>
    );
  };

  return (
    <div style={{height:"100%", width:"100%"}}>
      {tipo === TipoGrafico.Lineal && renderLineChart()}
      {tipo === TipoGrafico.Barra && renderBarChart()}
      {tipo === TipoGrafico.Pastel && renderPieChart()}
    </div>
  );
};

export default dispositivoChart;
