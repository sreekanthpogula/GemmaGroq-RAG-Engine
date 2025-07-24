import os
from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Load environment variables
load_dotenv()

# Initialize GroqChat with the API key from environment variables
groq_api_key = os.getenv("GROQ_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

st.title("End To End Document Q&A RAG App With Gemma And Groq API")
st.write("This app uses LangChain, Groq API, and Gemma to answer questions based on the content of PDF documents.")
llm = ChatGroq(groq_api_key=groq_api_key, model_name="gemma-2-9b-it")

prompt= ChatPromptTemplate.from_messages(
    """Answer the question based on the context below. 
    If the question cannot be answered based on the context, say 'I don't know'.
    \n\nContext: {context}
    \n\nQuestion: {question}
    """
)

def vector_embedding(text: str) -> list[float]:
    embeddings = GoogleGenerativeAIEmbeddings()
    return embeddings.embed(text)
