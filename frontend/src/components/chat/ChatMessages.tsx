import ChatMessage from "./ChatMessage";
import type { ChatMessage as ChatMessageType } from "../../types/chat";

interface Props {

    messages: ChatMessageType[];

}

export default function ChatMessages({
    messages,
}: Props) {

    return (

        <div className="flex-1 overflow-y-auto p-5 space-y-2">

            {messages.map((message) => (

                <ChatMessage
                    key={message.id}
                    message={message}
                />

            ))}

        </div>

    );

}