export default function ChatInput() {
  return (
    <div
      className="
        border-t
        border-slate-800
        bg-slate-900
        p-4
      "
    >
      <input
        type="text"
        placeholder="Ask something about your document..."
        className="
          w-full
          rounded-xl
          border
          border-slate-700
          bg-slate-800
          p-4
          outline-none
          transition
          focus:border-blue-500
        "
      />
    </div>
  );
}