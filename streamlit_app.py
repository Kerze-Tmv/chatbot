import streamlit as st
from openai import OpenAI

# ==============================
# CONFIG
# ==============================
st.set_page_config(
    page_title="SMAN 1 TUNJUNGAN - Chatbot AI",
    page_icon="🎓",
    layout="wide",
)

client = OpenAI(
    api_key=st.secrets["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)

MODEL_NAME = "llama-3.1-8b-instant"

# ==============================
# CSS MODERN RESPONSIVE
# ==============================
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #f8fafc, #e2e8f0);
    font-family: 'Segoe UI', sans-serif;
}

/* Center container */
.block-container {
    max-width: 900px;
    margin: auto;
    padding-top: 30px;
}

/* Header */
.main-title {
    text-align: center;
    font-size: 28px;
    font-weight: 800;
    color: #0f172a;
}

.sub-title {
    text-align: center;
    color: #64748b;
    margin-bottom: 25px;
}

/* Chat wrapper */
.chat-wrapper {
    margin-bottom: 100px;
}

/* Chat Bubble */
.chat-bubble {
    padding: 14px 18px;
    border-radius: 22px;
    margin-bottom: 14px;
    max-width: 75%;
    line-height: 1.6;
    font-size: 15px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.05);
    word-wrap: break-word;
}

/* User */
.user {
    background: linear-gradient(135deg, #2563eb, #1e40af);
    color: white;
    margin-left: auto;
    border-bottom-right-radius: 6px;
}

/* Bot */
.bot {
    background: white;
    color: #0f172a;
    margin-right: auto;
    border-bottom-left-radius: 6px;
    border: 1px solid #e2e8f0;
}

/* Input styling */
[data-testid="stChatInput"] {
    max-width: 800px;
    margin: auto;
}

/* ==============================
   MOBILE OPTIMIZATION
   ============================== */

@media screen and (max-width: 768px) {

    .block-container {
        padding-left: 10px;
        padding-right: 10px;
    }

    .chat-bubble {
        max-width: 92%;
        font-size: 14px;
        padding: 12px 16px;
    }

    .main-title {
        font-size: 22px;
    }

    .sub-title {
        font-size: 13px;
    }
}

</style>
""", unsafe_allow_html=True)

# ==============================
# HEADER
# ==============================
st.markdown("<div class='main-title'>🎓 SMAN 1 TUNJUNGAN</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Chatbot AI Berbasis Groq Llama 3.1</div>", unsafe_allow_html=True)

# ==============================
# SESSION STATE
# ==============================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ==============================
# DISPLAY CHAT
# ==============================
st.markdown("<div class='chat-wrapper'>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f"<div class='chat-bubble user'>{msg['content']}</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div class='chat-bubble bot'>{msg['content']}</div>",
            unsafe_allow_html=True
        )

st.markdown("</div>", unsafe_allow_html=True)

# ==============================
# INPUT
# ==============================
if prompt := st.chat_input("Tulis pertanyaan Anda..."):

    # tampil langsung supaya tidak delay
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(
        f"<div class='chat-bubble user'>{prompt}</div>",
        unsafe_allow_html=True
    )

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
            max_tokens=500,
        )

        reply = completion.choices[0].message.content

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

    st.markdown(
        f"<div class='chat-bubble bot'>{reply}</div>",
        unsafe_allow_html=True
    )
