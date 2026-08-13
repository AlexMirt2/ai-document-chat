from openai import OpenAI

from app.core.config import settings
from app.services.ai.rag_service import RAGService


client = OpenAI(
    api_key=settings.groq_api_key,
    base_url="https://api.groq.com/openai/v1",
)


class ChatService:

    MAX_HISTORY_MESSAGES = 12

    @staticmethod
    def ask(
        message: str,
        document_id: int,
        history: list,
    ):

        try:
            context, sources = (
                RAGService.get_context(
                    message,
                    document_id,
                )
            )

            print(
                "===== CHAT REQUEST =====",
                flush=True,
            )

            print(
                f"Document ID: {document_id}",
                flush=True,
            )

            print(
                f"Context length: {len(context)}",
                flush=True,
            )

            recent_history = (
                history[
                    -ChatService.MAX_HISTORY_MESSAGES:
                ]
            )

            messages = [
                {
                    "role": "system",
                    "content": """
You are a helpful AI assistant.

The user has uploaded a PDF document.

Relevant excerpts from the document may be
provided below.

Instructions:

- Answer naturally and conversationally.
- Prefer information from the uploaded document
  when it is relevant.
- If the document does not contain the answer,
  say that the information was not found in the
  provided document.
- Never invent facts from the document.
- If the user asks about a specific page,
  use only the provided context for that page.
- Never invent page numbers.
""",
                }
            ]

            if context.strip():

                messages.append(
                    {
                        "role": "system",
                        "content": f"""
Relevant document context:

{context}
""",
                    }
                )

            messages.extend(
                recent_history
            )

            messages.append(
                {
                    "role": "user",
                    "content": message,
                }
            )

            print(
                f"Messages sent to Groq: {len(messages)}",
                flush=True,
            )

            response = (
                client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    temperature=0.3,
                    messages=messages,
                )
            )

            answer = (
                response.choices[0]
                .message
                .content
            )

            print(
                "Groq response received successfully.",
                flush=True,
            )

            return {
                "answer": answer,
                "sources": sources,
            }

        except Exception as exc:

            print(
                "========== CHAT ERROR ==========",
                flush=True,
            )

            print(
                type(exc).__name__,
                flush=True,
            )

            print(
                str(exc),
                flush=True,
            )

            print(
                "================================",
                flush=True,
            )

            raise