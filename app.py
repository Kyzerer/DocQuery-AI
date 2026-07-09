import streamlit as st
import os
import tempfile
from dotenv import load_dotenv

# Import backend modules
from document_loader import load_document
from text_preprocessor import preprocess_text
from chunker import split_text
from vector_store import (
    add_documents_to_store,
    get_uploaded_documents,
    delete_document_from_store
)
from retriever import retrieve_relevant_chunks
from llm_generator import generate_answer

# Load environment variables
load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="Enterprise AI Knowledge Hub",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Custom CSS
st.markdown("""
<style>
/* Font Imports */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

/* Global Font Override */
html, body, [class*="css"], .stMarkdown {
    font-family: 'Plus Jakarta Sans', 'Outfit', sans-serif;
}

/* Gradient Header */
.title-gradient {
    background: linear-gradient(135deg, #a78bfa 0%, #6366f1 50%, #4f46e5 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
    font-size: 2.8rem;
    margin-bottom: 0.2rem;
    letter-spacing: -0.02em;
}

.subtitle-desc {
    color: #9ca3af;
    font-size: 1.1rem;
    margin-bottom: 2rem;
    font-weight: 400;
}

/* Sidebar Custom Styling */
section[data-testid="stSidebar"] {
    background-color: #0f172a;
    border-right: 1px solid rgba(255, 255, 255, 0.05);
}

section[data-testid="stSidebar"] .stMarkdown h2 {
    color: #f3f4f6;
    font-weight: 700;
    font-size: 1.5rem;
    border-bottom: 2px solid #4f46e5;
    padding-bottom: 0.5rem;
}

/* Chat bubble aesthetics */
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-bottom: 2rem;
}

.citation-box {
    background: rgba(99, 102, 241, 0.08);
    border-left: 4px solid #6366f1;
    border-radius: 4px;
    padding: 0.75rem 1rem;
    margin-top: 0.5rem;
    font-size: 0.85rem;
    color: #e2e8f0;
}

.citation-header {
    font-weight: 600;
    color: #a78bfa;
    margin-bottom: 0.25rem;
}

/* Document Management list items */
.doc-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(255, 255, 255, 0.03);
    padding: 0.6rem 0.8rem;
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    margin-bottom: 0.5rem;
}

.doc-name {
    color: #e2e8f0;
    font-size: 0.9rem;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    max-width: 75%;
}

</style>
""", unsafe_allow_html=True)

# Helper to check API Key availability
def get_api_key():
    # Priority: 1. Sidebar input key, 2. Env variable (GEMINI_API_KEY / GOOGLE_API_KEY)
    if "api_key" in st.session_state and st.session_state.api_key:
        return st.session_state.api_key
    
    env_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    return env_key

# Main application title
st.markdown('<div class="title-gradient">Enterprise AI Knowledge Hub</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-desc">Secure, context-aware Retrieval-Augmented Generation (RAG) assistant for corporate documents.</div>', unsafe_allow_html=True)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "processed_files" not in st.session_state:
    st.session_state.processed_files = set()

