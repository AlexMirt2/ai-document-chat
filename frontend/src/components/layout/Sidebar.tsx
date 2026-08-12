import { useEffect, useMemo, useState } from "react";

import UploadButton from "../documents/UploadButton";
import DocumentList from "../documents/DocumentList";

import {
  deleteDocument,
  getDocuments,
} from "../../services/documentService";

import type { Document } from "../../types/Document";
import { useDocument } from "../../context/DocumentContext";

export default function Sidebar() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");

  const { selectedId, setSelectedId } = useDocument();

  async function loadDocuments() {
    try {
      setLoading(true);

      const data = await getDocuments();

      setDocuments(data);

      if (data.length > 0 && selectedId === null) {
        setSelectedId(data[0].id);
      }
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  }

  async function handleDelete(documentId: number) {
    try {
      await deleteDocument(documentId);

      const data = await getDocuments();

      setDocuments(data);

      if (data.length === 0) {
        setSelectedId(null);
      } else if (selectedId === documentId) {
        setSelectedId(data[0].id);
      }
    } catch (error) {
      console.error(error);
    }
  }

  useEffect(() => {
    loadDocuments();
  }, []);

  const filteredDocuments = useMemo(() => {
    return documents.filter((document) =>
      document.filename
        .toLowerCase()
        .includes(search.toLowerCase())
    );
  }, [documents, search]);

  return (
    <aside
      className="
        flex
        w-80
        flex-col
        border-r
        border-slate-800
        bg-slate-950
        p-5
      "
    >
      <h2 className="text-xl font-bold">
        📂 Documents
      </h2>

      <div className="mt-5">
        <UploadButton onUploaded={loadDocuments} />
      </div>

      <input
        type="text"
        placeholder="🔍 Search documents..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="
          mt-5
          w-full
          rounded-xl
          border
          border-slate-700
          bg-slate-900
          px-4
          py-3
          text-sm
          outline-none
          transition
          focus:border-blue-500
        "
      />

      <DocumentList
        documents={filteredDocuments}
        loading={loading}
        selectedId={selectedId}
        onSelect={setSelectedId}
        onDelete={handleDelete}
      />
    </aside>
  );
}