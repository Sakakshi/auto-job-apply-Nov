from PyPDF2 import PdfReader
import docx


def extract_text_from_resume(path: str) -> str:
    if path.lower().endswith(".pdf"):
        reader = PdfReader(path)
        return " ".join(page.extract_text() or "" for page in reader.pages)

    if path.lower().endswith(".docx"):
        doc = docx.Document(path)
        return " ".join(p.text for p in doc.paragraphs)

    return ""