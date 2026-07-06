import DocumentCard from "./DocumentCard";
import { useDocuments } from "../../hooks/useDocuments";

export default function DocumentList() {
  const { documents, loading } = useDocuments();

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
        No documents uploaded.
      </p>
    );
  }

  return (
    <div className="mt-6 space-y-3">
      {documents.map((document) => (
        <DocumentCard
          key={document.id}
          filename={document.filename}
        />
      ))}
    </div>
  );
}