# 📊 Conversational BI Assistant

A natural language chatbot that answers plain-English business questions by combining **Power BI semantic model knowledge** with live data — powered by RAG + LLM.

> *"Which customer segment drives the most revenue?"* → instant, grounded answer.

🚀 **[Live Demo](https://avivin11-conversationalbi.streamlit.app)**

---

## 🎯 What it does

Traditional BI requires users to know where to look. This assistant lets anyone ask questions in plain English and get answers grounded in the actual data model — no guessing, no hallucination.

- Ask questions about your Power BI semantic model in plain English
- Retrieves the exact measure definitions and table schemas relevant to the question
- Generates a grounded answer citing your actual DAX measures and columns
- Works with any Power BI PBIP project file — plug and play

---

## 🏗️ How it works

```
User Question
      ↓
ChromaDB (Vector Store)          ← Power BI TMDL files parsed + embedded
      ↓
Retrieved semantic context
      ↓
Groq LLM (Llama-3.3-70B)        ← context + question → grounded answer
      ↓
Answer displayed in Streamlit UI
```

This pattern is called **RAG — Retrieval-Augmented Generation**. Instead of the LLM guessing what your measures mean, it reads the actual definitions from your Power BI model before answering.

---

## 🧰 Tech Stack

| Layer | Tool |
|---|---|
| LLM | Llama-3.3-70B via Groq (free tier) |
| Vector Store | ChromaDB |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 |
| Orchestration | LangChain |
| Semantic Model | Power BI TMDL format (PBIP) |
| UI | Streamlit |
| Deployment | Streamlit Community Cloud |

---

## 🚦 Three modes

### 🎯 Demo Mode
Try instantly with a pre-loaded retail dashboard — no setup needed.

### 📁 Local PBIP Path
Point to your own Power BI PBIP `definition/` folder. The app parses your TMDL files and builds a knowledge base from your actual semantic model.

### ⬆️ Upload TMDL Files
Upload `.tmdl` files directly from your PBIP project. The app builds ChromaDB in real time from your uploaded files.

---

## 🚀 Run locally

```bash
# Clone the repo
git clone https://github.com/avivin11/ConversationalBI.git
cd ConversationalBI

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
copy .env.example .env
# Add your GROQ_API_KEY to .env
# Get a free key at https://console.groq.com

# Run the app
streamlit run ui/app.py
```

---

## 📁 Project Structure

```
ConversationalBI/
├── semantic/
│   └── pbip_parser.py      # Parses Power BI TMDL files → LangChain Documents
├── vectorstore/
│   └── embedder.py         # ChromaDB embed + retrieval
├── agent/
│   └── rag_chain.py        # RAG pipeline: retrieve → generate → answer
├── ui/
│   └── app.py              # Streamlit chat UI with three modes
├── chroma_db/              # Pre-built vectorstore (demo mode)
├── ingest.py               # CLI to build vectorstore from TMDL files
└── requirements.txt
```

---

## 🧠 AI concepts learned building this

| Concept | What it is |
|---|---|
| LLM API | Send text to a cloud model, get intelligent response back |
| Embeddings | Convert text meaning into numbers for semantic search |
| Vector Store | Database optimised for similarity search by meaning |
| RAG | Inject your own data into the LLM prompt to prevent hallucination |
| Chunking | Split documents into focused pieces for precise retrieval |
| Prompt Engineering | Structuring instructions to get consistent, grounded LLM output |

---

## 👤 Author

**Avi** — Business Intelligence Engineer expanding into AI/ML  
[LinkedIn](www.linkedin.com/in/avinash-jaiswal-77b20514) · [GitHub](https://github.com/avivin11)

---

*Built as part of a personal AI learning journey — from Power BI engineer to AI-powered BI developer.*