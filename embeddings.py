import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings

def get_embeddings_model(api_key: str = None) -> GoogleGenerativeAIEmbeddings:
    """Initialize and return the Google Generative AI Embeddings model.
    
    Args:
        api_key (str): Optional API key. If not provided, it will look up the
                       GEMINI_API_KEY or GOOGLE_API_KEY environment variables.
                       
    Returns:
        GoogleGenerativeAIEmbeddings: The initialized embeddings model.
    """
    key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        raise ValueError(
            "Gemini/Google API Key not found. "
            "Please configure the key in the .env file, system environment, "
            "or input it in the sidebar."
        )
        
    # We use 'models/gemini-embedding-001', which is supported under the current credentials
    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=key
    )
