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









# import os
# import uuid
# import sqlite3
# import random
# import json
# import hashlib
# import secrets
# import re
# from datetime import datetime, timedelta
# from dotenv import load_dotenv
# import streamlit as st
# from langchain_groq import ChatGroq
# from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# # --------------------------------------------------
# # ENV + PAGE CONFIG
# # --------------------------------------------------
# load_dotenv()

# st.set_page_config(
#     page_title="PrimeMind 4.0",
#     page_icon="chatgpt_3.png",
#     layout="centered"
# )

# # --------------------------------------------------
# # CUSTOM CSS — sleek dark auth UI
# # --------------------------------------------------
# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

# /* ---- Global ---- */
# html, body, [class*="css"] {
#     font-family: 'DM Sans', sans-serif;
# }

# /* ---- Auth card container ---- */
# .auth-card {
#     background: linear-gradient(145deg, #0f0f13, #1a1a24);
#     border: 1px solid rgba(255,255,255,0.07);
#     border-radius: 20px;
#     padding: 2.5rem 2.5rem 2rem;
#     max-width: 420px;
#     margin: 3rem auto;
#     box-shadow: 0 30px 80px rgba(0,0,0,0.5), 0 0 0 1px rgba(100,80,255,0.08);
# }

# .auth-logo {
#     font-family: 'Syne', sans-serif;
#     font-size: 2rem;
#     font-weight: 800;
#     background: linear-gradient(135deg, #a78bfa, #60a5fa);
#     -webkit-background-clip: text;
#     -webkit-text-fill-color: transparent;
#     background-clip: text;
#     text-align: center;
#     margin-bottom: 0.25rem;
# }

# .auth-tagline {
#     text-align: center;
#     color: rgba(255,255,255,0.35);
#     font-size: 0.8rem;
#     letter-spacing: 0.12em;
#     text-transform: uppercase;
#     margin-bottom: 2rem;
# }

# .auth-tab-row {
#     display: flex;
#     gap: 0;
#     background: rgba(255,255,255,0.04);
#     border-radius: 10px;
#     padding: 4px;
#     margin-bottom: 1.8rem;
# }

# .auth-tab {
#     flex: 1;
#     text-align: center;
#     padding: 0.55rem 0;
#     border-radius: 8px;
#     font-size: 0.85rem;
#     font-weight: 500;
#     cursor: pointer;
#     transition: all 0.2s;
#     color: rgba(255,255,255,0.45);
#     user-select: none;
# }

# .auth-tab.active {
#     background: linear-gradient(135deg, #7c3aed, #3b82f6);
#     color: white;
#     box-shadow: 0 4px 15px rgba(124,58,237,0.35);
# }

# .auth-divider {
#     border: none;
#     border-top: 1px solid rgba(255,255,255,0.07);
#     margin: 1.5rem 0;
# }

# .field-label {
#     font-size: 0.78rem;
#     font-weight: 500;
#     letter-spacing: 0.06em;
#     text-transform: uppercase;
#     color: rgba(255,255,255,0.5);
#     margin-bottom: 0.4rem;
# }

# /* ---- Streamlit element overrides ---- */
# div[data-testid="stTextInput"] input {
#     background: rgba(255,255,255,0.04) !important;
#     border: 1px solid rgba(255,255,255,0.1) !important;
#     border-radius: 10px !important;
#     color: white !important;
#     font-family: 'DM Sans', sans-serif !important;
#     padding: 0.65rem 0.9rem !important;
#     transition: border-color 0.2s !important;
# }
# div[data-testid="stTextInput"] input:focus {
#     border-color: rgba(124,58,237,0.6) !important;
#     box-shadow: 0 0 0 3px rgba(124,58,237,0.1) !important;
# }

# div[data-testid="stForm"] {
#     background: transparent !important;
#     border: none !important;
#     padding: 0 !important;
# }

# /* Primary buttons */
# div[data-testid="stFormSubmitButton"] > button,
# div[data-testid="stButton"] > button[kind="primary"] {
#     background: linear-gradient(135deg, #7c3aed, #3b82f6) !important;
#     border: none !important;
#     border-radius: 10px !important;
#     color: white !important;
#     font-family: 'Syne', sans-serif !important;
#     font-weight: 600 !important;
#     font-size: 0.9rem !important;
#     letter-spacing: 0.04em !important;
#     padding: 0.7rem !important;
#     width: 100% !important;
#     transition: all 0.2s !important;
#     box-shadow: 0 4px 20px rgba(124,58,237,0.3) !important;
# }
# div[data-testid="stFormSubmitButton"] > button:hover,
# div[data-testid="stButton"] > button[kind="primary"]:hover {
#     transform: translateY(-1px) !important;
#     box-shadow: 0 6px 25px rgba(124,58,237,0.45) !important;
# }

