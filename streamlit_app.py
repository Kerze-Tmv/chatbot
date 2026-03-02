import base64
import streamlit as st
from google import genai

# ==============================
# CONFIG
# ==============================
st.set_page_config(
    page_title="SMAN 1 TUNJUNGAN - Chatbot AI",
    page_icon="🎓",
    layout="wide"
)

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

model_name = "gemini-2.0-flash"

# ==============================
# LOAD LOGO
# ==============================
def get_base64_image(image_path):
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode()

logo_base64 = get_base64_image("logo.png")

# ==============================
# UI HEADER
# ==============================
st.markdown(f"""
<style>
.stApp {{
    background: #f1f5f9;
    font-family: 'Segoe UI', sans-serif;
}}
.chat-bubble {{
    padding: 14px 18px;
    border-radius: 18px;
    margin-bottom: 12px;
    max-width: 75%;
}}
.user {{
    background: #2563eb;
    color: white;
    margin-left: auto;
}}
.bot {{
    background: white;
    border: 1px solid #e2e8f0;
    margin-right: auto;
}}
</style>
""", unsafe_allow_html=True)

st.title("🎓 SMAN 1 TUNJUNGAN - Chatbot AI")

# ==============================
# SESSION
# ==============================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ==============================
# DISPLAY CHAT
# ==============================
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='chat-bubble user'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble bot'>{msg['content']}</div>", unsafe_allow_html=True)

# ==============================
# INPUT
# ==============================
if prompt := st.chat_input("Tulis pertanyaan Anda..."):

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f"<div class='chat-bubble user'>{prompt}</div>", unsafe_allow_html=True)

    with st.spinner("Chatbot sedang mengetik..."):

        chat_history = ""
        for m in st.session_state.messages:
            chat_history += f"{m['role']}: {m['content']}\n"

        full_prompt = (
            "Kamu adalah Chatbot AI resmi SMAN 1 TUNJUNGAN. "
            "Jawab dalam Bahasa Indonesia yang jelas dan profesional.\n\n"
            + chat_history
        )

        response = client.models.generate_content(
            model=model_name,
            contents=full_prompt,
        )

        reply = response.text

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.markdown(f"<div class='chat-bubble bot'>{reply}</div>", unsafe_allow_html=True)
