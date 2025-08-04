import fitz  # PyMuPDF
import docx
import re
import nltk
nltk.download('punkt')

def extract_text_from_pdf(file_path):
    text = ""
    doc = fitz.open(file_path)
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

def chunk_text_into_clauses(text):
    # Simple regex and sentence tokenization
    raw_clauses = re.split(r"\n\s*\d+\.\s*|\n\s*[A-Z][a-z]+:|\n\s*[A-Z\s]{5,}\n", text)
    clauses = []
    for chunk in raw_clauses:
        sentences = nltk.sent_tokenize(chunk)
        if len(sentences) > 0:
            clauses.append(" ".join(sentences))
    return [c.strip() for c in clauses if len(c.strip()) > 30]  # Filter noise