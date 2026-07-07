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

        <main className="flex flex-1">

            <div className="flex flex-1">

                <PDFViewer
                    fileUrl={fileUrl}
                />

            </div>

            <ChatPanel />

        </main>

    );

}