# My RAG Project

This project provides the following primary features:

1. **Vector database creation and management**: Splits documents (mainly PDFs) into chunks and stores embeddings in a Chroma vector database for subsequent retrieval.  
2. **RAG QA**: Uses the tools and models defined in `rag.py` to retrieve context from the vector database and generate answers based on that context.  
3. **Streamlit Frontend**: Deploys a quick interactive web interface with `streamlit.py` to interact with the RAG QA system.  
4. **DOCX to PDF Conversion**: Uses `convert_docx2pdf.py` to bulk-convert `.docx` files to PDF in a specified folder.

---

## File/Script Overview

- **`rag.py`**  
  - Core RAG logic.  
  - Reads model-related configurations from environment variables, instantiates both a reasoning model and a tool model (supports HuggingFace or local/OpenAI).  
  - Provides a `rag_with_reasoner` tool to search the Chroma vector store, then uses the retrieved content to generate an answer.  
  - Finally, it sets up a `ToolCallingAgent` with possible usage of a `GradioUI` for web-based interaction (optional).

- **`ingest_pdfs.py`**  
  - Handles bulk processing of PDF documents in a given directory.  
  - Loads and splits documents into chunks based on a specified text-splitting strategy.  
  - Uses `HuggingFaceEmbeddings` for embedding and stores vectors in a Chroma database (persisted locally).  

- **`streamlit.py`**  
  - A Streamlit web app example.  
  - Provides a browser-based chat interface for the RAG QA.  
  - Ensures the local vector database is available and references the logic in `rag.py`.  

- **`convert_docx2pdf.py`**  
  - Scans a target folder for `.docx` files and converts each one to PDF format.  
  - Requires the `docx2pdf` library.  

---

## Installation

1. **(Optional) Create and activate a virtual environment**:

    ```bash
    # Windows
    python -m venv myRAGEnv
    myRAGEnv\Scripts\activate

    # Linux / macOS
    python3 -m venv myRAGEnv
    source myRAGEnv/bin/activate
    ```

2. **Install required dependencies**:

    ```bash
    pip install -r requirements.txt
    ```
    
    If a `requirements.txt` file is not provided, you can install the major libraries manually (example):
    ```bash
    pip install langchain langchain_community sentence-transformers chromadb streamlit gradio python-dotenv docx2pdf
    ```

---

## Environment Variables and `.env` Setup

Create a `.env` file in the project root to store environment variables (example, adjust as needed):

```ini
# "yes" to use HuggingFace's HfApiModel; otherwise local/OpenAI is used
USE_HUGGINGFACE=yes
# "yes" to use OpenAI model (requires OPENAI_API_KEY)
USE_OPENAI=no

# HuggingFace API Token (needed if USE_HUGGINGFACE=yes)
HUGGINGFACE_API_TOKEN=hf_xxxxxxxxxxxxxxxxxx

# OpenAI API Key (needed if USE_OPENAI=yes)
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx

# Model IDs for reasoning and tool usage
REASONING_MODEL_ID=deepseek-r1:7b-8k
TOOL_MODEL_ID=qwen2.5:14b

# Directories for data and the Chroma vector store
DATA_DIR=./data
CHROMA_DB_DIR=./chroma_db
