import ChatMessages from "./ChatMessages";
import ChatInput from "./ChatInput";

export default function ChatPanel() {
  return (
    <div className="flex w-[380px] flex-col border-l border-slate-800 bg-slate-950">

      <div className="border-b border-slate-800 p-5">
        <h2 className="text-xl font-bold">
          🤖 AI Assistant
        </h2>

        <p className="mt-1 text-sm text-slate-400">
          Ask questions about the selected document.
        </p>
      </div>

      <ChatMessages />

      <ChatInput />

    </div>
  );
}