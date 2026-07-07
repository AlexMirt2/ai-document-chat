import { uploadDocument } from "../../services/documentService";

interface UploadButtonProps {
  onUploaded: () => void;
}

export default function UploadButton({
  onUploaded,
}: UploadButtonProps) {
  async function handleUpload(
    event: React.ChangeEvent<HTMLInputElement>
) {
    const file = event.target.files?.[0];

    if (!file) return;

    try {
      await uploadDocument(file);

      onUploaded();

      alert("Document uploaded successfully!");
    } catch (error) {
      console.error(error);

      alert("Upload failed.");
    }
  }

  return (
    <label
      className="
        flex
        cursor-pointer
        items-center
        justify-center
        rounded-xl
        bg-blue-600
        px-4
        py-3
        font-semibold
        transition-all
        hover:bg-blue-700
      "
    >
      + Upload PDF

      <input
        type="file"
        accept=".pdf"
        className="hidden"
        onChange={handleUpload}
      />
    </label>
  );
}