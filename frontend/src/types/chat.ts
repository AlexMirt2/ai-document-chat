export interface ChatSource {
  page: number;
  document_id: number;
}

export interface ChatMessage {
  id: string;

  role: "user" | "assistant";

  content: string;

  sources?: ChatSource[];
}