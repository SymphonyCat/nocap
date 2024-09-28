import os
from dotenv import dotenv_values
import streamlit as st
from groq import Groq

def parse_groq_stream(stream):
    for chunk in stream:
        if chunk.choices:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

# Aplicar CSS personalizado
def local_css():
    st.markdown(
        """
        <style>
        /* Cambiar el fondo de la página */
        .reportview-container {
            background-color: #000000;
        }
        /* Cambiar el color del texto */
        .main .block-container, .main .block-container p, .main .block-container h1, .main .block-container h2, .main .block-container h3 {
            color: #FFFFFF;
        }
        /* Cambiar el color de los botones */
        .css-1emrehy.edgvbvh3 {
            background-color: #00FF00;
            color: #000000;
        }
        /* Cambiar el color de los inputs */
        .css-1v0mbdj.edgvbvh3 {
            background-color: #1A1A1A;
            color: #FFFFFF;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

local_css()

# streamlit page configuration
st.set_page_config(
    page_title="CircuitSage",
    page_icon="🐱‍💻",
    layout="centered",
)

try:
    secrets = dotenv_values(".env")  # para entorno de desarrollo
    GROQ_API_KEY = secrets["GROQ_API_KEY"]
except:
    secrets = st.secrets  # para despliegue en Streamlit
    GROQ_API_KEY = secrets["GROQ_API_KEY"]

# guardar la api_key en la variable de entorno
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

INITIAL_RESPONSE = secrets["INITIAL_RESPONSE"]
INITIAL_MSG = secrets["INITIAL_MSG"]
CHAT_CONTEXT = secrets["CHAT_CONTEXT"]

client = Groq()

# inicializar el historial de chat si no está presente en la sesión de Streamlit
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant",
         "content": INITIAL_RESPONSE
         },
    ]

# título de la página
st.title("CircuitSage 🧠🤖")
st.caption("Al terminar de usar el chat favor de realizar la siguiente encuesta")
st.write("https://forms.gle/9Pq2kRkGftHZE8ew6")

# mostrar historial de chat
for message in st.session_state.chat_history:
    with st.chat_message(message["role"], avatar='🤖' if message["role"] == "assistant" else '🗨️'):
        st.markdown(message["content"])

# campo de entrada del usuario
user_prompt = st.chat_input("Pregúntame")

if user_prompt:
    with st.chat_message("user", avatar="🗨️"):
        st.markdown(user_prompt)
    st.session_state.chat_history.append(
        {"role": "user", "content": user_prompt})

    # obtener una respuesta del LLM
    messages = [
        {"role": "system", "content": CHAT_CONTEXT
         },
        {"role": "assistant", "content": INITIAL_MSG},
        *st.session_state.chat_history
    ]

    # Mostrar la respuesta del asistente en el contenedor de mensajes del chat
    with st.chat_message("assistant", avatar='🤖'):
        stream = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            stream=True  # para transmitir el mensaje
        )
        response = ''.join(parse_groq_stream(stream))
        st.markdown(response)
    st.session_state.chat_history.append(
        {"role": "assistant", "content": response})
