import DocumentCard from "./DocumentCard";
import type { Document } from "../../types/Document";

interface DocumentListProps {
  documents: Document[];
  loading: boolean;
  selectedId: number | null;
  onSelect: (id: number) => void;
  onDelete: (id: number) => void;
}

export default function DocumentList({
  documents,
  loading,
  selectedId,
  onSelect,
  onDelete,
}: DocumentListProps) {

  if (loading) {
    return (
      <p className="mt-6 text-slate-400">
        Loading documents...
      </p>
    );
  }

  if (documents.length === 0) {
    return (
      <p className="mt-6 text-slate-400">
        No matching documents found
      </p>
    );
  }

  return (
    <div className="mt-6 space-y-3">

      {documents.map((document) => (

        <DocumentCard
          key={document.id}
          filename={document.filename}
          uploadDate={document.upload_date}
          selected={selectedId === document.id}
          onClick={() => onSelect(document.id)}
          onDelete={() => onDelete(document.id)}
        />

      ))}

    </div>
  );
}