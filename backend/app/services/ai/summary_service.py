from openai import OpenAI

from app.core.config import settings


client = OpenAI(
    api_key=settings.groq_api_key,
    base_url="https://api.groq.com/openai/v1",
)


class SummaryService:

    @staticmethod
    def generate(pages):

        text = "\n\n".join(
            page["text"]
            for page in pages[:20]
        )

        if len(text) > 18000:
            text = text[:18000]

        prompt = f"""
Analyze the following document.

Return EXACTLY in this format:

SUMMARY:
A concise summary (200-300 words).

KEYWORDS:
keyword1, keyword2, keyword3, keyword4, keyword5, keyword6

Document:

{text}
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": "You summarize PDF documents."
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        result = response.choices[0].message.content

        summary = ""
        keywords = ""

        if "KEYWORDS:" in result:

            parts = result.split("KEYWORDS:")

            summary = (
                parts[0]
                .replace("SUMMARY:", "")
                .strip()
            )

            keywords = parts[1].strip()

        else:

            summary = result.strip()

        return summary, keywords