import ChatInput from "./ChatInput";

export default function ChatWindow() {
  return (
    <section className="flex flex-1 flex-col">

      <div className="flex flex-1 items-center justify-center">

        <div className="text-center">

          <h1 className="text-4xl font-bold">
            🤖 AI Document Chat
          </h1>

          <p className="mt-4 text-slate-400">
            Upload a PDF to begin chatting.
          </p>

        </div>

      </div>

      <ChatInput />

    </section>
  );
}