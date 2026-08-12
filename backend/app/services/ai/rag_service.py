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

        # =====================================================
        # SUMMARY MODE
        # =====================================================

        if cls.is_summary_request(question):

            pages = VectorStore.document_search(
                document_id
            )

            context_parts = []
            sources = []

            for page in pages:

                context_parts.append(
                    f"========== PAGE {page['page']} ==========\n\n"
                    f"{page['text']}"
                )

                sources.append(
                    {
                        "page": page["page"],
                        "document_id": document_id,
                    }
                )

            context = "\n\n".join(
                context_parts
            )

            print(
                "\n===== DOCUMENT SUMMARY MODE ====="
            )
            print(
                f"Pages loaded: {len(pages)}"
            )
            print(
                "=================================\n"
            )

            return (
                context,
                sources,
            )

        # =====================================================
        # NORMAL / EXACT PAGE RAG
        # =====================================================

        context, sources = VectorStore.build_context(
            question,
            document_id,
        )

        requested_page = VectorStore.detect_page_request(
            question
        )

        if requested_page is not None:

            print(
                "\n===== EXACT PAGE MODE ====="
            )
            print(
                f"Requested page: {requested_page}"
            )
            print(
                f"Sources: {sources}"
            )
            print(
                f"Context length: {len(context)}"
            )
            print(
                "===========================\n"
            )

        else:

            print(
                "\n========== SEMANTIC RAG =========="
            )
            print(
                f"Sources: {sources}"
            )
            print(
                f"Context length: {len(context)}"
            )
            print(
                context[:1500]
            )
            print(
                "==================================\n"
            )

        return (
            context,
            sources,
        )