from langchain_text_splitters import RecursiveCharacterTextSplitter



class TextSplitter:

    @staticmethod
    def split(pages):

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=150,
        )

        chunks = []

        for page in pages:

            pieces = splitter.split_text(page["text"])

            for index, piece in enumerate(pieces):

                chunks.append(
                    {
                        "page": page["page"],
                        "chunk_index": index,
                        "text": piece,
                    }
                )

        return chunks