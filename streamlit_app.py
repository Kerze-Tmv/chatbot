import streamlit as st
from openai import OpenAI
import json
import re
from datetime import datetime

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
# LOAD DATA (AMAN)
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
# HELPER FUNCTIONS
# ==============================
def normalize(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    return text.strip()

def find_teacher_by_name(prompt):
    for teacher in teachers:
        if normalize(teacher.get("nama", "")) in prompt:
            return teacher
        for alias in teacher.get("alias", []):
            if alias.lower() in prompt:
                return teacher
    return None

def find_by_jabatan(prompt):
    for teacher in teachers:
        jabatan = teacher.get("jabatan", "")
        if jabatan and jabatan.lower() in prompt:
            return teacher
    return None

def find_all_waka():
    waka_list = []
    for teacher in teachers:
        jabatan = teacher.get("jabatan", "")
        if jabatan and "waka" in jabatan.lower():
            waka_list.append(f"{jabatan} - {teacher.get('nama','')}")
    return waka_list

def find_teacher_by_subject(prompt):
    matches = []
    for teacher in teachers:
        for subject in teacher.get("mapel", []):
            pattern = r"\b" + re.escape(subject.lower()) + r"\b"
            if re.search(pattern, prompt):
                matches.append(teacher)
                break
    return matches

# ==============================
# HEADER
# ==============================
st.title("🎓 SMAN 1 TUNJUNGAN")
st.caption("Chatbot AI Resmi Sekolah")

# ==============================
# SESSION
# ==============================
if "messages" not in st.session_state:
    st.session_state.messages = []

# tampilkan riwayat chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg["role"] == "assistant":
            st.code(msg["content"], language="text")

# ==============================
# INPUT
# ==============================
if prompt := st.chat_input("Tulis pertanyaan Anda..."):

    # tampilkan pesan user langsung
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    clean_prompt = normalize(prompt)
    reply = None

    with st.spinner("Sedang memproses..."):

        # ==========================
        # FUN
        # ==========================
        if "guru" in clean_prompt and "ganteng" in clean_prompt:
            reply = "Guru paling ganteng adalah Pak Dhimas 😎"

        # ==========================
        # DATA SEKOLAH
        # ==========================
        if reply is None:
            identitas = school_data.get("identitas", {})
            alamat = school_data.get("alamat", {})
            statistik = school_data.get("statistik", {})
            legalitas = school_data.get("legalitas", {})

            if "alamat" in clean_prompt:
                reply = (
                    f"Alamat {identitas.get('nama_sekolah','SMAN 1 TUNJUNGAN')} adalah "
                    f"{alamat.get('jalan','-')}, Kec. {alamat.get('kecamatan','-')}, "
                    f"Kab. {alamat.get('kabupaten','-')}, Prov. {alamat.get('provinsi','-')}."
                )

            elif "npsn" in clean_prompt:
                reply = f"NPSN adalah {identitas.get('npsn','Tidak tersedia')}."

            elif "jumlah siswa" in clean_prompt:
                reply = f"Jumlah total siswa adalah {statistik.get('jumlah_siswa_total','-')} siswa."

            elif "kelas 10" in clean_prompt:
                reply = f"Jumlah siswa kelas 10 adalah {statistik.get('per_tingkat',{}).get('kelas_10','-')} siswa."

            elif "kelas 11" in clean_prompt:
                reply = f"Jumlah siswa kelas 11 adalah {statistik.get('per_tingkat',{}).get('kelas_11','-')} siswa."

            elif "kelas 12" in clean_prompt:
                reply = f"Jumlah siswa kelas 12 adalah {statistik.get('per_tingkat',{}).get('kelas_12','-')} siswa."

            elif "umur" in clean_prompt or "berdiri" in clean_prompt:
                tanggal_str = legalitas.get("sk_pendirian", {}).get("tanggal")
                if tanggal_str:
                    tahun_berdiri = datetime.strptime(tanggal_str, "%Y-%m-%d").year
                    tahun_sekarang = datetime.now().year
                    umur = tahun_sekarang - tahun_berdiri
                    reply = f"Sekolah berdiri sejak {tahun_berdiri} dan berusia {umur} tahun."
                else:
                    reply = "Data tahun berdiri tidak tersedia."

        # ==========================
        # WAKA
        # ==========================
        if reply is None and "waka" in clean_prompt:
            waka_list = find_all_waka()
            if waka_list:
                reply = "Daftar Wakil Kepala Sekolah:\n" + "\n".join(waka_list)

        # ==========================
        # JABATAN
        # ==========================
        if reply is None:
            jabatan_match = find_by_jabatan(clean_prompt)
            if jabatan_match:
                reply = f"{jabatan_match.get('jabatan')} adalah {jabatan_match.get('nama')}."

        # ==========================
        # NAMA GURU
        # ==========================
        if reply is None:
            teacher_match = find_teacher_by_name(clean_prompt)
            if teacher_match:
                jabatan = teacher_match.get("jabatan")
                jabatan_text = f" ({jabatan})" if jabatan else ""
                mapel = ", ".join(teacher_match.get("mapel", []))
                reply = f"{teacher_match.get('nama')}{jabatan_text} mengampu: {mapel}."

        # ==========================
        # MAPEL
        # ==========================
        if reply is None:
            subject_matches = find_teacher_by_subject(clean_prompt)
            if subject_matches:
                names = [t.get("nama") for t in subject_matches]
                reply = f"Guru yang mengampu mata pelajaran tersebut adalah: {', '.join(names)}."

        # ==========================
        # FALLBACK AI
        # ==========================
        if reply is None:
            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {
                        "role": "system",
                        "content": "Anda adalah Chatbot Resmi SMAN 1 TUNJUNGAN. Jawab sopan dan profesional."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=400,
            )
            reply = completion.choices[0].message.content

    # tampilkan jawaban
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)
        st.code(reply, language="text")
