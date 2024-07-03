// init_mongo.js
db = db.getSiblingDB('Dispositivos'); // Cambia a la base de datos 'mydatabase'

db.createCollection("Dispositivos", {
    timeseries: {
      timeField: 'timestamp', // Campo que contiene las marcas de tiempo
    }
  });
