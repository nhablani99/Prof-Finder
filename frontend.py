import streamlit as st
from backend import load_faiss_vectorstore, search_vectorstore

VECTORSTORE_DIR = "data_new/faiss"

@st.cache_resource
def load_vectorstore():
    return load_faiss_vectorstore(VECTORSTORE_DIR)

vectorstore = load_vectorstore()

st.title("UW Prof Finder")
st.write("Search for professors at the University of Waterloo")

with st.sidebar:
    with st.form(key="user_input_form"):
        query = st.text_input("Research topic, professor name, or department", max_chars=100,placeholder= "e.g., Machine Learning, John Doe, Computer Science")
        submit = st.form_submit_button("Search")



if submit:
    if query.strip():
        with st.spinner("Searching..."):
            results = search_vectorstore(vectorstore, query)
        if results:
            st.success(f"Found {len(results)} result(s) for your query.")
            for i, result in enumerate(results, 1):
                st.write(f"### Result {i}")
                st.write(f"**Name**: {result.metadata.get('name', 'N/A')}")
                st.write(f"**Title**: {result.metadata.get('title', 'N/A')}")
                st.write(f"**Department**: {result.metadata.get('department', 'N/A')}")
                st.write(f"**Email**: {result.metadata.get('email', 'N/A')}")
                st.write(f"**Expertise**: {result.metadata.get('expertise', 'N/A')}")
                st.write(f"**Profile URL**: [Profile Link]({result.metadata.get('profile_url', 'N/A')})")
                st.write(f"**Content**: {result.page_content}")
                st.write("---")
        else:
            st.warning("No results found for your query.")
    else:
        st.error("Please enter a query to search.")