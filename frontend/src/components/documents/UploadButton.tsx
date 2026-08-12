import { useRef, useState } from "react";
import { uploadDocument } from "../../services/documentService";
import toast from "react-hot-toast";

interface UploadButtonProps {
  onUploaded: () => void;
}

export default function UploadButton({
  onUploaded,
}: UploadButtonProps) {
  const [dragging, setDragging] = useState(false);
  const [uploading, setUploading] = useState(false);

  const inputRef = useRef<HTMLInputElement>(null);

  async function upload(file: File) {
    if (file.type !== "application/pdf") {
      toast.error("Only PDF files are allowed.");
      return;
    }

    try {
      setUploading(true);

      await uploadDocument(file);

      onUploaded();

      toast.success("Document uploaded successfully.");
    } catch (error) {
      console.error(error);
      toast.error("Upload failed.");
    } finally {
      setUploading(false);
    }
  }

  async function handleUpload(
    event: React.ChangeEvent<HTMLInputElement>
  ) {
    const file = event.target.files?.[0];

    if (!file) return;

    await upload(file);

    event.target.value = "";
  }

  async function handleDrop(
    event: React.DragEvent<HTMLDivElement>
  ) {
    event.preventDefault();

    setDragging(false);

    const file = event.dataTransfer.files?.[0];

    if (!file) return;

    await upload(file);
  }

  return (
    <div
      onClick={() => inputRef.current?.click()}
      onDragOver={(e) => {
        e.preventDefault();
        setDragging(true);
      }}
      onDragLeave={() => setDragging(false)}
      onDrop={handleDrop}
      className={`
        cursor-pointer
        rounded-2xl
        border-2
        border-dashed
        p-6
        text-center
        transition-all
        duration-200

        ${
          dragging
            ? "border-blue-500 bg-blue-900/20"
            : "border-slate-700 bg-slate-900 hover:border-blue-500 hover:bg-slate-800"
        }
      `}
    >
      <div className="text-5xl">
        📄
      </div>

      <h3 className="mt-3 font-semibold text-white">
        {uploading
          ? "Uploading..."
          : "Drag & Drop PDF"}
      </h3>

      <p className="mt-2 text-sm text-slate-400">
        or click to browse
      </p>

      <input
        ref={inputRef}
        type="file"
        accept=".pdf"
        className="hidden"
        onChange={handleUpload}
      />
    </div>
  );
}