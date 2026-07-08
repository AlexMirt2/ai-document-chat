import { useState } from "react";

import ChatInput from "./ChatInput";
import ChatMessages from "./ChatMessages";

import { askAI } from "../../services/chatService";

import type { ChatMessage } from "../../types/chat";

export default function ChatPanel() {

    const [messages, setMessages] = useState<ChatMessage[]>([]);

    const [loading, setLoading] = useState(false);

    async function send(message: string) {

        const userMessage: ChatMessage = {

            id: crypto.randomUUID(),

            role: "user",

            content: message,

        };

        setMessages((prev) => [...prev, userMessage]);

        setLoading(true);

        try {

            const answer = await askAI(message);

            const aiMessage: ChatMessage = {

                id: crypto.randomUUID(),

                role: "assistant",

                content: answer,

            };

            setMessages((prev) => [...prev, aiMessage]);

        } catch {

            const aiMessage: ChatMessage = {

                id: crypto.randomUUID(),

                role: "assistant",

                content:
                    "Something went wrong.",

            };

            setMessages((prev) => [...prev, aiMessage]);

        }

        setLoading(false);

    }

    return (

        <div className="flex w-[380px] flex-col border-l border-slate-800 bg-slate-950">

            <div className="border-b border-slate-800 p-5">

                <h2 className="text-xl font-bold">

                    🤖 AI Assistant

                </h2>

            </div>

            <ChatMessages
                messages={messages}
            />

            <ChatInput

                onSend={send}

                loading={loading}

            />

        </div>

    );

}