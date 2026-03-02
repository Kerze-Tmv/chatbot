import streamlit as st
from openai import OpenAI
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
def get_base64_image(image_path):
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode()

logo_base64 = get_base64_image("logo.png")

# ==============================
# DATABASE GURU
# ==============================
teacher_data = {
    "dhimas wisang aldoko": ["Informatika"],
    "dra. yuni ni'wati": ["Bahasa Inggris", "Kepala Sekolah"],
    "dra. nurlaela atmaningtri": ["Ekonomi TL", "PKWU"],
    "ninik juliastuti": ["Kimia TL", "Kimia"],
    "lilik fitri kusumawati": ["Ekonomi"],
    "titik nurhayati": ["Biologi TL"],
    "sumartini": ["Seni Budaya"],
    "dra. retno umi haryati": ["Biologi TL"],
    "drs. masngud": ["Pendidikan Agama Islam"],
    "dra. theresia mulyorini": ["Bahasa Inggris", "B. Inggris TL"],
    "yarto": ["Fisika TL", "Fisika"],
    "watiningsih": ["Matematika TL"],
    "suhartini": ["Bahasa Indonesia"],
    "dra. sri astutik": ["Bahasa Indonesia"],
    "hari setyawati": ["Ekonomi", "PKWU"],
    "sunarni": ["Matematika", "Matematika TL"],
    "muhammad ainur rofiq": ["Sejarah Indonesia", "Sejarah TL"],
    "anik aprilyani": ["Geografi", "Waka Kurikulum"],
    "donna heri satyani": ["Geografi", "Geografi TL"],
    "sulastriyani": ["Sejarah Indonesia", "Sejarah TL"],
    "firman fridayanto": ["Bahasa Inggris"],
    "ikwan insanjaya": ["Seni Budaya"],
    "kari rahayu": ["Biologi"],
    "zainal arifin": ["Pendidikan Agama Islam"],
    "novita ariana": ["BK"],
    "rahayu indrayati": ["PJOK"],
    "sriyani": ["Sosiologi", "Sosiologi TL"],
    "endang setyowati": ["BK"],
    "galuh sekar wijayanti": ["BK"],
    "ayudhia sari rahmadani": ["Bahasa Indonesia"],
    "syarifuddin ahmad": ["Bahasa Indonesia", "Waka Humas"],
    "irma pramestiningrum": ["Fisika TL", "Fisika"],
    "neneng oktora budiasri": ["Matematika"],
    "dwi nur setiyawati": ["BK"],
    "wahidatun nurul hidayah": ["BK"],
    "santi aprilia riyanti": ["Kimia", "PKWU"],
    "jatmiko": ["Bahasa Indonesia", "Waka Sarpras"],
    "nihza al lutfi": ["Sejarah Indonesia", "Geografi", "Waka Kesiswaan"],
    "udin hendri santoso": ["Geografi", "PKWU"],
    "haniffuddin": ["Sosiologi", "Sosiologi TL"],
    "sam getta gumilar": ["PJOK"],
    "anik setyarini": ["Pendidikan Pancasila"],
    "alifa nurul tafricha": ["Pendidikan Pancasila"],
    "nurlaili miftakhuzzilvana": ["Bahasa Jawa"],
    "moh. cholilur rohman": ["Matematika", "Matematika TL"],
    "basar siswantoro": ["PJOK"],
    "lailly oktavianingrum": ["Kimia TL"],
    "sri purwati": ["Matematika"],
    "dhony wijaya": ["Matematika Wajib"],
    "siti listyowati": ["Fisika", "Fisika TL"],
    "satria yoga tama": ["Bahasa Jawa"],
    "manggar shintia wibawanti": ["Matematika"],
    "joko priyanto": ["PKWU", "Sejarah"],
    "ahmad ni'am": ["Pendidikan Agama Islam"],
    "wiwit suryaningsih": ["Biologi TL", "Fisika", "Biologi"],
    "nyoto": ["Matematika"],
    "lilik kurniawan": ["PKWU", "Sejarah"],
    "dwi setyowati": ["Basa Jawa"],
    "ana dwi ariyani": ["Kimia", "Informatika", "Fisika"],
    "wheny wulandari": ["Bahasa Inggris"],
    "sr. veronika sedo bura": ["Agama Katolik"],
    "sri rusmini": ["Agama Kristen"],
    "sukemi": ["Pendidikan Agama Islam"],
    "eko budi lestari": ["Agama Budha"],
}

# ==============================
# CSS UI
# ==============================
st.markdown(f"""
<style>
.stApp {{
    background: linear-gradient(135deg, #f8fafc, #e2e8f0);
    font-family: 'Segoe UI', sans-serif;
}}

header {{visibility: hidden;}}
#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}

.fixed-header {{
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
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

.logo {{
    width: 55px;
    height: 55px;
    border-radius: 12px;
}}

.header-text h1 {{
    font-size: 20px;
    margin: 0;
    font-weight: 800;
}}

.header-text p {{
    font-size: 13px;
    margin: 0;
    color: #64748b;
}}

.header-spacer {{
    height: 110px;
}}

.chat-bubble {{
    padding: 14px 18px;
    border-radius: 22px;
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
        <div class="header-text">
            <h1>SMAN 1 TUNJUNGAN</h1>
            <p>Chatbot AI Sekolah</p>
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
    st.markdown(f"<div class='chat-bubble user'>{prompt}</div>", unsafe_allow_html=True)

    lower_prompt = prompt.lower()
    reply = None

    # RULE GURU GANTENG
    if "guru" in lower_prompt and "ganteng" in lower_prompt:
        reply = "Guru paling ganteng adalah Pak Dhimas 😎"

    # CEK NAMA GURU
    if reply is None:
        for teacher, subjects in teacher_data.items():
            if teacher in lower_prompt:
                reply = f"{teacher.title()} mengampu: {', '.join(subjects)}."
                break

    # CEK MAPEL
    if reply is None:
        for teacher, subjects in teacher_data.items():
            for subject in subjects:
                if subject.lower() in lower_prompt:
                    reply = f"Guru yang mengampu {subject} adalah {teacher.title()}."
                    break
            if reply:
                break

    # FALLBACK AI
    if reply is None:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "system", "content": "Jawab dalam Bahasa Indonesia dengan sopan."},
                      *st.session_state.messages],
            temperature=0.3,
            max_tokens=400,
        )
        reply = completion.choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.markdown(f"<div class='chat-bubble bot'>{reply}</div>", unsafe_allow_html=True)
