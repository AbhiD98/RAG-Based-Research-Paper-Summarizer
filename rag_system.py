from pdf_processor import PDFProcessor
from vector_store import VectorStore
from bedrock_client import BedrockClient
from config import TOP_K_RESULTS
from typing import List, Dict

class RAGSystem:
    def __init__(self):
        self.pdf_processor = PDFProcessor()
        self.vector_store = VectorStore()
        self.bedrock_client = BedrockClient()
        self.papers = {}  # Store paper metadata
    
    def add_paper(self, pdf_file, paper_name: str):
        # Process PDF
        chunks = self.pdf_processor.process_pdf(pdf_file, paper_name)
        
        # Add to vector store
        self.vector_store.add_documents(chunks)
        
        # Store paper metadata
        self.papers[paper_name] = {
            "chunks": len(chunks),
            "added": True
        }
        
        return f"Added {len(chunks)} chunks from {paper_name}"
    
    def query(self, question: str) -> str:
        # Retrieve relevant chunks
        results = self.vector_store.search(question, TOP_K_RESULTS)
        
        if not results:
            return "No relevant information found. Please upload some papers first."
        
        # Extract chunks for context
        context_chunks = [result[0] for result in results]
        
        # Generate answer using Bedrock
        answer = self.bedrock_client.generate_answer(question, context_chunks)
        
        return answer
    
    def summarize_paper(self, paper_name: str) -> str:
        # Find chunks for specific paper
        paper_chunks = [chunk for chunk in self.vector_store.chunks 
                       if chunk['paper_name'] == paper_name]
        
        if not paper_chunks:
            return f"Paper '{paper_name}' not found."
        
        return self.bedrock_client.summarize_paper(paper_chunks, paper_name)
    
    def get_papers_list(self) -> List[str]:
        return list(self.papers.keys())
    

    def save_index(self, path: str = "rag_index"):
        self.vector_store.save(path)
    
    def load_index(self, path: str = "rag_index"):
        self.vector_store.load(path)