# Sidebar Setup
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    
    # API Key configuration
    sidebar_api_key = st.text_input(
        "Enter Gemini API Key",
        type="password",
        value=os.environ.get("GEMINI_API_KEY", ""),
        help="Paste your Gemini API key here if it's not set in the environment variables."
    )
    if sidebar_api_key:
        st.session_state.api_key = sidebar_api_key
        
    api_key = get_api_key()
    
    st.markdown("---")
    st.markdown("## 📥 Document Upload")
    
    # Enable file upload only if API Key is configured (to generate embeddings successfully)
    if not api_key:
        st.warning("🔑 Please configure your Gemini API Key above or in .env to upload documents.")
        uploaded_files = None
    else:
        uploaded_files = st.file_uploader(
            "Upload Files",
            type=["pdf", "docx", "txt", "md", "html"],
            accept_multiple_files=True,
            help="Supported: PDF, DOCX, TXT, MD, HTML"
        )

    # Process Uploaded Files
    if uploaded_files:
        for file in uploaded_files:
            if file.name not in st.session_state.processed_files:
                # 1. Fetch already existing documents to avoid duplicate processing
                existing_docs = get_uploaded_documents(api_key)
                if file.name in existing_docs:
                    st.session_state.processed_files.add(file.name)
                    st.info(f"📄 '{file.name}' is already loaded in the database.")
                    continue
                
                with st.spinner(f"Extracting & processing '{file.name}'..."):
                    try:
                        # Save file to a temporary file
                        suffix = os.path.splitext(file.name)[1]
                        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
                            tmp_file.write(file.getvalue())
                            tmp_path = tmp_file.name
                        
                        # 2. Extract text & metadata
                        raw_text, metadata = load_document(tmp_path)
                        metadata["source"] = file.name  # Overwrite metadata to use original filename
                        
                        # Clean up temp file
                        os.unlink(tmp_path)
                        
                        # 3. Preprocess text
                        clean_text = preprocess_text(raw_text)
                        
                        # 4. Chunk text
                        chunks = split_text(clean_text, metadata)
                        
                        # 5 & 6. Embed and store in ChromaDB
                        if chunks:
                            add_documents_to_store(chunks, api_key)
                            st.session_state.processed_files.add(file.name)
                            st.success(f"✅ Successfully ingested '{file.name}' ({len(chunks)} chunks).")
                        else:
                            st.warning(f"⚠️ '{file.name}' contained no extractable text.")
                            
                    except Exception as e:
                        st.error(f"❌ Error processing '{file.name}': {e}")
        
    st.markdown("---")
    st.markdown("## 📂 Uploaded Knowledge")
    
    # Display list of documents stored in Chroma
    if api_key:
        documents_list = get_uploaded_documents(api_key)
        if documents_list:
            for idx, doc in enumerate(documents_list):
                col1, col2 = st.columns([0.8, 0.2])
                with col1:
                    st.markdown(f"📄 **{doc}**")
                with col2:
                    # Provide button to delete document
                    if st.button("🗑️", key=f"del_{idx}", help=f"Delete '{doc}'"):
                        with st.spinner(f"Deleting '{doc}'..."):
                            success = delete_document_from_store(doc, api_key)
                            if success:
                                st.session_state.processed_files.discard(doc)
                                st.success(f"Deleted '{doc}'")
                                st.rerun()
                            else:
                                st.error(f"Failed to delete '{doc}'")
        else:
            st.info("No documents uploaded yet.")
    else:
        st.info("Enter API Key to view knowledge library.")

# Chat Section
if not api_key:
    st.info("👋 Welcome! Please enter your Gemini API Key in the sidebar configuration to begin.")
else:
    # Retrieve current documents list
    docs = get_uploaded_documents(api_key)
    
    if not docs:
        st.info("💡 Get started by uploading enterprise documents (PDF, DOCX, TXT, MD, HTML) in the sidebar.")
    else:
        # Display conversation history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if "citations" in message and message["citations"]:
                    # Display citations
                    citation_text = ", ".join([cit["source"] for cit in message["citations"]])
                    st.markdown(f'<div class="citation-box"><div class="citation-header">Sources Cited:</div>📄 {citation_text}</div>', unsafe_allow_html=True)

        # Chat Input
        if prompt := st.chat_input("Ask a question about the uploaded documents..."):
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Store user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Generate response
            with st.chat_message("assistant"):
                # 1. Retrieve matching chunks from vector DB
                with st.spinner("Searching internal knowledge base..."):
                    context_chunks = retrieve_relevant_chunks(prompt, api_key=api_key, k=5)
                
                # 2. Generate answer and citations from the LLM
                with st.spinner("Analyzing context & formulating response..."):
                    answer, citations = generate_answer(prompt, context_chunks, api_key=api_key)
                
                st.markdown(answer)
                
                # Display citations if available
                if citations:
                    citation_text = ", ".join([cit["source"] for cit in citations])
                    st.markdown(f'<div class="citation-box"><div class="citation-header">Sources Cited:</div>📄 {citation_text}</div>', unsafe_allow_html=True)
                
                # Store assistant response and citations
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "citations": citations
                })
