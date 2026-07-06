import DocumentCard from "./DocumentCard";

const mockDocuments = [
  "Licenta.pdf",
  "Python.pdf",
  "FastAPI.pdf",
];

export default function DocumentList() {
  return (
    <div className="mt-6 space-y-3">

      {mockDocuments.map((doc) => (

        <DocumentCard
          key={doc}
          filename={doc}
        />

      ))}

    </div>
  );
}