import sqlite3
import os

# Define path to database
DB_PATH = os.path.join("data","companion.db")

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn 

def init_db():
    """Create the necessary table if they don't exist"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create Browser History Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS browser_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            visit_time TIMESTAMP,
            url TEXT,
            title TEXT,
            cleaned_title TEXT, 
            topic_id INTEGER DEFAULT -1
        )
    ''')       
    
    # Create Chat Logs Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TIMESTAMP,
            role TEXT,
            content TEXT,
            topic_id INTEGER DEFAULT -1
        )
    ''') 
    
    conn.commit()
    conn.close()
    print(f"Database intialized successfully at: {DB_PATH}")

# --- THIS PART IS CRITICAL --- 
if __name__ == "__main__":
    # Create the 'data' folder if it doesn't exist 
    if not os.path.exists("data"):
        os.makedirs("data")  
    
    
    #Run the Function 
    init_db()   