# /* Secondary buttons (tab toggle) */
# div[data-testid="stButton"] > button[kind="secondary"] {
#     background: rgba(255,255,255,0.04) !important;
#     border: 1px solid rgba(255,255,255,0.08) !important;
#     border-radius: 10px !important;
#     color: rgba(255,255,255,0.6) !important;
#     font-family: 'DM Sans', sans-serif !important;
#     transition: all 0.2s !important;
# }
# div[data-testid="stButton"] > button[kind="secondary"]:hover {
#     background: rgba(255,255,255,0.08) !important;
#     color: white !important;
# }

# /* Success / error alerts */
# div[data-testid="stAlert"] {
#     border-radius: 10px !important;
#     font-family: 'DM Sans', sans-serif !important;
#     font-size: 0.85rem !important;
# }

# /* Sidebar logout button */
# .logout-btn > button {
#     background: rgba(239,68,68,0.1) !important;
#     border: 1px solid rgba(239,68,68,0.25) !important;
#     color: #f87171 !important;
#     border-radius: 8px !important;
# }
# .logout-btn > button:hover {
#     background: rgba(239,68,68,0.2) !important;
# }

# /* App title */
# .app-title {
#     font-family: 'Syne', sans-serif;
#     font-size: 1.6rem;
#     font-weight: 800;
#     background: linear-gradient(135deg, #a78bfa, #60a5fa);
#     -webkit-background-clip: text;
#     -webkit-text-fill-color: transparent;
#     background-clip: text;
# }
# </style>
# """, unsafe_allow_html=True)

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

# USER_AVATAR = "🧑‍💻"
# ASSISTANT_AVATAR = "🤖"

# # --------------------------------------------------
# # DATABASE
# # --------------------------------------------------
# DB_NAME = "chatgpt_clone.db"

# def get_conn():
#     return sqlite3.connect(DB_NAME, check_same_thread=False)

# def init_db():
#     conn = get_conn()
#     c = conn.cursor()

#     # Users table
#     c.execute("""
#         CREATE TABLE IF NOT EXISTS users (
#             id TEXT PRIMARY KEY,
#             username TEXT UNIQUE NOT NULL,
#             email TEXT UNIQUE NOT NULL,
#             password_hash TEXT NOT NULL,
#             salt TEXT NOT NULL,
#             created_at TEXT
#         )
#     """)

#     # Conversations table (with user_id column)
#     c.execute("""
#         CREATE TABLE IF NOT EXISTS conversations (
#             id TEXT PRIMARY KEY,
#             user_id TEXT NOT NULL DEFAULT '',
#             title TEXT,
#             created_at TEXT
#         )
#     """)

#     # Migrate old conversations table if user_id column is missing
#     try:
#         c.execute("ALTER TABLE conversations ADD COLUMN user_id TEXT NOT NULL DEFAULT ''")
#         conn.commit()
#     except sqlite3.OperationalError:
#         pass  # Column already exists

#     # Messages table
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
# # AUTH HELPERS
# # --------------------------------------------------
# def hash_password(password: str, salt: str = None):
#     if salt is None:
#         salt = secrets.token_hex(16)
#     pw_hash = hashlib.sha256((password + salt).encode("utf-8")).hexdigest()
#     return pw_hash, salt

# def validate_email(email: str) -> bool:
#     return bool(re.match(r"^[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}$", email))

# def validate_password(password: str):
#     """Returns (ok: bool, message: str)"""
#     if len(password) < 8:
#         return False, "Password must be at least 8 characters."
#     if not re.search(r"[A-Z]", password):
#         return False, "Password must contain at least one uppercase letter."
#     if not re.search(r"[0-9]", password):
#         return False, "Password must contain at least one number."
#     return True, ""

# def register_user(username: str, email: str, password: str):
#     """Returns (success: bool, message: str)"""
#     username = username.strip()
#     email = email.strip().lower()

#     if not username or len(username) < 3:
#         return False, "Username must be at least 3 characters."
#     if not validate_email(email):
#         return False, "Please enter a valid email address."
#     ok, msg = validate_password(password)
#     if not ok:
#         return False, msg

