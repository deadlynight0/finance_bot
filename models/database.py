import sqlite3
from datetime import datetime


def init_db():
    conn = sqlite3.connect('finance_bot.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        last_name TEXT,
        registration_date TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount REAL,
        category TEXT,
        type TEXT,
        date TEXT,
        description TEXT,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        target_amount REAL,
        current_amount REAL DEFAULT 0,
        description TEXT,
        created_date TEXT,
        achieved INTEGER DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT,
        type TEXT,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    ''')
    
    conn.commit()
    conn.close()

def is_user_registered(user_id):
    conn = sqlite3.connect('finance_bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user is not None

def save_transaction(user_id, amount, category, trans_type, description=None):
    conn = sqlite3.connect('finance_bot.db')
    cursor = conn.cursor()
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute('INSERT INTO transactions (user_id, amount, category, type, date, description) VALUES (?, ?, ?, ?, ?, ?)',
                  (user_id, amount, category, trans_type, date, description))
    
    if trans_type == 'expense':
        update_goals_progress(user_id)
    
    conn.commit()
    conn.close()

def update_goals_progress(user_id):
    conn = sqlite3.connect('finance_bot.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    UPDATE goals 
    SET current_amount = (
        SELECT SUM(amount) 
        FROM transactions 
        WHERE user_id = ? AND type = 'income'
    ) - (
        SELECT SUM(amount) 
        FROM transactions 
        WHERE user_id = ? AND type = 'expense'
    )
    WHERE user_id = ? AND achieved = 0
    ''', (user_id, user_id, user_id))
    
    cursor.execute('''
    UPDATE goals 
    SET achieved = 1 
    WHERE user_id = ? AND current_amount >= target_amount AND achieved = 0
    ''', (user_id,))
    
    conn.commit()
    conn.close()

def is_valid_category(user_id, category, cat_type):
    conn = sqlite3.connect('finance_bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM categories WHERE user_id = ? AND name = ? AND type = ?', 
                  (user_id, category, cat_type))
    result = cursor.fetchone()
    conn.close()
    return result is not None