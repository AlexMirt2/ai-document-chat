import { useEffect, useRef } from "react";
import ChatMessage from "./ChatMessage";
import type { ChatMessage as ChatMessageType } from "../../types/chat";

interface Props {
  messages: ChatMessageType[];
  loading: boolean;
}

export default function ChatMessages({
  messages,
  loading,
}: Props) {

  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (containerRef.current) {
        containerRef.current.scrollTo({
            top: containerRef.current.scrollHeight,
            behavior: "smooth",
        });
    }
}, [messages, loading]);

  if (messages.length === 0) {
    return (
      <div className="flex flex-1 flex-col items-center justify-center p-8 text-center text-slate-400">

        <div className="mb-6 text-6xl">
          🤖
        </div>

        <h3 className="text-xl font-semibold text-white">
          AI Document Assistant
        </h3>

        <p className="mt-3 max-w-xs">
          Ask questions about the selected PDF.
        </p>

        <div className="mt-8 space-y-2 text-sm">

          <p>• Summarize this document</p>

          <p>• What conclusions does it contain?</p>

          <p>• What dates are mentioned?</p>

          <p>• Explain page 5</p>

        </div>

      </div>
    );
  }

  return (

    <div
    ref={containerRef}
    className="flex-1 overflow-y-auto p-5 space-y-3"
>

      {messages.map((message) => (

        <ChatMessage
          key={message.id}
          message={message}
        />

      ))}

      {loading && (

        <div className="flex justify-start">

          <div className="rounded-xl bg-slate-700 px-4 py-3">

            <div className="animate-pulse">

              🤖 Thinking...

            </div>

          </div>

        </div>

      )}

    </div>

  );
}