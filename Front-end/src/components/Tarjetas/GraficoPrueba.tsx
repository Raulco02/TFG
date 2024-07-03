// src/components/SensorChart.tsx

import React, { useEffect } from 'react';
import { ResponsiveContainer, LineChart, BarChart, PieChart, Pie, Cell, Bar, Line, XAxis, YAxis, Tooltip, CartesianGrid, Legend } from 'recharts';
import dayjs from 'dayjs';
import { TipoGrafico, TiempoGrafico } from '../../resources/enums/enums';

interface SensorData {
  timestamp: string;
  value: number;
  sensor: string;
}

interface SensorChartProps {
  data: SensorData[];
  tipo: TipoGrafico;
  tiempoGrafico: TiempoGrafico;
  unidad?: string;
}

// Paleta de colores predefinida
const colors = [
  "#8884d8", "#82ca9d", "#ffc658", "#ff8042", "#8dd1e1",
  "#d0ed57", "#a4de6c", "#d0ed57", "#ffc0cb", "#b0e0e6"
];

const SensorChart: React.FC<SensorChartProps> = ({ data, tipo, tiempoGrafico, unidad='' }) => {
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

  const sensors = Array.from(new Set(data.map(d => d.sensor)));

  const sensorMap: { [key: string]: { [key: string]: number[] } } = {};
  dates.forEach(date => {
    sensorMap[date] = {};
    sensors.forEach(sensor => {
      sensorMap[date][sensor] = [];
    });
  });

  data.forEach(({ timestamp, value, sensor }) => {
    const date = dayjs(timestamp).format(format);
    if (sensorMap[date]) {
      sensorMap[date][sensor].push(value);
    }
  });

  const chartData = dates.map(date => {
    const entry: { date: string; [key: string]: number | null } = { date };
    sensors.forEach(sensor => {
      const values = sensorMap[date][sensor];
      entry[sensor] = values.length ? values.reduce((a, b) => a + b, 0) / values.length : null;
    });
    return entry;
  });

  const sensorColors = sensors.reduce<{ [key: string]: string }>((acc, sensor, index) => {
    acc[sensor] = colors[index % colors.length];
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
      {sensors.map(sensor => (
        <Line
          key={sensor}
          type="monotone"
          dataKey={sensor}
          stroke={sensorColors[sensor]}
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
      {sensors.map(sensor => (
        <Bar key={sensor} dataKey={sensor} fill={sensorColors[sensor]} />
      ))}
    </BarChart>
    </ResponsiveContainer>
  );

  const renderPieChart = () => {
    const pieData = sensors.map(sensor => {
      const total = chartData.reduce((sum, entry) => sum + (entry[sensor] || 0), 0);
      return { name: sensor, value: total };
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

export default SensorChart;
