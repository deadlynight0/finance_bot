Функциональные требования

Основные

Регистрация и авторизация пользователей - бот должен поддерживать регистрацию и авторизацию пользователей с использованием их Telegram-аккаунтов.

Связывать пользователя с его Telegram-аккаунтом, чтобы все данные были уникально ассоциированы с одним пользователем.
Гарантировать, что каждый пользователь имеет собственный набор финансовых данных, не пересекающийся с другими.
Ввод и категоризация расходов и доходов - пользователи могут вводить информацию о своих расходах и доходах, а также категоризировать их (например, еда, транспорт, здоровье).

Команды для добавления записей:
/add_income [сумма] [категория] – Добавить доход (пример: /add_income 50000 зарплата).
/add_expense [сумма] [категория] – Добавить расход (пример: /add_expense 2500 еда).
При добавлении операций:
Проверять корректность входных данных (числовые значения, существование категории).
Если категория не указана (например, для дохода), использовать категорию по умолчанию или запрашивать уточнение.
Возможность расширять список категорий, если это предусмотрено, или вести закрытый список.
Все операции записываются в базу данных с привязкой к пользователю, датой и временем записи, категорией и суммой.
Просмотр истории транзакций - бот должен предоставлять возможность просмотра истории транзакций по категориям и периодам.

Команда /view_transactions [период] – Отображение транзакций за указанный период.
Период может быть предопределён (например, «день», «неделя», «месяц», «год») или может быть задан конкретными датами (если реализуется такой функционал).
Возможность фильтрации по категории:
Например, /view_transactions месяц еда – показать все транзакции по категории «еда» за текущий месяц.
Вывод итогов за период: общая сумма доходов, общая сумма расходов, чистый баланс за период.
При отсутствии транзакций за запрошенный период или категорию – вывод соответствующего сообщения.
Установка и отслеживание финансовых целей - пользователи могут устанавливать финансовые цели (например, накопить определенную сумму) и отслеживать их достижение.

Команда /set_goal [сумма] [описание] – Установка цели.
Пример: /set_goal 100000 "Скопить на отпуск".
Хранить цели в базе данных: целевая сумма, описание, дата установки.
Рассчитывать прогресс:
Если цель – накопить сумму, отслеживать разницу между суммой доходов минус расходов и целевым значением.
Как только накопления достигнут или превысят цель, бот должен уведомить пользователя о достижении цели.
Возможность просмотра текущих целей и прогресса:
Например, через команду /statistics или отдельную команду (если потребуется).
Предоставление статистики и аналитики - бот должен анализировать финансовую активность пользователя и предоставлять отчеты и графики по расходам, доходам и прогрессу в достижении целей.

Общий доход за период:

Сумма всех добавленных доходов за выбранный период.

Общий расход за период:

Сумма всех добавленных расходов за выбранный период.

Чистый баланс за период:

Разница между общим доходом и общим расходом, позволяющая оценить, был ли период прибыльным или убыточным.

Структура расходов и доходов по категориям:

Список категорий с указанием суммы расходов и/или доходов в каждой категории за выбранный период.

Пример представления:

Еда: 30% от общих расходов, сумма X
Транспорт: 20% от общих расходов, сумма Y
Здоровье: 10% от общих расходов, сумма Z… и так далее.
Для доходов аналогично:

Зарплата: A% от общего дохода, сумма A1
Дополнительный доход: B% от общего дохода, сумма B1
Это позволит пользователю понять, на какие категории приходится наибольшая доля его расходов и доходов.

Тренды расходов и доходов по периодам:

Возможность увидеть, как изменялись расходы и доходы по неделям или месяцам. Например, сравнение текущего месяца с предыдущим:

Расходы в прошлом месяце: X
Расходы в текущем месяце: YИзменение: (Y - X) и процентное соотношение разницы.
Графическое представление (опционально):

Отправка изображений с графиками (столбчатые диаграммы, круговые диаграммы, линейные графики) для визуализации динамики расходов, доходов или соотношения категорий. Если графики невозможны, предоставить текстовые сводки с процентными изменениями.

Прогресс по установленным целям:

Для каждой финансовой цели (например, накопить определённую сумму), бот должен предоставить:

Текущую накопленную сумму.
Процент достижения цели (текущая сумма / целевая сумма * 100%).
Прогнозируемый срок достижения цели (опционально, если можно оценить средний темп накоплений).
Уведомление о достижении цели:

Если цель достигнута (текущие накопления ≥ целевой суммы), предоставить об этом информацию в отчёте или отдельном уведомлении.

Определение «самых затратных» категорий за период:

Выделить TOP-N категорий по расходам или доходам, чтобы пользователь мог сфокусироваться на наиболее значимых для него областях.

Сравнение категорий с предыдущим периодом:

Анализ изменений в затратах по конкретной категории:

Например, в прошлый месяц на «Еду» ушло X рублей, в этот месяц Y рублей. В статистике можно отразить изменение и процентный рост или снижение.
Примечание
Возможность указать период, за который необходима аналитика. По умолчанию — текущий месяц, но пользователь может запросить статистику за любую дату или период.
Возможность получить как краткий обзор (общие суммы по доходам и расходам, баланс), так и подробный отчёт (разбивка по категориям, динамика, достижения целей).
Интерфейс бота
/start - Приветственное сообщение и краткая инструкция по использованию бота.
/register - Регистрация нового пользователя в системе.
/login - Авторизация пользователя для доступа к его данным.
/add_income [сумма] [категория] - Добавление дохода с указанием суммы и категории.
/add_expense [сумма] [категория] - Добавление расхода с указанием суммы и категории.
/set_goal [сумма] [описание] - Установка финансовой цели с указанием суммы и описания.
/view_transactions [период] - Просмотр истории транзакций за указанный период.
/statistics - Просмотр статистики по расходам и доходам, а также прогрессу в достижении финансовых целей.
/help - Список доступных команд и описание их использования.
Технические требования:

Язык программирования: Python 3.

Библиотека для работы с Telegram API: Telebot

База данных: SQLite3 для хранения информации о мероприятиях, участниках и их статусах подтверждения.
