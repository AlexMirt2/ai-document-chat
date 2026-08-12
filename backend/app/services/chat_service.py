from openai import OpenAI

from app.core.config import settings
from app.services.ai.rag_service import RAGService


client = OpenAI(
    api_key=settings.groq_api_key,
    base_url="https://api.groq.com/openai/v1",
)


SYSTEM_PROMPT = """
You are a helpful AI assistant.

The user has uploaded one PDF document.

Your goal is to answer naturally.

Rules:

1. Always use the provided document context whenever it contains relevant information.

2. If the document answers the question, base your answer on it.

3. If the document only partially answers the question, complete the answer using your own knowledge and explicitly mention which part comes from your own knowledge.

4. If the document contains no relevant information, answer using your own knowledge and clearly state that the answer was not found in the uploaded document.

5. Never invent information that supposedly exists inside the document.

6. If the user asks about a specific page, only answer using that page.

7. Continue the conversation naturally.

Do not say that you cannot access the document if document excerpts are provided.
"""


class ChatService:

    @staticmethod
    def ask(
    db,
    message: str,
    document_id: int,
    history: list,
    ):

        context, sources = RAGService.get_context(
            message,
            document_id,
        )
        from app.services.document_service import DocumentService

        document = DocumentService.get_document(
         db,
         document_id,
        )
        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]

        if (
         document
         and document.summary
        ):
         messages.append(
        {
            "role": "system",
            "content": f"""
        Document summary:

        {document.summary}

         Keywords:

         {document.keywords}
"""
        }
    )
  
        if context.strip():

            messages.append(
                {
                    "role": "system",
                    "content": f"""
Document context:

{context}
""",
                }
            )

        if history:

            messages.extend(history[-12:])

        messages.append(
            {
                "role": "user",
                "content": message,
            }
        )

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0.2,
            messages=messages,
        )

        answer = response.choices[0].message.content

        return {
            "answer": answer,
            "sources": sources,
        }