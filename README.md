# DocQuery AI 💼🔍

An **Enterprise AI Knowledge Hub** using **Retrieval-Augmented Generation (RAG)**. 

DocQuery AI allows users to upload enterprise documents (PDF, DOCX, TXT, MD, HTML), process them into a local vector database, and perform semantic similarity searches to generate context-bounded answers using Gemini, complete with sources cited.

---

## 🚀 Key Features

* **Multi-Format Document Upload**: Supports PDF, Microsoft Word (`.docx`), plain text (`.txt`), Markdown (`.md`), and HTML.
* **Intelligent Document Processing**: Automatically cleans text (removing carriage returns, normalizing whitespaces) and splits text using LangChain's `RecursiveCharacterTextSplitter`.
* **Local Vector Database**: Generates embeddings using `models/gemini-embedding-001` and stores them locally using ChromaDB.
* **Factual & Context-Bounded Answers**: Connects to the `gemini-2.5-flash` model. Prompts instruct the LLM to answer questions *only* based on the retrieved context, preventing hallucinations.
* **Source Citations**: Every generated answer explicitly shows which uploaded documents were used as the source.
* **Conversation History**: Retains session-based chat history.
* **Knowledge Management**: View uploaded files and delete them from the database in real-time.

---

## 🛠️ Tech Stack

* **Language**: Python 3.13
* **AI Framework**: LangChain
* **Vector Store**: ChromaDB
* **LLM**: Gemini API (`gemini-2.5-flash`, `gemini-embedding-001`)
* **UI**: Streamlit (Premium dark mode UI with glassmorphic cards)

---

## 📦 Installation & Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Kyzerer/DocQuery-AI.git
   cd DocQuery-AI
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   Create a `.env` file in the root directory and add your Gemini API Key:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

4. **Run the Application**:
   ```bash
   python -m streamlit run app.py
   ```

---

## 📁 Project Structure

* `app.py`: Streamlit entrypoint and premium UI layout.
* `document_loader.py`: Parsers for PDF, DOCX, TXT, MD, and HTML files.
* `text_preprocessor.py`: Text cleaning utilities.
* `chunker.py`: Text splitter using RecursiveCharacterTextSplitter.
* `embeddings.py`: Embeddings model setup.
* `vector_store.py`: ChromaDB CRUD operations (add, list, delete).
* `retriever.py`: Semantic retrieval logic.
* `llm_generator.py`: Response generation and citation formatting.
