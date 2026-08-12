import re
from collections import defaultdict
from typing import Optional

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from app.core.config import settings


class VectorStore:

    PERSIST_DIRECTORY = settings.vector_db_dir
    COLLECTION_NAME = "documents"

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    @classmethod
    def load(cls):
        return Chroma(
            collection_name=cls.COLLECTION_NAME,
            persist_directory=cls.PERSIST_DIRECTORY,
            embedding_function=cls.embeddings,
        )

    @classmethod
    def add_document(
        cls,
        document_id: int,
        chunks: list[dict],
    ):
        db = cls.load()

        # Dacă documentul a fost procesat anterior,
        # ștergem vectorii vechi înainte de a-i adăuga pe cei noi.
        old = db.get(
            where={
                "document_id": document_id,
            }
        )

        if old["ids"]:
            db.delete(ids=old["ids"])

        texts = [
            chunk["text"]
            for chunk in chunks
        ]

        metadatas = [
            {
                "document_id": document_id,
                "page": chunk["page"],
                "chunk_index": chunk["chunk_index"],
            }
            for chunk in chunks
        ]

        ids = [
            f"{document_id}_{chunk['page']}_{chunk['chunk_index']}"
            for chunk in chunks
        ]

        db.add_texts(
            texts=texts,
            metadatas=metadatas,
            ids=ids,
        )

        print("Embeddings stored successfully")
        print(
            "Collection count:",
            db._collection.count(),
        )

    @classmethod
    def semantic_search(
        cls,
        question: str,
        document_id: int,
        k: int = 8,
    ):
        db = cls.load()

        results = db.similarity_search_with_score(
            question,
            k=k,
            filter={
                "document_id": document_id,
            },
        )

        cleaned = []
        seen = set()

        for document, score in results:

            key = (
                document.metadata["page"],
                document.metadata["chunk_index"],
            )

            if key in seen:
                continue

            seen.add(key)

            cleaned.append(
                (
                    document,
                    score,
                )
            )

        return cleaned

    @classmethod
    def page_search(
        cls,
        document_id: int,
        page: int,
    ):
        db = cls.load()

        results = db.get(
            where={
                "$and": [
                    {
                        "document_id": document_id,
                    },
                    {
                        "page": page,
                    },
                ]
            },
            include=[
                "documents",
                "metadatas",
            ],
        )

        chunks = []

        documents = results.get("documents") or []
        metadatas = results.get("metadatas") or []

        for text, metadata in zip(
            documents,
            metadatas,
        ):
            chunks.append(
                {
                    "text": text,
                    "page": metadata["page"],
                    "chunk_index": metadata["chunk_index"],
                }
            )

        chunks.sort(
            key=lambda chunk: chunk["chunk_index"]
        )

        return chunks

    @classmethod
    def document_search(
        cls,
        document_id: int,
    ):
        db = cls.load()

        results = db.get(
            where={
                "document_id": document_id,
            },
            include=[
                "documents",
                "metadatas",
            ],
        )

        pages = defaultdict(list)

        documents = results.get("documents") or []
        metadatas = results.get("metadatas") or []

        for text, metadata in zip(
            documents,
            metadatas,
        ):
            pages[
                metadata["page"]
            ].append(
                (
                    metadata["chunk_index"],
                    text,
                )
            )

        ordered_pages = []

        for page in sorted(pages.keys()):

            pieces = sorted(
                pages[page],
                key=lambda item: item[0],
            )

            ordered_pages.append(
                {
                    "page": page,
                    "text": "\n".join(
                        piece[1]
                        for piece in pieces
                    ),
                }
            )

        return ordered_pages

    @classmethod
    def get_page_count(
        cls,
        document_id: int,
    ) -> int:
        pages = cls.document_search(
            document_id
        )

        if not pages:
            return 0

        return max(
            page["page"]
            for page in pages
        )

    @staticmethod
    def detect_page_request(
        question: str,
    ) -> Optional[int]:

        question = question.lower()

        patterns = [
            r"\bpage\s*[:#]?\s*(\d+)\b",
            r"\bpagina\s*[:#]?\s*(\d+)\b",
            r"\bpag\.?\s*[:#]?\s*(\d+)\b",
            r"\bpg\.?\s*[:#]?\s*(\d+)\b",
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                question,
            )

            if match:
                return int(
                    match.group(1)
                )

        return None

    @classmethod
    def build_context(
        cls,
        question: str,
        document_id: int,
    ):

        requested_page = cls.detect_page_request(
            question
        )

        # =====================================================
        # EXACT PAGE MODE
        # =====================================================

        if requested_page is not None:

            chunks = cls.page_search(
                document_id=document_id,
                page=requested_page,
            )

            print(
                f"\n========== EXACT PAGE SEARCH =========="
            )
            print(
                f"Requested page: {requested_page}"
            )
            print(
                f"Chunks found: {len(chunks)}"
            )

            # Pagina cerută nu există în vector database.
            if not chunks:

                print(
                    "Requested page was not found."
                )
                print(
                    "=======================================\n"
                )

                return (
                    "",
                    [],
                )

            context_parts = []

            for chunk in chunks:
                context_parts.append(
                    chunk["text"]
                )

            context = "\n\n".join(
                context_parts
            )

            sources = [
                {
                    "page": requested_page,
                    "document_id": document_id,
                }
            ]

            print(
                "=======================================\n"
            )

            return (
                context.strip(),
                sources,
            )

        # =====================================================
        # NORMAL SEMANTIC RAG MODE
        # =====================================================

        results = cls.semantic_search(
            question,
            document_id,
        )

        context_parts = []
        sources = []
        seen_pages = set()

        for document, score in results:

            context_parts.append(
                document.page_content
            )

            page = document.metadata["page"]

            if page not in seen_pages:

                seen_pages.add(page)

                sources.append(
                    {
                        "page": page,
                        "document_id": document_id,
                    }
                )

        context = "\n\n".join(
            context_parts
        )

        return (
            context.strip(),
            sources,
        )

    @staticmethod
    def delete_document(
        document_id: int,
    ):
        db = VectorStore.load()

        results = db.get(
            where={
                "document_id": document_id,
            }
        )

        ids = results["ids"]

        if ids:
            db.delete(
                ids=ids
            )