st.title("🏢 Zyro Dynamics HR Help Desk v2")

import streamlit as st

# 👉 PASTE YOUR ask_bot FUNCTION HERE
# (copy from your notebook exactly)

# Example placeholder:
def ask_bot(question):
    return {"answer": "test", "sources": []}

st.set_page_config(page_title="Zyro HR Help Desk", page_icon="🤖")

st.title("🏢 Zyro Dynamics HR Help Desk (RAG Chatbot)")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_query = st.chat_input("Ask HR question...")

if user_query:

    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    result = ask_bot(user_query)
    answer = result["answer"]

    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)

        if result.get("sources"):
            with st.expander("📚 Sources"):
                for doc in result["sources"]:
                    st.write(doc.page_content)
