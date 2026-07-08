from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.vectorstores import Chroma


embeddings = HuggingFaceEmbeddings(

    model_name="sentence-transformers/all-MiniLM-L6-v2"

)


class VectorStore:

    @staticmethod
    def create(chunks):

        db = Chroma.from_texts(

            texts=chunks,

            embedding=embeddings,

            persist_directory="vector_db",

        )

        db.persist()

        return db