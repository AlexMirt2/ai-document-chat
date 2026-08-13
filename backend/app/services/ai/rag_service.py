from app.services.ai.vector_store import VectorStore


class RAGService:

    SUMMARY_KEYWORDS = [
        "summary",
        "summarize",
        "resume",
        "rezumat",
        "rezuma",
        "despre ce este",
        "despre document",
        "explain document",
        "overview",
        "explica documentul",
        "care este continutul",
        "ce contine documentul",
    ]

    @classmethod
    def is_summary_request(
        cls,
        question: str,
    ) -> bool:

        question = question.lower()

        return any(
            keyword in question
            for keyword in cls.SUMMARY_KEYWORDS
        )

    @classmethod
    def get_context(
        cls,
        question: str,
        document_id: int,
    ):

        if cls.is_summary_request(question):

            pages = VectorStore.document_search(
                document_id
            )

            context_parts = []
            sources = []

            for page in pages:

                context_parts.append(
                    f"""
========== PAGE {page["page"]} ==========

{page["text"]}
"""
                )

                sources.append(
                    {
                        "page": page["page"],
                        "document_id": document_id,
                    }
                )

            context = "\n".join(
                context_parts
            )

            print(
                "\n===== DOCUMENT SUMMARY MODE =====",
                flush=True,
            )

            print(
                f"Pages loaded: {len(pages)}",
                flush=True,
            )

            print(
                "=================================\n",
                flush=True,
            )

            return (
                context,
                sources,
            )

        context, sources = (
            VectorStore.build_context(
                question,
                document_id,
            )
        )

        print(
            "\n========== RAG ==========",
            flush=True,
        )

        print(
            f"Sources: {sources}",
            flush=True,
        )

        print(
            context[:1500],
            flush=True,
        )

        print(
            "=========================\n",
            flush=True,
        )

        return (
            context,
            sources,
        )