#     pw_hash, salt = hash_password(password)
#     uid = str(uuid.uuid4())
#     try:
#         conn = get_conn()
#         c = conn.cursor()
#         c.execute(
#             "INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)",
#             (uid, username, email, pw_hash, salt, datetime.utcnow().isoformat())
#         )
#         conn.commit()
#         conn.close()
#         return True, "Account created successfully! Please log in."
#     except sqlite3.IntegrityError as e:
#         err = str(e).lower()
#         if "username" in err:
#             return False, "Username is already taken."
#         if "email" in err:
#             return False, "An account with that email already exists."
#         return False, "Registration failed. Please try again."

# def authenticate_user(username: str, password: str):
#     """Returns (success: bool, user_id: str | None)"""
#     conn = get_conn()
#     c = conn.cursor()
#     c.execute(
#         "SELECT id, password_hash, salt FROM users WHERE username=? COLLATE NOCASE",
#         (username.strip(),)
#     )
#     row = c.fetchone()
#     conn.close()
#     if row:
#         uid, stored_hash, salt = row
#         pw_hash, _ = hash_password(password, salt)
#         if pw_hash == stored_hash:
#             return True, uid
#     return False, None

# # --------------------------------------------------
# # CONVERSATION DB HELPERS
# # --------------------------------------------------
# def create_conversation(user_id: str) -> str:
#     cid = str(uuid.uuid4())
#     conn = get_conn()
#     c = conn.cursor()
#     c.execute(
#         "INSERT INTO conversations VALUES (?, ?, ?, ?)",
#         (cid, user_id, "New chat", datetime.utcnow().isoformat())
#     )
#     conn.commit()
#     conn.close()
#     return cid

# def get_conversations(user_id: str):
#     conn = get_conn()
#     c = conn.cursor()
#     c.execute(
#         "SELECT id, title FROM conversations WHERE user_id=? ORDER BY created_at DESC",
#         (user_id,)
#     )
#     rows = c.fetchall()
#     conn.close()
#     return rows

# def get_messages(cid: str):
#     conn = get_conn()
#     c = conn.cursor()
#     c.execute(
#         "SELECT role, content, timestamp FROM messages WHERE conversation_id=? ORDER BY id ASC",
#         (cid,)
#     )
#     rows = c.fetchall()
#     conn.close()
#     return [{"role": r, "content": ct, "timestamp": t} for r, ct, t in rows]

# def save_message(cid: str, role: str, content: str):
#     conn = get_conn()
#     c = conn.cursor()
#     c.execute(
#         "INSERT INTO messages VALUES (NULL, ?, ?, ?, ?)",
#         (cid, role, content, datetime.utcnow().isoformat())
#     )
#     conn.commit()
#     conn.close()

# def update_title(cid: str, text: str):
#     title = text[:40] + "..." if len(text) > 40 else text
#     conn = get_conn()
#     c = conn.cursor()
#     c.execute("UPDATE conversations SET title=? WHERE id=?", (title, cid))
#     conn.commit()
#     conn.close()

# def delete_conversation(cid: str):
#     conn = get_conn()
#     c = conn.cursor()
#     c.execute("DELETE FROM messages WHERE conversation_id=?", (cid,))
#     c.execute("DELETE FROM conversations WHERE id=?", (cid,))
#     conn.commit()
#     conn.close()

# def expire_conversations(user_id: str, days: int = 30):
#     conn = get_conn()
#     c = conn.cursor()
#     cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat()
#     c.execute(
#         "DELETE FROM conversations WHERE user_id=? AND created_at < ?",
#         (user_id, cutoff)
#     )
#     conn.commit()
#     conn.close()

# # --------------------------------------------------
# # SESSION STATE INIT
# # --------------------------------------------------
# defaults = {
#     "authenticated": False,
#     "user_id": None,
#     "username": None,
#     "conversation_id": None,
#     "auth_mode": "login",   # "login" | "signup"
# }
# for k, v in defaults.items():
#     if k not in st.session_state:
#         st.session_state[k] = v

# # --------------------------------------------------
# # AUTH SCREEN
# # --------------------------------------------------
# def show_auth_screen():
#     # Centered auth card
#     st.markdown('<div class="auth-card">', unsafe_allow_html=True)
#     st.markdown('<div class="auth-logo">⚡ PrimeMind</div>', unsafe_allow_html=True)
#     st.markdown('<div class="auth-tagline">Your intelligent assistant</div>', unsafe_allow_html=True)

