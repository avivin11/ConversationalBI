# 📊 Project Tracker — RAG Conversational BI Assistant
> Update this file at the end of every session. Paste it alongside MASTER_PROMPT.md at the start of every new chat.

---

## 🗂️ All Phases — Description Index

| # | Phase | Goal | Status |
|---|---|---|---|
| 0 | Environment setup | Python env, installs, API keys verified | Completed |
| 1 | PBIP extraction + ChromaDB ingestion | Parse semantic model → embed into vector store | 🟡 In Progress |
| 2 | NL-to-SQL agent + RAG chain | LLM answers questions using live data + semantic context | ⬜ Not started |
| 3 | Streamlit chatbot UI | Working chat interface with chart output | ⬜ Not started |
| 4 | Power BI embed + deploy | Chatbot inside .pbix + public Streamlit URL | ⬜ Not started |

---

## 📋 Phase Descriptions

### Phase 0 — Environment Setup
**Goal:** Get every tool installed and API keys verified before writing any project code.
**Why this phase exists:** AI projects fail most often at setup — version conflicts, missing packages, wrong import paths. Solving this once means clean sailing for every phase after.
**Deliverable:** Running `python -c "import langchain, chromadb, streamlit, groq; print('OK')"` prints OK with no errors. A test Groq API call returns a response.

---

### Phase 1 — PBIP Extraction + ChromaDB Ingestion
**Goal:** Convert Power BI semantic model metadata (tables, columns, DAX measures, relationships) into embedded documents stored in ChromaDB.
**Why this phase exists:** This is the "knowledge base" of the RAG system. Without it, the chatbot has no understanding of what Gross Margin means, which tables exist, or how the data model is structured. It would hallucinate definitions.
**Deliverable:** `python ingest.py` runs without error. ChromaDB is populated. A test retrieval query returns correct semantic model documents.
**AI concept learned:** What embeddings are, what chunking means, why semantic search beats keyword search, what a vector store does.

---

### Phase 2 — NL-to-SQL Agent + RAG Chain
**Goal:** Wire up the two-track pipeline — Track A (ChromaDB retrieval) + Track B (NL-to-SQL over live database) — into a single chain that produces grounded answers.
**Why this phase exists:** Retrieval alone gives context but no numbers. SQL alone gives numbers but no business meaning. Combined, they give accurate, explainable answers.
**Deliverable:** `answer("What was gross margin last month?", db_uri)` returns a correct answer citing the DAX definition and a real number from the database.
**AI concept learned:** What an LLM agent is, how prompt engineering works, what the full RAG loop looks like end-to-end.

---

### Phase 3 — Streamlit Chatbot UI
**Goal:** Wrap the RAG chain in a usable web interface with conversation history, example questions, and auto-rendered charts from SQL results.
**Why this phase exists:** The pipeline works in a script — but a script is not a product. Streamlit makes it accessible to non-technical stakeholders and portfolio-ready.
**Deliverable:** `streamlit run ui/app.py` opens a browser chat interface. Questions return answers with charts. Semantic context is visible in an expander.
**AI concept learned:** How to turn an AI script into a deployable product. The difference between a demo and a system.

---

### Phase 4 — Power BI Embed + Deploy
**Goal:** Deploy the Streamlit app to a free public URL (Streamlit Community Cloud) and embed it inside a Power BI report via the HTML Viewer visual.
**Why this phase exists:** This is what separates the project from a standalone Python script. A chatbot living inside Power BI is a genuinely novel BI pattern — exactly what employers and stakeholders want to see in 2025.
**Deliverable:** A `.pbix` file where one report page contains the live chatbot. A public URL that anyone can visit. A GitHub repo with a README.
**AI concept learned:** How AI products are shipped. The architecture pattern of embedding AI tools inside existing BI surfaces.

---

## ✅ Completed Phases

# Phase0 Completed
---

✅ Task 0.1 — Virtual environment created
✅ Task 0.2 — Dependencies installed
✅ Task 0.3 — .env file created with GROQ_API_KEY
✅ Task 0.4 — All imports verified
✅ Task 0.5 — Groq API call returns response
---

Phase 1 — COMPLETE ✅
✅ TMDL parser written and tested
✅ 20 documents extracted from retail semantic model
✅ Embedding model downloaded (all-MiniLM-L6-v2)
✅ ChromaDB vectorstore built (chroma_db/ folder created)
✅ Retrieval test passing

AI concepts learned:
- Embeddings: text → 384 numbers representing meaning
- Chunking: one document per measure = precise retrieval
- Vector store: similarity search by meaning, not keywords
- RAG foundation: knowledge base is now ready for Phase 2



---


---

Phase 2 — COMPLETE ✅

✅ get_semantic_context() — retrieves from ChromaDB
✅ load_llm() — loads Groq LLM
✅ generate_answer() — sends context + question to LLM  
✅ answer() — main entry point, returns dict with answer + context

AI concepts learned:
- Full RAG loop working end to end
- Returning dict from main function keeps UI clean
- LLM says "I don't know" when context is incomplete — correct behaviour
- Context quality determines answer quality
---

Phase 3 — COMPLETE ✅

✅ Block 1: page setup
✅ Block 2: session state initialised
✅ Block 3: chat history displayed on rerun
✅ Block 4: user input handled, RAG chain called, answer displayed

AI concepts learned:
- Streamlit reruns entire script on every interaction
- session_state persists data between reruns
- st.spinner wraps slow operations (LLM call)
- st.expander shows sources without cluttering the UI

## ⬜ Upcoming — Phase 4: Power BI Embed + Deploy
*(Detail will be filled in when Phase 3 is confirmed complete)*

**Entry requirement:** Streamlit app running locally without errors.

---

## 📋 Phase Completion Log

| Date | Phase | What was confirmed | Confirmed by |
|27-06-2206|Phase 0| installation of dependent library, groq key, python venv|Avi|
|28-06-2206|Phase 1| ingest.py, embedder.py and pbip_parser.py was created|Avi|
|1-07-2026|Phase 1| ragchain.py was developed which called load llm,pbip_parser and embedder.py|Avi|

---

## 🧠 Cumulative AI Learning Log

| Phase | Concept | One-line summary |
|---|---|---|
| 0 | LLM API | Send text over internet → get AI response back. No GPU needed. |
| 0 | API key | Auth token for LLM service. Treat like a password. |
| 0 | Virtual env | Isolated Python install per project. Prevents version conflicts. |

---

## 🔧 Known Issues / Blockers Log

| Date | Issue | Status | Resolution |
|---|---|---|---|
| — | — | — | — |

---

