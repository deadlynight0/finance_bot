import io
import matplotlib.pyplot as plt
from telebot import types
from datetime import datetime
from models.database import is_user_registered
from utils.helpers import get_period_dates
from handlers.bot import bot
import sqlite3

def process_statistics_period(message):
    user_id = message.from_user.id
    period = message.text
    show_statistics(user_id, period, message.chat.id)

def show_statistics(user_id, period, chat_id):
    conn = sqlite3.connect('finance_bot.db')
    cursor = conn.cursor()
    
    start_date = get_period_dates(period)
    
    income_query = 'SELECT SUM(amount) FROM transactions WHERE user_id = ? AND type = "income"'
    expense_query = 'SELECT SUM(amount) FROM transactions WHERE user_id = ? AND type = "expense"'
    params = [user_id]
    
    if start_date:
        income_query += ' AND date >= ?'
        expense_query += ' AND date >= ?'
        params.append(start_date.strftime('%Y-%m-%d %H:%M:%S'))
    
    cursor.execute(income_query, tuple(params))
    total_income = cursor.fetchone()[0] or 0
    
    cursor.execute(expense_query, tuple(params))
    total_expense = cursor.fetchone()[0] or 0
    
    balance = total_income - total_expense
    
    income_cats_query = 'SELECT category, SUM(amount) FROM transactions WHERE user_id = ? AND type = "income"'
    if start_date:
        income_cats_query += ' AND date >= ?'
    income_cats_query += ' GROUP BY category ORDER BY SUM(amount) DESC'
    
    cursor.execute(income_cats_query, tuple(params))
    income_categories = cursor.fetchall()
    
    expense_cats_query = 'SELECT category, SUM(amount) FROM transactions WHERE user_id = ? AND type = "expense"'
    if start_date:
        expense_cats_query += ' AND date >= ?'
    expense_cats_query += ' GROUP BY category ORDER BY SUM(amount) DESC'
    
    cursor.execute(expense_cats_query, tuple(params))
    expense_categories = cursor.fetchall()
    
    conn.close()
    
    message_text = f"📊 Статистика за {period}:\n\n"
    message_text += f"Общий доход: {total_income:.2f} руб.\n"
    message_text += f"Общий расход: {total_expense:.2f} руб.\n"
    message_text += f"Баланс: {balance:.2f} руб.\n\n"
    
    if income_categories:
        message_text += "📈 Доходы по категориям:\n"
        for cat, amount in income_categories:
            percentage = (amount / total_income * 100) if total_income > 0 else 0
            message_text += f"- {cat}: {amount:.2f} руб. ({percentage:.1f}%)\n"
        message_text += "\n"
    
    if expense_categories:
        message_text += "📉 Расходы по категориям:\n"
        for cat, amount in expense_categories:
            percentage = (amount / total_expense * 100) if total_expense > 0 else 0
            message_text += f"- {cat}: {amount:.2f} руб. ({percentage:.1f}%)\n"
    
    create_and_send_charts(chat_id, income_categories, expense_categories, total_income, total_expense)
    bot.send_message(chat_id, message_text)

def create_and_send_charts(chat_id, income_categories, expense_categories, total_income, total_expense):
    if income_categories:
        labels = [cat[0] for cat in income_categories]
        sizes = [cat[1] for cat in income_categories]
        
        plt.figure(figsize=(10, 6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.title('Доходы по категориям')
        plt.axis('equal')
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        bot.send_photo(chat_id, buf)
        plt.close()
        buf.close()
    
    if expense_categories:
        labels = [cat[0] for cat in expense_categories]
        sizes = [cat[1] for cat in expense_categories]
        
        plt.figure(figsize=(10, 6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.title('Расходы по категориям')
        plt.axis('equal')
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        bot.send_photo(chat_id, buf)
        plt.close()
        buf.close()
    
    if total_income > 0 or total_expense > 0:
        labels = ['Доходы', 'Расходы']
        sizes = [total_income, total_expense]
        
        plt.figure(figsize=(10, 6))
        plt.bar(labels, sizes, color=['green', 'red'])
        plt.title('Доходы vs Расходы')
        plt.ylabel('Сумма (руб.)')
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        bot.send_photo(chat_id, buf)
        plt.close()
        buf.close()

@bot.message_handler(commands=['statistics'])
def statistics(message):
    user_id = message.from_user.id
    if not is_user_registered(user_id):
        bot.send_message(message.chat.id, "Пожалуйста, зарегистрируйтесь с помощью /register.")
        return
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    periods = ['день', 'неделя', 'месяц', 'год', 'все']
    for period in periods:
        markup.add(types.KeyboardButton(period))
    
    msg = bot.send_message(message.chat.id, "Выберите период для статистики:", reply_markup=markup)
    bot.register_next_step_handler(msg, process_statistics_period)