#     # Tab switcher
#     col1, col2 = st.columns(2)
#     with col1:
#         if st.button(
#             "Sign In",
#             use_container_width=True,
#             type="primary" if st.session_state.auth_mode == "login" else "secondary",
#             key="tab_login"
#         ):
#             st.session_state.auth_mode = "login"
#             st.rerun()
#     with col2:
#         if st.button(
#             "Create Account",
#             use_container_width=True,
#             type="primary" if st.session_state.auth_mode == "signup" else "secondary",
#             key="tab_signup"
#         ):
#             st.session_state.auth_mode = "signup"
#             st.rerun()

#     st.markdown("<hr class='auth-divider'>", unsafe_allow_html=True)

#     # ---- LOGIN FORM ----
#     if st.session_state.auth_mode == "login":
#         with st.form("login_form", clear_on_submit=False):
#             st.markdown('<div class="field-label">Username</div>', unsafe_allow_html=True)
#             username = st.text_input(
#                 "Username", placeholder="Enter your username",
#                 label_visibility="collapsed"
#             )
#             st.markdown('<div class="field-label">Password</div>', unsafe_allow_html=True)
#             password = st.text_input(
#                 "Password", type="password",
#                 placeholder="Enter your password",
#                 label_visibility="collapsed"
#             )
#             submitted = st.form_submit_button("Sign In →", use_container_width=True)

#         if submitted:
#             if not username or not password:
#                 st.error("Please fill in all fields.")
#             else:
#                 ok, uid = authenticate_user(username, password)
#                 if ok:
#                     st.session_state.authenticated = True
#                     st.session_state.user_id = uid
#                     st.session_state.username = username.strip()
#                     st.session_state.conversation_id = create_conversation(uid)
#                     st.rerun()
#                 else:
#                     st.error("❌ Invalid username or password.")

#     # ---- SIGNUP FORM ----
#     else:
#         with st.form("signup_form", clear_on_submit=False):
#             st.markdown('<div class="field-label">Username</div>', unsafe_allow_html=True)
#             new_username = st.text_input(
#                 "Username", placeholder="Choose a username (min. 3 chars)",
#                 label_visibility="collapsed"
#             )
#             st.markdown('<div class="field-label">Email</div>', unsafe_allow_html=True)
#             new_email = st.text_input(
#                 "Email", placeholder="your@email.com",
#                 label_visibility="collapsed"
#             )
#             st.markdown('<div class="field-label">Password</div>', unsafe_allow_html=True)
#             new_password = st.text_input(
#                 "Password", type="password",
#                 placeholder="Min. 8 chars, 1 uppercase, 1 number",
#                 label_visibility="collapsed"
#             )
#             st.markdown('<div class="field-label">Confirm Password</div>', unsafe_allow_html=True)
#             confirm_password = st.text_input(
#                 "Confirm Password", type="password",
#                 placeholder="Repeat your password",
#                 label_visibility="collapsed"
#             )
#             submitted = st.form_submit_button("Create Account →", use_container_width=True)

#         if submitted:
#             if not all([new_username, new_email, new_password, confirm_password]):
#                 st.error("Please fill in all fields.")
#             elif new_password != confirm_password:
#                 st.error("❌ Passwords do not match.")
#             else:
#                 success, message = register_user(new_username, new_email, new_password)
#                 if success:
#                     st.success(f"✅ {message}")
#                     st.session_state.auth_mode = "login"
#                     st.rerun()
#                 else:
#                     st.error(f"❌ {message}")

#     st.markdown("</div>", unsafe_allow_html=True)  # close auth-card


# # --------------------------------------------------
# # MAIN APP (authenticated)
# # --------------------------------------------------
# def show_main_app():
#     # Sidebar
#     with st.sidebar:
#         # User info + logout
#         st.markdown(f"👤 **{st.session_state.username}**")
#         st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
#         if st.button("🚪 Log Out", use_container_width=True):
#             for k in defaults:
#                 st.session_state[k] = defaults[k]
#             st.rerun()
#         st.markdown("</div>", unsafe_allow_html=True)

#         st.divider()
#         st.header("🗂 Chat History")

#         if st.button("➕ New chat", use_container_width=True):
#             st.session_state.conversation_id = create_conversation(st.session_state.user_id)
#             st.rerun()

#         st.divider()

#         chats = get_conversations(st.session_state.user_id)
#         for cid, title in chats:
#             is_active = (cid == st.session_state.conversation_id)
#             btn_type = "primary" if is_active else "secondary"
#             if st.button(f"💬 {title}", key=f"chat_{cid}", use_container_width=True, type=btn_type):
#                 st.session_state.conversation_id = cid
#                 st.rerun()

