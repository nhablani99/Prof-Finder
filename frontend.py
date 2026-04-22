import streamlit as st
from backend import load_faiss_vectorstore, search_vectorstore

VECTORSTORE_DIR = "data_new/faiss"

st.set_page_config(page_title="UW Prof Finder", layout="wide")

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
    [data-testid="stChatMessage"],
    [data-testid="stChatMessage"] * {
        background-color: #3a3a3a !important;
        border-color: #4a4a4a !important;
    }
    [data-testid="stChatMessage"] {
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        border: 1px solid #4a4a4a;
    }
    [data-testid="stChatInput"] {
        background-color: #000000 !important;
    }
    .stChatInput > div,
    .stChatInput > div * {
        background-color: #2f2f2f !important;
    }
    .stChatInput > div {
        border: 1px solid #424242 !important;
        border-radius: 16px !important;
        padding: 4px 8px !important;
        transition: border-color 0.2s ease !important;
    }
    .stChatInput > div:focus-within {
        border-color: #616161 !important;
    }
    .stChatInput textarea {
        background-color: #2f2f2f !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 0 !important;
        padding: 10px 12px !important;
        outline: none !important;
        box-shadow: none !important;
        font-size: 15px !important;
        line-height: 1.5 !important;
    }
    .stChatInput textarea:focus {
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
    }
    .stChatInput textarea::placeholder {
        color: #8e8e8e !important;
    }
    .stChatInput button {
        background-color: transparent !important;
        color: #8e8e8e !important;
        border: none !important;
        border-radius: 8px !important;
        transition: color 0.2s ease !important;
    }
    .stChatInput button:hover {
        color: #FFFFFF !important;
        background-color: #424242 !important;
    }
    [data-testid="stBottom"],
    [data-testid="stBottom"] > div,
    [data-testid="stBottomBlockContainer"] {
        background-color: #000000 !important;
        max-width: 100% !important;
        width: 100% !important;
        padding-left: 5% !important;
        padding-right: 5% !important;
    }
    [data-testid="stMainBlockContainer"] {
        max-width: 800px !important;
        margin: 0 auto !important;
    }
    [data-testid="stChatMessageAvatarAssistant"] {
        background-color: #3a3a3a !important;
        border-radius: 50% !important;
    }
    [data-testid="stChatMessageAvatarUser"] {
        background-color: #3a3a3a !important;
        border-radius: 50% !important;
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
    [data-testid="stChatMessage"] [data-testid="column"]:last-child {
        display: flex;
        align-items: center;
        justify-content: flex-end;
    }
    [data-testid="stChatMessage"] [data-testid="column"]:last-child button {
        opacity: 0 !important;
        transition: opacity 0.2s ease !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 4px 8px !important;
        min-height: 0 !important;
        height: auto !important;
        line-height: 1 !important;
    }
    [data-testid="stChatMessage"]:hover [data-testid="column"]:last-child button {
        opacity: 1 !important;
    }
    [data-testid="stChatMessage"] [data-testid="column"]:last-child button:hover {
        background-color: #4a4a4a !important;
        border-radius: 6px !important;
    }
    .stTextInput input {
        background-color: #2f2f2f !important;
        color: #FFFFFF !important;
        border: 1px solid #424242 !important;
        border-radius: 8px !important;
    }
    #uw-logo {
        position: fixed;
        top: 42px;
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

if "edit_index" not in st.session_state:
    st.session_state.edit_index = None

def edit_message(idx):
    st.session_state.edit_index = idx

for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        if msg["role"] == "user" and st.session_state.edit_index == i:
            edited = st.text_input("Edit your query:", value=msg["content"], key=f"edit_{i}", label_visibility="collapsed")
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("Submit", key=f"submit_{i}"):
                    st.session_state.messages = st.session_state.messages[:i]
                    st.session_state.edit_index = None
                    st.session_state.pending_query = edited
                    st.rerun()
            with col2:
                if st.button("Cancel", key=f"cancel_{i}"):
                    st.session_state.edit_index = None
                    st.rerun()
        elif msg["role"] == "user":
            col_msg, col_btn = st.columns([20, 1])
            with col_msg:
                st.markdown(msg["content"], unsafe_allow_html=True)
            with col_btn:
                st.button("✏️", key=f"edit_btn_{i}", on_click=edit_message, args=(i,), help="Edit this query")
        else:
            st.markdown(msg["content"], unsafe_allow_html=True)

query = st.chat_input("Search by topic, professor name, or department...")

if "pending_query" in st.session_state and st.session_state.pending_query:
    query = st.session_state.pending_query
    st.session_state.pending_query = None

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
