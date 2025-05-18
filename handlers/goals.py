from telebot import types
from datetime import datetime
from models.database import is_user_registered
from utils.helpers import get_progress_bar
from handlers.bot import bot
import sqlite3

@bot.message_handler(commands=['set_goal'])
def set_goal(message):
    user_id = message.from_user.id
    if not is_user_registered(user_id):
        bot.send_message(message.chat.id, "Пожалуйста, зарегистрируйтесь с помощью /register.")
        return
    
    try:
        parts = message.text.split(maxsplit=2)
        if len(parts) < 3:
            bot.send_message(message.chat.id, "Неверный формат команды. Используйте: /set_goal [сумма] [описание]")
            return
        
        target_amount = float(parts[1])
        description = parts[2]
        
        if target_amount <= 0:
            bot.send_message(message.chat.id, "Сумма цели должна быть положительной!")
            return
        
        conn = sqlite3.connect('finance_bot.db')
        cursor = conn.cursor()
        created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('INSERT INTO goals (user_id, target_amount, description, created_date) VALUES (?, ?, ?, ?)',
                      (user_id, target_amount, description, created_date))
        conn.commit()
        conn.close()
        
        bot.send_message(message.chat.id, f"Цель '{description}' на сумму {target_amount} руб. успешно установлена!")
    
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат суммы. Используйте число (например: 10000).")

@bot.message_handler(commands=['view_goals'])
def view_goals(message):
    user_id = message.from_user.id
    if not is_user_registered(user_id):
        bot.send_message(message.chat.id, "Пожалуйста, зарегистрируйтесь с помощью /register.")
        return
    
    conn = sqlite3.connect('finance_bot.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT SUM(amount) FROM transactions WHERE user_id = ? AND type = "income"', (user_id,))
    total_income = cursor.fetchone()[0] or 0
    
    cursor.execute('SELECT SUM(amount) FROM transactions WHERE user_id = ? AND type = "expense"', (user_id,))
    total_expense = cursor.fetchone()[0] or 0
    
    current_balance = total_income - total_expense
    
    cursor.execute('SELECT id, target_amount, current_amount, description, created_date, achieved FROM goals WHERE user_id = ? ORDER BY created_date DESC', (user_id,))
    goals = cursor.fetchall()
    conn.close()
    
    if not goals:
        bot.send_message(message.chat.id, "У вас пока нет финансовых целей. Используйте /set_goal, чтобы установить цель.")
        return
    
    message_text = "🎯 Ваши финансовые цели:\n\n"
    message_text += f"Текущий баланс: {current_balance:.2f} руб.\n\n"
    
    for goal in goals:
        goal_id, target_amount, current_amount, description, created_date, achieved = goal
        created_date_obj = datetime.strptime(created_date, '%Y-%m-%d %H:%M:%S')
        formatted_date = created_date_obj.strftime('%d.%m.%Y')
        
        progress = min(current_balance / target_amount * 100, 100) if target_amount > 0 else 0
        progress_bar = get_progress_bar(progress)
        
        status = "✅ Достигнута" if achieved else "⏳ В процессе"
        
        message_text += (
            f"#{goal_id} | {description}\n"
            f"Цель: {target_amount:.2f} руб. | {status}\n"
            f"Дата установки: {formatted_date}\n"
            f"Прогресс: {progress:.1f}%\n"
            f"{progress_bar}\n\n"
        )
    
    bot.send_message(message.chat.id, message_text)