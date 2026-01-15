# Smart-context-aware-NLP-model-using-RAG
A local-first AI study companion that uses RAG, BERTopic, and Browser History to provide context-aware tutoring. Powered by Llama 3 &amp; Streamlit.
Smart-context-aware-NLP-model-using-RAG is an intelligent study assistant that solves "LLM Amnesia." unlike standard ChatGPT, Cortex reads your local browser history and chat logs to understand what you are studying, providing personalized, context-aware answers using RAG (Retrieval-Augmented Generation).



Key Features
Unified Memory: Mines local Chrome/Edge history using browser-history.

Smart Clustering: Uses BERTopic to cluster browsing history into study subjects (e.g., "Python", "Roman History").

Conversation Analysis: Uses Gensim LDA to track conversation themes over time.

RAG Engine: Uses TF-IDF & Cosine Similarity to retrieve relevant history for every query.

Privacy-First: All data is stored locally in SQLite. No history is uploaded to the cloud.

Tech Stack
UI: Streamlit

Database: SQLite

NLP: spaCy, BERTopic, Gensim, Scikit-Learn

LLM Inference: Groq API (Llama 3.1 8B)

Installation
Clone the repo

git clone https://github.com/yourusername/cortex-rag.git
cd Smart-context-aware-NLP-model-using-RAG
Install dependencies

pip install -r requirements.txt
python -m spacy download en_core_web_sm
Set up API Key Open app.py and add your Groq API Key (or set it in .env).

Run the Pipeline

# 1. Initialize DB
python src/db_manager.py
# 2. Fetch History
python -m src.history_fetcher
# 3. Train Topic Model
python -m src.topic_modeler
# 4. Launch App
streamlit run app.py
