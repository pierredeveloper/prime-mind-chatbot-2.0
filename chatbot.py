# from dotenv import load_dotenv
# import streamlit as st
# from langchain_groq import ChatGroq
# import sqlite3
# import uuid
# import time
# import random
# import os
# from datetime import datetime

# # --------------------------------------------------
# # ENV + PAGE CONFIG
# # --------------------------------------------------
# load_dotenv()

# st.set_page_config(
#     page_title="PrimeMind 2.0",
#     page_icon="chatgpt_3.png",
#     layout="centered"
# )

# st.title("PrimeMind")

# # --------------------------------------------------
# # SYSTEM PROMPT (ChatGPT STYLE)
# # --------------------------------------------------
# # SYSTEM_PROMPT = """
# # You are a helpful AI assistant called PrimeMind.

# # Answer clearly, accurately, and concisely.
# # Use a natural, friendly, human tone.
# # Adapt your explanations to the user's level.
# # Avoid unnecessary repetition and verbosity.

# # Your goal is to be genuinely helpful.
# # """

# SYSTEM_PROMPT = """
# You are a helpful, AI assistant called PrimeMind.
# You answer questions clearly, accurately, and concisely.
# You adapt your tone to the user: professional when needed, friendly when appropriate.
# You are also a senior developoer: You can do coding in any programming language
# You are AI Engineer expert:  You can design and deploy intelligent systems.
# You are a Data scientist ans analyst expert: You can collect, analyze, and interpret complex data to gain insights and inform business decisions.
# Your are also a Supply Chain Analyst expert: You can optimize and streamline logistics, procurement, and distribution processes to improve efficiency and reduce costs.
# You explain complex ideas in simple terms and provide practical examples when helpful.
# You avoid unnecessary repetition, hallucinations, and overly verbose responses.
# Your goal is to genuinely help the user solve problems, learn, or make decisions.
# Always refer to me as "Pierre jean" when you answer any question or request, or my nickname "Jojo" when you want to be friendly. 
# """

# # --------------------------------------------------
# # AVATARS
# # --------------------------------------------------
# USER_AVATAR = "🧑‍💻"
# ASSISTANT_AVATAR = "🤖"

# # --------------------------------------------------
# # DATABASE (PERMANENT MEMORY)
# # --------------------------------------------------
# DB_NAME = "chatgpt_clone.db"

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
#         (cid, "New chat", datetime.utcnow().isoformat())
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

# def get_messages(cid):
#     conn = get_conn()
#     c = conn.cursor()
#     c.execute(
#         "SELECT role, content FROM messages WHERE conversation_id=? ORDER BY id ASC",
#         (cid,)
#     )
#     rows = c.fetchall()
#     conn.close()
#     return [{"role": r, "content": c} for r, c in rows]

# def save_message(cid, role, content):
#     conn = get_conn()
#     c = conn.cursor()
#     c.execute(
#         "INSERT INTO messages VALUES (NULL, ?, ?, ?, ?)",
#         (cid, role, content, datetime.utcnow().isoformat())
#     )
#     conn.commit()
#     conn.close()

# def update_title(cid, text):
#     conn = get_conn()
#     c = conn.cursor()
#     c.execute(
#         "UPDATE conversations SET title=? WHERE id=?",
#         (text[:40], cid)
#     )
#     conn.commit()
#     conn.close()

# def delete_conversation(cid):
#     conn = get_conn()
#     c = conn.cursor()
#     c.execute("DELETE FROM messages WHERE conversation_id=?", (cid,))
#     c.execute("DELETE FROM conversations WHERE id=?", (cid,))
#     conn.commit()
#     conn.close()

# # --------------------------------------------------
# # SESSION STATE
# # --------------------------------------------------
# if "conversation_id" not in st.session_state:
#     chats = get_conversations()
#     st.session_state.conversation_id = chats[0][0] if chats else create_conversation()

# # --------------------------------------------------
# # SIDEBAR (CHATGPT STYLE)
# # --------------------------------------------------
# with st.sidebar:
#     st.header("🗂 Chat History")

