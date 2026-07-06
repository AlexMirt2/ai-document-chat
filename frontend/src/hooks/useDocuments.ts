import { useEffect, useState } from "react";

import { getDocuments } from "../services/documentService";
import type { Document } from "../types/Document";

export function useDocuments() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchDocuments() {
      try {
        const data = await getDocuments();
        setDocuments(data);
      } catch (error) {
        console.error("Failed to load documents:", error);
      } finally {
        setLoading(false);
      }
    }

    fetchDocuments();
  }, []);

  return {
    documents,
    loading,
  };
}