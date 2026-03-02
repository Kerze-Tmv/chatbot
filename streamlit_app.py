import base64
import streamlit as st
from openai import OpenAI

# ==============================
# CONFIG
# ==============================
st.set_page_config(
    page_title="SMAN 1 TUNJUNGAN - Chatbot AI",
    page_icon="🎓",
    layout="wide"
)

client = OpenAI(
    api_key=st.secrets["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)

# ==============================
# MODEL (RECOMMENDED)
# ==============================
MODEL_NAME = "llama3-8b-8192"

# ==============================
# SESSION STATE
# ==============================
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🎓 SMAN 1 TUNJUNGAN - Chatbot AI (Groq)")

# ==============================
# DISPLAY CHAT
# ==============================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==============================
# INPUT
# ==============================
if prompt := st.chat_input("Tulis pertanyaan Anda..."):

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("AI sedang mengetik..."):

        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "Kamu adalah Chatbot AI resmi SMAN 1 TUNJUNGAN. Jawab dalam Bahasa Indonesia yang jelas dan profesional."
                },
                *st.session_state.messages
            ],
            temperature=0.3,
            max_tokens=300
        )

        reply = completion.choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": reply})

    with st.chat_message("assistant"):
        st.markdown(reply)
