import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv

def load_faiss_vectorstore(vectorstore_dir: str) -> FAISS:
    """
    Loads the FAISS vectorstore from the specified directory.

    Parameters:
    - vectorstore_dir: Path to the directory containing the FAISS vectorstore.

    Returns:
    - vectorstore: The loaded FAISS vectorstore.
    """
    print(f"Loading FAISS vectorstore from {vectorstore_dir}...")
    load_dotenv()
    huggingface_api_key = os.getenv("HUGGINGFACE_API_KEY")
    if not huggingface_api_key:
        raise ValueError("OPENAI_API_KEY not found. Please set it in the .env file or pass it explicitly.")

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.load_local(vectorstore_dir, embeddings,allow_dangerous_deserialization=True)
    
    print("FAISS vectorstore loaded successfully.")
    return vectorstore


def search_vectorstore(vectorstore: FAISS, query:str) -> list:
    print(f"Searching for top results for query: '{query}'")
    results = vectorstore.similarity_search(query)
    return results

if __name__ == "__main__":
    load_dotenv()
    huggingface_api_key = os.getenv("HUGGINGFACE_API_KEY")
    if not huggingface_api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables.")
    
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