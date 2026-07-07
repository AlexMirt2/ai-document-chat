import { useState } from "react";
import { Document, Page, pdfjs } from "react-pdf";

import "react-pdf/dist/Page/AnnotationLayer.css";
import "react-pdf/dist/Page/TextLayer.css";

pdfjs.GlobalWorkerOptions.workerSrc = new URL(
  "pdfjs-dist/build/pdf.worker.min.mjs",
  import.meta.url,
).toString();

interface PDFViewerProps {
  fileUrl: string | null;
}

export default function PDFViewer({
  fileUrl,
}: PDFViewerProps) {
  const [numPages, setNumPages] = useState(0);

  const [pageNumber, setPageNumber] = useState(1);

  if (!fileUrl) {
    return (
      <div className="flex flex-1 items-center justify-center text-slate-400">
        Select a document
      </div>
    );
  }

  return (
    <div className="flex flex-1 flex-col items-center overflow-y-auto bg-slate-800 p-6">

      <Document
      loading={
    <div className="mt-10 text-slate-400">
        Loading PDF...
     </div>
     }
     error={
    <div className="mt-10 text-red-400">
        Failed to load PDF.
    </div>
     }
        file={fileUrl}
        onLoadSuccess={({ numPages }) => {
          setNumPages(numPages);
          setPageNumber(1);
        }}
      >
        <Page
          pageNumber={pageNumber}
          width={900}
        />
      </Document>

      <div className="mt-6 flex items-center gap-4">

        <button
          onClick={() => setPageNumber((p) => Math.max(1, p - 1))}
          disabled={pageNumber === 1}
          className="rounded bg-slate-700 px-4 py-2 disabled:opacity-40"
        >
          ◀
        </button>

        <span>

          {pageNumber} / {numPages}

        </span>

        <button
          onClick={() =>
            setPageNumber((p) => Math.min(numPages, p + 1))
          }
          disabled={pageNumber === numPages}
          className="rounded bg-slate-700 px-4 py-2 disabled:opacity-40"
        >
          ▶
        </button>

      </div>

    </div>
  );
}