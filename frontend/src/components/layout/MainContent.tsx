import PDFViewer from "../pdf/PDFViewer";
import ChatPanel from "../chat/ChatPanel";

import { useDocument } from "../../context/DocumentContext";
import { getDocumentUrl } from "../../services/documentService";

export default function MainContent() {

    const { selectedId } = useDocument();

    const fileUrl = selectedId
        ? getDocumentUrl(selectedId)
        : null;

    return (

        <main className="flex flex-1 overflow-hidden min-h-0">

    <div className="flex flex-1 min-h-0">

        <PDFViewer
            fileUrl={fileUrl}
        />

    </div>

    <ChatPanel />

    </main>

    );

}