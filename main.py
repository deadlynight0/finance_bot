from handlers.bot import bot
import handlers.registration
import handlers.help
import handlers.transactions
import handlers.goals
import handlers.statistics
from models.database import init_db

if __name__ == '__main__':
    init_db()
    print("Запуск бота...........")
    bot.polling(none_stop=True, interval=1)