from telebot import types
from datetime import datetime
from models.database import is_user_registered, save_transaction, is_valid_category
from utils.helpers import get_period_dates
from handlers.bot import bot
import sqlite3

def process_income_category(message, amount):
    category = message.text
    user_id = message.from_user.id
    
    if is_valid_category(user_id, category, 'income'):
        save_transaction(user_id, amount, category, 'income')
        bot.send_message(message.chat.id, f"Доход в размере {amount} руб. по категории '{category}' успешно добавлен.")
    else:
        bot.send_message(message.chat.id, "Неверная категория. Пожалуйста, попробуйте снова.")

def process_expense_category(message, amount):
    category = message.text
    user_id = message.from_user.id
    
    if is_valid_category(user_id, category, 'expense'):
        save_transaction(user_id, amount, category, 'expense')
        bot.send_message(message.chat.id, f"Расход в размере {amount} руб. по категории '{category}' успешно добавлен.")
    else:
        bot.send_message(message.chat.id, "Неверная категория. Пожалуйста, попробуйте снова.")

@bot.message_handler(commands=['add_income'])
def add_income(message):
    user_id = message.from_user.id
    if not is_user_registered(user_id):
        bot.send_message(message.chat.id, "Пожалуйста, зарегистрируйтесь с помощью /register.")
        return
    
    try:
        command, amount, *category_parts = message.text.split()
        category = ' '.join(category_parts) if category_parts else None
        
        amount = float(amount)
        if amount <= 0:
            bot.send_message(message.chat.id, "Сумма должна быть положительной!")
            return
        
        if not category:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            conn = sqlite3.connect('finance_bot.db')
            cursor = conn.cursor()
            cursor.execute('SELECT name FROM categories WHERE user_id = ? AND type = "income"', (user_id,))
            categories = cursor.fetchall()
            conn.close()
            
            for cat in categories:
                markup.add(types.KeyboardButton(cat[0]))
            
            msg = bot.send_message(message.chat.id, "Выберите категорию дохода:", reply_markup=markup)
            bot.register_next_step_handler(msg, process_income_category, amount)
        else:
            save_transaction(user_id, amount, category, 'income')
            bot.send_message(message.chat.id, f"Доход в размере {amount} руб. по категории '{category}' успешно добавлен.")
    
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат команды. Используйте: /add_income [сумма] [категория]")

@bot.message_handler(commands=['add_expense'])
def add_expense(message):
    user_id = message.from_user.id
    if not is_user_registered(user_id):
        bot.send_message(message.chat.id, "Пожалуйста, зарегистрируйтесь с помощью /register.")
        return
    
    try:
        command, amount, *category_parts = message.text.split()
        category = ' '.join(category_parts) if category_parts else None
        
        amount = float(amount)
        if amount <= 0:
            bot.send_message(message.chat.id, "Сумма должна быть положительной!")
            return
        
        if not category:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            conn = sqlite3.connect('finance_bot.db')
            cursor = conn.cursor()
            cursor.execute('SELECT name FROM categories WHERE user_id = ? AND type = "expense"', (user_id,))
            categories = cursor.fetchall()
            conn.close()
            
            for cat in categories:
                markup.add(types.KeyboardButton(cat[0]))
            
            msg = bot.send_message(message.chat.id, "Выберите категорию расхода:", reply_markup=markup)
            bot.register_next_step_handler(msg, process_expense_category, amount)
        else:
            save_transaction(user_id, amount, category, 'expense')
            bot.send_message(message.chat.id, f"Расход в размере {amount} руб. по категории '{category}' успешно добавлен.")
    
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат команды. Используйте: /add_expense [сумма] [категория]")

def process_period_selection(message):
    user_id = message.from_user.id
    period = message.text
    show_transactions(user_id, period, None, message.chat.id)

def show_transactions(user_id, period, category, chat_id):
    conn = sqlite3.connect('finance_bot.db')
    cursor = conn.cursor()
    
    start_date = get_period_dates(period)
    
    query = 'SELECT date, type, category, amount, description FROM transactions WHERE user_id = ?'
    params = [user_id]
    
    if start_date:
        query += ' AND date >= ?'
        params.append(start_date.strftime('%Y-%m-%d %H:%M:%S'))
    
    if category:
        query += ' AND category = ?'
        params.append(category)
    
    query += ' ORDER BY date DESC'
    
    cursor.execute(query, tuple(params))
    transactions = cursor.fetchall()
    conn.close()
    
    if not transactions:
        bot.send_message(chat_id, f"Нет транзакций за указанный период{'' if not category else f' по категории {category}'}.")
        return
    
    total_income = 0
    total_expense = 0
    message_text = f"📋 Транзакции за {period}{'' if not category else f' (категория: {category})'}:\n\n"
    
    for trans in transactions:
        date, trans_type, trans_category, amount, description = trans
        date_obj = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        formatted_date = date_obj.strftime('%d.%m.%Y %H:%M')
        
        if trans_type == 'income':
            total_income += amount
            message_text += f"📈 {formatted_date} | {trans_category} | +{amount:.2f} руб."
        else:
            total_expense += amount
            message_text += f"📉 {formatted_date} | {trans_category} | -{amount:.2f} руб."
        
        if description:
            message_text += f" | {description}"
        
        message_text += "\n"
    
    message_text += f"\nИтого доходов: +{total_income:.2f} руб.\n"
    message_text += f"Итого расходов: -{total_expense:.2f} руб.\n"
    message_text += f"Баланс: {total_income - total_expense:.2f} руб."
    
    if len(message_text) > 4000:
        parts = [message_text[i:i+4000] for i in range(0, len(message_text), 4000)]
        for part in parts:
            bot.send_message(chat_id, part)
    else:
        bot.send_message(chat_id, message_text)

@bot.message_handler(commands=['view_transactions'])
def view_transactions(message):
    user_id = message.from_user.id
    if not is_user_registered(user_id):
        bot.send_message(message.chat.id, "Пожалуйста, зарегистрируйтесь с помощью /register.")
        return
    
    try:
        parts = message.text.split()
        if len(parts) == 1:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            periods = ['день', 'неделя', 'месяц', 'год', 'все']
            for period in periods:
                markup.add(types.KeyboardButton(period))
            
            msg = bot.send_message(message.chat.id, "Выберите период:", reply_markup=markup)
            bot.register_next_step_handler(msg, process_period_selection)
        elif len(parts) == 2:
            period = parts[1]
            show_transactions(user_id, period, None, message.chat.id)
        elif len(parts) >= 3:
            period = parts[1]
            category = ' '.join(parts[2:])
            show_transactions(user_id, period, category, message.chat.id)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {str(e)}")