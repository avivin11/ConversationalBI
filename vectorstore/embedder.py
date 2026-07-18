"""
vectorstore/embedder.py — ChromaDB Embedding + Retrieval
=========================================================
Handles two jobs:
  1. INGESTION  — embed Documents and save to ChromaDB
  2. RETRIEVAL  — given a question, find the most relevant Documents

AI CONCEPT — How embedding + retrieval works:
  Every section of your semantic model gets converted into 384 numbers
  (a vector) by sentence-transformers. ChromaDB stores those vectors.
  When a user asks a question, that question is also converted to 384
  numbers — and ChromaDB finds the stored vectors closest in meaning.
  That's semantic search: finds meaning, not just matching words.
"""

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

from utils.config import (
    EMBEDDING_MODEL,
    CHROMA_PERSIST_DIR,
    CHROMA_COLLECTION_NAME,
)


def get_embedding_model() -> HuggingFaceEmbeddings:
    """
    Load the sentence-transformers embedding model.
    First run downloads ~80MB. Every run after that loads from cache.
    """
    print(f"🧠 Loading embedding model: {EMBEDDING_MODEL}")
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    return embeddings


def build_vectorstore(documents: list[Document]) -> Chroma:
    """
    Embed all documents and store them in ChromaDB on disk.
    Run once via ingest.py — not every time the app starts.
    """
    embeddings = get_embedding_model()

    import chromadb
    client=chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
    existing=[c.name for c in client.list_collections()]
    if CHROMA_COLLECTION_NAME in existing:
        client.delete_collection(CHROMA_COLLECTION_NAME)



    print(f"📦 Building ChromaDB vectorstore...")
    print(f"   Documents to embed: {len(documents)}")

    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        collection_name=CHROMA_COLLECTION_NAME,
        persist_directory=CHROMA_PERSIST_DIR,
    )

    print(f"   ✅ Vectorstore built with {len(documents)} documents")
    return vectorstore


def load_vectorstore() -> Chroma:
    """
    Load an existing ChromaDB vectorstore from disk.
    Called by the app at startup — fast because embedding already done.
    """
    embeddings = get_embedding_model()

    print(f"📂 Loading ChromaDB from: {CHROMA_PERSIST_DIR}")

    vectorstore = Chroma(
        collection_name=CHROMA_COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_PERSIST_DIR,
    )

    count = vectorstore._collection.count()
    if count == 0:
        raise ValueError(
            "ChromaDB is empty. Run python ingest.py --source pbip first."
        )

    print(f"   ✅ Loaded {count} documents from vectorstore")
    return vectorstore


def retrieve_context(question: str, vectorstore: Chroma, k: int = 4) -> list[Document]:
    """
    Find the k most relevant documents for a given question.
    This is the R in RAG — Retrieval.
    """
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k},
    )
    return retriever.invoke(question)


def format_context(docs: list[Document]) -> str:
    """Format retrieved documents into a single string for the LLM prompt."""
    sections = []
    for doc in docs:
        title = (
            doc.metadata.get("measure_name")
            or doc.metadata.get("table_name")
            or doc.metadata.get("section_title", "")
        )
        sections.append(f"[{title}]\n{doc.page_content}")
    return "\n\n---\n\n".join(sections)


if __name__ == "__main__":
    # Quick test: python vectorstore/embedder.py
    model = get_embedding_model()
    test = model.embed_query("What is gross margin?")
    print(f"✅ Embedding model working. Vector length: {len(test)}")