import base64
import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="SMAN 1 TUNJUNGAN - Chatbot AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================
# LOAD SECRET TOKEN
# ==============================
HF_TOKEN = st.secrets["HF_TOKEN"]

# ==============================
# LOAD LOGO
# ==============================
def get_base64_image(image_path):
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode()

logo_base64 = get_base64_image("logo.png")

# ==============================
# RESPONSIVE UI STYLE
# ==============================
st.markdown(f"""
<style>

.stApp {{
    background: #f1f5f9;
    font-family: 'Segoe UI', sans-serif;
}}

.block-container {{
    max-width: 1000px;
    margin: auto;
}}

.fixed-header {{
    position: fixed;
    top: 55px;
    left: 0;
    right: 0;
    height: 120px;
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
    gap: 20px;
}}

.school-logo {{
    width: 75px;
    height: 75px;
}}

.header-text h1 {{
    font-size: 30px;
    font-weight: 800;
    margin: 0;
    color: #1e293b;
}}

.header-text p {{
    font-size: 14px;
    margin: 4px 0 0 0;
    color: #64748b;
}}

.header-spacer {{
    height: 190px;
}}

.chat-bubble {{
    padding: 14px 18px;
    border-radius: 18px;
    margin-bottom: 12px;
    font-size: 15px;
    max-width: 70%;
    line-height: 1.6;
}}

.user {{
    background: #2563eb;
    color: white;
    margin-left: auto;
}}

.bot {{
    background: white;
    border: 1px solid #e2e8f0;
    color: #1e293b;
    margin-right: auto;
}}

[data-testid="stChatInput"] {{
    max-width: 800px;
    margin: auto;
}}

@media screen and (max-width: 768px) {{

    .fixed-header {{
        height: 85px;
        top: 50px;
    }}

    .school-logo {{
        width: 50px;
        height: 50px;
    }}

    .header-text h1 {{
        font-size: 20px;
    }}

    .header-text p {{
        font-size: 12px;
    }}

    .header-spacer {{
        height: 140px;
    }}

    .chat-bubble {{
        max-width: 92%;
    }}

    [data-testid="stChatInput"] {{
        max-width: 100%;
    }}

}}

</style>

<div class="fixed-header">
    <div class="header-content">
        <img src="data:image/png;base64,{logo_base64}" class="school-logo">
        <div class="header-text">
            <h1>SMAN 1 TUNJUNGAN</h1>
            <p>Chatbot AI Berbasis Artificial Intelligence</p>
        </div>
    </div>
</div>

<div class="header-spacer"></div>
""", unsafe_allow_html=True)

# ==============================
# MODEL
# ==============================
model_id = "Qwen/Qwen2.5-0.5B-Instruct"

@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained(
        model_id,
        token=HF_TOKEN
    )
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        token=HF_TOKEN,
        torch_dtype=torch.float32,
        device_map="auto",
        low_cpu_mem_usage=True
    )
    return tokenizer, model

tokenizer, model = load_model()

# ==============================
# SESSION STATE
# ==============================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "system_added" not in st.session_state:
    st.session_state.messages.append({
        "role": "system",
        "content": (
            "Kamu adalah Chatbot AI resmi SMAN 1 TUNJUNGAN. "
            "Jawab dalam Bahasa Indonesia yang jelas dan profesional. "
            "Jika tidak yakin, katakan dengan jujur."
        )
    })
    st.session_state.system_added = True

# ==============================
# CHAT DISPLAY
# ==============================
chat_area = st.container()

with chat_area:
    for msg in st.session_state.messages:
        if msg["role"] == "system":
            continue

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

# ==============================
# INPUT FLOW
# ==============================
if prompt := st.chat_input("Tulis pertanyaan Anda..."):

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with chat_area:
        st.markdown(
            f"<div class='chat-bubble user'>{prompt}</div>",
            unsafe_allow_html=True
        )

    with st.spinner("Chatbot sedang mengetik..."):

        text = tokenizer.apply_chat_template(
            st.session_state.messages,
            tokenize=False,
            add_generation_prompt=True
        )

        inputs = tokenizer(text, return_tensors="pt").to(model.device)

        outputs = model.generate(
            **inputs,
            max_new_tokens=150,
            temperature=0.35,
            top_p=0.9,
            repetition_penalty=1.25,
            do_sample=True
        )

        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        reply = response.split("assistant")[-1].strip()

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

    with chat_area:
        st.markdown(
            f"<div class='chat-bubble bot'>{reply}</div>",
            unsafe_allow_html=True
        )
