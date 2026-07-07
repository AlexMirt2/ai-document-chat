import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import "./index.css";

import App from "./App";

import { DocumentProvider } from "./context/DocumentContext";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <DocumentProvider>
      <App />
    </DocumentProvider>
  </StrictMode>
);