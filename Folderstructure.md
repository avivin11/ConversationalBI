rag_bi/
├── requirements.txt          ← install this first
├── .env.example              ← copy → .env, add your key
├── .gitignore
├── test_groq.py              ← run this to verify Phase 0
├── ingest.py                 ← Phase 1 entry point
├── utils/config.py           ← central settings
├── semantic/
│   ├── semantic_model.md     ← edit this with YOUR model details
│   └── pbip_parser.py        ← auto-parses Power BI PBIP files
├── vectorstore/embedder.py   ← ChromaDB embed + retrieval
├── agent/
│   ├── llm.py                ← Groq/Gemini loader
│   └── rag_chain.py          ← full RAG + SQL pipeline
└── ui/app.py                 ← Streamlit chat interface