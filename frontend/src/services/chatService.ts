import api from "./api";

export async function askAI(
  message: string,
  documentId: number,
  history: unknown[],
) {
  const response = await api.post("/api/chat", {
    message,
    document_id: documentId,
    history,
  });

  return response.data;
}