import {
  createContext,
  useContext,
  useEffect,
  useState,
} from "react";

import type { ChatMessage } from "../types/chat";

interface DocumentContextType {
  selectedId: number | null;
  setSelectedId: (id: number | null) => void;

  chats: Record<number, ChatMessage[]>;
  setChats: React.Dispatch<
    React.SetStateAction<Record<number, ChatMessage[]>>
  >;

  currentPage: number;
  setCurrentPage: (page: number) => void;
}

const DocumentContext = createContext<
  DocumentContextType | undefined
>(undefined);

export function DocumentProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const [selectedId, setSelectedId] = useState<number | null>(() => {
    const saved = localStorage.getItem("selectedDocument");

    return saved ? Number(saved) : null;
  });

  const [chats, setChats] = useState<
    Record<number, ChatMessage[]>
  >(() => {
    const saved = localStorage.getItem(
      "documentChats"
    );

    return saved ? JSON.parse(saved) : {};
  });

  const [currentPage, setCurrentPage] = useState(1);

  useEffect(() => {
    localStorage.setItem(
      "documentChats",
      JSON.stringify(chats)
    );
  }, [chats]);

  useEffect(() => {
    if (selectedId === null) {
      localStorage.removeItem(
        "selectedDocument"
      );
      return;
    }

    localStorage.setItem(
      "selectedDocument",
      selectedId.toString()
    );
  }, [selectedId]);

  return (
    <DocumentContext.Provider
      value={{
        selectedId,
        setSelectedId,

        chats,
        setChats,

        currentPage,
        setCurrentPage,
      }}
    >
      {children}
    </DocumentContext.Provider>
  );
}

export function useDocument() {
  const context = useContext(DocumentContext);

  if (!context) {
    throw new Error(
      "useDocument must be used inside DocumentProvider"
    );
  }

  return context;
}