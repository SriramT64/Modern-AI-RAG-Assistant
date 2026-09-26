import streamlit as st
import requests

st.set_page_config(
    page_title="Local RAG AI Assistant",
    page_icon="🤖"
)

st.title("🤖 Local RAG AI Assistant")
st.caption("Ask questions from your private knowledge base")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask a question...")

if question:

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    try:
        response = requests.post(
            "http://127.0.0.1:8000/ask",
            json={"question": question},
            timeout=120
        )

        response.raise_for_status()

        data = response.json()

        answer = data["answer"]
        sources = data.get("sources", [])

    except Exception as e:
        answer = f"API Error: {e}"
        sources = []

    with st.chat_message("assistant"):
        st.markdown(answer)

        if sources:
            with st.expander("📚 Retrieved Sources"):
                for i, source in enumerate(sources, 1):
                    st.markdown(f"**Source {i}**")
                    st.write(source)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })