import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import tailwindcss from "@tailwindcss/vite";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { extractRoutesPlugin } from "./vite-plugins/extract-routes";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export default defineConfig({
  server: {
    host: "::",
    port: 8080,
    // The API is the Python worker (`pywrangler dev` in ../python-worker-wsl,
    // port 8787). Proxying keeps browser requests same-origin in dev, matching
    // the deployed setup where the worker serves these assets itself.
    proxy: {
      "/api": "http://localhost:8787",
      "/docs": "http://localhost:8787",
      "/openapi.json": "http://localhost:8787",
    },
  },
  plugins: [
    extractRoutesPlugin({
      sourceFile: "src/App.tsx",
      outputFile: "src/devtools/routes.generated.json",
    }),
    react(),
    tailwindcss(),
  ],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
