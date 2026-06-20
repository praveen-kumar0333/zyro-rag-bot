

# import streamlit as st

# # 👉 PASTE YOUR ask_bot FUNCTION HERE
# # (copy from your notebook exactly)

# # Example placeholder:
# def ask_bot(question):
#     return {"answer": "test", "sources": []}

# st.set_page_config(page_title="Zyro HR Help Desk", page_icon="🤖")
# st.title("🏢 Zyro Dynamics HR Help Desk v2")

# st.title("🏢 Zyro Dynamics HR Help Desk (RAG Chatbot)")

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])

# user_query = st.chat_input("Ask HR question...")

# if user_query:

#     st.session_state.messages.append({"role": "user", "content": user_query})
#     with st.chat_message("user"):
#         st.markdown(user_query)

#     result = ask_bot(user_query)
#     answer = result["answer"]

#     st.session_state.messages.append({"role": "assistant", "content": answer})
#     with st.chat_message("assistant"):
#         st.markdown(answer)

#         if result.get("sources"):
#             with st.expander("📚 Sources"):
#                 for doc in result["sources"]:
#                     st.write(doc.page_content)




















import streamlit as st
import os

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

# --------------------
# CONFIG
# --------------------
st.set_page_config(page_title="Zyro HR Help Desk", page_icon="🤖")

st.title("🏢 Zyro Dynamics HR Help Desk")

# --------------------
# EMBEDDINGS + FAISS
# --------------------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = vectorstore.as_retriever()

# --------------------
# LLM
# --------------------
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant"
)

# --------------------
# RAG FUNCTION
# --------------------
def ask_bot(question):

    docs = retriever.invoke(question)
    context = "\n\n".join([d.page_content for d in docs])

    response = llm.invoke(
        f"Answer using only this context:\n\n{context}\n\nQuestion: {question}"
    )

    return {
        "answer": response.content,
        "sources": docs
    }

# --------------------
# CHAT UI
# --------------------
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

    st.session_state.messages.append({"role": "assistant", "content": result["answer"]})

    with st.chat_message("assistant"):
        st.markdown(result["answer"])

        with st.expander("📚 Sources"):
            for doc in result["sources"]:
                st.write(doc.page_content)











