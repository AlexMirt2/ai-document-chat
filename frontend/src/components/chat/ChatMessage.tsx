import type { ChatMessage as ChatMessageType } from "../../types/chat";
import { useDocument } from "../../context/DocumentContext";

interface Props {
  message: ChatMessageType;
}

export default function ChatMessage({ message }: Props) {
  const isUser = message.role === "user";

  const { setCurrentPage } = useDocument();

  return (
    <div
      className={`mb-3 flex ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >
      <div
        className={`max-w-[80%] rounded-xl px-4 py-3 whitespace-pre-wrap ${
          isUser
            ? "bg-blue-600 text-white"
            : "bg-slate-700 text-slate-100"
        }`}
      >
        <div>{message.content}</div>

        {!isUser &&
          message.sources &&
          message.sources.length > 0 && (
            <div className="mt-4 border-t border-slate-600 pt-3">

              <div className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-400">
                📄 Sources
              </div>

              <div className="flex flex-wrap gap-2">

                {message.sources.map((source, index) => (

                  <button
                    key={index}
                    onClick={() =>
                      setCurrentPage(source.page + 1)
                    }
                    className="
                      rounded-lg
                      bg-slate-800
                      px-3
                      py-1
                      text-sm
                      transition
                      hover:bg-blue-600
                      cursor-pointer
                    "
                  >
                    Page {source.page + 1}
                  </button>

                ))}

              </div>

            </div>
          )}
      </div>
    </div>
  );
}