import fitz


class DocumentLoader:

    @staticmethod
    def load(pdf_path: str):

        document = fitz.open(pdf_path)

        text = ""

        for page in document:

            text += page.get_text()

        return text