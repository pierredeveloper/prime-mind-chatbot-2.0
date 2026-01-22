from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq
import sqlite3
import uuid
import time
import random
import os
from datetime import datetime

# --------------------------------------------------
# ENV + PAGE CONFIG
# --------------------------------------------------
load_dotenv()

st.set_page_config(
    page_title="PrimeMind 2.0",
    page_icon="chatgpt_3.png",
    layout="centered"
)

st.title("PrimeMind")

# --------------------------------------------------
# SYSTEM PROMPT (ChatGPT STYLE)
# --------------------------------------------------
# SYSTEM_PROMPT = """
# You are a helpful AI assistant called PrimeMind.

# Answer clearly, accurately, and concisely.
# Use a natural, friendly, human tone.
# Adapt your explanations to the user's level.
# Avoid unnecessary repetition and verbosity.

# Your goal is to be genuinely helpful.
# """

SYSTEM_PROMPT = """
You are a helpful, AI assistant called PrimeMind.
You answer questions clearly, accurately, and concisely.
You adapt your tone to the user: professional when needed, friendly when appropriate.
You are also a senior developoer: You can do coding in any programming language
You are AI Engineer expert:  You can design and deploy intelligent systems.
You explain complex ideas in simple terms and provide practical examples when helpful.
You avoid unnecessary repetition, hallucinations, and overly verbose responses.
Your goal is to genuinely help the user solve problems, learn, or make decisions.
"""

# --------------------------------------------------
# AVATARS
# --------------------------------------------------
USER_AVATAR = "🧑‍💻"
ASSISTANT_AVATAR = "🤖"

# --------------------------------------------------
# DATABASE (PERMANENT MEMORY)
# --------------------------------------------------
DB_NAME = "chatgpt_clone.db"

def get_conn():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            title TEXT,
            created_at TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id TEXT,
            role TEXT,
            content TEXT,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

# --------------------------------------------------
# DB HELPERS
# --------------------------------------------------
def create_conversation():
    cid = str(uuid.uuid4())
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO conversations VALUES (?, ?, ?)",
        (cid, "New chat", datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()
    return cid

def get_conversations():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT id, title FROM conversations ORDER BY created_at DESC")
    rows = c.fetchall()
    conn.close()
    return rows

def get_messages(cid):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "SELECT role, content FROM messages WHERE conversation_id=? ORDER BY id ASC",
        (cid,)
    )
    rows = c.fetchall()
    conn.close()
    return [{"role": r, "content": c} for r, c in rows]

def save_message(cid, role, content):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO messages VALUES (NULL, ?, ?, ?, ?)",
        (cid, role, content, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()

def update_title(cid, text):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "UPDATE conversations SET title=? WHERE id=?",
        (text[:40], cid)
    )
    conn.commit()
    conn.close()

def delete_conversation(cid):
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM messages WHERE conversation_id=?", (cid,))
    c.execute("DELETE FROM conversations WHERE id=?", (cid,))
    conn.commit()
    conn.close()

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "conversation_id" not in st.session_state:
    chats = get_conversations()
    st.session_state.conversation_id = chats[0][0] if chats else create_conversation()

# --------------------------------------------------
# SIDEBAR (CHATGPT STYLE)
# --------------------------------------------------
with st.sidebar:
    st.header("🗂 Chat History")

    if st.button("➕ New chat"):
        st.session_state.conversation_id = create_conversation()
        st.rerun()

    chats = get_conversations()
    for cid, title in chats:
        if st.button(title, key=cid):
            st.session_state.conversation_id = cid
            st.rerun()

    st.divider()

    if st.button("🗑 Delete chat"):
        delete_conversation(st.session_state.conversation_id)
        remaining = get_conversations()
        st.session_state.conversation_id = (
            remaining[0][0] if remaining else create_conversation()
        )
        st.rerun()

# --------------------------------------------------
# LOAD CHAT HISTORY
# --------------------------------------------------
chat_history = get_messages(st.session_state.conversation_id)

for msg in chat_history:
    avatar = USER_AVATAR if msg["role"] == "user" else ASSISTANT_AVATAR
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# --------------------------------------------------
# LLM
# --------------------------------------------------
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile",
    temperature=0.7,
    model_kwargs={"top_p": 0.9}
)

# --------------------------------------------------
# TYPING EFFECT
# --------------------------------------------------
def typewriter(text, delay=0.01):
    for char in text:
        yield char
        time.sleep(delay)

# --------------------------------------------------
# USER INPUT
# --------------------------------------------------
user_prompt = st.chat_input("Ask Chatbot...")

if user_prompt:
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(user_prompt)

    save_message(st.session_state.conversation_id, "user", user_prompt)

    if len(chat_history) == 0:
        update_title(st.session_state.conversation_id, user_prompt)

    randomizer = f"(response_variation: {random.randint(1, 999999)})"

    messages = (
        [{"role": "system", "content": SYSTEM_PROMPT},
         {"role": "system", "content": randomizer}]
        + chat_history
        + [{"role": "user", "content": user_prompt}]
    )

    response = llm.invoke(messages)
    assistant_reply = response.content

    save_message(
        st.session_state.conversation_id,
        "assistant",
        assistant_reply
    )

    with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
        st.write_stream(typewriter(assistant_reply))

































































































