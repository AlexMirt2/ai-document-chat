interface DocumentCardProps {
  filename: string;
  uploadDate: string;
  selected: boolean;
  onClick: () => void;
}

export default function DocumentCard({
  filename,
  uploadDate,
  selected,
  onClick,
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
    <button
      onClick={onClick}
      title={filename}
      className={`
        w-full
        rounded-xl
        border
        p-4
        text-left
        transition-all

        ${
          selected
            ? "border-blue-500 bg-blue-900/40 shadow-lg"
            : "border-slate-700 bg-slate-800 hover:bg-slate-700 hover:border-blue-500"
        }
      `}
    >
      <div className="flex items-start gap-3">

        <div className="text-2xl">
          📄
        </div>

        <div className="min-w-0 flex-1">

          <p
            className="
              overflow-hidden
              text-ellipsis
              whitespace-nowrap
              font-medium
            "
          >
            {filename}
          </p>

          <p className="mt-1 text-xs text-slate-400">
            📅 {formattedDate}
          </p>

        </div>

      </div>

    </button>
  );
}