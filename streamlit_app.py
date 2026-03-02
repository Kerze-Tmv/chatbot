import streamlit as st
from huggingface_hub import InferenceClient

st.title("💬 Chatbot (Zephyr - Hugging Face)")

client = InferenceClient(
    model="HuggingFaceH4/zephyr-7b-beta",
    token=st.secrets["HF_TOKEN"],
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input user
if prompt := st.chat_input("What is up?"):

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Gabungkan jadi satu prompt
    prompt_text = ""
    for m in st.session_state.messages:
        prompt_text += f"{m['role']}: {m['content']}\n"

    response = client.text_generation(
        prompt_text,
        max_new_tokens=300,
        temperature=0.7,
    )

    reply = response

    with st.chat_message("assistant"):
        st.markdown(reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )
