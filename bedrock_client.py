import boto3
import json
import os
from typing import List, Dict
from config import AWS_REGION, BEDROCK_INFERENCE_ID

class BedrockClient:
    def __init__(self):
        # Check AWS credentials
        if not os.getenv("AWS_ACCESS_KEY_ID") or not os.getenv("AWS_SECRET_ACCESS_KEY"):
            raise ValueError("AWS credentials not found. Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables.")
        
        self.client = boto3.client(
            service_name='bedrock-runtime',
            region_name=AWS_REGION,
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )
    
    def generate_answer(self, query: str, context_chunks: List[Dict]) -> str:
        # Prepare context from retrieved chunks
        context = ""
        citations = []
        
        for i, chunk in enumerate(context_chunks):
            context += f"[Source {i+1}] {chunk['text']}\n\n"
            citations.append(f"[{chunk['paper_name']}, Page {chunk['page']}]")
        
        prompt = f"""Based on the following research paper excerpts, answer the question and include citations.

Context:
{context}

Question: {query}

Instructions:
- Provide a comprehensive answer based on the context
- Include citations in the format [Paper Name, Page X]
- If comparing multiple papers, highlight differences
- Be specific and technical when appropriate

Answer:"""

        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        })
        
        try:
            response = self.client.invoke_model(
                body=body,
                modelId=BEDROCK_INFERENCE_ID,
                accept='application/json',
                contentType='application/json'
            )
            
            response_body = json.loads(response.get('body').read())
            return response_body['content'][0]['text']
            
        except Exception as e:
            return f"Error generating answer: {str(e)}"
    
    def summarize_paper(self, chunks: List[Dict], paper_name: str) -> str:
        # Get first few chunks for summary
        text_sample = " ".join([chunk['text'] for chunk in chunks[:3]])
        
        prompt = f"""Summarize this research paper in 5 key points:

Paper: {paper_name}
Content: {text_sample}

Provide a concise 5-point summary covering:
1. Main objective/problem
2. Methodology
3. Key findings
4. Contributions
5. Limitations/Future work

Summary:"""

        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 500,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        })
        
        try:
            response = self.client.invoke_model(
                body=body,
                modelId=BEDROCK_INFERENCE_ID,
                accept='application/json',
                contentType='application/json'
            )
            
            response_body = json.loads(response.get('body').read())
            return response_body['content'][0]['text']
            
        except Exception as e:
            return f"Error generating summary: {str(e)}"