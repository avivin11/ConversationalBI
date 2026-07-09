"""
utils/config.py — Central Configuration Loader
================================================
Single source of truth for all settings — API keys, model names, paths.
Reads everything from your .env file so nothing is hardcoded.
"""

import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
import streamlit as st

def get_secret(key: str,default: str=None):
    try:
        return st.secrets[key]
    except:
        return os.getenv(key,default)

# LLM settings


GROQ_API_KEY = get_secret("GROQ_API_KEY")
GROQ_MODEL =get_secret("GROQ_MODEL", "llama-3.3-70b-versatile")
GEMINI_API_KEY = get_secret("GEMINI_API_KEY")
GEMINI_MODEL = get_secret("GEMINI_MODEL", "gemini-1.5-flash")

# Embedding model — runs locally on CPU, no API key needed
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ChromaDB settings
CHROMA_PERSIST_DIR =get_secret("CHROMA_PERSIST_DIR", "./chroma_db")
CHROMA_COLLECTION_NAME = get_secret("CHROMA_COLLECTION_NAME", "semantic_model")

# Database
DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///./data/sales.db")

# Paths
SEMANTIC_MODEL_PATH = "./semantic/semantic_model.md"
TMDL_DEFINITION_PATH = get_secret("TMDL_DEFINITION_PATH")


def validate_config():
    """Check that required settings are present before app starts."""
    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY not set.\n"
            "Open .env and add: GROQ_API_KEY=your_key_here"
        )
    print("✅ Config loaded. Groq key found.")


if __name__ == "__main__":
    validate_config()
    print(f"   Model     : {GROQ_MODEL}")
    print(f"   ChromaDB  : {CHROMA_PERSIST_DIR}")
    print(f"   TMDL path : {TMDL_DEFINITION_PATH}")