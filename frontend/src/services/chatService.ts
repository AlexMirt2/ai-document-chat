import api from "./api";

export async function askAI(
    message: string
) {

    const response = await api.post(
        "/api/chat",
        {
            message,
        }
    );

    return response.data.response;

}