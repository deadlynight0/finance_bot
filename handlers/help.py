from handlers.bot import bot

@bot.message_handler(commands=['help'])
def help(message):
    help_text = """
📌 Доступные команды:
/start - Начало работы с ботом
/register - Регистрация нового пользователя
/help - Список команд

💰 Управление финансами:
/add_income [сумма] [категория] - Добавить доход
/add_expense [сумма] [категория] - Добавить расход
/view_transactions [период] [категория] - Просмотр транзакций
/statistics - Просмотр статистики

🎯 Финансовые цели:
/set_goal [сумма] [описание] - Установить финансовую цель
/view_goals - Просмотр текущих целей
"""

    bot.send_message(message.chat.id, help_text)