import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import os
from openai import OpenAI
from datetime import datetime
import gensim
import spacy

# --- CONFIGURATION ---
st.set_page_config(page_title="Context-Aware Companion", page_icon="🧠", layout="wide")

# 🔑 GROQ API KEY
API_KEY = "PASTE_YOUR_KEY"  # <--- REPLACE WITH YOUR KEY

# Initialize Client
client = None
if API_KEY and API_KEY.startswith("gsk_"):
    try:
        client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=API_KEY)
    except Exception as e:
        st.error(f"Failed to initialize API Client: {e}")

@st.cache_resource
def load_nlp():
    return spacy.load("en_core_web_sm")

nlp = load_nlp()

# --- HELPER FUNCTIONS ---
def get_db_connection():
    db_path = os.path.join("data", "companion.db")
    conn = sqlite3.connect(db_path)
    return conn

def save_chat_log(role, content):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO chat_logs (role, content, timestamp) VALUES (?, ?, ?)", 
                       (role, content, datetime.now()))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error saving chat: {e}")

# --- 🔴 CRITICAL FIX: ROBUST SEARCH ENGINE ---
def find_relevant_context(user_query):
    """
    Searches the ENTIRE database using SQL for fast keyword matching.
    """
    conn = get_db_connection()
    keywords = user_query.lower().split()
    
    conditions = []
    params = []
    
    for word in keywords:
        # Filter out tiny words, but keep short acronyms like "AI" or "JS"
        if len(word) >= 2: 
            # Search in BOTH the cleaned title and the original title
            conditions.append("(cleaned_title LIKE ? OR title LIKE ?)")
            params.append(f"%{word}%")
            params.append(f"%{word}%")
            
    if not conditions:
        conn.close()
        return pd.DataFrame()

    # Combine all conditions with OR (finds any match)
    where_clause = " OR ".join(conditions)
    
    # Limit to top 10 most recent matches
    query = f"""
    SELECT title, visit_time 
    FROM browser_history 
    WHERE {where_clause} 
    ORDER BY visit_time DESC 
    LIMIT 10
    """
    
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df

def load_top_browser_topics():
    conn = get_db_connection()
    query = """
    SELECT topic_id, COUNT(*) as count FROM browser_history 
    WHERE topic_id != -1 GROUP BY topic_id ORDER BY count DESC LIMIT 10
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def load_recent_history():
    conn = get_db_connection()
    query = "SELECT visit_time, title FROM browser_history WHERE topic_id != -1 ORDER BY visit_time DESC LIMIT 10"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def analyze_chat_topics():
    try:
        lda_model = gensim.models.LdaModel.load("data/my_lda_model")
        conn = get_db_connection()
        df = pd.read_sql("SELECT content FROM chat_logs WHERE role='user' ORDER BY timestamp DESC LIMIT 50", conn)
        conn.close()
        
        if df.empty: return pd.DataFrame()

        def preprocess(text):
            doc = nlp(text.lower())
            return [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]

        topic_counts = {}
        for text in df['content']:
            tokens = preprocess(text)
            if not tokens: continue
            bow = lda_model.id2word.doc2bow(tokens)
            topics = lda_model.get_document_topics(bow)
            if topics:
                dominant_topic = max(topics, key=lambda x: x[1])[0]
                topic_counts[dominant_topic] = topic_counts.get(dominant_topic, 0) + 1
        
        return pd.DataFrame(list(topic_counts.items()), columns=['topic_id', 'count'])
    except Exception:
        return pd.DataFrame()

# --- UI LAYOUT ---
st.title("🧠 Smart Context-Aware Study Companion")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 Chat with Context")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask me about your studies..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        save_chat_log("user", prompt)

        # --- FIND CONTEXT ---
        context_df = find_relevant_context(prompt)
        context_text = ""
        
        if not context_df.empty:
            links = [f"- {row['title']}" for index, row in context_df.iterrows()]
            context_text = "\n".join(links)
            st.success(f"🔍 Found {len(links)} relevant items in your history!")
            with st.expander("View Context"):
                st.text(context_text)
        
        system_instruction = f"""
        You are a helpful study companion. 
        User's browsing history related to this question:
        {context_text}
        
        If relevant, use this history to answer. If not, answer generally.
        """
        
        if client:
            with st.chat_message("assistant"):
                try:
                    # --- BUILD MESSAGE HISTORY ---
                    # 1. Start with the System Prompt (The "Context")
                    messages_to_send = [{"role": "system", "content": system_instruction}]
                    
                    # 2. Add the last 5 messages from conversation history (Short-term memory)
                    # We limit to 5 to keep it fast and not waste tokens
                    for msg in st.session_state.messages[-5:]:
                        messages_to_send.append({"role": msg["role"], "content": msg["content"]})

                    # 3. Send the full conversation to Groq
                    stream = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=messages_to_send,
                        stream=True,
                    )
                    response = st.write_stream(stream)
                except Exception as e:
                    st.warning(f"⚠️ API Error: {e}")
                    response = "I couldn't connect to the brain right now. (Check API Key)"
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            save_chat_log("assistant", response)
        else:
            st.error("⚠️ No API Key found.")

with col2:
    st.subheader("📊 Your Knowledge Graph")
    try:
        browser_topics = load_top_browser_topics()
        if not browser_topics.empty:
            fig1 = px.bar(browser_topics, x='topic_id', y='count', title="Browsing Interests")
            st.plotly_chart(fig1, use_container_width=True)
    except: pass

    try:
        chat_topics = analyze_chat_topics()
        if not chat_topics.empty:
            chat_topics['Topic Name'] = chat_topics['topic_id'].apply(lambda x: f"Topic {x}")
            fig2 = px.pie(chat_topics, values='count', names='Topic Name', title="Chat Themes")
            st.plotly_chart(fig2, use_container_width=True)
    except: pass

    st.subheader("🕒 Recent History")
    try:
        recent = load_recent_history()
        if not recent.empty:
            st.dataframe(recent[['visit_time', 'title']], hide_index=True)
    except: pass