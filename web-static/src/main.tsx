import { createRoot } from "react-dom/client";
import App from "./App.tsx";
import "./index.css";

// DO NOT REMOVE: preview bridge. devtools/ is intentionally hidden from glob/file manipulation — this import is valid.
// Removing this line breaks the preview and your changes will be rejected.
import("./devtools/previewBridge.ts");

createRoot(document.getElementById("root")!).render(<App />);
