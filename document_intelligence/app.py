import streamlit as st
import base64
from src.pipeline import DocumentPipeline

# ================= INIT PIPELINE ================= #
@st.cache_resource
def init_pipeline():
    return DocumentPipeline()

pipeline = init_pipeline()

st.set_page_config(page_title="Document RAG System", layout="wide")
st.title("🧠 Document RAG System")

# ================= SESSION STATE ================= #
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "highlighted_pdf" not in st.session_state:
    st.session_state.highlighted_pdf = None

if "loaded_doc" not in st.session_state:
    st.session_state.loaded_doc = None

if "temp_path" not in st.session_state:
    st.session_state.temp_path = None

# ================= SIDEBAR: UPLOAD ================= #
st.sidebar.header("📂 Upload Document")

uploaded_file = st.sidebar.file_uploader(
    "Upload PDF / TXT / DOCX", type=["pdf", "txt", "docx"]
)

# ✅ Load document only ONCE (no repeated processing)
if uploaded_file:
    if st.session_state.loaded_doc != uploaded_file.name:
        temp_path = f"temp_{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        with st.sidebar.spinner("Processing document..."):
            pipeline.upload_document(temp_path)

        st.session_state.loaded_doc = uploaded_file.name
        st.session_state.temp_path = temp_path
        st.session_state.highlighted_pdf = None
        st.session_state.chat_history = []

temp_path = st.session_state.temp_path

# ================= SIDEBAR: HIGHLIGHT ================= #
st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Highlight Keywords")

keywords = st.sidebar.text_input("Enter keywords (comma separated):")

if st.sidebar.button("✨ Highlight PDF"):
    if keywords and temp_path:
        highlighted_path, found_words, not_found_words, _ = pipeline.highlight_keywords(keywords)

        if highlighted_path:
            st.session_state.highlighted_pdf = highlighted_path

            if found_words:
                st.sidebar.success(f"✅ Found: {', '.join(found_words)}")

            if not_found_words:
                st.sidebar.warning(f"❌ Not found: {', '.join(not_found_words)}")
    else:
        st.sidebar.warning("Upload PDF and enter keywords!")

# ================= MAIN LAYOUT ================= #
col_pdf, col_chat = st.columns([1.5, 1])

# ================= PDF VIEWER ================= #
with col_pdf:
    st.subheader("📄 Document Viewer")

    def show_pdf(path):
        with open(path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode("utf-8")
        st.markdown(
            f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600px"></iframe>',
            unsafe_allow_html=True
        )

    if uploaded_file and temp_path and uploaded_file.name.endswith(".pdf"):
        pdf_to_show = st.session_state.highlighted_pdf if st.session_state.highlighted_pdf else temp_path
        show_pdf(pdf_to_show)

# ================= CHATBOT ================= #
with col_chat:
    st.subheader("💬 Chat with Document")

    if not uploaded_file:
        st.info("📂 Upload a document to start chatting.")
    else:
        user_input = st.chat_input("Ask a question...")

        if user_input:
            with st.spinner("🤖 Thinking..."):
                answer, chunks, debug_info = pipeline.chat(user_input)

            st.session_state.chat_history.append(("user", user_input))
            st.session_state.chat_history.append(("assistant", answer))

        for role, msg in st.session_state.chat_history:
            with st.chat_message(role):
                st.write(msg)
