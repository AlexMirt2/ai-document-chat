import UploadButton from "../documents/UploadButton";
import DocumentList from "../documents/DocumentList";

export default function Sidebar() {
  return (
    <aside
      className="
        flex
        w-80
        flex-col
        border-r
        border-slate-800
        bg-slate-950
        p-5
      "
    >
      <h2 className="text-xl font-bold">
        📂 Documents
      </h2>

      <div className="mt-5">
        <UploadButton />
      </div>

      <DocumentList />
    </aside>
  );
}