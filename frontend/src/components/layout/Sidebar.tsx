import { useEffect, useState } from "react";

import UploadButton from "../documents/UploadButton";
import DocumentList from "../documents/DocumentList";

import { getDocuments } from "../../services/documentService";

import type { Document } from "../../types/Document";
import { useDocument } from "../../context/DocumentContext";

export default function Sidebar() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const { selectedId, setSelectedId } = useDocument();
  const [loading, setLoading] = useState(true);

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

  useEffect(() => {
    loadDocuments();
  }, []);

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

      <DocumentList
     documents={documents}
     loading={loading}
     selectedId={selectedId}
     onSelect={setSelectedId}
/>
    </aside>
  );
}