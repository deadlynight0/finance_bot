from telebot import types
from models.database import is_user_registered
from models.user import register_user
from handlers.bot import bot

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    
    if is_user_registered(user_id):
        bot.send_message(message.chat.id, 
                         f"Привет, {message.from_user.first_name}!\n"
                         "Я бот для управления личными финансами.\n"
                         "Используй /help для списка команд.")
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_reg = types.KeyboardButton('/register')
        markup.add(btn_reg)
        
        bot.send_message(message.chat.id, 
                         f"Привет, {message.from_user.first_name}!\n"
                         "Я бот для управления личными финансами.\n"
                         "Пожалуйста, зарегистрируйся с помощью команды /register.", 
                         reply_markup=markup)

@bot.message_handler(commands=['register'])
def register(message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    
    if is_user_registered(user_id):
        bot.send_message(message.chat.id, "Вы уже зарегистрированы!")
    else:
        register_user(user_id, username, first_name, last_name)
        bot.send_message(message.chat.id, 
                         "Регистрация прошла успешно!\n"
                         "Теперь вы можете добавлять доходы и расходы, устанавливать цели и просматривать статистику.\n"
                         "Используйте /help для списка команд.")