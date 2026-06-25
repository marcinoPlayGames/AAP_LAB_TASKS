from parsers.pdf_parser import read_pdf
from parsers.excel_parser import read_excel
from rapidfuzz import fuzz


class RAGService:


    def __init__(self):

        self.regulamin = ""
        self.taryfikator = []

        self.load_documents()


    def load_documents(self):

        self.regulamin = read_pdf(
            "data/regulamin.pdf"
        )

        self.taryfikator = read_excel(
            "data/taryfikator.xlsx"
        )
    
    def similarity(
        self,
        text,
        query
    ):

        return fuzz.token_set_ratio(
            text.lower(),
            query.lower()
        )


    def search(self, query):

        query = query.lower()

        regulamin_results = []
        taryfikator_results = []
        
        detected_penalty = None
        
        matches = []

        for line in self.regulamin.split("\n"):

            score = self.similarity(
                line,
                query
            )

            if score >= 40:

                matches.append(
                    (score, line)
                )

        matches.sort(reverse=True)
        print(matches)

        regulamin_results = [
            line
            for _, line in matches[:3]
        ]
        
        matches = []

        for item in self.taryfikator:

            score = self.similarity(
                item["przewinienie"],
                query
            )

            if score >= 50:
                matches.append((score, item))

        matches.sort(reverse=True)
        print(matches)
        
        for _, item in matches[:3]:

            taryfikator_results.append(
                f"Przewinienie: {item['przewinienie']}\n"
                f"Kara: {item['kara']}"
            )

        detected_penalty = (
            matches[0][1]["kara"]
            if matches
            else None
        )

                
        return {
            "regulamin": "\n".join(regulamin_results)
            if regulamin_results
            else "Brak informacji.",

            "taryfikator": "\n".join(taryfikator_results)
            if taryfikator_results
            else "Brak informacji.",
            
            "kara": detected_penalty
        }