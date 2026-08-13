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

        context, sources = (
            RAGService.get_context(
                message,
                document_id,
            )
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
  you may use your general knowledge.
- Never claim that information came from the
  document if it was not present there.
- If the user asks about a specific page,
  use only the provided context for that page.
- Do not invent page numbers or document content.
- Continue the conversation naturally.
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

        # Keep only recent conversation history.
        recent_history = (
            history[
                -ChatService.MAX_HISTORY_MESSAGES:
            ]
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

        response = (
            client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                temperature=0.3,
                messages=messages,
            )
        )

        return {
            "answer": (
                response.choices[0]
                .message.content
            ),
            "sources": sources,
        }