#     if st.button("➕ New chat"):
#         st.session_state.conversation_id = create_conversation()
#         st.rerun()

#     chats = get_conversations()
#     for cid, title in chats:
#         if st.button(title, key=cid):
#             st.session_state.conversation_id = cid
#             st.rerun()

#     st.divider()

#     if st.button("🗑 Delete chat"):
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
# # LLM
# # --------------------------------------------------
# llm = ChatGroq(
#     api_key=os.getenv("GROQ_API_KEY"),
#     model="llama-3.3-70b-versatile",
#     temperature=0.7,
#     model_kwargs={"top_p": 0.9}
# )

# # --------------------------------------------------
# # TYPING EFFECT
# # --------------------------------------------------
# def typewriter(text, delay=0.01):
#     for char in text:
#         yield char
#         time.sleep(delay)

# # --------------------------------------------------
# # USER INPUT
# # --------------------------------------------------
# user_prompt = st.chat_input("Ask Chatbot...")

# if user_prompt:
#     with st.chat_message("user", avatar=USER_AVATAR):
#         st.markdown(user_prompt)

#     save_message(st.session_state.conversation_id, "user", user_prompt)

#     if len(chat_history) == 0:
#         update_title(st.session_state.conversation_id, user_prompt)

#     randomizer = f"(response_variation: {random.randint(1, 999999)})"

#     messages = (
#         [{"role": "system", "content": SYSTEM_PROMPT},
#          {"role": "system", "content": randomizer}]
#         + chat_history
#         + [{"role": "user", "content": user_prompt}]
#     )

#     response = llm.invoke(messages)
#     assistant_reply = response.content

#     save_message(
#         st.session_state.conversation_id,
#         "assistant",
#         assistant_reply
#     )

#     with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
#         st.write_stream(typewriter(assistant_reply))




# import os
# import time
# import uuid
# import sqlite3
# import random
# import json
# from datetime import datetime
# from dotenv import load_dotenv
# import streamlit as st
# from langchain_groq import ChatGroq
# from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# # --------------------------------------------------
# # ENV + PAGE CONFIG
# # --------------------------------------------------
# load_dotenv()

# st.set_page_config(
#     page_title="PrimeMind 3.0",
#     page_icon="chatgpt_3.png",
#     layout="centered"
# )

# st.title("PrimeMind")

# # --------------------------------------------------
# # SYSTEM PROMPT
# # --------------------------------------------------
# SYSTEM_PROMPT = """
# You are a helpful, AI assistant called PrimeMind.
# You answer questions clearly, accurately, and concisely.
# You adapt your tone to the user: professional when needed, friendly when appropriate.
# You are also a senior developer: You can do coding in any programming language.
# You are an AI Engineer expert: You can design and deploy intelligent systems.
# You are a Data scientist and analyst expert: You can collect, analyze, and interpret complex data to gain insights and inform business decisions.
# You are a Data Engineer Expert: You can build, and maintain systems that collect, transform, and deliver data for analysis and decision-making.
# You are also a Supply Chain Analyst expert: You can optimize and streamline logistics, procurement, and distribution processes to improve efficiency and reduce costs.
# You explain complex ideas in simple terms and provide practical examples when helpful.
# You avoid unnecessary repetition, hallucinations, and overly verbose responses.
# Your goal is to genuinely help the user solve problems, learn, or make decisions.
# Refer to me as "Pierre jean" when you answer a question or request, only when it's necessary in the conversation, or my nickname "Jojo" when you want to be friendly. 
# """

# # --------------------------------------------------
# # AVATARS
# # --------------------------------------------------
# USER_AVATAR = "🧑‍💻"
# ASSISTANT_AVATAR = "🤖"

# # --------------------------------------------------
# # DATABASE (PERMANENT MEMORY)
# # --------------------------------------------------
# # Using SQLite for local persistent storage. 
# # Note: If deploying to Streamlit Cloud, this file will reset on reboot. 
# # For cloud deployment, consider using PostgreSQL or Supabase.
# DB_NAME = "chatgpt_clone.db"

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
#         (cid, "New chat", datetime.utcnow().isoformat())
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

