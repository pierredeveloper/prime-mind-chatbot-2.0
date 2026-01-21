# from dotenv import load_dotenv
# import streamlit as st
# from langchain_groq import ChatGroq
# import time
# import random
# import os
# import sqlite3
# from datetime import datetime
# import uuid

# # --------------------------------------------------
# # ENV + STREAMLIT SETUP
# # --------------------------------------------------
# load_dotenv()

# st.set_page_config(
#     page_title="PrimeMind 2.0",
#     page_icon="chatgpt_3.png",
#     layout="centered"
# )

# st.title("💬 PrimeMind")

# # --------------------------------------------------
# # SYSTEM STYLE
# # --------------------------------------------------
# SYSTEM_STYLE = """
# You are a helpful, intelligent AI assistant called PrimeMind.

# Be clear, accurate, and concise.
# Use a friendly, professional, human tone.
# Avoid repetition or robotic phrasing.

# Your goal is to provide practical answers that genuinely help.
# """

# # --------------------------------------------------
# # AVATARS
# # --------------------------------------------------
# USER_AVATAR = "🧑‍💻"
# ASSISTANT_AVATAR = "🤖"

# # --------------------------------------------------
# # DATABASE
# # --------------------------------------------------
# DB_NAME = "primemind.db"

# def get_conn():
#     return sqlite3.connect(DB_NAME, check_same_thread=False)

# def init_db():
#     conn = get_conn()
#     c = conn.cursor()

#     c.execute("""
#         CREATE TABLE IF NOT EXISTS conversations (
#             id TEXT PRIMARY KEY,
#             title TEXT,
#             created_at TEXT
#         )
#     """)

#     c.execute("""
#         CREATE TABLE IF NOT EXISTS messages (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             conversation_id TEXT,
#             role TEXT,
#             content TEXT,
#             timestamp TEXT
#         )
#     """)

#     conn.commit()
#     conn.close()

# init_db()

# # --------------------------------------------------
# # DB HELPERS
# # --------------------------------------------------
# def create_conversation():
#     cid = str(uuid.uuid4())
#     conn = get_conn()
#     c = conn.cursor()
#     c.execute(
#         "INSERT INTO conversations VALUES (?, ?, ?)",
#         (cid, "New Chat", datetime.utcnow().isoformat())
#     )
#     conn.commit()
#     conn.close()
#     return cid

# def get_conversations():
#     conn = get_conn()
#     c = conn.cursor()
#     c.execute("SELECT id, title FROM conversations ORDER BY created_at DESC")
#     rows = c.fetchall()
#     conn.close()
#     return rows

# def get_messages(conversation_id):
#     conn = get_conn()
#     c = conn.cursor()
#     c.execute(
#         "SELECT role, content FROM messages WHERE conversation_id=? ORDER BY id ASC",
#         (conversation_id,)
#     )
#     rows = c.fetchall()
#     conn.close()
#     return [{"role": r, "content": c} for r, c in rows]

# def save_message(conversation_id, role, content):
#     conn = get_conn()
#     c = conn.cursor()
#     c.execute(
#         "INSERT INTO messages VALUES (NULL, ?, ?, ?, ?)",
#         (conversation_id, role, content, datetime.utcnow().isoformat())
#     )
#     conn.commit()
#     conn.close()

# def update_title(conversation_id, text):
#     conn = get_conn()
#     c = conn.cursor()
#     c.execute(
#         "UPDATE conversations SET title=? WHERE id=?",
#         (text[:40], conversation_id)
#     )
#     conn.commit()
#     conn.close()

# def delete_conversation(conversation_id):
#     conn = get_conn()
#     c = conn.cursor()
#     c.execute("DELETE FROM messages WHERE conversation_id=?", (conversation_id,))
#     c.execute("DELETE FROM conversations WHERE id=?", (conversation_id,))
#     conn.commit()
#     conn.close()

# # --------------------------------------------------
# # SESSION STATE
# # --------------------------------------------------
# if "conversation_id" not in st.session_state:
#     chats = get_conversations()
#     st.session_state.conversation_id = chats[0][0] if chats else create_conversation()

# # --------------------------------------------------
# # SIDEBAR
# # --------------------------------------------------
# with st.sidebar:
#     st.header("🗂 Chat History")

#     if st.button("➕ New Chat"):
#         st.session_state.conversation_id = create_conversation()
#         st.rerun()

#     chats = get_conversations()
#     for cid, title in chats:
#         if st.button(title, key=cid):
#             st.session_state.conversation_id = cid
#             st.rerun()

