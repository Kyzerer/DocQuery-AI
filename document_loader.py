import os
import pypdf
import docx
from bs4 import BeautifulSoup

def load_pdf(file_path: str) -> str:
    """Extract text from a PDF file."""
    reader = pypdf.PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def load_docx(file_path: str) -> str:
    """Extract text from a DOCX file."""
    doc = docx.Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])

def load_txt(file_path: str) -> str:
    """Extract text from a TXT or Markdown file."""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def load_html(file_path: str) -> str:
    """Extract text from an HTML file using BeautifulSoup."""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        for s in soup(["script", "style"]):
            s.decompose()
        # Extract text content
        return soup.get_text()

def load_document(file_path: str) -> tuple[str, dict]:
    """Load document text and return it along with source metadata.
    
    Args:
        file_path (str): Path to the document.
        
    Returns:
        tuple[str, dict]: A tuple containing the extracted text and a metadata dict.
    """
    ext = os.path.splitext(file_path)[1].lower()
    filename = os.path.basename(file_path)
    
    if ext == ".pdf":
        text = load_pdf(file_path)
    elif ext == ".docx":
        text = load_docx(file_path)
    elif ext == ".txt":
        text = load_txt(file_path)
    elif ext == ".md":
        text = load_txt(file_path)  # Markdown can be loaded as text
    elif ext in [".html", ".htm"]:
        text = load_html(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")
        
    metadata = {
        "source": filename
    }
    return text, metadata
