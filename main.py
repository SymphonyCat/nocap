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
# Initialize the chat history if present as Streamlit session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant",
         "content": INITIAL_RESPONSE
         },
    ]

client = Groq()

# Page title
st.title("Que tal")
st.caption("CircuitSage")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message("role", avatar=''):
        st.markdown(message["content"])

user_prompt = st.chat_input("Let's chat!")

def parse_groq_stream(stream):
    for chunk in stream:
        if chunk.choices:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

if user_prompt:
    with st.chat_message("user", avatar=""):
        st.markdown(user_prompt)
    st.session_state.chat_history.append(
        {"role": "user", "content": user_prompt})

    messages = [
        {"role": "system", "content": CHAT_CONTEXT
         },
        {"role": "assistant", "content": INITIAL_MSG},
        *st.session_state.chat_history
    ]

    stream = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        stream=True  # for streaming the message
    )
    response = st.write_stream(parse_groq_stream(stream))
    st.session_state.chat_history.append(
        {"role": "assistant", "content": response})
