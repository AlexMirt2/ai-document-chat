from openai import OpenAI

from app.core.config import settings


client = OpenAI(
    api_key=settings.groq_api_key,
    base_url="https://api.groq.com/openai/v1",
)


class ChatService:

    @staticmethod
    def ask(message: str):

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[

                {
                    "role": "system",
                    "content":
                        "You are a helpful AI assistant."
                },

                {
                    "role": "user",
                    "content": message
                }

            ],

            temperature=0.3,

        )

        return response.choices[0].message.content