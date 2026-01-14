import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: "dist"
  },
  // Use relative paths for API calls (works with combined deployment)
  base: "./",
  server: {
    proxy: {
      // Proxy API requests to Django backend during development
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      }
    }
  }
});


