interface UploadButtonProps {
  onClick?: () => void;
}

export default function UploadButton({ onClick }: UploadButtonProps) {
  return (
    <button
      onClick={onClick}
      className="
        w-full
        rounded-xl
        bg-blue-600
        px-4
        py-3
        font-semibold
        transition-all
        hover:bg-blue-700
        hover:scale-[1.02]
        active:scale-95
      "
    >
      + Upload PDF
    </button>
  );
}