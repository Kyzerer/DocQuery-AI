from langchain_core.documents import Document
from vector_store import get_vector_store

def retrieve_relevant_chunks(query: str, api_key: str = None, k: int = 5) -> list[Document]:
    """Retrieve the top k most relevant chunks from ChromaDB based on semantic similarity search.
    
    Args:
        query (str): The natural language query.
        api_key (str): Optional API Key.
        k (int): Number of relevant document chunks to return.
        
    Returns:
        list[Document]: List of matching Document chunks.
    """
    db = get_vector_store(api_key)
    # Perform similarity search using the vector store
    return db.similarity_search(query, k=k)
