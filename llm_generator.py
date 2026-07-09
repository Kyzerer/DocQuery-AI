import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

SYSTEM_PROMPT = """You are an Enterprise AI Knowledge Assistant. Your goal is to answer the user's question based strictly on the provided document context.

Rules:
1. Use ONLY the facts, figures, and details provided in the Context below to answer the user's question.
2. If the answer cannot be found or inferred directly from the provided Context, say: "I cannot find the answer in the provided documents."
3. Do not make up facts, hallucinate, or use any outside knowledge.
4. Keep your answer professional, clear, and structured.

Context:
{context}"""

def get_llm(api_key: str = None) -> ChatGoogleGenerativeAI:
    """Initialize and return the Gemini Chat Model.
    
    Args:
        api_key (str): Optional API Key. If not provided, it checks environment variables.
        
    Returns:
        ChatGoogleGenerativeAI: The initialized Gemini LLM.
    """
    key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        raise ValueError(
            "Gemini/Google API Key not found. "
            "Please configure the key in the .env file, system environment, "
            "or input it in the sidebar."
        )
        
    # We use 'gemini-2.5-flash' which is fast, highly cost-effective, and fully supported
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=key,
        temperature=0.0  # Set temperature to 0 to ensure high factual accuracy and avoid hallucinations
    )

def generate_answer(query: str, context_chunks: list[Document], api_key: str = None) -> tuple[str, list[dict]]:
    """Generate an answer using Gemini based on retrieved chunks and extract citations.
    
    Args:
        query (str): The user question.
        context_chunks (list[Document]): Chunks retrieved from the vector DB.
        api_key (str): Optional API Key.
        
    Returns:
        tuple[str, list[dict]]: The generated answer text and a list of citation dictionaries.
    """
    if not context_chunks:
        return "I cannot find the answer in the provided documents.", []
        
    # Format the retrieved context for the prompt
    context_text = ""
    for idx, chunk in enumerate(context_chunks):
        source = chunk.metadata.get("source", "Unknown Document")
        context_text += f"--- Document Chunk {idx + 1} (Source: {source}) ---\n"
        context_text += chunk.page_content.strip() + "\n\n"
        
    llm = get_llm(api_key)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{question}")
    ])
    
    chain = prompt | llm | StrOutputParser()
    
    # Generate response
    answer = chain.invoke({
        "context": context_text,
        "question": query
    })
    
    # Extract unique source citations from context chunks
    citations = []
    seen_sources = set()
    for chunk in context_chunks:
        source = chunk.metadata.get("source", "Unknown Document")
        if source not in seen_sources:
            seen_sources.add(source)
            citations.append({
                "source": source
            })
            
    return answer, citations
