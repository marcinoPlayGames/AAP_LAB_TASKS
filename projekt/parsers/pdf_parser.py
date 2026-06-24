from pypdf import PdfReader


def read_pdf(path):

    reader = PdfReader(path)

    text = ""

    for page in reader.pages:
        content = page.extract_text()

        if content:
            text += content

    return text