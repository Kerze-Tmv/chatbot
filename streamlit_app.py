import streamlit as st
from openai import OpenAI
import json
import re
import base64

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
def get_base64_image(path):
    with open(path, "rb") as img:
        return base64.b64encode(img.read()).decode()

logo_base64 = get_base64_image("logo.png")

# ==============================
# LOAD DATA
# ==============================
try:
    with open("teachers.json", "r", encoding="utf-8") as f:
        teachers_data = json.load(f)
        teachers = teachers_data.get("guru", teachers_data)
except:
    teachers = []

try:
    with open("school_profile.json", "r", encoding="utf-8") as f:
        school_data = json.load(f)
except:
    school_data = {}

# ==============================
# STYLE
# ==============================
st.markdown(f"""
<style>
.chat-row {{
    display: flex;
    margin-bottom: 15px;
}}

.user {{
    justify-content: flex-end;
}}

.bot {{
    justify-content: flex-start;
}}

.bubble {{
    padding: 12px 16px;
    border-radius: 18px;
    max-width: 70%;
    font-size: 14px;
}}

.user-bubble {{
    background: #2563eb;
    color: white;
}}

.bot-bubble {{
    background: #f1f5f9;
    color: black;
}}

.logo {{
    width: 38px;
    height: 38px;
    margin-right: 10px;
}}

.header {{
    text-align: center;
    margin-bottom: 25px;
}}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='header'><h2>🎓 SMAN 1 TUNJUNGAN</h2><p style='color:gray;'>Chatbot AI Resmi Sekolah</p></div>", unsafe_allow_html=True)

# ==============================
# HELPER
# ==============================
def normalize(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    return text.strip()

def render_user(msg):
    st.markdown(f"""
    <div class="chat-row user">
        <div class="bubble user-bubble">{msg}</div>
    </div>
    """, unsafe_allow_html=True)

def render_bot(msg):
    st.markdown(f"""
    <div class="chat-row bot">
        <img src="data:image/png;base64,{logo_base64}" class="logo">
        <div class="bubble bot-bubble">{msg}</div>
    </div>
    """, unsafe_allow_html=True)

# ==============================
# SESSION
# ==============================
if "messages" not in st.session_state:
    st.session_state.messages = []

# render history
for m in st.session_state.messages:
    if m["role"] == "user":
        render_user(m["content"])
    else:
        render_bot(m["content"])

# ==============================
# INPUT
# ==============================
if prompt := st.chat_input("Tulis pertanyaan Anda..."):

    st.session_state.messages.append({"role": "user", "content": prompt})
    render_user(prompt)

    clean_prompt = normalize(prompt)
    reply = None
    osis = school_data.get("osis", {})

    # ==========================
    # LIST GURU
    # ==========================
    if any(k in clean_prompt for k in ["daftar guru", "list guru", "semua guru"]):
        guru_list = [
            f"{t.get('nama')} ({t.get('jabatan','')})"
            for t in teachers
        ]
        reply = "<b>Daftar Guru:</b><br>" + "<br>".join([f"• {g}" for g in guru_list])

    # ==========================
    # LIST WAKA
    # ==========================
    elif any(k in clean_prompt for k in ["waka", "wakil kepala"]):
        waka_list = [
            f"{t.get('jabatan')} - {t.get('nama')}"
            for t in teachers
            if "waka" in t.get("jabatan","").lower()
            or "wakil kepala" in t.get("jabatan","").lower()
        ]
        reply = "<b>Daftar Wakil Kepala Sekolah:</b><br>" + "<br>".join([f"• {w}" for w in waka_list])

    # ==========================
    # OSIS LENGKAP
    # ==========================
    elif "osis" in clean_prompt and osis:

        periode = osis.get("periode", "-")
        inti = osis.get("inti", {})
        seksi = osis.get("seksi", [])

        text = f"<b>Struktur OSIS Periode {periode}</b><br><br>"
        text += "<b>Pengurus Inti:</b><br>"

        for jab, data in inti.items():
            text += f"• {jab.replace('_',' ').title()}: {data['nama']} ({data['kelas']})<br>"

        text += "<br><b>Seksi Bidang:</b><br>"

        for s in seksi:
            text += f"<br><b>{s['nama_seksi']}</b><br>"
            text += f"• Ketua: {s['ketua']['nama']} ({s['ketua']['kelas']})<br>"
            for a in s.get("anggota", []):
                text += f"&nbsp;&nbsp;&nbsp;• {a['nama']} ({a['kelas']})<br>"

        reply = text

    # ==========================
    # STREAMING AI
    # ==========================
    if reply is None:

        full_reply = ""
        placeholder = st.empty()

        stream = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "Anda adalah Chatbot Resmi SMAN 1 TUNJUNGAN."},
                {"role": "user", "content": prompt}
            ],
            stream=True,
            temperature=0.2,
        )

        for chunk in stream:
            if chunk.choices[0].delta.content:
                full_reply += chunk.choices[0].delta.content
                placeholder.markdown(f"""
                <div class="chat-row bot">
                    <img src="data:image/png;base64,{logo_base64}" class="logo">
                    <div class="bubble bot-bubble">{full_reply}▌</div>
                </div>
                """, unsafe_allow_html=True)

        reply = full_reply
        placeholder.empty()

    render_bot(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
