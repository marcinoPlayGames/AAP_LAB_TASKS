from parsers.pdf_parser import read_pdf
from parsers.excel_parser import read_excel


class RAGService:


    def __init__(self):

        self.regulamin = ""
        self.taryfikator = ""

        self.load_documents()


    def load_documents(self):

        self.regulamin = read_pdf(
            "data/regulamin.pdf"
        )

        self.taryfikator = read_excel(
            "data/taryfikator.xlsx"
        )


    def search(self, query):

        query = query.lower()

        regulamin_results = []
        taryfikator_results = []

        for line in self.regulamin.split("\n"):

            if any(
                word in line.lower()
                for word in query.split()
            ):
                regulamin_results.append(line)


        for item in self.taryfikator:

            if query in item["przewinienie"].lower():

                taryfikator_results.append(
                    f"Przewinienie: {item['przewinienie']}\n"
                    f"Kara: {item['kara']}"
                )

                
        return {
            "regulamin": "\n".join(regulamin_results)
            if regulamin_results
            else "Brak informacji.",

            "taryfikator": "\n".join(taryfikator_results)
            if taryfikator_results
            else "Brak informacji."
        }