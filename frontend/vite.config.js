import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // Proxy any API requests that start with /api to your Python backend
      '/api': {
        target: 'http://localhost:5000', // The address of your Flask backend
        changeOrigin: true,
        // You can rewrite the path if needed, but it's optional
        // rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
})