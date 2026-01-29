from src.db_manager import get_db_connection
from datetime import datetime

def inject_dummy_chats():
    print("💉 Injecting dummy chat logs into database...")
    conn = get_db_connection()
    cursor = conn.cursor()

    # A mix of Python, Biology, and History questions
    dummy_data = [
        ("user", "How do I fix a list index out of range error in Python?", datetime.now()),
        ("user", "What is the difference between a list and a tuple in Python?", datetime.now()),
        ("user", "Explain the function of the mitochondria in the cell.", datetime.now()),
        ("user", "Who was the first emperor of Rome?", datetime.now()),
        ("user", "Show me code to loop through a dictionary in Python.", datetime.now()),
        ("user", "What are the stages of mitosis in biology?", datetime.now()),
        ("user", "Why did the Roman Empire fall?", datetime.now()),
        ("user", "How do I install pandas using pip?", datetime.now())
    ]

    cursor.executemany('''
        INSERT INTO chat_logs (role, content, timestamp) 
        VALUES (?, ?, ?)
    ''', dummy_data)

    conn.commit()
    conn.close()
    print(f"✅ Successfully added {len(dummy_data)} chat logs.")

if __name__ == "__main__":
    inject_dummy_chats()