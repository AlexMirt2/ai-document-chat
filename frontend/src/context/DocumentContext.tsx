import { createContext, useContext, useState } from "react";

interface DocumentContextType {
  selectedId: number | null;
  setSelectedId: (id: number | null) => void;
}

const DocumentContext = createContext<DocumentContextType | undefined>(
  undefined
);

export function DocumentProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const [selectedId, setSelectedId] = useState<number | null>(null);

  return (
    <DocumentContext.Provider
      value={{
        selectedId,
        setSelectedId,
      }}
    >
      {children}
    </DocumentContext.Provider>
  );
}

export function useDocument() {
  const context = useContext(DocumentContext);

  if (!context) {
    throw new Error("useDocument must be used inside DocumentProvider");
  }

  return context;
}