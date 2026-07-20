# ui/app.py

import sys
import os

# fix import path — same pattern as rag_chain.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from agent.rag_chain import answer

# Configure the page
# title: "BI Assistant"
# page_icon: "📊"
# layout: "wide"
st.set_page_config(
    page_title= "BI Assistant",
    page_icon= "📊",
    layout= "wide"
)

if "mode" not in st.session_state:
    st.session_state.mode=None
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore=None
if "messages" not in st.session_state:
    st.session_state.messages=[]


# Back button — shows on every page except landing page
if st.session_state.mode is not None:
    if st.button("← Back to Home"):
        st.session_state.mode = None
        st.session_state.vectorstore = None
        st.session_state.messages = []
        st.rerun()

# Block 2 — initialise chat history
# Only runs on the very first load, not on every rerun
# "messages" will be a list of dicts: {"role": "user"/"assistant", "content": "..."}

if st.session_state.mode is None:
    st.title("📊 Conversational BI Assistant")
    st.markdown("Answer plain-English question about you powerbi data model")
    st.divider()

    st.subheader("How would you like to get started?")
    col1,col2,col3=st.columns(3)
    with col1:
        st.markdown("### Demo Mode")
        st.markdown("Try with our pre-loaded retail dashboard sample.")
        if st.button("Launch Demo"):
            st.session_state.mode="demo"
            st.rerun()

    with col2:
        st.markdown("### Local PBIP path")
        st.markdown("Point to your local PowerBI Project file definition/ folder.")
        if st.button("Use Local Path"):
            st.session_state.mode="local"
            st.rerun()

    with col3:
        st.markdown("### upload PBIP file")
        st.markdown("Upload PBIP definition folder")
        if st.button("Upload Files"):
            st.session_state.mode="upload"
            st.rerun()
    st.stop()

if st.session_state.vectorstore is None:
    
    
    #--Demo --Mode---------------------
    if st.session_state.mode=="demo":
        with st.spinner("loading data model..."):
            from vectorstore.embedder import load_vectorstore
            st.session_state.vectorstore=load_vectorstore()
        st.success("Data model loaded. Start asking questions about your report")
        st.rerun()

#__local mode_______________________
    elif st.session_state.mode=="local":
        st.title(" Local PBIP Path")
        path=st.text_input("paste the full path to your definition/ folder",
                           placeholder="C:/Projects/MyReport.SemanticModel/definition")
        if st.button("Load Data Model") and path:
            with st.spinner("Parsing TMDL files and building knowledge base.."):
                from Semantic.pbip_parser import parse_tmdl_to_documents
                from vectorstore.embedder import build_vectorstore
                docs=parse_tmdl_to_documents(path)
                st.session_state.vectorstore=build_vectorstore(docs)
            st.success(f"loaded {len(docs)} documents, start asking questions!")
            st.rerun()
        st.stop()

#__upload mode________________________
    elif st.session_state.mode=="upload":
        st.title("upload PBIP definition folder")
        st.markdown("upload all definition files from semantic model folder")

        uploaded_files=st.file_uploader(
            "Select your .tmdl files",
            type=["tmdl"],
            accept_multiple_files=True
            )
        if st.button("Build knowledge base") and uploaded_files:
            with st.spinner("parsing uploaded files and building knowledge base..."):
                import tempfile,os
                from Semantic.pbip_parser import parse_table_tmdl, parse_measures_as_individual_docs, parse_relationships
                from vectorstore.embedder import build_vectorstore

                docs=[]

                with tempfile.TemporaryDirectory() as tmpdir:
                    for uploaded_file in uploaded_files:
                        file_path=os.path.join(tmpdir,uploaded_file.name)
                        with open(file_path,"wb") as f:
                            f.write(uploaded_file.read())
                    
                    for fname in os.listdir(tmpdir) :
                        fpath=os.path.join(tmpdir,fname)
                        if fname == "relationships.tmdl":
                            docs.extend(parse_relationships(fpath))
                        elif fname.endswith(".tmdl"):
                            table_docs=parse_table_tmdl(fpath)
                            if table_docs:
                                docs.append(table_docs)
                            docs.extend(parse_measures_as_individual_docs(fpath))
                st.session_state.vectorstore=build_vectorstore(docs)
            st.success(f"loaded {len(docs)} documents, start asking questions!")
            st.rerun()
        st.stop()


#Block 3 — display chat history on every rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#block 4 handle new user input
if prompt:= st.chat_input("Ask a questio about your data"):
    st.session_state.messages.append({"role": "user","content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."): 
            result=answer(prompt,st.session_state.vectorstore)
        st.markdown(result["answer"])
        with st.expander("Sources Used"):
            st.markdown(result["context"])
    st.session_state.messages.append({"role":"assistant","content":result["answer"]})
