interface DocumentCardProps {
  filename: string;
  uploadDate: string;
  selected: boolean;
  onClick: () => void;
  onDelete: () => void;
}

export default function DocumentCard({
  filename,
  uploadDate,
  selected,
  onClick,
  onDelete,
}: DocumentCardProps) {
  const formattedDate = new Date(uploadDate).toLocaleDateString(
    "ro-RO",
    {
      day: "2-digit",
      month: "short",
      year: "numeric",
    }
  );

  return (
    <div
      className={`
        w-full
        rounded-xl
        border
        p-4
        transition-all
        ${
          selected
            ? "border-blue-500 bg-blue-900/40 shadow-lg"
            : "border-slate-700 bg-slate-800 hover:bg-slate-700 hover:border-blue-500"
        }
      `}
    >
      <div className="flex items-start gap-3">
        <button
          onClick={onClick}
          title={filename}
          className="flex min-w-0 flex-1 items-start gap-3 text-left"
        >
          <div className="shrink-0 text-2xl">
            📄
          </div>

          <div className="min-w-0 flex-1">
            <p
              className="truncate font-medium"
              title={filename}
            >
              {filename}
            </p>

            <p className="mt-1 text-xs text-slate-400">
              📅 {formattedDate}
            </p>
          </div>
        </button>

        <button
          onClick={(e) => {
            e.stopPropagation();

            if (window.confirm(`Delete "${filename}"?`)) {
              onDelete();
            }
          }}
          className="
            shrink-0
            rounded-lg
            p-2
            text-red-400
            transition
            hover:bg-red-600
            hover:text-white
          "
          title="Delete document"
        >
          🗑️
        </button>
      </div>
    </div>
  );
}