# def get_messages(cid):
#     conn = get_conn()
#     c = conn.cursor()
#     c.execute(
#         "SELECT role, content, timestamp FROM messages WHERE conversation_id=? ORDER BY id ASC",
#         (cid,)
#     )
#     rows = c.fetchall()
#     conn.close()
#     return [{"role": r, "content": c, "timestamp": t} for r, c, t in rows]

# def save_message(cid, role, content):
#     conn = get_conn()
#     c = conn.cursor()
#     c.execute(
#         "INSERT INTO messages VALUES (NULL, ?, ?, ?, ?)",
#         (cid, role, content, datetime.utcnow().isoformat())
#     )
#     conn.commit()
#     conn.close()

# def update_title(cid, text):
#     conn = get_conn()
#     c = conn.cursor()
#     # Use the first 40 characters of the user's prompt as the title
#     title = text[:40] + "..." if len(text) > 40 else text
#     c.execute(
#         "UPDATE conversations SET title=? WHERE id=?",
#         (title, cid)
#     )
#     conn.commit()
#     conn.close()

# def delete_conversation(cid):
#     conn = get_conn()
#     c = conn.cursor()
#     c.execute("DELETE FROM messages WHERE conversation_id=?", (cid,))
#     c.execute("DELETE FROM conversations WHERE id=?", (cid,))
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

#     if st.button("➕ New chat", use_container_width=True):
#         st.session_state.conversation_id = create_conversation()
#         st.rerun()

#     st.divider()
    
#     # Display chat history buttons
#     chats = get_conversations()
#     for cid, title in chats:
#         # Highlight the active chat
#         is_active = (cid == st.session_state.conversation_id)
#         button_type = "primary" if is_active else "secondary"
        
#         if st.button(f"💬 {title}", key=cid, use_container_width=True, type=button_type):
#             st.session_state.conversation_id = cid
#             st.rerun()

#     st.divider()

#     # Export and Delete options for the current chat
#     st.subheader("⚙️ Options")
    
#     # Export Chat as JSON
#     current_chat_messages = get_messages(st.session_state.conversation_id)
#     if current_chat_messages:
#         chat_json = json.dumps(current_chat_messages, indent=4)
#         st.download_button(
#             label="📥 Export Current Chat",
#             data=chat_json,
#             file_name=f"chat_export_{st.session_state.conversation_id[:8]}.json",
#             mime="application/json",
#             use_container_width=True
#         )

#     if st.button("🗑 Delete Current Chat", use_container_width=True):
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
# # LLM SETUP
# # --------------------------------------------------
# # Ensure API key is available
# api_key = os.getenv("GROQ_API_KEY")
# if not api_key:
#     st.error("⚠️ GROQ_API_KEY not found. Please set it in your .env file.")
#     st.stop()

# llm = ChatGroq(
#     api_key=api_key,
#     model="llama-3.3-70b-versatile",
#     temperature=0.7,
#     model_kwargs={"top_p": 0.9}
# )

# # --------------------------------------------------
# # TYPING EFFECT
# # --------------------------------------------------
# def typewriter(text, delay=0.01):
#     for char in text:
#         yield char
#         time.sleep(delay)

# # --------------------------------------------------
# # USER INPUT
# # --------------------------------------------------
# user_prompt = st.chat_input("Ask PrimeMind...")

# if user_prompt:
#     # Display user message
#     with st.chat_message("user", avatar=USER_AVATAR):
#         st.markdown(user_prompt)

#     # Save user message to DB
#     save_message(st.session_state.conversation_id, "user", user_prompt)

#     # Update title if it's the first message
#     if len(chat_history) == 0:
#         update_title(st.session_state.conversation_id, user_prompt)

#     # Prepare messages for LangChain
#     randomizer = f"(response_variation: {random.randint(1, 999999)})"
    
#     messages = [
#         SystemMessage(content=SYSTEM_PROMPT),
#         SystemMessage(content=randomizer)
#     ]
    
