import { useRef, useState } from "react";

interface Props {
  onSend(message: string): void;
  loading: boolean;
}

export default function ChatInput({
  onSend,
  loading,
}: Props) {
  const [message, setMessage] = useState("");

  const textareaRef = useRef<HTMLTextAreaElement>(null);

  function handleSend() {
    if (!message.trim()) return;

    onSend(message);

    setMessage("");

    textareaRef.current?.focus();
  }

  function handleKeyDown(
    e: React.KeyboardEvent<HTMLTextAreaElement>
  ) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  return (
    <div className="border-t border-slate-800 p-5">
      <textarea
        ref={textareaRef}
        rows={3}
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Ask something..."
        className="
          w-full
          resize-none
          rounded-xl
          bg-slate-800
          p-3
          outline-none
        "
      />

      <button
        onClick={handleSend}
        disabled={loading}
        className="
          mt-3
          w-full
          rounded-xl
          bg-blue-600
          py-3
          font-semibold
          hover:bg-blue-700
          disabled:opacity-50
        "
      >
        {loading ? "Thinking..." : "Send"}
      </button>
    </div>
  );
}