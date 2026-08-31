import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import tailwindcss from "@tailwindcss/vite";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { extractRoutesPlugin } from "./vite-plugins/extract-routes";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Hybrid sandbox preview: the dispatcher starts this server with PORT and
// BACKEND_ORIGIN set — /api proxies to the deployed preview worker and the
// HMR websocket runs over wss through the preview-domain proxy. Locally
// neither is set and the defaults below apply (local pywrangler dev).
const backendOrigin = process.env.BACKEND_ORIGIN ?? "http://localhost:8787";
// changeOrigin: the deployed worker is routed by Host header.
const backendProxy = { target: backendOrigin, changeOrigin: true };

export default defineConfig({
  server: {
    // Bind all interfaces — required for the sandbox container's port proxy.
    host: "0.0.0.0",
    port: Number(process.env.PORT ?? 8080),
    // Requests arrive with the preview-domain hostname, not localhost.
    allowedHosts: true,
    // Proxying keeps browser requests same-origin in dev, matching the
    // deployed setup where the worker serves these assets itself.
    proxy: {
      "/api": backendProxy,
      "/docs": backendProxy,
      "/openapi.json": backendProxy,
    },
    ...(process.env.BACKEND_ORIGIN
      ? { hmr: { protocol: "wss" as const, clientPort: 443 } }
      : {}),
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
