import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    rollupOptions: {
      output: {
        entryFileNames: `assets/[name].react.js`,
        chunkFileNames: `assets/[name].react.js`,
        assetFileNames: `assets/[name].react.[ext]`
      },
    }
  }
})
