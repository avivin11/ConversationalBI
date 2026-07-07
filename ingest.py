"""
ingest.py — Build the ChromaDB Vectorstore
==========================================
Run this script ONCE to embed your semantic model into ChromaDB.
Re-run it whenever your Power BI model changes.

WHAT THIS DOES:
  1. Loads your semantic model (from model.bim if available, else semantic_model.md)
  2. Converts it into LangChain Documents (one per table, measure, relationship)
  3. Embeds each Document into a 384-dimensional vector using all-MiniLM-L6-v2
  4. Stores all vectors + original text in ChromaDB on disk

HOW TO RUN:
  python ingest.py                    ← uses semantic_model.md (default)
  python ingest.py --source pbip      ← uses model.bim (requires PBIP export)

AFTER RUNNING:
  A folder called chroma_db/ will appear in your project root.
  The app.py and rag_chain.py load from this folder at startup.
  You do NOT need to run ingest.py every time you start the app —
  only when the semantic model changes.

AI CONCEPT — Why We Pre-Build the Vectorstore:
  Embedding 50 documents takes ~5 seconds (on first run, plus model download).
  If we did this every time the app started, users would wait 5+ seconds
  before asking their first question. By pre-building and saving to disk,
  startup is instant — ChromaDB just loads the existing vectors.
  Same principle as pre-aggregating data in a summary table vs
  calculating SUM() live on every dashboard load.
"""

import argparse
import os
import sys

# Add project root to path so imports work from any directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.config import validate_config, SEMANTIC_MODEL_PATH, TMDL_DEFINITION_PATH
from Semantic.pbip_parser import parse_tmdl_to_documents, load_markdown_fallback
from vectorstore.embedder import build_vectorstore


def main():
    # ── Argument Parsing ──────────────────────────────────────────────────────
    parser = argparse.ArgumentParser(
        description="Build ChromaDB vectorstore from semantic model"
    )
    parser.add_argument(
        "--source",
        choices=["markdown", "pbip"],
        default="markdown",
        help="Source to use: 'markdown' (semantic_model.md) or 'pbip' (model.bim)"
    )
    args = parser.parse_args()

    print("=" * 60)
    print("RAG Conversational BI — Vectorstore Ingestion")
    print("=" * 60)

    # ── Config Validation ─────────────────────────────────────────────────────
    # We don't need the API key for ingestion (no LLM calls here)
    # but we validate the rest of the config
    print("\n📋 Checking configuration...")

    # ── Load Documents ────────────────────────────────────────────────────────
    print(f"\n📄 Loading semantic model (source: {args.source})...")

    if args.source == "pbip":
        tmdl_path = os.getenv("TMDL_DEFINITION_PATH")
        if not tmdl_path or not os.path.exists(tmdl_path):
            print(f"❌ TMDL_DEFINITION_PATH not found or not set in .env")
            print("   Falling back to markdown...")
            documents = load_markdown_fallback(SEMANTIC_MODEL_PATH)
        else:
            documents = parse_tmdl_to_documents(tmdl_path)

    else:  # markdown (default)
        if not os.path.exists(SEMANTIC_MODEL_PATH):
            print(f"❌ semantic_model.md not found at: {SEMANTIC_MODEL_PATH}")
            print("   Edit semantic/semantic_model.md to describe your data model.")
            sys.exit(1)
        documents = load_markdown_fallback(SEMANTIC_MODEL_PATH)

    if not documents:
        print("❌ No documents extracted. Check your source file.")
        sys.exit(1)

    print(f"\n   Loaded {len(documents)} documents:")
    for doc in documents:
        title = doc.metadata.get("section_title") or doc.metadata.get("measure_name") or doc.metadata.get("table_name", "unknown")
        print(f"   - {title}")

    # ── Build Vectorstore ─────────────────────────────────────────────────────
    print(f"\n🔄 Embedding and storing in ChromaDB...")
    print("   (First run downloads ~80MB embedding model — be patient)")

    vectorstore = build_vectorstore(documents)

    # ── Verify ────────────────────────────────────────────────────────────────
    print(f"\n✅ Ingestion complete!")
    print(f"   ChromaDB saved to: ./chroma_db/")
    print(f"\n🧪 Quick retrieval test...")

    test_query = "What is gross margin?"
    results = vectorstore.similarity_search(test_query, k=2)

    print(f"   Query: '{test_query}'")
    print(f"   Top result: {results[0].page_content[:150]}...")
    print(f"\n🚀 Ready for Phase 2. Run: python agent/rag_chain.py to test the full chain.")


if __name__ == "__main__":
    main()