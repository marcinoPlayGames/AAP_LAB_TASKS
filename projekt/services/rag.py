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

        query = query.lower()

        results = []

        for line in self.context.split("\n"):

            line_lower = line.lower()

            if any(
                word in line_lower
                for word in query.split()
            ):
                results.append(line)
                
        if not results:
            return "Brak pasującego kontekstu."

        return "\n".join(results)