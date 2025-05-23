import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    hmr: true, // Explicitly enable HMR (should be default, but let's ensure it's on)
    watch: {
      usePolling: true, // Use polling for file changes (sometimes needed on Windows)
    },
  },
})
