import type { ChatMessage as ChatMessageType } from "../../types/chat";

interface Props {

    message: ChatMessageType;

}

export default function ChatMessage({ message }: Props) {

    const isUser = message.role === "user";

    return (

        <div
            className={`mb-2 flex ${
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

                {message.content}

            </div>

        </div>

    );

}