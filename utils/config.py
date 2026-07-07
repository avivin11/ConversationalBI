"""
utils/config.py — Central Configuration Loader
================================================
Single source of truth for all settings — API keys, model names, paths.
Reads everything from your .env file so nothing is hardcoded.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# LLM settings
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# Embedding model — runs locally on CPU, no API key needed
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ChromaDB settings
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "semantic_model")

# Database
DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///./data/sales.db")

# Paths
SEMANTIC_MODEL_PATH = "./semantic/semantic_model.md"
TMDL_DEFINITION_PATH = os.getenv("TMDL_DEFINITION_PATH")


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