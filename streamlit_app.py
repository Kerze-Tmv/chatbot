import streamlit as st
from huggingface_hub import InferenceClient

st.title("💬 Chatbot (Hugging Face)")

st.write(
    "This chatbot uses a Hugging Face model via Inference API."
)

hf_token = st.text_input("Hugging Face API Key", type="password")

if not hf_token:
    st.info("Please add your Hugging Face API key to continue.", icon="🔑")
else:
    client = InferenceClient(
        model="Qwen/Qwen2.5-3B-Instruct",
        token=hf_token,
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):

        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        response = client.chat_completion(
            messages=st.session_state.messages,
            max_tokens=300,
        )

        reply = response.choices[0].message.content

        with st.chat_message("assistant"):
            st.markdown(reply)

        st.session_state.messages.append(
            {"role": "assistant", "content": reply}
        )
