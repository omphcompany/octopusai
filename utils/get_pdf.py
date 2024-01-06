from PyPDF2 import PdfReader
from langchain.schema import Document

def get_pdf_text(pdf_docs):
    """
    Generates the text content from a list of PDF documents.

    Parameters:
        pdf_docs (list): A list of PDF documents.

    Returns:
        str: The concatenated text extracted from all the pages of the PDF documents.
    """
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


