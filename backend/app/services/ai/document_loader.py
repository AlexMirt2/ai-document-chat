import fitz


class DocumentLoader:

    @staticmethod
    def load(pdf_path: str):

        document = fitz.open(pdf_path)

        pages = []

        for page_number, page in enumerate(document, start=1):

            text = page.get_text().strip()

            if text:

                pages.append(
                    {
                        "page": page_number,
                        "text": text,
                    }
                )

        document.close()

        return pages