from parsers.pdf_parser import read_pdf
from parsers.excel_parser import read_excel


class RAGService:


    def __init__(self):

        self.context = ""

        self.load_documents()


    def load_documents(self):

        pdf = read_pdf(
            "data/regulamin.pdf"
        )

        excel = read_excel(
            "data/taryfikator.xlsx"
        )


        self.context = (
            pdf
            +
            "\n\n"
            +
            excel
        )


    def search(self, query):

        keywords = query.lower().split()

        results = []

        for line in self.context.split("\n"):

            if any(
                word in line.lower()
                for word in keywords
            ):
                results.append(line)

        return "\n".join(results)