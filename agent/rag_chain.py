import sys
import os
from dotenv import load_dotenv
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

from vectorstore.embedder import load_vectorstore, retrieve_context, format_context
from langchain_groq import ChatGroq

def get_semantic_context(question: str) ->str:
    """
    Retrieve and format the context for a given question.
    This is the R in RAG — Retrieval.
    """
    vectorstore=load_vectorstore()
    docs=retrieve_context(question,vectorstore)
    string_context=format_context(docs)
    return string_context

def load_llm() -> ChatGroq:
    """
    Load the Groq LLM with the API key and model from environment variables.
    This is the G in RAG — Generation.
    """
    api_key = os.getenv("GROQ_API_KEY")
    model=os.getenv("GROQ_MODEL")

    if not api_key:
        print("API key not found. Please set GROQ_API_KEY in your environment.")
        raise ValueError("GROQ_API_KEY not found in environment.")
    chat=ChatGroq(
        api_key=api_key,
        model=model,
        temperature=2.0

    )
    return chat

def generate_answer(question: str, context:str) ->str:
    """
    send the question and context to the llm and get the answer in plain string"""
    llm=load_llm()
    prompt=f"You are Business Intelligence Assitant.Answer the question based on the context below. If the answer is not in the context, say 'I don't know'.\n\nContext: {context}\n\nQuestion: {question}\n\nAnswer:"
    response=llm.invoke(prompt)
    return response.content


def answer(question: str) ->dict:
    """
    TThis function will be used outside to get the answer from LLM based on the question and context
    """
    context=get_semantic_context(question)
    output=generate_answer(question,context)

    return {"question":question,"context":context,"answer":output}

if __name__ == "__main__":
    question='what is Customer segments?'
    answer_dict=answer(question)
    print("\n----answer----\n")
    print(answer_dict["answer"])
    print("\n----context----\n")
    print(answer_dict["context"])