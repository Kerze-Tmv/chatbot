import streamlit as st
from openai import OpenAI
import json, re, base64
from datetime import datetime

# ==============================
# CONFIG
# ==============================
st.set_page_config(
    page_title="SMAN 1 TUNJUNGAN - Chatbot AI",
    page_icon="🎓",
    layout="wide"
)

# SAFE API KEY
api_key = st.secrets.get("GROQ_API_KEY")
if not api_key:
    st.error("API Key tidak ditemukan.")
    st.stop()

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

MODEL_NAME = "llama-3.1-8b-instant"

# ==============================
# UTIL
# ==============================
def normalize(text):
    return re.sub(r"[^\w\s]", " ", text.lower()).strip()

def load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("guru", data.get("osis", data))
    except:
        return default

def get_base64_image(path):
    try:
        with open(path, "rb") as img:
            return base64.b64encode(img.read()).decode()
    except:
        return ""

# ==============================
# LOAD DATA
# ==============================
teachers = load_json("teachers.json", [])
osis = load_json("osis.json", {})
school_data = load_json("school_profile.json", {})

logo_base64 = get_base64_image("logo.png")

# ==============================
# RESPONSE ENGINE
# ==============================
def handle_school_profile(prompt):
    p = normalize(prompt)
    identitas = school_data.get("identitas", {})
    alamat = school_data.get("alamat", {})
    statistik = school_data.get("statistik", {})
    legalitas = school_data.get("legalitas", {})

    if "alamat" in p:
        return f"Alamat {identitas.get('nama_sekolah')} adalah {alamat.get('jalan')}, Kec. {alamat.get('kecamatan')}, Kab. {alamat.get('kabupaten')}, Prov. {alamat.get('provinsi')}."
    if "npsn" in p:
        return f"NPSN {identitas.get('nama_sekolah')} adalah {identitas.get('npsn')}."
    if "jumlah siswa" in p:
        return f"Jumlah total siswa adalah {statistik.get('jumlah_siswa_total')} siswa."
    if "berdiri" in p:
        tanggal = legalitas.get("sk_pendirian", {}).get("tanggal")
        if tanggal:
            tahun = datetime.strptime(tanggal, "%Y-%m-%d").year
            umur = datetime.now().year - tahun
            return f"{identitas.get('nama_sekolah')} berdiri sejak {tahun} dan saat ini berusia {umur} tahun."
    return None


def find_teacher(prompt):
    p = normalize(prompt)
    results = []

    for t in teachers:
        nama = normalize(t.get("nama",""))
        jabatan = normalize(t.get("jabatan",""))
        mapel = [normalize(m) for m in t.get("mapel",[])]
        alias = [normalize(a) for a in t.get("alias",[])]

        if nama in p or any(a in p for a in alias):
            return format_teacher(t)

        if jabatan and jabatan in p:
            return f"{t.get('jabatan')} adalah {t.get('nama')}."

        if any(m.replace(" tl","") in p for m in mapel):
            results.append(t)

    if results:
        return "<b>Guru Pengampu:</b><br><br>" + "<br>".join(
            f"• {t.get('nama')}" for t in results
        )

    return None


def format_teacher(t):
    text = f"<b>{t.get('nama')}</b><br><br>"
    if t.get("jabatan"):
        text += f"Jabatan: {t.get('jabatan')}<br>"
    if t.get("mapel"):
        text += f"Mengampu: {', '.join(t.get('mapel'))}"
    return text


def find_waka(prompt):
    p = normalize(prompt)
    waka = [t for t in teachers if "waka" in normalize(t.get("jabatan",""))]

    if p.strip() == "waka":
        return "<b>Daftar Wakil Kepala Sekolah:</b><br><br>" + "<br>".join(
            f"• {t.get('jabatan')} - {t.get('nama')}" for t in waka
        )

    for t in waka:
        if normalize(t.get("jabatan")) in p:
            return f"{t.get('jabatan')} adalah {t.get('nama')}."
    return None


def find_osis(prompt):
    p = normalize(prompt)
    inti = osis.get("inti", {})

    matches = []
    for jab, data in inti.items():
        jab_text = jab.replace("_", " ")
        if any(w in p for w in jab_text.split()):
            matches.append(f"• {jab_text.title()}: {data.get('nama')} ({data.get('kelas')})")

    if matches:
        return "<b>Pengurus OSIS:</b><br><br>" + "<br>".join(matches)
    return None


def ai_fallback(prompt):
    try:
        with st.spinner("AI sedang mengetik..."):
            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "Anda adalah Chatbot Resmi SMAN 1 TUNJUNGAN."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
            )
            return completion.choices[0].message.content
    except:
        return "Maaf, AI sedang tidak tersedia."


# ==============================
# CHAT
# ==============================
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"], unsafe_allow_html=True)

if prompt := st.chat_input("Tulis pertanyaan Anda..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    reply = (
        handle_school_profile(prompt)
        or find_teacher(prompt)
        or find_waka(prompt)
        or find_osis(prompt)
        or ai_fallback(prompt)
    )

    with st.chat_message("assistant"):
        st.markdown(reply, unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": reply})
