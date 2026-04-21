import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv

def _get_huggingface_api_key() -> str:
    load_dotenv()
    key = os.getenv("HUGGINGFACE_API_KEY")
    if not key:
        try:
            import streamlit as st
            key = st.secrets.get("HUGGINGFACE_API_KEY")
        except Exception:
            pass
    if not key:
        raise ValueError("HUGGINGFACE_API_KEY not found. Set it in .env or Streamlit secrets.")
    return key

def load_faiss_vectorstore(vectorstore_dir: str) -> FAISS:
    print(f"Loading FAISS vectorstore from {vectorstore_dir}...")
    huggingface_api_key = _get_huggingface_api_key()

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.load_local(vectorstore_dir, embeddings,allow_dangerous_deserialization=True)
    
    print("FAISS vectorstore loaded successfully.")
    return vectorstore


def search_vectorstore(vectorstore: FAISS, query:str) -> list:
    print(f"Searching for top results for query: '{query}'")
    results = vectorstore.similarity_search(query)
    return results

if __name__ == "__main__":
    huggingface_api_key = _get_huggingface_api_key()
    
    vectorstore_dir = "data_new/faiss"

    vectorstore = load_faiss_vectorstore(vectorstore_dir)

    query = "machine learning in healthcare"
    top_k = 5

    results = search_vectorstore(vectorstore, query)

    for i, result in enumerate(results):
        print(f"\nResult {i}:\n")
        print(f"Name: {result.metadata.get('name', 'N/A')}")
        print(f"Title: {result.metadata.get('title', 'N/A')}")
        print(f"Department: {result.metadata.get('department', 'N/A')}")
        print(f"Email: {result.metadata.get('email', 'N/A')}")
        print(f"Expertise: {result.metadata.get('expertise', 'N/A')}")
        print(f"Profile URL: {result.metadata.get('profile_url', 'N/A')}")
        print(f"Content: {result.page_content}")