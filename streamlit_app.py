import streamlit as st
from huggingface_hub import InferenceClient

st.title("💬 Chatbot (Phi-3 Mini)")

client = InferenceClient(
    model="microsoft/Phi-3-mini-4k-instruct",
    token=st.secrets["HF_TOKEN"],
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Say something..."):

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    prompt_text = ""

    for m in st.session_state.messages:
        if m["role"] == "user":
            prompt_text += f"<|user|>\n{m['content']}\n"
        else:
            prompt_text += f"<|assistant|>\n{m['content']}\n"

    prompt_text += "<|assistant|>\n"

    response = client.text_generation(
        prompt_text,
        max_new_tokens=300,
        temperature=0.7,
    )

    reply = response.strip()

    with st.chat_message("assistant"):
        st.markdown(reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )
