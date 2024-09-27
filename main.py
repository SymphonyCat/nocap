import os
from dotenv import dotenv_values
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="The Tech Buddy ",
    page_icon="",
    layout="centered",
)
GROQ_API_KEY='YOUR_GROQ_API_KEY'

INITIAL_RESPONSE="Enter what you want to show as the first response of your bot, example: Hello! my friend I am a painter from 70's. Whatsup?"

CHAT_CONTEXT="Enter how do you want to personalize your chatbot, example: You are a painter from the 70's and you are respond sentences with painting references.(This is for the system)"

INITIAL_MSG="Enter the first message from the assistant to initiate the chat history, example: Hey there! I know everything about painting, ask me anything.(This is for the assistant)"
try:
    secrets = dotenv_values(".env")  # for dev env
    GROQ_API_KEY = secrets["GROQ_API_KEY"]
except:
    secrets = st.secrets  # for streamlit deployment
    GROQ_API_KEY = secrets["GROQ_API_KEY"]

# Save the API key to environment variable
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

INITIAL_RESPONSE = secrets["INITIAL_RESPONSE"]
INITIAL_MSG = secrets["INITIAL_MSG"]
CHAT_CONTEXT = secrets["CHAT_CONTEXT"]
