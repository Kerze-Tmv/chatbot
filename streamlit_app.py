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
    # CEK INFORMATIKA KHUSUS (PASTI MATCH)
    # ==============================
    if reply is None and "informatika" in clean_prompt:
        reply = "Guru yang mengampu Informatika adalah Dhimas Wisang Aldoko."

    # ==============================
    # CEK NAMA DHIMAS
    # ==============================
    if reply is None and "dhimas" in clean_prompt:
        reply = "Dhimas Wisang Aldoko mengampu mata pelajaran Informatika."

    # ==============================
    # FALLBACK AI
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
Jawab dalam Bahasa Indonesia yang sopan.
"""
                    },
                    *st.session_state.messages
                ],
                temperature=0.2,
                max_tokens=400,
            )

            reply = completion.choices[0].message.content
            reply = reply.replace("Tunjunggan", "TUNJUNGAN")

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.markdown(
        f"<div class='chat-bubble bot'>{reply}</div>",
        unsafe_allow_html=True
    )
