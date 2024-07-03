import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'
import { resolve } from 'path';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      // Configura alias para asegurar que las rutas de React Router se resuelvan correctamente
      'react-router-dom': resolve(__dirname, './node_modules/react-router-dom'),
    },
  },
  server: {
    // Configura el servidor Vite para que maneje las solicitudes de ruta correctamente
    fs: {
      strict: false,
    },
  },
})
