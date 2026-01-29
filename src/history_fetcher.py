import spacy
from browser_history import get_history
from src.db_manager import get_db_connection, init_db
import re


#load spaCy model
print(" loading spaCy model")
nlp = spacy.load("en_core_web_sm")

def clean_text(text):
    
    """uses spacy to clean browser titles """
    if not text:
        return ""
    
    #1. Basic cleanup 
    text = re.sub(r'[\-|:]', ' ', text)
    
    #2. spacy processing 
    doc = nlp(text.lower())
    
    #3. keep only alphabetic words, remove stop words, use lemmas
    tokens = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop ]
    
    return  " ".join(tokens)

def fetch_and_store_history():
    
    """Fetches history from browser and save new entries to sqlite."""
    print("scanning browser history...")
    try:
        # this gets your 73,000 items again
        history_data = get_history().histories
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        count=0
        print(f"Found {len(history_data)} items. Processing & saving...")
        
        for date, url, title in history_data:
            if not title:
                continue
            
            #clean the title 
            clean_t = clean_text(title)
            
            # save to DB
            cursor.execute('''
                           INSERT INTO browser_history(visit_time, url, title, cleaned_title)
                           VALUES (?,?,?,?)''',(date, url, title, clean_t))
            count += 1
            
            # show progress
            if count % 100 == 0:
                print(f" Saved{count} items...", end = "\r")
        
        conn.commit()
        conn.close()
        print(f"\n Success! Saved {count} history items to the database")        

    except Exception as e:
        print(f"Error:{e}")

if __name__=="__main__":
    init_db()
    fetch_and_store_history()        
    
              
            