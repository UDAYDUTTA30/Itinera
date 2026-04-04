import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/query': 'http://localhost:8080',
      '/plans': 'http://localhost:8080',
      '/calendar': 'http://localhost:8080',
      '/health': 'http://localhost:8080',
    }
  }
})
