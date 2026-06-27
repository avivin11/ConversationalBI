# 📊 Project Tracker — RAG Conversational BI Assistant
> Update this file at the end of every session. Paste it alongside MASTER_PROMPT.md at the start of every new chat.

---

## 🗂️ All Phases — Description Index

| # | Phase | Goal | Status |
|---|---|---|---|
| 0 | Environment setup | Python env, installs, API keys verified | 🟡 In Progress |
| 1 | PBIP extraction + ChromaDB ingestion | Parse semantic model → embed into vector store | ⬜ Not started |
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

*(None yet — will be populated as phases are confirmed done)*

---

## 🟡 Current Phase — Phase 0: Environment Setup

### What we are doing
Setting up the Python environment, installing all dependencies, configuring API keys, and verifying every tool loads correctly before any project code is written.

### What has been completed so far

#### Project scaffold generated ✅
A full project folder structure was generated with all module files pre-built and annotated. This was done so implementation can begin immediately in each phase without wasting time on boilerplate.

**Files created:**
```
rag_bi/
├── requirements.txt          ← all pip installs pinned to stable versions
├── .env.example              ← safe API key template
├── .gitignore                ← excludes .env and chroma_db from git
├── ingest.py                 ← CLI to build vectorstore (run once per model update)
├── utils/config.py           ← central config — API keys, model names, paths
├── semantic/pbip_parser.py   ← PBIP model.bim parser → LangChain Documents
├── semantic/semantic_model.md← hand-written fallback knowledge base (starter)
├── vectorstore/embedder.py   ← ChromaDB embed + retrieval helpers
├── agent/llm.py              ← Groq / Gemini LLM loader (one-line swap)
├── agent/rag_chain.py        ← full RAG + SQL agent combined chain
└── ui/app.py                 ← Streamlit chat UI
```

**Why it was done this way:**
Each file has inline AI concept explanations as comments — this is intentional. The goal is not just to have working code but to understand every decision. Every file is functions-only (no classes), synchronous, and readable at a basic Python level.

**Inline learning built into the code:**
- `embedder.py` explains what embeddings are in plain English before the first function
- `rag_chain.py` explains Track A vs Track B and why both are needed
- `pbip_parser.py` explains what a PBIP file is and how to get one

---

### What still needs to be done to complete Phase 0

#### ⬜ Task 0.1 — Create virtual environment
```bash
# Run in your project folder (e.g. C:\Projects\rag_bi)
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac / Linux
```
**Confirm done:** Terminal prompt shows `(venv)` prefix.

#### ⬜ Task 0.2 — Install all dependencies
```bash
pip install -r requirements.txt
```
**Known watch-out:** This installs sentence-transformers which downloads the all-MiniLM-L6-v2 model (~80MB) on first use — not on install. So install will be fast; first `ingest.py` run will be slower.
**Confirm done:** No red error lines. Warnings about metadata are fine.

#### ⬜ Task 0.3 — Create .env file and add Groq API key
```bash
copy .env.example .env        # Windows
# cp .env.example .env        # Mac / Linux
```
Then open `.env` and paste your key:
- Groq free key: https://console.groq.com → API Keys → Create
- Gemini free key: https://aistudio.google.com → Get API Key

**Confirm done:** `.env` exists, `GROQ_API_KEY` is filled in.

#### ⬜ Task 0.4 — Verify all imports load
```bash
python -c "import langchain, chromadb, streamlit; from langchain_groq import ChatGroq; print('All imports OK')"
```
**Confirm done:** Prints `All imports OK`.

#### ⬜ Task 0.5 — Test Groq API call
```python
# Run this as a one-off script: python test_groq.py
from dotenv import load_dotenv
import os
load_dotenv()
from langchain_groq import ChatGroq

llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model="llama3-70b-8192")
response = llm.invoke("Say: Groq is working.")
print(response.content)
```
**Confirm done:** Prints a response from the LLM. No auth errors.

---

### AI concepts introduced this phase

| Concept | Plain English explanation |
|---|---|
| LLM API vs local model | Instead of running a model on your laptop (impossible — too slow), you send text to Groq's servers over the internet and get a response back. Same pattern as calling a SQL Server — you send a query, you get results. |
| API key | Your personal authentication token for the LLM service. Like a SQL Server connection string — it proves you're allowed to use it. Never commit it to git. |
| Virtual environment | An isolated Python installation for this project only — so its package versions don't conflict with other projects on your machine. Same concept as a separate SQL Server instance per environment. |

---

### Future dependency — what Phase 1 needs from Phase 0

Phase 1 cannot start until:
- [x] Scaffold files exist (done — generated in this session)
- [ ] `pip install -r requirements.txt` completes without error
- [ ] `.env` file exists with a valid `GROQ_API_KEY`
- [ ] All imports verified working
- [ ] Groq API test call returns a response

---

## ⬜ Upcoming — Phase 1: PBIP Extraction + ChromaDB Ingestion
*(Detail will be filled in when Phase 0 is confirmed complete)*

**Entry requirement:** Phase 0 all tasks checked off.
**First action in Phase 1:** Either (a) save your Power BI file as PBIP format and locate `model.bim`, or (b) edit `semantic/semantic_model.md` to describe your own data model. Then run `python ingest.py`.

---

## ⬜ Upcoming — Phase 2: NL-to-SQL Agent + RAG Chain
*(Detail will be filled in when Phase 1 is confirmed complete)*

**Entry requirement:** ChromaDB populated, test retrieval returning correct documents.

---

## ⬜ Upcoming — Phase 3: Streamlit Chatbot UI
*(Detail will be filled in when Phase 2 is confirmed complete)*

**Entry requirement:** `answer()` function returning correct answers in terminal.

---

## ⬜ Upcoming — Phase 4: Power BI Embed + Deploy
*(Detail will be filled in when Phase 3 is confirmed complete)*

**Entry requirement:** Streamlit app running locally without errors.

---

## 📋 Phase Completion Log

| Date | Phase | What was confirmed | Confirmed by |
|---|---|---|---|
| — | — | No phases completed yet | — |

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

*Last updated: Session 1*
*Current phase: Phase 0 — Environment setup*
*Next action: Run `pip install -r requirements.txt` and complete Tasks 0.1–0.5*
