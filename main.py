import os
from dotenv import dotenv_values
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="CircuitSage 🧠🤖",
    page_icon="🐱‍💻",
    layout="centered",
)
GROQ_API_KEY='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'

INITIAL_RESPONSE="En que puedo ayudarte hoy?"

CHAT_CONTEXT="Eres un asistente tecnico para computadoras y laptops, estaras preparado para realizar las preguntas necesarias para resolver cualquier duda del usuario sobre harware y software, cualquier otro tema fuera de lugar descartalo de inmedidato y hazelo saver al usuario"

INITIAL_MSG="Hola, soy CircuitSage, y estoy aqui para ayudarte en lo que necesites"
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
