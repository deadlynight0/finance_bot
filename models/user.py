from datetime import datetime
from config import DEFAULT_CATEGORIES
import sqlite3

def register_user(user_id, username, first_name, last_name):
    conn = sqlite3.connect('finance_bot.db')
    cursor = conn.cursor()
    registration_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute('INSERT INTO users (user_id, username, first_name, last_name, registration_date) VALUES (?, ?, ?, ?, ?)',
                  (user_id, username, first_name, last_name, registration_date))
    
    for category_type, categories in DEFAULT_CATEGORIES.items():
        for category in categories:
            cursor.execute('INSERT INTO categories (user_id, name, type) VALUES (?, ?, ?)',
                          (user_id, category, category_type))
    
    conn.commit()
    conn.close()