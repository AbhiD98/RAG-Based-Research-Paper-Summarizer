import streamlit as st
from rag_system import RAGSystem
import os

# Page config
st.set_page_config(
    page_title="Research Paper Q&A System",
    page_icon="📚",
    layout="wide"
)

# Initialize session state
if 'credentials_ok' not in st.session_state:
    try:
        st.session_state.rag_system = RAGSystem()
        st.session_state.rag_system.load_index()
        st.session_state.credentials_ok = True
    except ValueError as e:
        st.session_state.credentials_ok = False
        st.session_state.credentials_error = str(e)
        st.session_state.rag_system = None

st.title("📚 Research Paper Q&A System")
st.markdown("Upload research papers and ask questions with AI-powered citations")

# Sidebar for paper management
with st.sidebar:
    st.header("📄 Paper Management")
    
    # Upload papers
    uploaded_files = st.file_uploader(
        "Upload PDF Papers",
        type="pdf",
        accept_multiple_files=True
    )
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            if st.button(f"Process {uploaded_file.name}"):
                with st.spinner(f"Processing {uploaded_file.name}..."):
                    result = st.session_state.rag_system.add_paper(
                        uploaded_file, 
                        uploaded_file.name
                    )
                    st.success(result)
                    st.session_state.rag_system.save_index()
    
    # Show uploaded papers
    papers = st.session_state.rag_system.get_papers_list() if st.session_state.rag_system else []
    if papers:
        st.subheader("📋 Uploaded Papers")
        for paper in papers:
            st.write(f"• {paper}")

# Main interface
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🤖 Ask Questions")
    
    # Query input
    query = st.text_area(
        "Enter your question:",
        placeholder="e.g., What are the main advantages of CNN over RNN in NLP?",
        height=100
    )
    
    if st.button("🔍 Ask Question", type="primary"):
        if query and papers:
            with st.spinner("Searching and generating answer..."):
                answer = st.session_state.rag_system.query(query)
                st.markdown("### Answer:")
                st.markdown(answer)
        elif not papers:
            st.warning("Please upload some papers first!")
        else:
            st.warning("Please enter a question!")

with col2:
    st.header("📊 Paper Summaries")
    
    if papers:
        selected_paper = st.selectbox("Select paper to summarize:", papers)
        
        if st.button("📝 Generate Summary"):
            with st.spinner("Generating summary..."):
                summary = st.session_state.rag_system.summarize_paper(selected_paper)
                st.markdown("### Summary:")
                st.markdown(summary)
    else:
        st.info("Upload papers to see summaries")

# Example queries
st.header("💡 Example Queries")
examples = [
    "What methods are used for image classification?",
    "What are the main contributions of this research?",
    "What datasets were used in these studies?",
    "What are the limitations mentioned in the papers?"
]

for example in examples:
    if st.button(f"📌 {example}"):
        st.session_state.query = example

# Footer
st.markdown("---")
st.markdown("**Tech Stack:** AWS Bedrock Claude Sonnet • TF-IDF • Scikit-learn • Streamlit")

# AWS credentials check
if not st.session_state.get('credentials_ok', True):
    st.error(f"⚠️ {st.session_state.get('credentials_error', 'AWS credentials error')}")
    st.info("💡 Set your credentials using: set AWS_ACCESS_KEY_ID=your_key && set AWS_SECRET_ACCESS_KEY=your_secret")
    st.info("Then refresh the page.")
    st.stop()