#         st.divider()
#         st.subheader("⚙️ Options")

#         current_msgs = get_messages(st.session_state.conversation_id)
#         if current_msgs:
#             chat_json = json.dumps(current_msgs, indent=4)
#             st.download_button(
#                 label="📥 Export Current Chat",
#                 data=chat_json,
#                 file_name=f"chat_export_{st.session_state.conversation_id[:8]}.json",
#                 mime="application/json",
#                 use_container_width=True
#             )

#         if st.button("🗑 Delete Current Chat", use_container_width=True):
#             delete_conversation(st.session_state.conversation_id)
#             remaining = get_conversations(st.session_state.user_id)
#             st.session_state.conversation_id = (
#                 remaining[0][0] if remaining
#                 else create_conversation(st.session_state.user_id)
#             )
#             st.rerun()

#     # Main area title
#     st.markdown('<span class="app-title">⚡ PrimeMind</span>', unsafe_allow_html=True)

#     # Chat history
#     chat_history = get_messages(st.session_state.conversation_id)
#     for msg in chat_history:
#         avatar = USER_AVATAR if msg["role"] == "user" else ASSISTANT_AVATAR
#         with st.chat_message(msg["role"], avatar=avatar):
#             st.markdown(msg["content"])

#     user_prompt = st.chat_input("Ask PrimeMind...")

#     if user_prompt:
#         with st.chat_message("user", avatar=USER_AVATAR):
#             st.markdown(user_prompt)

#         save_message(st.session_state.conversation_id, "user", user_prompt)

#         if len(chat_history) == 0:
#             update_title(st.session_state.conversation_id, user_prompt)

#         randomizer = f"(response_variation: {random.randint(1, 999999)})"
#         messages = [
#             SystemMessage(content=SYSTEM_PROMPT),
#             SystemMessage(content=randomizer),
#         ]

#         for msg in chat_history:
#             if msg["role"] == "user":
#                 messages.append(HumanMessage(content=msg["content"]))
#             else:
#                 messages.append(AIMessage(content=msg["content"]))

#         messages.append(HumanMessage(content=user_prompt))

#         try:
#             with st.spinner("PrimeMind is thinking..."):
#                 api_key = os.getenv("GROQ_API_KEY")
#                 if not api_key:
#                     st.error("⚠️ GROQ_API_KEY not found. Please set it in your .env file.")
#                     st.stop()

#                 llm = ChatGroq(
#                     api_key=api_key,
#                     model="llama-3.3-70b-versatile",
#                     temperature=0.7,
#                     model_kwargs={"top_p": 0.9},
#                 )
#                 response = llm.invoke(messages)
#                 assistant_reply = response.content

#             save_message(st.session_state.conversation_id, "assistant", assistant_reply)

#             with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
#                 st.write(assistant_reply)

#         except Exception as e:
#             st.error(f"An error occurred: {e}")

#         expire_conversations(st.session_state.user_id)


# # --------------------------------------------------
# # ROUTER
# # --------------------------------------------------
# if st.session_state.authenticated:
#     show_main_app()
# else:
#     show_auth_screen()









import os
import uuid
import sqlite3
import random
import json
import hashlib
import secrets
import re
import time
import base64
import tempfile
from datetime import datetime, timedelta
from dotenv import load_dotenv
import streamlit as st
from gtts import gTTS
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()

st.set_page_config(page_title="PrimeMind 4.0", layout="centered")

# --------------------------------------------------
# SYSTEM PROMPT
# --------------------------------------------------
SYSTEM_PROMPT = "You are PrimeMind, a helpful AI assistant."

USER_AVATAR = "🧑‍💻"
ASSISTANT_AVATAR = "🤖"

# --------------------------------------------------
# DATABASE
# --------------------------------------------------
DB_NAME = "chatgpt_clone.db"

