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
        
        # 1. Szukanie regulaminu
                
        regulamin_matches = []

        for line in self.regulamin.split("\n"):

            score = self.similarity(
                line,
                query
            )

            if score >= 40:

                regulamin_matches.append(
                    (score, line)
                )

        regulamin_matches.sort(
            reverse=True
        )

        regulamin_results = [
            line
            for _, line in regulamin_matches[:3]
        ]
        
        # 2. Najważniejsze - kontekst z regulaminu
        
        regulamin_text = " ".join(
            regulamin_results
        )
        
        # 3. Szukanie taryfikatora po regulaminie
        
        taryfikator_matches = []

        for item in self.taryfikator:

            score = self.similarity(
                item["przewinienie"],
                regulamin_text
            )

            taryfikator_matches.append(
                (score, item)
            )


        taryfikator_matches.sort(
            key=lambda x: x[0],
            reverse=True
        )


        if taryfikator_matches:

            best_score, best_item = taryfikator_matches[0]


            if best_score >= 45:

                taryfikator_results.append(
                    f"Przewinienie: {best_item['przewinienie']}\n"
                    f"Kara: {best_item['kara']}"
                )


                detected_penalty = best_item["kara"]

        print("REGULAMIN:")
        print(regulamin_text)

        print("TARYFIKATOR:")
        print(taryfikator_results)

        print("KARA:")
        print(detected_penalty)

                
        return {

            "regulamin":
                regulamin_text
                if regulamin_text
                else "Brak informacji.",


            "taryfikator":
                "\n".join(taryfikator_results)
                if taryfikator_results
                else "Brak informacji.",


            "kara":
                detected_penalty
        }

    def load_documents(self):

        self.regulamin = read_pdf(
            "data/regulamin.pdf"
        )

        self.taryfikator = read_excel(
            "data/taryfikator.xlsx"
        )

    def reload(self):

        self.regulamin = ""
        self.taryfikator = []

        self.load_documents()