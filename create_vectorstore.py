import os
import json
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

def create_faiss_vectorstore(input_file:str,output_dir:str) -> FAISS:
    load_dotenv()
    huggingface_api_key = os.getenv("HUGGINGFACE_API_KEY")
    if not huggingface_api_key:
        raise ValueError("HUGGINGFACE_API_KEY not found in environment variables.")
    
    with open(input_file, "r") as f:
        documents_data = json.load(f)
    documents = [Document(**doc) for doc in documents_data]

    embeddings = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2")

    print("Creating FAISS vectorstore...")
    vectorstore = FAISS.from_documents(documents, embeddings)

    os.makedirs(output_dir, exist_ok=True)

    vectorstore.save_local(output_dir)
    print(f"FAISS vectorstore saved to {output_dir}")

if __name__ == "__main__":
    input_file = "data_new/json/langchain_documents.json"
    output_dir = "data_new/faiss"
    create_faiss_vectorstore(input_file, output_dir)