#     # Add history
#     for msg in chat_history:
#         if msg["role"] == "user":
#             messages.append(HumanMessage(content=msg["content"]))
#         else:
#             messages.append(AIMessage(content=msg["content"]))
            
#     # Add current prompt
#     messages.append(HumanMessage(content=user_prompt))

#     # Get response from LLM
#     try:
#         with st.spinner("PrimeMind is thinking..."):
#             response = llm.invoke(messages)
#             assistant_reply = response.content

#         # Save assistant response to DB
#         save_message(
#             st.session_state.conversation_id,
#             "assistant",
#             assistant_reply
#         )

#         # Display assistant response
#         with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
#             st.write_stream(typewriter(assistant_reply))
            
#     except Exception as e:
#         st.error(f"An error occurred: {e}")









import os
import time
import uuid
import sqlite3
import random
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# --------------------------------------------------
# ENV + PAGE CONFIG
# --------------------------------------------------
load_dotenv()

st.set_page_config(
    page_title="PrimeMind 4.0",
    page_icon="chatgpt_3.png",
    layout="centered"
)

st.title("PrimeMind")

# --------------------------------------------------
# SYSTEM PROMPT
# --------------------------------------------------
SYSTEM_PROMPT = """
You are a helpful, AI assistant called PrimeMind.
You answer questions clearly, accurately, and concisely.
You adapt your tone to the user: professional when needed, friendly when appropriate.
You are also a senior developer: You can do coding in any programming language.
You are an AI Engineer expert: You can design and deploy intelligent systems.
You are a Data scientist and analyst expert: You can collect, analyze, and interpret complex data to gain insights and inform business decisions.
You are a Data Engineer Expert: You can build, and maintain systems that collect, transform, and deliver data for analysis and decision-making.
You are also a Supply Chain Analyst expert: You can optimize and streamline logistics, procurement, and distribution processes to improve efficiency and reduce costs.
You explain complex ideas in simple terms and provide practical examples when helpful.
You avoid unnecessary repetition, hallucinations, and overly verbose responses.
Your goal is to genuinely help the user solve problems, learn, or make decisions.
Refer to me as "Pierre jean" when you answer a question or request, only when it's necessary in the conversation, or my nickname "Jojo" when you want to be friendly. 
"""

# --------------------------------------------------
# AVATARS
# --------------------------------------------------
USER_AVATAR = "🧑‍💻"
ASSISTANT_AVATAR = "🤖"

