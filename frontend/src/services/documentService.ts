import api from "./api";

export async function getDocuments() {
  const response = await api.get(
    "/api/documents"
  );

  return response.data;
}


export async function uploadDocument(
  file: File
) {
  const formData = new FormData();

  formData.append(
    "file",
    file
  );

  const response = await api.post(
    "/api/documents/upload",
    formData
  );

  return response.data;
}


export function getDocumentUrl(
  id: number
) {
  const baseUrl =
    import.meta.env.VITE_API_URL ||
    "http://127.0.0.1:8000";

  return `${baseUrl}/api/documents/${id}/download`;
}


export async function deleteDocument(
  documentId: number
) {
  await api.delete(
    `/api/documents/${documentId}`
  );
}