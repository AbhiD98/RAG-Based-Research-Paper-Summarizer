# 📚 Research Paper Q&A System

AI-powered system to upload research papers and ask questions with citations using AWS Bedrock Claude Sonnet.

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   python setup.py
   ```

2. **Set AWS credentials:**
   ```bash
   set AWS_ACCESS_KEY_ID=your_access_key
   set AWS_SECRET_ACCESS_KEY=your_secret_key
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## ✨ Features

- **Multi-PDF Upload**: Process multiple research papers
- **Semantic Search**: Find relevant content using embeddings
- **AI Q&A**: Get answers with paper citations
- **Paper Summaries**: Generate 5-point summaries

## 🛠️ Tech Stack

- **AWS Bedrock**: Claude Sonnet 3.5 for answer generation
- **TF-IDF**: Vector similarity search
- **Scikit-learn**: Text embeddings
- **Streamlit**: Web interface
- **PyPDF2**: PDF text extraction

## 📖 Usage

1. Upload PDF research papers via sidebar
2. Ask questions in natural language
3. Get AI-generated answers with citations
4. Compare findings across multiple papers
5. Generate paper summaries

## 🔧 Configuration

Edit `config.py` to modify:
- AWS region and model ID
- Chunk size and overlap
- Number of retrieved results

## 📊 Example Queries

- "What are the main advantages of CNN over RNN?"
- "Compare performance metrics across papers"
- "What datasets were used in these studies?"
- "Summarize the key contributions"
