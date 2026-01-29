from bertopic import BERTopic
from src.db_manager import get_db_connection
import pandas as pd
import os

# critical for windows: prevents "freeze_support" crashes
os.environ["TOKENIZERS_PARALLELISM"] = "false" 

def train_and_save_topics():
    print("loading data from database...")
    conn = get_db_connection()
    
    query = "SELECT id, cleaned_title FROM browser_history WHERE cleaned_title != '' LIMIT 1000"
    df = pd.read_sql(query, conn)
    conn.close()
    
    print(f" loaded {len(df)} items.Initializing AI Model...")
    
    if len(df) < 50:
        print("Not enough data! Run history_fetcher.py first.")
        
    # Initialize BERTopic
    # min_topic_size=15: A topic needs 15 related items to count
    print("Train BERTopic...(This might take 2-5 minutes)")
    topic_model = BERTopic(language = "english", min_topic_size = 15, verbose=True)
    
    # this finds the topics
    topics, prob = topic_model.fit_transform(df['cleaned_title'])
    
    # Print the top topics found
    print("\n TOPICS FOUND:")
    print(topic_model.get_topic_info().head(10))
    
    # --- SAVE RESULTS TO DB ---
    print("Saving topics IDs back to database...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # prepare data for batch update 
    data_to_update = []
    for index, row in df.iterrows():
        topic_id = int(topics[index])
        db_id = int(row['id'])
        data_to_update.append((topic_id, db_id))
        
    # Batch update the databse
    cursor.executemany("UPDATE browser_history SET topic_id = ? where id = ?", data_to_update) 
    
    conn.commit()
    conn.close()
    
    # Save the model file so the App can use it later
    topic_model.save("data/my_Topic_model")
    print(" Success! Your companion has organized your history.")   

if __name__ == "__main__":
    train_and_save_topics()    