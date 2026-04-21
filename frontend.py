import streamlit as st
from backend import load_faiss_vectorstore, search_vectorstore

VECTORSTORE_DIR = "data_new/faiss"

st.set_page_config(page_title="UW Prof Finder", layout="centered")

st.markdown("""
<style>
    .stApp, [data-testid="stAppViewContainer"],
    [data-testid="stMain"], [data-testid="stMainBlockContainer"],
    [data-testid="stVerticalBlock"], [data-testid="stBottom"],
    [data-testid="stBottomBlockContainer"],
    .stApp > div, .stApp > div > div {
        background-color: #000000 !important;
        color: #FFFFFF;
    }
    header[data-testid="stHeader"] {
        background-color: #000000 !important;
    }
    h1, h2, h3 {
        color: #FFD54F !important;
    }
    p, span, label, li, div, .stMarkdown, .stText {
        color: #FFFFFF !important;
    }
    [data-testid="stChatMessage"] {
        background-color: #1a1a1a !important;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        border: 1px solid #2a2a2a;
    }
    [data-testid="stChatInput"] {
        background-color: #000000 !important;
    }
    [data-testid="stChatInput"] > div {
        background-color: #000000 !important;
    }
    .stChatInput textarea {
        background-color: #1a1a1a !important;
        color: #FFFFFF !important;
        border: 1px solid #FFD54F !important;
        border-radius: 10px !important;
    }
    .stChatInput textarea::placeholder {
        color: #999999 !important;
    }
    .stChatInput button {
        background-color: #FFD54F !important;
        color: #000000 !important;
    }
    [data-testid="stChatMessageAvatarAssistant"] {
        background-color: #FFD54F !important;
    }
    [data-testid="stAlert"] {
        background-color: #1a1a1a;
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
    [data-testid="InputInstructions"] {
        display: none;
    }
    #uw-logo {
        position: fixed;
        top: 14px;
        left: 20px;
        z-index: 999;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_vectorstore():
    return load_faiss_vectorstore(VECTORSTORE_DIR)

vectorstore = load_vectorstore()

st.markdown("""
<div id="uw-logo">
    <img src="https://uwaterloo.ca/brand/sites/ca.brand/files/universityofwaterloo_logo_horiz_rev.png"
         style="max-width: 180px;"
         alt="University of Waterloo">
</div>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>UW Prof Finder</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #999999 !important;'>Search for professors at the University of Waterloo</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"], unsafe_allow_html=True)

query = st.chat_input("Search by topic, professor name, or department...")

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Searching..."):
            results = search_vectorstore(vectorstore, query)

        if results:
            response = f"Found **{len(results)}** result(s) for your query.\n\n---\n\n"
            for i, result in enumerate(results, 1):
                response += f"### Result {i}\n"
                response += f"**Name**: {result.metadata.get('name', 'N/A')}\n\n"
                response += f"**Title**: {result.metadata.get('title', 'N/A')}\n\n"
                response += f"**Department**: {result.metadata.get('department', 'N/A')}\n\n"
                response += f"**Email**: {result.metadata.get('email', 'N/A')}\n\n"
                response += f"**Expertise**: {result.metadata.get('expertise', 'N/A')}\n\n"
                response += f"**Profile URL**: [Profile Link]({result.metadata.get('profile_url', 'N/A')})\n\n"
                response += f"**Content**: {result.page_content}\n\n---\n\n"
            st.markdown(response)
        else:
            response = "No results found for your query. Try a different search term."
            st.warning(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
