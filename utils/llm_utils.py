import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv

# ✅ Securely Fetch API Key from Streamlit Secrets
load_dotenv()

# Configure your Google Generative AI API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

@st.cache_resource
def get_llm():
    """Creates and caches the Gemini 1.5 Pro language model."""
    return ChatGoogleGenerativeAI(model="gemini-1.5-pro")


def get_llm_chain():
    """Sets up the conversation chain with memory and prompt."""
    template = """You are a helpful data science tutor. You can explain data science concepts, give code examples, and answer questions.

    Previous conversation:
    {chat_history}

    New human question: {question}
    Response:"""
    prompt_template = PromptTemplate.from_template(template)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation = LLMChain(
        llm=get_llm(),
        prompt=prompt_template,
        verbose=True,
        memory=memory,
    )
    return conversation