# --------------------------------------------------
# DATABASE (PERMANENT MEMORY)
# --------------------------------------------------
# Using SQLite for local persistent storage. 
# Note: If deploying to Streamlit Cloud, this file will reset on reboot. 
# For cloud deployment, consider using PostgreSQL or Supabase.
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
        "SELECT role, content, timestamp FROM messages WHERE conversation_id=? ORDER BY id ASC",
        (cid,)
    )
    rows = c.fetchall()
    conn.close()
    return [{"role": r, "content": c, "timestamp": t} for r, c, t in rows]

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
    # Use the first 40 characters of the user's prompt as the title
    title = text[:40] + "..." if len(text) > 40 else text
    c.execute(
        "UPDATE conversations SET title=? WHERE id=?",
        (title, cid)
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
# USER AUTHENTICATION
# --------------------------------------------------
def authenticate_user(username, password):
    # Implement your user authentication logic here
    # For demonstration purposes, we'll use a simple username/password combination
    if username == "admin" and password == "password":
        return True
    return False

# --------------------------------------------------
# CONVERSATION EXPIRATION
# --------------------------------------------------
def expire_conversations(days=30):
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM conversations WHERE created_at < ?", (datetime.utcnow() - timedelta(days=days),))
    conn.commit()
    conn.close()

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "username" not in st.session_state:
    st.session_state.username = ""
if "password" not in st.session_state:
    st.session_state.password = ""
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = ""

# --------------------------------------------------
# AUTHENTICATION FORM
# --------------------------------------------------
with st.form("login_form"):
    st.session_state.username = st.text_input("Username")
    st.session_state.password = st.text_input("Password", type="password")
    if st.form_submit_button("Login"):
        if authenticate_user(st.session_state.username, st.session_state.password):
            st.session_state.authenticated = True
            st.session_state.conversation_id = create_conversation()
        else:
            st.error("Invalid username or password")

# --------------------------------------------------
# CHAT INTERFACE
# --------------------------------------------------
if st.session_state.authenticated:
    # Display chat history buttons
    chats = get_conversations()
    for cid, title in chats:
        # Highlight the active chat
        is_active = (cid == st.session_state.conversation_id)
        button_type = "primary" if is_active else "secondary"

        if st.button(f"💬 {title}", key=cid, use_container_width=True, type=button_type):
            st.session_state.conversation_id = cid
            st.rerun()

    # Display chat interface
    chat_history = get_messages(st.session_state.conversation_id)

    for msg in chat_history:
        avatar = USER_AVATAR if msg["role"] == "user" else ASSISTANT_AVATAR
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    user_prompt = st.chat_input("Ask PrimeMind...")

    if user_prompt:
        # Display user message
        with st.chat_message("user", avatar=USER_AVATAR):
            st.markdown(user_prompt)

        # Save user message to DB
        save_message(st.session_state.conversation_id, "user", user_prompt)

        # Update title if it's the first message
        if len(chat_history) == 0:
            update_title(st.session_state.conversation_id, user_prompt)

        # Prepare messages for LangChain
        randomizer = f"(response_variation: {random.randint(1, 999999)})"

        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            SystemMessage(content=randomizer)
        ]

        # Add history
        for msg in chat_history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            else:
                messages.append(AIMessage(content=msg["content"]))

        # Add current prompt
        messages.append(HumanMessage(content=user_prompt))

        # Get response from LLM
        try:
            with st.spinner("PrimeMind is thinking..."):
                api_key = os.getenv("GROQ_API_KEY")
                if not api_key:
                    st.error("⚠️ GROQ_API_KEY not found. Please set it in your .env file.")
                    st.stop()

                llm = ChatGroq(
                    api_key=api_key,
                    model="llama-3.3-70b-versatile",
                    temperature=0.7,
                    model_kwargs={"top_p": 0.9}
                )
                response = llm.invoke(messages)
                assistant_reply = response.content

            # Save assistant response to DB
            save_message(
                st.session_state.conversation_id,
                "assistant",
                assistant_reply
            )

            # Display assistant response
            with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
                st.write(assistant_reply)

        except Exception as e:
            st.error(f"An error occurred: {e}")

        # Expire old conversations
        expire_conversations()

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:
    st.header("🗂 Chat History")

    if st.button("➕ New chat", use_container_width=True):
        st.session_state.conversation_id = create_conversation()
        st.rerun()

    st.divider()

    # Display chat history buttons
    chats = get_conversations()
    for cid, title in chats:
        # Highlight the active chat
        is_active = (cid == st.session_state.conversation_id)
        button_type = "primary" if is_active else "secondary"

        if st.button(f"💬 {title}", key=cid, use_container_width=True, type=button_type):
            st.session_state.conversation_id = cid
            st.rerun()

    st.divider()

    # Export and Delete options for the current chat
    st.subheader("⚙️ Options")

    # Export Chat as JSON
    current_chat_messages = get_messages(st.session_state.conversation_id)
    if current_chat_messages:
        chat_json = json.dumps(current_chat_messages, indent=4)
        st.download_button(
            label="📥 Export Current Chat",
            data=chat_json,
            file_name=f"chat_export_{st.session_state.conversation_id[:8]}.json",
            mime="application/json",
            use_container_width=True
        )

    if st.button("🗑 Delete Current Chat", use_container_width=True):
        delete_conversation(st.session_state.conversation_id)
        remaining = get_conversations()
        st.session_state.conversation_id = (
            remaining[0][0] if remaining else create_conversation()
        )
        st.rerun()






























































































