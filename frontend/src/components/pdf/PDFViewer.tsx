import { useEffect, useState } from "react";
import { Document, Page, pdfjs } from "react-pdf";

import "react-pdf/dist/Page/AnnotationLayer.css";
import "react-pdf/dist/Page/TextLayer.css";

import { useDocument } from "../../context/DocumentContext";

pdfjs.GlobalWorkerOptions.workerSrc = new URL(
  "pdfjs-dist/build/pdf.worker.min.mjs",
  import.meta.url
).toString();

interface PDFViewerProps {
  fileUrl: string | null;
}

export default function PDFViewer({
  fileUrl,
}: PDFViewerProps) {
  const [numPages, setNumPages] = useState(0);
  const [pdfError, setPdfError] = useState(false);

  const {
    currentPage,
    setCurrentPage,
  } = useDocument();

  useEffect(() => {
    setCurrentPage(1);
    setNumPages(0);
    setPdfError(false);
  }, [fileUrl, setCurrentPage]);

  if (!fileUrl) {
    return (
      <div className="flex flex-1 items-center justify-center text-slate-400">
        Select a document
      </div>
    );
  }

  return (
    <div className="thin-scrollbar flex flex-1 flex-col items-center overflow-y-auto bg-slate-800 p-6">

      <Document
        file={fileUrl}
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
        onLoadSuccess={({ numPages }) => {
          setNumPages(numPages);
          setCurrentPage(1);
          setPdfError(false);
        }}
        onLoadError={(error) => {
          console.error("PDF loading error:", error);
          setPdfError(true);
        }}
      >
        {!pdfError && numPages > 0 && (
          <Page
            pageNumber={Math.min(
              Math.max(currentPage, 1),
              numPages
            )}
            width={700}
          />
        )}
      </Document>

      {numPages > 0 && (
        <div className="mt-6 flex items-center gap-4">

          <button
            onClick={() =>
              setCurrentPage(
                Math.max(1, currentPage - 1)
              )
            }
            disabled={currentPage === 1}
            className="
              rounded-lg
              bg-slate-700
              px-4
              py-2
              transition
              hover:bg-slate-600
              disabled:cursor-not-allowed
              disabled:opacity-40
            "
          >
            ◀
          </button>

          <span className="min-w-[80px] text-center">
            {currentPage} / {numPages}
          </span>

          <button
            onClick={() =>
              setCurrentPage(
                Math.min(numPages, currentPage + 1)
              )
            }
            disabled={currentPage === numPages}
            className="
              rounded-lg
              bg-slate-700
              px-4
              py-2
              transition
              hover:bg-slate-600
              disabled:cursor-not-allowed
              disabled:opacity-40
            "
          >
            ▶
          </button>

        </div>
      )}

    </div>
  );
}