from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def split_text(text: str, metadata: dict, chunk_size: int = 1000, chunk_overlap: int = 200) -> list[Document]:
    """Split preprocessed text into chunked LangChain Document objects.
    
    Args:
        text (str): The preprocessed text.
        metadata (dict): Metadata mapping back to the original document.
        chunk_size (int): Maximum size of each chunk (in characters).
        chunk_overlap (int): Overlap size between adjacent chunks (in characters).
        
    Returns:
        list[Document]: List of LangChain Document chunks.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    
    # Split the raw text into chunks
    chunks = splitter.split_text(text)
    
    # Wrap each chunk in a LangChain Document object with metadata
    documents = []
    for idx, chunk in enumerate(chunks):
        chunk_metadata = metadata.copy()
        chunk_metadata["chunk_index"] = idx
        documents.append(Document(page_content=chunk, metadata=chunk_metadata))
        
    return documents
