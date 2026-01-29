import spacy
import gensim
from gensim import corpora
from src.db_manager import get_db_connection
import pandas as pd

# Load spaCy for cleaning
nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    """
    LDA needs a list of tokens (words), not a string.
    """
    doc = nlp(text.lower())
    # Keep only alphabetic, non-stop words
    return [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]

def train_lda_model():
    print("⏳ Loading chat logs from database...")
    conn = get_db_connection()
    
    # Fetch all chat logs
    df = pd.read_sql("SELECT id, content FROM chat_logs", conn)
    conn.close()

    if df.empty:
        print("❌ No chat logs found! Chat with your bot first.")
        return

    print(f"📊 Processing {len(df)} chat logs...")

    # 1. Preprocess data (Convert text to list of words)
    processed_docs = df['content'].apply(preprocess_text).tolist()

    # 2. Create Dictionary (Map words to IDs)
    dictionary = corpora.Dictionary(processed_docs)

    # 3. Create Corpus (Bag of Words)
    corpus = [dictionary.doc2bow(text) for text in processed_docs]

    if not corpus:
        print("❌ Not enough valid words to train model.")
        return

    print("🧠 Training Gensim LDA Model...")
    # We ask for 3 topics to start
    lda_model = gensim.models.LdaModel(
        corpus=corpus,
        id2word=dictionary,
        num_topics=3, 
        passes=10,
        random_state=42
    )

    # 4. Print Topics
    print("\n✅ LDA CHAT TOPICS FOUND:")
    for idx, topic in lda_model.print_topics(-1):
        print(f"Topic {idx}: {topic}")
    
    # Save model
    lda_model.save("data/my_lda_model")

if __name__ == "__main__":
    train_lda_model()