import re
import sqlite3

from collections import defaultdict
from pathlib import Path
from typing import Optional

from app.core.config import settings


class VectorStore:

    DATABASE_PATH = settings.database_path

    @classmethod
    def _connect(cls):
        Path(
            cls.DATABASE_PATH
        ).parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        connection = sqlite3.connect(
            cls.DATABASE_PATH
        )

        connection.row_factory = sqlite3.Row

        return connection

    @classmethod
    def initialize(cls):

        connection = cls._connect()

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS document_chunks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id INTEGER NOT NULL,
                page INTEGER NOT NULL,
                chunk_index INTEGER NOT NULL,
                text TEXT NOT NULL
            )
            """
        )

        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_document_chunks_document
            ON document_chunks(document_id)
            """
        )

        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_document_chunks_page
            ON document_chunks(document_id, page)
            """
        )

        connection.commit()
        connection.close()

    @classmethod
    def add_document(
        cls,
        document_id: int,
        chunks: list[dict],
    ):

        cls.initialize()

        connection = cls._connect()

        # Remove previous chunks for this document.
        connection.execute(
            """
            DELETE FROM document_chunks
            WHERE document_id = ?
            """,
            (
                document_id,
            ),
        )

        connection.executemany(
            """
            INSERT INTO document_chunks (
                document_id,
                page,
                chunk_index,
                text
            )
            VALUES (?, ?, ?, ?)
            """,
            [
                (
                    document_id,
                    chunk["page"],
                    chunk["chunk_index"],
                    chunk["text"],
                )
                for chunk in chunks
            ],
        )

        connection.commit()

        count = connection.execute(
            """
            SELECT COUNT(*)
            FROM document_chunks
            WHERE document_id = ?
            """,
            (
                document_id,
            ),
        ).fetchone()[0]

        connection.close()

        print(
            "Chunks stored:",
            count,
            flush=True,
        )

    @classmethod
    def _get_chunks(
        cls,
        document_id: int,
    ):

        cls.initialize()

        connection = cls._connect()

        rows = connection.execute(
            """
            SELECT
                page,
                chunk_index,
                text
            FROM document_chunks
            WHERE document_id = ?
            ORDER BY page, chunk_index
            """,
            (
                document_id,
            ),
        ).fetchall()

        connection.close()

        return rows

    @staticmethod
    def _tokenize(text: str):

        return set(
            re.findall(
                r"\b[\wÀ-ÿ]{2,}\b",
                text.lower(),
            )
        )

    @classmethod
    def _score(
        cls,
        question: str,
        text: str,
    ):

        question_tokens = cls._tokenize(
            question
        )

        text_tokens = cls._tokenize(
            text
        )

        if not question_tokens or not text_tokens:
            return 0.0

        common = (
            question_tokens
            & text_tokens
        )

        if not common:
            return 0.0

        score = (
            len(common)
            / len(question_tokens)
        )

        # Small bonus for exact phrases.
        question_normalized = (
            " ".join(
                question.lower().split()
            )
        )

        text_normalized = (
            " ".join(
                text.lower().split()
            )
        )

        if (
            question_normalized
            and question_normalized in text_normalized
        ):
            score += 1.0

        return score

    @classmethod
    def semantic_search(
        cls,
        question: str,
        document_id: int,
        k: int = 6,
    ):

        rows = cls._get_chunks(
            document_id
        )

        scored = []

        for row in rows:

            score = cls._score(
                question,
                row["text"],
            )

            if score > 0:

                scored.append(
                    (
                        {
                            "text": row["text"],
                            "page": row["page"],
                            "chunk_index": row["chunk_index"],
                        },
                        score,
                    )
                )

        scored.sort(
            key=lambda item: item[1],
            reverse=True,
        )

        return scored[:k]

    @classmethod
    def page_search(
        cls,
        document_id: int,
        page: int,
    ):

        rows = cls._get_chunks(
            document_id
        )

        chunks = []

        for row in rows:

            if row["page"] != page:
                continue

            chunks.append(
                {
                    "text": row["text"],
                    "page": row["page"],
                    "chunk_index": row["chunk_index"],
                }
            )

        chunks.sort(
            key=lambda chunk:
            chunk["chunk_index"]
        )

        return chunks

    @classmethod
    def document_search(
        cls,
        document_id: int,
    ):

        rows = cls._get_chunks(
            document_id
        )

        pages = defaultdict(list)

        for row in rows:

            pages[
                row["page"]
            ].append(
                (
                    row["chunk_index"],
                    row["text"],
                )
            )

        ordered_pages = []

        for page in sorted(
            pages.keys()
        ):

            pieces = sorted(
                pages[page],
                key=lambda item:
                item[0],
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

    @staticmethod
    def detect_page_request(
        question: str,
    ) -> Optional[int]:

        patterns = [
            r"page\s+(\d+)",
            r"pagina\s+(\d+)",
            r"pag\s+(\d+)",
            r"pg\s+(\d+)",
        ]

        question = question.lower()

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

        requested_page = (
            cls.detect_page_request(
                question
            )
        )

        # Exact page mode.
        if requested_page is not None:

            chunks = cls.page_search(
                document_id,
                requested_page,
            )

            if not chunks:

                return (
                    "",
                    [],
                )

            context = "\n\n".join(
                chunk["text"]
                for chunk in chunks
            )

            return (
                context,
                [
                    {
                        "page": requested_page,
                        "document_id": document_id,
                    }
                ],
            )

        # Normal relevance search.
        results = cls.semantic_search(
            question,
            document_id,
            k=6,
        )

        context_parts = []
        sources = []
        seen_pages = set()

        for chunk, score in results:

            context_parts.append(
                chunk["text"]
            )

            page = chunk["page"]

            if page not in seen_pages:

                seen_pages.add(page)

                sources.append(
                    {
                        "page": page,
                        "document_id": document_id,
                    }
                )

        return (
            "\n\n".join(
                context_parts
            ).strip(),
            sources,
        )

    @staticmethod
    def delete_document(
        document_id: int,
    ):

        connection = (
            VectorStore._connect()
        )

        connection.execute(
            """
            DELETE FROM document_chunks
            WHERE document_id = ?
            """,
            (
                document_id,
            ),
        )

        connection.commit()
        connection.close()

        print(
            "Deleted chunks for document:",
            document_id,
            flush=True,
        )