def get_conn():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        username TEXT UNIQUE,
        email TEXT UNIQUE,
        password_hash TEXT,
        salt TEXT,
        created_at TEXT
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS conversations (
        id TEXT PRIMARY KEY,
        user_id TEXT,
        title TEXT,
        created_at TEXT
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conversation_id TEXT,
        role TEXT,
        content TEXT,
        timestamp TEXT
    )""")

    conn.commit()
    conn.close()

init_db()

# --------------------------------------------------
# AUTH
# --------------------------------------------------
def hash_password(pw, salt=None):
    if not salt:
        salt = secrets.token_hex(16)
    return hashlib.sha256((pw + salt).encode()).hexdigest(), salt

def register_user(username, email, password):
    pw, salt = hash_password(password)
    try:
        conn = get_conn()
        conn.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)",
                     (str(uuid.uuid4()), username, email, pw, salt, datetime.utcnow().isoformat()))
        conn.commit()
        return True
    except:
        return False

def authenticate(username, password):
    conn = get_conn()
    row = conn.execute("SELECT id, password_hash, salt FROM users WHERE username=?", (username,)).fetchone()
    if row:
        uid, pw, salt = row
        if hash_password(password, salt)[0] == pw:
            return True, uid
    return False, None

# --------------------------------------------------
# CHAT DB
# --------------------------------------------------
def create_chat(uid):
    cid = str(uuid.uuid4())
    conn = get_conn()
    conn.execute("INSERT INTO conversations VALUES (?, ?, ?, ?)",
                 (cid, uid, "New chat", datetime.utcnow().isoformat()))
    conn.commit()
    return cid

def get_messages(cid):
    conn = get_conn()
    rows = conn.execute("SELECT role, content FROM messages WHERE conversation_id=?", (cid,))
    return rows.fetchall()

def save_msg(cid, role, content):
    conn = get_conn()
    conn.execute("INSERT INTO messages VALUES (NULL, ?, ?, ?, ?)",
                 (cid, role, content, datetime.utcnow().isoformat()))
    conn.commit()

# --------------------------------------------------
# EFFECTS
# --------------------------------------------------
def typewriter(text, delay=0.01):
    output = ""
    for char in text:
        output += char
        yield output + "▌"
        time.sleep(delay)
    yield output

def typing_indicator(ph):
    for dots in ["", ".", "..", "..."]:
        ph.markdown(f"*PrimeMind is typing{dots}*")
        time.sleep(0.3)

def play_sound(url, loop=False):
    loop_attr = "loop" if loop else ""
    st.markdown(f"""
    <audio autoplay {loop_attr}>
    <source src="{url}" type="audio/mp3">
    </audio>
    """, unsafe_allow_html=True)

def speak(text):
    tts = gTTS(text)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        tts.save(f.name)
        audio = open(f.name, "rb").read()
    b64 = base64.b64encode(audio).decode()
    st.markdown(f"""
    <audio autoplay>
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# SESSION
# --------------------------------------------------
if "auth" not in st.session_state:
    st.session_state.auth = False

# --------------------------------------------------
# AUTH UI
# --------------------------------------------------
if not st.session_state.auth:
    tab1, tab2 = st.tabs(["Login", "Signup"])

    with tab1:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Login"):
            ok, uid = authenticate(u, p)
            if ok:
                st.session_state.auth = True
                st.session_state.uid = uid
                st.session_state.cid = create_chat(uid)
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        u = st.text_input("New Username")
        e = st.text_input("Email")
        p = st.text_input("Password", type="password")
        if st.button("Create Account"):
            if register_user(u, e, p):
                st.success("Account created")
            else:
                st.error("Error")

# --------------------------------------------------
# MAIN APP
# --------------------------------------------------
else:
    st.title("⚡ PrimeMind")

    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()

    msgs = get_messages(st.session_state.cid)

    for role, content in msgs:
        with st.chat_message(role):
            st.markdown(content)

    prompt = st.chat_input("Ask...")

    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)

        save_msg(st.session_state.cid, "user", prompt)

        messages = [SystemMessage(content=SYSTEM_PROMPT)]
        for r, c in msgs:
            if r == "user":
                messages.append(HumanMessage(content=c))
            else:
                messages.append(AIMessage(content=c))
        messages.append(HumanMessage(content=prompt))

        with st.chat_message("assistant"):
            ph = st.empty()

            typing_indicator(ph)

            llm = ChatGroq(
                api_key=os.getenv("GROQ_API_KEY"),
                model="llama-3.3-70b-versatile"
            )

            res = llm.invoke(messages)
            reply = res.content

            # 🔊 start typing sound
            play_sound("https://assets.mixkit.co/active_storage/sfx/2568/2568-preview.mp3", loop=True)

            # 🎙️ voice
            speak(reply)

            for t in typewriter(reply, delay=0.01):
                ph.markdown(t)

            # 🔔 done sound
            play_sound("https://assets.mixkit.co/active_storage/sfx/957/957-preview.mp3")

        save_msg(st.session_state.cid, "assistant", reply)





























































































