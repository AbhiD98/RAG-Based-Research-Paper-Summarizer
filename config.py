import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# AWS Bedrock Configuration
AWS_REGION = "Region"
BEDROCK_INFERENCE_ID = "Model ID"

# RAG Configuration
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K_RESULTS = 5
