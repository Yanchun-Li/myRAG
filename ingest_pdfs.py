from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import os
import shutil

load_dotenv()

def load_and_process_pdfs(data_dir:str):
    """Load PDFs from a directory and process them."""
    loader = DirectoryLoader(
        data_dir,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader
    )
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    documents = loader.load()
    chunks = text_splitter.split_documents(documents)
    return chunks

def create_vector_store(chunks, persist_directory:str):
    """Create a vector store from the chunks and Persist Chroma vector store."""
    if os.path.exists(persist_directory):
        print(f"Clearing existing vector store at {persist_directory}")
        shutil.rmtree(persist_directory)
    
    # Initialize HuggingFace embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2",
        model_kwargs={'device': 'cpu'}
    )

    # Create and persist Chroma vector store
    print("Creating Chroma vector store...")
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    return vectordb

def main():
    # Define the directory containing the PDFs
    data_dir = os.getenv("DATA_DIR")
    db_dir = os.getenv("CHROMA_DB_DIR")

    if not data_dir:
        data_dir = os.path.join(os.path.dirname(__file__), "data")
    if not db_dir:
        db_dir = os.path.join(os.path.dirname(__file__), "chroma_db")

    # Process PDFs
    print(f"Loading and processing PDFs from {data_dir}...")
    chunks = load_and_process_pdfs(data_dir)
    print(f"Created {len(chunks)} chunks from PDFs")

    # Create vector store
    print("Creating vector store...")
    vectordb = create_vector_store(chunks, db_dir)
    print(f"Created vector store at {db_dir}")

if __name__ == "__main__":
    main()