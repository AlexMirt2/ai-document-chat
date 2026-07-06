interface DocumentCardProps {
  filename: string;
}

export default function DocumentCard({
  filename,
}: DocumentCardProps) {
  return (
    <div
      className="
        cursor-pointer
        rounded-xl
        border
        border-slate-700
        bg-slate-800
        p-3
        transition-all
        hover:border-blue-500
        hover:bg-slate-700
      "
    >
      <p className="truncate">
        📄 {filename}
      </p>
    </div>
  );
}