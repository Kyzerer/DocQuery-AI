import re

def preprocess_text(text: str) -> str:
    """Preprocess extracted text to clean up whitespaces, carriage returns, and excessive newlines.
    
    Args:
        text (str): The raw extracted text.
        
    Returns:
        str: The preprocessed/cleaned text.
    """
    if not text:
        return ""
    # Replace carriage returns with standard newlines
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # Normalize multiple space characters into a single space
    text = re.sub(r"[ \t]+", " ", text)
    # Normalize excessive newlines to at most double newlines (preserving paragraphs)
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Strip leading/trailing whitespace
    return text.strip()
