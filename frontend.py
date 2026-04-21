import streamlit as st
from backend import load_faiss_vectorstore, search_vectorstore

VECTORSTORE_DIR = "data_new/faiss"

st.set_page_config(page_title="UW Prof Finder", layout="centered")

st.markdown("""
<style>
    .stApp, [data-testid="stAppViewContainer"] {
        background-color: #000000;
        color: #FFFFFF;
    }
    header[data-testid="stHeader"] {
        background-color: #000000;
    }
    .stSidebar, [data-testid="stSidebar"] {
        background-color: #1a1a1a;
        color: #FFFFFF;
    }
    h1, h2, h3 {
        color: #FFD54F !important;
    }
    p, span, label, li, div, .stMarkdown, .stText {
        color: #FFFFFF !important;
    }
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span {
        color: #FFFFFF !important;
    }
    div[data-testid="stFormSubmitButton"] > button {
        background-color: #FFD54F;
        color: #000000 !important;
        font-weight: bold;
        border: none;
    }
    div[data-testid="stFormSubmitButton"] > button:hover {
        background-color: #FFCA28;
        color: #000000 !important;
    }
    .stTextInput input {
        background-color: #1a1a1a;
        color: #FFFFFF !important;
        border: 1px solid #FFD54F;
    }
    .stTextInput input::placeholder {
        color: #999999 !important;
    }
    [data-testid="stAlert"] {
        background-color: #1a1a1a;
        color: #FFFFFF !important;
    }
    [data-testid="stAlert"] p {
        color: #FFD54F !important;
    }
    a {
        color: #FFD54F !important;
    }
    hr {
        border-color: #333333;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_vectorstore():
    return load_faiss_vectorstore(VECTORSTORE_DIR)

vectorstore = load_vectorstore()

with st.sidebar:
    st.image(
        "https://uwaterloo.ca/brand/sites/ca.brand/files/universityofwaterloo_logo_horiz_rgb.png",
        use_container_width=True,
    )
    st.markdown("---")
    with st.form(key="user_input_form"):
        query = st.text_input(
            "Research topic, professor name, or department",
            max_chars=100,
            placeholder="e.g., Machine Learning, John Doe, Computer Science",
        )
        submit = st.form_submit_button("Search")

st.title("UW Prof Finder")
st.write("Search for professors at the University of Waterloo")

if submit:
    if query.strip():
        with st.spinner("Searching..."):
            results = search_vectorstore(vectorstore, query)
        if results:
            st.success(f"Found {len(results)} result(s) for your query.")
            for i, result in enumerate(results, 1):
                st.markdown(f"### Result {i}")
                st.write(f"**Name**: {result.metadata.get('name', 'N/A')}")
                st.write(f"**Title**: {result.metadata.get('title', 'N/A')}")
                st.write(f"**Department**: {result.metadata.get('department', 'N/A')}")
                st.write(f"**Email**: {result.metadata.get('email', 'N/A')}")
                st.write(f"**Expertise**: {result.metadata.get('expertise', 'N/A')}")
                st.write(f"**Profile URL**: [Profile Link]({result.metadata.get('profile_url', 'N/A')})")
                st.write(f"**Content**: {result.page_content}")
                st.markdown("---")
        else:
            st.warning("No results found for your query.")
    else:
        st.error("Please enter a query to search.")
