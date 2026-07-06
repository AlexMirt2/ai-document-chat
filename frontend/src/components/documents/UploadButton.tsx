import { uploadDocument } from "../../services/documentService";

export default function UploadButton() {

  async function handleUpload(
    event: React.ChangeEvent<HTMLInputElement>
  ) {

    const file = event.target.files?.[0];

    if (!file) return;

    try {

      await uploadDocument(file);

      alert("Document uploaded!");

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
        hover:scale-[1.02]
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