from langchain_text_splitters import RecursiveCharacterTextSplitter


class TextSplitter:

    @staticmethod
    def split(text: str):

        splitter = RecursiveCharacterTextSplitter(

            chunk_size=800,

            chunk_overlap=150,

        )

        return splitter.split_text(text)