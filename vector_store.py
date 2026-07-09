import os
from langchain_chroma import Chroma
from langchain_core.documents import Document
from embeddings import get_embeddings_model

CHROMA_DIR = "./chroma_db"
COLLECTION_NAME = "enterprise_knowledge_hub"

def get_vector_store(api_key: str = None) -> Chroma:
    """Initialize and return the Chroma vector store.
    
    Args:
        api_key (str): Gemini API Key for embedding model initialization.
        
    Returns:
        Chroma: The initialized Chroma vector store.
    """
    embeddings = get_embeddings_model(api_key)
    # Chroma manages the creation of directory automatically
    return Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME
    )

def add_documents_to_store(documents: list[Document], api_key: str = None):
    """Add a list of document chunks to the vector store.
    
    Args:
        documents (list[Document]): List of chunked Documents.
        api_key (str): API Key.
    """
    db = get_vector_store(api_key)
    db.add_documents(documents)

def get_uploaded_documents(api_key: str = None) -> list[str]:
    """Retrieve unique names of all uploaded documents from Chroma database.
    
    Args:
        api_key (str): API Key.
        
    Returns:
        list[str]: Sorted list of unique file names.
    """
    try:
        db = get_vector_store(api_key)
        collection = db._collection
        results = collection.get(include=["metadatas"])
        metadatas = results.get("metadatas", [])
        
        sources = set()
        for m in metadatas:
            if m and "source" in m:
                sources.add(m["source"])
        return sorted(list(sources))
    except Exception as e:
        # Handle cases where DB is not initialized or collection is empty
        print(f"Error listing documents from Chroma: {e}")
        return []

def delete_document_from_store(filename: str, api_key: str = None) -> bool:
    """Delete all chunks belonging to a specific document filename.
    
    Args:
        filename (str): Name of the file to delete.
        api_key (str): API Key.
        
    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    try:
        db = get_vector_store(api_key)
        collection = db._collection
        # Get IDs matching the source filename
        results = collection.get(where={"source": filename}, include=[])
        ids = results.get("ids", [])
        if ids:
            collection.delete(ids=ids)
            return True
        return False
    except Exception as e:
        print(f"Error deleting document {filename}: {e}")
        return False
