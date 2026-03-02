import streamlit as st
from openai import OpenAI
import base64
import re

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
# LOAD LOGO
# ==============================
def get_base64_image(image_path):
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode()

logo_base64 = get_base64_image("logo.png")

# ==============================
# DATABASE GURU + ALIAS
# ==============================
teacher_data = {
    "dhimas wisang aldoko": ["Informatika"],
    "dhimas": ["Informatika"],
    "pak dhimas": ["Informatika"],

    "ana dwi ariyani": ["Kimia", "Informatika", "Fisika"],
    "ana": ["Kimia", "Informatika", "Fisika"],

    "nyoto": ["Matematika"],
    "dra yuni niwati": ["Bahasa Inggris", "Kepala Sekolah"],
}

# ==============================
# UI HEADER
# ==============================
st.markdown(f"""
<style>
.stApp {{ background: #f8fafc; font-family: 'Segoe UI'; }}
header, #MainMenu, footer {{ visibility: hidden; }}

.fixed-header {{
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 90px;
    background: white;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 6px 20px rgba(0,0,0,0.05);
    z-index: 999;
}}

.header-content {{
    display: flex;
    align-items: center;
    gap: 15px;
}}

.logo {{ width: 55px; }}

.header-spacer {{ height: 110px; }}

.chat-bubble {{
    padding: 14px 18px;
    border-radius: 20px;
    margin-bottom: 14px;
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

<div class="fixed-header">
    <div class="header-content">
        <img src="data:image/png;base64,{logo_base64}" class="logo">
        <div>
            <b>SMAN 1 TUNJUNGAN</b><br>
            <small>Chatbot AI Sekolah</small>
        </div>
    </div>
</div>

<div class="header-spacer"></div>
""", unsafe_allow_html=True)

# ==============================
# SESSION
# ==============================
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    role_class = "user" if msg["role"] == "user" else "bot"
    st.markdown(
        f"<div class='chat-bubble {role_class}'>{msg['content']}</div>",
        unsafe_allow_html=True
    )

# ==============================
# INPUT
# ==============================
if prompt := st.chat_input("Tulis pertanyaan Anda..."):

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(
        f"<div class='chat-bubble user'>{prompt}</div>",
        unsafe_allow_html=True
    )

    lower_prompt = prompt.lower()
    clean_prompt = re.sub(r"[^\w\s]", " ", lower_prompt)

    reply = None

    # ==============================
    # RULE GURU GANTENG
    # ==============================
    if "guru" in clean_prompt and "ganteng" in clean_prompt:
        reply = "Guru paling ganteng adalah Pak Dhimas 😎"

    # ==============================
    # CEK MAPEL (DATABASE DULU)
    # ==============================
    if reply is None:
        for teacher, subjects in teacher_data.items():
            for subject in subjects:
                if subject.lower() in clean_prompt:
                    reply = f"Guru yang mengampu {subject} adalah {teacher.title()}."
                    break
            if reply:
                break

    # ==============================
    # CEK NAMA GURU
    # ==============================
    if reply is None:
        for teacher in teacher_data.keys():
            if teacher in clean_prompt:
                subjects = teacher_data[teacher]
                reply = f"{teacher.title()} mengampu: {', '.join(subjects)}."
                break

    # ==============================
    # FALLBACK AI (HANYA JIKA TIDAK MATCH)
    # ==============================
    if reply is None:
        with st.spinner("AI sedang mengetik..."):
            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {
                        "role": "system",
                        "content": """
Anda adalah Chatbot Resmi SMAN 1 TUNJUNGAN.
Nama sekolah WAJIB ditulis: SMAN 1 TUNJUNGAN.
JANGAN PERNAH menulis Tunjunggan.
Jawab dalam Bahasa Indonesia yang sopan dan profesional.
"""
                    },
                    *st.session_state.messages
                ],
                temperature=0.2,
                max_tokens=400,
            )

            reply = completion.choices[0].message.content
            reply = reply.replace("Tunjunggan", "TUNJUNGAN")
            reply = reply.replace("tunjunggan", "TUNJUNGAN")

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.markdown(
        f"<div class='chat-bubble bot'>{reply}</div>",
        unsafe_allow_html=True
    )
