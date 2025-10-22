import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# AWS Bedrock Configuration
AWS_REGION = "ap-south-1"
BEDROCK_INFERENCE_ID = "apac.anthropic.claude-sonnet-4-20250514-v1:0"

# RAG Configuration
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K_RESULTS = 5
