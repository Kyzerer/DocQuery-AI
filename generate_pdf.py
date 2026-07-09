import os
from fpdf import FPDF
from fpdf.enums import XPos, YPos

class DocQueryPDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_margins(15, 20, 15)
        self.alias_nb_pages()
        
    def header(self):
        # We only print header on pages after the cover page (Page 1)
        if self.page_no() > 1:
            self.set_font("helvetica", "B", 9)
            self.set_text_color(79, 70, 229) # Indigo primary
            self.cell(0, 6, "DocQuery AI - Enterprise Knowledge Hub (RAG)", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="L")
            self.set_draw_color(229, 231, 235) # Light grey border
            self.set_line_width(0.3)
            self.line(15, 22, 195, 22)
            self.ln(6)

    def footer(self):
        if self.page_no() > 1:
            self.set_y(-15)
            self.set_font("helvetica", "I", 8)
            self.set_text_color(156, 163, 175) # Light grey text
            self.cell(0, 10, f"Page {self.page_no()} of {{nb}}", align="C")
            
    def cover_page(self):
        self.add_page()
        
        # Background design (top-right colored accent bands)
        self.set_fill_color(243, 244, 246) # Light grey canvas
        self.rect(0, 0, 210, 297, "F")
        
        # Right sidebar vertical accent bar
        self.set_fill_color(79, 70, 229) # Indigo accent
        self.rect(198, 0, 12, 297, "F")
        self.set_fill_color(139, 92, 246) # Purple secondary accent
        self.rect(193, 0, 5, 297, "F")
        
        # Cover content layout
        self.set_y(55)
        self.set_font("helvetica", "B", 14)
        self.set_text_color(109, 40, 217) # Purple
        self.cell(0, 10, "ENTERPRISE SOLUTION MANUAL", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        # Title
        self.set_font("helvetica", "B", 38)
        self.set_text_color(17, 24, 39) # Slate-900
        self.cell(0, 18, "DocQuery AI", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        # Divider Line
        self.set_draw_color(79, 70, 229)
        self.set_line_width(1.5)
        self.line(15, 87, 85, 87)
        
        self.ln(12)
        
        # Subtitle
        self.set_font("helvetica", "B", 18)
        self.set_text_color(79, 70, 229) # Indigo
        self.cell(0, 10, "Knowledge Hub & Q&A RAG Platform", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        # Description paragraph
        self.ln(5)
        self.set_font("helvetica", "", 11)
        self.set_text_color(75, 85, 99) # Slate-600
        desc = ("A high-performance web application designed for secure indexing, retrieval, "
                "and semantic parsing of corporate internal documentation (PDF, Word, TXT, MD, HTML) "
                "leveraging LangChain, ChromaDB, and Google Gemini API.")
        self.multi_cell(160, 6, desc)
        
        # System status card
        self.set_y(175)
        self.set_fill_color(255, 255, 255)
        self.set_draw_color(209, 213, 219)
        self.set_line_width(0.3)
        self.rect(15, 175, 160, 48, "DF")
        
        # Status Card Content
        self.set_xy(20, 180)
        self.set_font("helvetica", "B", 10)
        self.set_text_color(107, 114, 128) # Grey
        self.cell(40, 6, "METADATA CONFIG")
        self.cell(60, 6, "DEPLOYMENT SETTINGS", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        self.set_x(20)
        self.set_font("helvetica", "", 9)
        self.set_text_color(31, 41, 55) # Dark
        self.cell(40, 6, "Version: 2.1.0 (Stable)")
        self.cell(60, 6, "Runtime Server: Streamlit Local Host", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        self.set_x(20)
        self.cell(40, 6, "Framework: LangChain v0.1+")
        self.cell(60, 6, "Default Port: 8501", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        self.set_x(20)
        self.cell(40, 6, "Vector DB: Chroma DB")
        self.cell(60, 6, "URL: http://localhost:8501", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        # Date footer
        self.set_y(260)
        self.set_font("helvetica", "B", 10)
        self.set_text_color(75, 85, 99)
        self.cell(0, 5, "Developer: Kyzerer", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_font("helvetica", "", 9)
        self.cell(0, 5, "Date: July 2026", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
    def add_heading_1(self, text):
        self.ln(6)
        self.set_font("helvetica", "B", 16)
        self.set_text_color(17, 24, 39) # Dark slate
        self.cell(0, 10, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)
        
    def add_heading_2(self, text):
        self.ln(4)
        self.set_font("helvetica", "B", 12)
        self.set_text_color(79, 70, 229) # Indigo
        self.cell(0, 8, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1)
        
    def add_paragraph(self, text):
        self.set_font("helvetica", "", 10)
        self.set_text_color(55, 65, 81) # Slate grey
        self.multi_cell(0, 5.5, text)
        self.ln(3)

    def add_bullet_point(self, title, text):
        self.set_font("helvetica", "B", 10)
        self.set_text_color(31, 41, 55)
        self.set_x(20)
        self.cell(4, 5.5, "-", ln=0)
        self.cell(40, 5.5, title + ":", ln=0)
        
        self.set_font("helvetica", "", 10)
        self.set_text_color(55, 65, 81)
        self.multi_cell(0, 5.5, text)
        self.ln(1.5)

    def add_code_block(self, code_text):
        self.ln(2)
        self.set_fill_color(243, 244, 246) # grey-100
        self.set_draw_color(229, 231, 235) # grey-200
        self.set_font("courier", "", 9)
        self.set_text_color(31, 41, 55)
        
        lines = code_text.strip().split("\n")
        max_height = len(lines) * 4.5 + 4
        
        # Calculate current Y position and add page break if needed
        if self.get_y() + max_height > 270:
            self.add_page()
            
        x_start = self.get_x()
        y_start = self.get_y()
        
        # Draw background rectangle
        self.rect(x_start, y_start, 180, max_height, "DF")
        
        # Add padding text
        self.set_xy(x_start + 4, y_start + 2)
        for line in lines:
            self.cell(0, 4.5, line, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.set_x(x_start + 4)
            
        self.set_y(y_start + max_height)
        self.ln(4)

    def add_callout(self, text, type="note"):
        self.ln(2)
        if type == "important":
            self.set_fill_color(254, 242, 242) # Red 50
            border_color = (239, 68, 68) # Red 500
            text_color = (153, 27, 27) # Red 800
            label = "IMPORTANT:"
        else:
            self.set_fill_color(239, 246, 255) # Blue 50
            border_color = (59, 130, 246) # Blue 500
            text_color = (30, 58, 138) # Blue 900
            label = "NOTE:"
            
        lines = self.multi_cell(172, 5, f"{label} {text}", split_only=True)
        max_height = len(lines) * 5 + 6
        
        if self.get_y() + max_height > 270:
            self.add_page()
            
        x = self.get_x()
        y = self.get_y()
        
        # Draw background rect
        self.rect(x, y, 180, max_height, "F")
        # Draw left border accent line
        self.set_draw_color(*border_color)
        self.set_line_width(1.2)
        self.line(x, y, x, y + max_height)
        
        # Draw text inside box
        self.set_xy(x + 5, y + 3)
        self.set_font("helvetica", "", 9.5)
        self.set_text_color(*text_color)
        self.multi_cell(170, 5, f"{label} {text}")
        
        self.set_y(y + max_height)
        self.ln(4)
        
    def add_table(self, headers, rows):
        self.ln(3)
        # Column widths
        widths = [45, 135]
        
        # Header Row
        self.set_fill_color(79, 70, 229) # Indigo
        self.set_text_color(255, 255, 255)
        self.set_font("helvetica", "B", 9.5)
        self.set_draw_color(209, 213, 219)
        self.set_line_width(0.2)
        
        # Print headers
        for h, w in zip(headers, widths):
            self.cell(w, 8, h, border=1, ln=0, align="L", fill=True)
        self.ln()
        
        # Data Rows
        self.set_font("helvetica", "", 9)
        self.set_text_color(55, 65, 81)
        
        fill = False
        for row in rows:
            # Check page break
            if self.get_y() + 8 > 270:
                self.add_page()
                # Reprint headers if page broke
                self.set_fill_color(79, 70, 229)
                self.set_text_color(255, 255, 255)
                self.set_font("helvetica", "B", 9.5)
                for h, w in zip(headers, widths):
                    self.cell(w, 8, h, border=1, ln=0, fill=True)
                self.ln()
                self.set_font("helvetica", "", 9)
                self.set_text_color(55, 65, 81)
                
            self.set_fill_color(249, 250, 251) if fill else self.set_fill_color(255, 255, 255)
            
            # Print first cell (module name)
            self.set_font("courier", "B", 9)
            self.cell(widths[0], 8.5, row[0], border=1, ln=0, fill=True)
            
            # Print second cell (description)
            self.set_font("helvetica", "", 9)
            self.cell(widths[1], 8.5, row[1], border=1, ln=1, fill=True)
            
            fill = not fill
        self.ln(4)

def build_project_manual():
    pdf = DocQueryPDF()
    pdf.cover_page()
    
    # Page 2: System Architecture & Workflow
    pdf.add_page()
    pdf.add_heading_1("1. System Architecture & Workflow")
    pdf.add_paragraph("DocQuery AI implements a classic Retrieval-Augmented Generation (RAG) pattern. RAG optimizes Large Language Model (LLM) performance by anchoring the models to proprietary enterprise records, preventing hallucinations, and ensuring all generated answers are fully auditable.")
    
    pdf.add_heading_2("1.1 Document Processing & Vector Storage")
    pdf.add_paragraph("The workflow begins when a document is uploaded via the Streamlit dashboard. The backend processes the document through the following pipelined stages:")
    
    pdf.add_bullet_point("Text Extraction", "Determines file extensions and invokes the correct parsing driver (pypdf for PDFs, python-docx for Word files, BeautifulSoup for HTML, or standard readers for TXT/MD files).")
    pdf.add_bullet_point("Text Preprocessing", "Normalizes spacing and line endings to form a clean, continuous block of content.")
    pdf.add_bullet_point("Recursive Chunking", "Segments the cleaned content using characters like paragraph breaks and spaces to ensure high cohesive integrity. Standard size is 1000 characters with 200 characters overlap.")
    pdf.add_bullet_point("Embedding Generation", "Calculates dense vector representations for each text chunk using the Google Generative AI embeddings endpoint.")
    pdf.add_bullet_point("Persistent Storage", "Indexes and stores the generated vectors inside ChromaDB, mapping metadata (like the source filename) back to the chunks.")
    
    pdf.add_heading_2("1.2 Query, Retrieval, and Response Loop")
    pdf.add_paragraph("When a user enters a question in the chat interface, the following actions are executed:")
    pdf.add_bullet_point("Semantic Search", "The query is converted into a vector embedding and matched against indexed chunks in ChromaDB using cosine similarity.")
    pdf.add_bullet_point("Context Ingestion", "The top-k (default k=5) matching text blocks are extracted and concatenated to form a context snippet.")
    pdf.add_bullet_point("Factual LLM Assembly", "The system wraps the context and user query inside a strict system prompt, which is sent to the Gemini 2.5 Flash model.")
    pdf.add_bullet_point("Citation Retrieval", "The generated response is displayed alongside the distinct document filenames (citations) that provided the context.")

    pdf.add_callout("This platform does not utilize external cloud databases or third-party web search services. All vector stores and metadata indices are written and read locally on disk, ensuring absolute data privacy and isolation.", "note")

    # Page 3: Core Code Modules
    pdf.add_page()
    pdf.add_heading_1("2. Core Code Modules & Index")
    pdf.add_paragraph("DocQuery AI has been built following clean code conventions. Every system operation is separated into discrete, reusable Python modules:")
    
    headers = ["Module File", "System Component Purpose & Implementation Details"]
    rows = [
        ["app.py", "Streamlit UI container; manages session states, sidebars, uploads, deletes, and chat interface."],
        ["document_loader.py", "Extracts raw text. Uses PyPDFReader, docx.Document, and BeautifulSoup parsing drivers."],
        ["text_preprocessor.py", "Cleans extracted text, removing double spaces and triple newlines for optimal parsing."],
        ["chunker.py", "Wraps RecursiveCharacterTextSplitter to chunk text blocks while preserving source metadata."],
        ["embeddings.py", "Instantiates GoogleGenerativeAIEmbeddings under models/gemini-embedding-001."],
        ["vector_store.py", "Direct interface for Chroma DB; implements document additions, lists, and chunk-level deletions."],
        ["retriever.py", "Queries Chroma DB and returns the top k similarity-matched document chunks."],
        ["llm_generator.py", "Connects to ChatGoogleGenerativeAI (gemini-2.5-flash) and processes context-bounded prompts."]
    ]
    pdf.add_table(headers, rows)
    
    pdf.add_heading_2("2.1 Local Configuration Template")
    pdf.add_paragraph("Authentication keys are loaded automatically from a root .env file. Below is the configuration layout:")
    pdf.add_code_block("GEMINI_API_KEY=your_gemini_api_key_here\nGOOGLE_API_KEY=your_gemini_api_key_here")

    # Page 4: User Manual & Execution
    pdf.add_page()
    pdf.add_heading_1("3. User Manual & Operations Guide")
    pdf.add_paragraph("To run and test the application, follow these guidelines to manage files, prompt the model, and verify results.")
    
    pdf.add_heading_2("3.1 Installing & Starting the Application")
    pdf.add_paragraph("First, verify that your environment variables are configured in the .env file. Next, execute the installation and launch commands:")
    pdf.add_code_block("# Step 1: Install dependencies\npip install -r requirements.txt\n\n# Step 2: Start Streamlit server\npython -m streamlit run app.py")
    pdf.add_paragraph("The server will start and bind locally. You can open and interact with the application by navigating to http://localhost:8501 in your browser.")
    
    pdf.add_heading_2("3.2 Document Upload & List Verification")
    pdf.add_paragraph("1. In the left-hand sidebar, upload any PDF, Word, TXT, MD, or HTML document. You will see a loading spinner during parsing and ingestion.\n"
                      "2. Once ingestion is complete, the document name will appear under the 'Uploaded Knowledge' section in the sidebar.\n"
                      "3. You can verify document registration in the database immediately.")

    pdf.add_heading_2("3.3 Chat Q&A and Verification")
    pdf.add_paragraph("Submit natural language questions inside the main chat interface. DocQuery AI will query ChromaDB, fetch similar passages, and present the answer. Under the response, a 'Sources Cited' box will display the original filenames.\n\n"
                      "To test boundary rules (hallucination checks), query the model about a topic not mentioned in your uploaded documents. The LLM should strictly output: 'I cannot find the answer in the provided documents.'")
    
    pdf.add_heading_2("3.4 Document Deletion")
    pdf.add_paragraph("To remove a file from the database, click the trash can icon next to its name in the sidebar. The system will delete all vector chunks matching that filename in ChromaDB and trigger a visual refresh.")
    
    pdf.add_callout("Deleting a document is irreversible. Once deleted, its chunks are purged from ChromaDB and will no longer be retrieved to answer chat queries.", "important")
    
    # Save the PDF file
    output_path = "d:/airag/DocQuery_AI_Project_Manual.pdf"
    pdf.output(output_path)
    print(f"PDF successfully generated at: {output_path}")

if __name__ == "__main__":
    build_project_manual()
