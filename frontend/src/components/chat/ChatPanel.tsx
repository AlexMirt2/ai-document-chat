import { useState } from "react";

import ChatInput from "./ChatInput";
import ChatMessages from "./ChatMessages";

import { askAI } from "../../services/chatService";

import type { ChatMessage } from "../../types/chat";

import { useDocument } from "../../context/DocumentContext";
import ConfirmDialog from "../ui/ConfirmDialog";

import toast from "react-hot-toast";


export default function ChatPanel() {

  const [showDeleteDialog, setShowDeleteDialog] =
  useState(false);

  const {
    selectedId,
    chats,
    setChats,
  } = useDocument();

  const [loading, setLoading] =
    useState(false);

  const messages =
    selectedId !== null
      ? chats[selectedId] ?? []
      : [];


  function clearChat() {
  if (selectedId === null) return;

  setChats((prev) => ({
    ...prev,
    [selectedId]: [],
  }));

  toast.success("Conversation deleted.");

  setShowDeleteDialog(false);
}   
  async function send(message: string) {
  if (selectedId === null) {
    toast.error("Please select a document.");
    return;
  }

  const userMessage: ChatMessage = {
    id: crypto.randomUUID(),
    role: "user",
    content: message,
  };

  const history = [
    ...messages.map((m) => ({
      role: m.role,
      content: m.content,
    })),
    {
      role: "user",
      content: message,
    },
  ];

  setChats((prev) => ({
    ...prev,
    [selectedId]: [
      ...(prev[selectedId] ?? []),
      userMessage,
    ],
  }));

  setLoading(true);

  try {
    const result = await askAI(
      message,
      selectedId,
      history
    );

    const aiMessage: ChatMessage = {
      id: crypto.randomUUID(),
      role: "assistant",
      content: result.answer,
      sources: result.sources,
    };

    setChats((prev) => ({
      ...prev,
      [selectedId]: [
        ...(prev[selectedId] ?? []),
        aiMessage,
      ],
    }));
  } catch {
    toast.error("AI request failed.");

    const aiMessage: ChatMessage = {
      id: crypto.randomUUID(),
      role: "assistant",
      content: "Something went wrong. Please try again.",
    };

    setChats((prev) => ({
      ...prev,
      [selectedId]: [
        ...(prev[selectedId] ?? []),
        aiMessage,
      ],
    }));
  } finally {
    setLoading(false);
  }
}

  return (
    <div className="flex w-95 flex-col border-l border-slate-800 bg-slate-950">
      <div className="flex items-center justify-between border-b border-slate-800 p-5">
       <h2 className="text-xl font-bold">
         🤖 AI Assistant
       </h2>

      <button
        onClick={() => setShowDeleteDialog(true)}
        disabled={
        selectedId === null ||
        messages.length === 0
    }
        className="
        rounded-lg
        px-3
        py-2
        text-sm
      text-red-400
        transition
      hover:bg-red-600
      hover:text-white
        disabled:cursor-not-allowed
        disabled:opacity-40
        "
       title="Delete conversation"
  >
       🗑️
  </button>

  <ConfirmDialog
  open={showDeleteDialog}
  title="🗑️ Delete conversation"
  description="Are you sure you want to permanently delete this conversation? This action cannot be undone."
  confirmText="Delete"
  cancelText="Cancel"
  onConfirm={clearChat}
  onCancel={() => setShowDeleteDialog(false)}
/>
  </div>

      <ChatMessages
        messages={messages}
        loading={loading}
      />

      <ChatInput
        onSend={send}
        loading={loading}
      />
    </div>
  );
}