#     st.divider()

#     if st.button("🗑 Delete Chat"):
#         delete_conversation(st.session_state.conversation_id)
#         remaining = get_conversations()
#         st.session_state.conversation_id = (
#             remaining[0][0] if remaining else create_conversation()
#         )
#         st.rerun()

# # --------------------------------------------------
# # LOAD CHAT HISTORY
# # --------------------------------------------------
# chat_history = get_messages(st.session_state.conversation_id)

# for msg in chat_history:
#     avatar = USER_AVATAR if msg["role"] == "user" else ASSISTANT_AVATAR
#     with st.chat_message(msg["role"], avatar=avatar):
#         st.markdown(msg["content"])

# # --------------------------------------------------
# # GROQ LLM
# # --------------------------------------------------
# llm = ChatGroq(
#     api_key=os.getenv("GROQ_API_KEY"),
#     model="llama-3.3-70b-versatile",
#     temperature=0.9,
#     model_kwargs={"top_p": 0.9},
# )

# # --------------------------------------------------
# # HUMAN TYPING EFFECT
# # --------------------------------------------------
# def human_type_text(text, delay=0.01):
#     for char in text:
#         yield char
#         time.sleep(delay)

# # --------------------------------------------------
# # USER INPUT
# # --------------------------------------------------
# user_prompt = st.chat_input("Ask Chatbot...")

# if user_prompt:
#     # Show user message immediately with emoji
#     with st.chat_message("user", avatar=USER_AVATAR):
#         st.markdown(user_prompt)

#     save_message(st.session_state.conversation_id, "user", user_prompt)

#     if len(chat_history) == 0:
#         update_title(st.session_state.conversation_id, user_prompt)

#     randomizer = f"(variation_key: {random.randint(1, 999999)})"

#     messages = (
#         [
#             {"role": "system", "content": SYSTEM_STYLE},
#             {"role": "system", "content": randomizer},
#         ]
#         + chat_history
#         + [{"role": "user", "content": user_prompt}]
#     )

#     response = llm.invoke(messages)
#     assistant_response = response.content

#     save_message(
#         st.session_state.conversation_id,
#         "assistant",
#         assistant_response
#     )

#     with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
#         st.write_stream(human_type_text(assistant_response))



























from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq
import time
import random
import os
import sqlite3

# Load env variables
load_dotenv()

# -----------------------------
# DATABASE SETUP (PERMANENT MEMORY)
# -----------------------------
DB_PATH = "chat_memory.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            content TEXT
        )
    """)
    conn.commit()
    conn.close()

def load_chat_history():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT role, content FROM chat_history ORDER BY id ASC")
    rows = c.fetchall()
    conn.close()
    return [{"role": r[0], "content": r[1]} for r in rows]

def save_message(role, content):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO chat_history (role, content) VALUES (?, ?)",
        (role, content)
    )
    conn.commit()
    conn.close()

# Initialize DB
init_db()

# -----------------------------
# STREAMLIT SETUP
# -----------------------------
st.set_page_config(
    page_title="Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("💬 PrimeMind")

# Load memory into session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = load_chat_history()

# Display memory
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# LLM SETUP
# -----------------------------
llm = ChatGroq(
    api_key=st.secrets["GROQ_API_KEY"],
    model="llama-3.3-70b-versatile",
    temperature=0.9
)

SYSTEM_STYLE = """
You are a helpful, intelligent AI assistant called PrimeMind.

Be clear, accurate, and concise.
Use a friendly, professional, human tone.
Avoid repetition or robotic phrasing.

Your goal is to provide practical answers that genuinely help.
"""

# -----------------------------
# HUMAN TYPING EFFECT
# -----------------------------
def human_type_text(text, delay=0.010):
    for char in text:
        yield char
        time.sleep(delay)

# -----------------------------
# CHAT INPUT
# -----------------------------
user_prompt = st.chat_input("Ask Chatbot...")

if user_prompt:
    # Display user message
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})
    save_message("user", user_prompt)

    randomizer = f"(variation_key: {random.randint(1, 999999)})"

    messages = [
        {"role": "system", "content": SYSTEM_STYLE},
        {"role": "system", "content": randomizer}
    ] + st.session_state.chat_history

    # LLM response
    response = llm.invoke(messages)
    assistant_response = response.content

    # Save assistant reply
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": assistant_response
    })
    save_message("assistant", assistant_response)

    # Display with typing animation
    with st.chat_message("assistant"):
        st.write_stream(human_type_text(assistant_response))






























































































