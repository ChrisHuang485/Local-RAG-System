import os

LLM_MODEL_NAME = "qwen3:14b"
EMBEDDING_MODEL_NAME = "BAAI/bge-m3"
RERANKER_MODEL_NAME = "BAAI/bge-reranker-base"
LOCAL_MODELS_PATH = "./local_models"
EMBEDDING_MODEL_PATH = LOCAL_MODELS_PATH + "bge-m3"
RERANKER_MODEL_PATH = LOCAL_MODELS_PATH + "bge-reranker-base"


DEFAULT_KNOWLEDGE_BASE = "my_knowledge_base"
CHROMA_PERSIST_DIR = "./chroma_db_parent"

CHUNK_SIZE_PARENT = 1000
CHUNK_OVERLAP_PARENT = 100
CHUNK_SIZE_CHILD = 200
CHUNK_OVERLAP_CHILD = 20
SEARCH_K = 10
TOP_N = 3

DEFAULT_SYSTEM_PROMPT = """
You are an intelligent and helpful local knowledge base assistant. Your task is to answer the user's question based on the provided reference information below.

Please follow these guidelines:
1. Answer the question using ONLY the provided [Context]. Do not use outside knowledge or make up information.
2. If the answer is not contained within the [Context], simply state: "I cannot find the answer in the provided documents."
3. Keep your answer clear, accurate, and professional.
4. If applicable, reference the specific section or document name provided in the context.
5. USER INSTRUCTION: {user_req}

Context:
{context}

Question: {question}

Helpful Answer:
"""