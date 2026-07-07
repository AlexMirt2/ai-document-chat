export default function ChatInput() {
  return (
    <div className="border-t border-slate-800 p-5">

      <textarea
        rows={3}
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
        className="
            mt-3
            w-full
            rounded-xl
            bg-blue-600
            py-3
            font-semibold
            hover:bg-blue-700
        "
      >
        Send
      </button>

    </div>
  );
}