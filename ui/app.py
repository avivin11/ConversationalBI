# ui/app.py

import sys
import os
from dotenv import load_dotenv
load_dotenv()
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

# Block 2 — initialise chat history
# Only runs on the very first load, not on every rerun
# "messages" will be a list of dicts: {"role": "user"/"assistant", "content": "..."}

if "messages" not in st.session_state:
    st.session_state.messages = []


# Block 3 — display chat history on every rerun
# st.chat_message("user") renders a user bubble
# st.chat_message("assistant") renders an assistant bubble

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # display the message content inside the bubble
        st.markdown(message["content"])

# Block 4 — handle new user input
# st.chat_input() shows the text box at the bottom of the page
# it returns the typed text when user hits Enter, otherwise None

if prompt := st.chat_input("Ask a question about your data..."):
    
    # Step 1 — add user message to history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Step 2 — call answer() and display the response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result=answer(prompt)
        st.markdown(result["answer"])
        with st.expander("Sources Used"):
           st.markdown(result["context"])
           

    st.session_state.messages.append({"role":"assistant","content":result["answer"]})
    # Step 3 — add assistant response to history
    # append {"role": "assistant", "content": result["answer"]} to messages