import PyPDF2
from typing import List, Dict
import re

class PDFProcessor:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def extract_text(self, pdf_file) -> str:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    
    def chunk_text(self, text: str, paper_name: str) -> List[Dict]:
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk_words = words[i:i + self.chunk_size]
            chunk_text = " ".join(chunk_words)
            
            # Calculate approximate page number
            page_num = (i // self.chunk_size) + 1
            
            chunks.append({
                "text": chunk_text,
                "paper_name": paper_name,
                "page": page_num,
                "chunk_id": len(chunks)
            })
        
        return chunks
    
    def process_pdf(self, pdf_file, paper_name: str) -> List[Dict]:
        text = self.extract_text(pdf_file)
        return self.chunk_text(text, paper_name)