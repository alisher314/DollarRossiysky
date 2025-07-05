import telebot # Импортируем библиотеку PyTelegramBotAPI для создания бота
from telebot import types # Импортируем модуль types из telebot для работы с типами объектов Telegram (например, клавиатурами)
import requests # Импортируем библиотеку requests для выполнения HTTP-запросов (получения данных из интернета)
import math # Импортируем модуль math для математических операций, таких как округление

# Вспомогательная функция для проверки, является ли строка целым числом
def is_int(value):
    try:
        int(value) # Пытаемся преобразовать значение в целое число (int)
        return True # Если преобразование успешно, возвращаем True
    except ValueError: # Если возникает ошибка ValueError (значение не может быть преобразовано)
        return False # Возвращаем False

# Вспомогательная функция для округления суммы вверх до ближайших 50 000
def round_up_to_hundred_thousand(value): # Название функции сохранено, но логика изменена на округление до 50 000
    return math.ceil(value / 50000) * 50000 # Округляем вверх до ближайших 50 000

# Вспомогательная функция для округления суммы вниз до ближайших 50 000
def round_down_to_hundred_thousand(value): # Название функции сохранено, но логика изменена на округление до 50 000
    return math.floor(value / 50000) * 50000 # Округляем вниз до ближайших 50 000


# Функция для получения курса валюты от Центрального Банка Узбекистана
def get_cb_rate(currency_code='USD'): # Определяем функцию, которая принимает код валюты (по умолчанию 'USD')
    url = 'https://cbu.uz/ru/arkhiv-kursov-valyut/json/' # URL-адрес API Центрального Банка Узбекистана для получения курсов валют в формате JSON
    try:
        response = requests.get(url, timeout=5) # Отправляем GET-запрос по указанному URL и получаем ответ с таймаутом 5 секунд
        response.raise_for_status() # Проверяем, был ли HTTP-запрос успешным (статус 2xx)
        data = response.json() # Парсим JSON-ответ в Python-объект (список словарей)

        for item in data: # Перебираем каждый элемент (словарь) в полученных данных
            if item['Ccy'] == currency_code: # Если код валюты (Ccy) текущего элемента совпадает с искомым
                # Возвращаем курс валюты (Rate), сначала преобразованный в float для обработки десятичных знаков,
                # а затем в int, отбрасывая дробную часть.
                return int(float(item['Rate']))

        return None  # Если валюта с указанным кодом не найдена, возвращаем None
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API ЦБ: {e}") # Выводим ошибку в консоль
        return None # В случае ошибки запроса возвращаем None
    except ValueError as e:
        print(f"Ошибка при парсинге JSON или преобразовании курса: {e}") # Выводим ошибку в консоль
        return None # В случае ошибки парсинга или преобразования возвращаем None


# Функция для создания главного меню с выбором валюты
def main_menu():
    # Создаем пространство для клавиатуры (ReplyKeyboardMarkup - клавиатура, которая заменяет стандартную)
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True) # resize_keyboard=True делает кнопки автоматически подстраивающимися под размер экрана
    # Создаем сами кнопки
    button1 = types.KeyboardButton('Dollar') # Создаем кнопку с текстом 'Dollar'
    button2 = types.KeyboardButton('Rossiyskiy') # Создаем кнопку с текстом 'Rossiyskiy'
    # Добавляем кнопки в пространство клавиатуры
    kb.add(button1, button2) # Добавляем обе кнопки в клавиатуру

    return kb # Возвращаем объект клавиатуры


# Функция для создания кнопок "Купить" и "Продать"
def olish_sotish():
    # Создаем пространство для клавиатуры
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True) # resize_keyboard=True делает кнопки автоматически подстраивающимися под размер экрана
    # Создаем сами кнопки
    button1 = types.KeyboardButton('Olish') # Создаем кнопку с текстом 'Olish' (Купить)
    button2 = types.KeyboardButton('Sotish') # Создаем кнопку с текстом 'Sotish' (Продать)
    # Добавляем кнопки в пространство клавиатуры
    kb.add(button1, button2) # Добавляем обе кнопки в клавиатуру
    return kb  # Обязательно возвращаем объект клавиатуры!

# НОВАЯ ФУНКЦИЯ: Создание кнопок "Ha" и "Yoq"
def ha_yoq_buttons():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True) # Создаем пространство для клавиатуры
    button_ha = types.KeyboardButton('Ha') # Создаем кнопку с текстом 'Ha' (Да)
    button_yoq = types.KeyboardButton('Yoq') # Создаем кнопку с текстом 'Yoq' (Нет)
    kb.add(button_ha, button_yoq) # Добавляем обе кнопки в клавиатуру
    return kb # Возвращаем объект клавиатуры


# Создаем объект бота
bot = telebot.TeleBot('****') # Инициализируем бота, передавая ему токен.


# Обработчик команды /start
@bot.message_handler(commands=['start']) # Декоратор, указывающий, что функция start будет обрабатывать команду /start
def start(message): # Определяем функцию start, которая принимает объект сообщения
    user_id = message.from_user.id # Получаем ID пользователя, отправившего команду
    bot.send_message(user_id, 'Dollar Rossiyskiy!?', reply_markup=main_menu()) # Отправляем сообщение пользователю с вопросом и прикрепляем главное меню


# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text']) # Декоратор, указывающий, что функция text будет обрабатывать любые текстовые сообщения
def text(message): # Определяем функцию text, которая принимает объект сообщения
    user_id = message.from_user.id # Получаем ID пользователя
    if message.text == 'Dollar': # Если текст сообщения "Dollar"
        bot.send_message(user_id, 'Nime kilish kerak?',reply_markup=olish_sotish()) # Отправляем сообщение "Что нужно сделать?" и прикрепляем кнопки "Купить/Продать"
        # Переход на этап dollar_olish_sotish
        bot.register_next_step_handler(message, dollar_olish_sotish) # Регистрируем следующий шаг: ожидаем ответ пользователя и передаем его функции dollar_olish_sotish
    elif message.text == 'Rossiyskiy': # Если текст сообщения "Rossiyskiy"
        bot.send_message(user_id, 'Nime kilish kerak?',reply_markup=olish_sotish()) # Отправляем сообщение "Что нужно сделать?" и прикрепляем кнопки "Купить/Продать"
        # Переход на этап Rossiyskiy_olish_sotish
        bot.register_next_step_handler(message, Rossiyskiy_olish_sotish) # Регистрируем следующий шаг: ожидаем ответ пользователя и передаем его функции Rossiyskiy_olish_sotish
    else: # Если текст сообщения не "Dollar" и не "Rossiyskiy"
        bot.send_message(user_id, 'Hayer', reply_markup=types.ReplyKeyboardRemove()) # Отправляем сообщение "Нет" (или "Неверный ввод") и убираем клавиатуру


# Функция для обработки выбора "Купить/Продать" для доллара
def dollar_olish_sotish(message):
    user_id = message.from_user.id # Получаем ID пользователя
    kurs = get_cb_rate('USD') # Получаем текущий курс доллара от ЦБ (динамически)

    if kurs is None: # Проверяем, удалось ли получить курс
        bot.send_message(user_id, 'Bugun ishlamiymiz.', reply_markup=types.ReplyKeyboardRemove())
        return # Прерываем выполнение функции, если курс не получен

    if message.text == 'Olish': # Если пользователь выбрал "Olish" (Купить)
        buying_rate = kurs + 500 # Вычисляем курс покупки доллара (курс ЦБ плюс наценка)
        # Отправляем сообщение с курсом доллара и запрашиваем сумму для покупки
        bot.send_message(user_id, f'bugun dollar oshti {buying_rate}sum dan, kancha dollar olasiz?', reply_markup=types.ReplyKeyboardRemove())
        # Регистрируем следующий шаг для обработки введенной суммы долларов при покупке
        bot.register_next_step_handler(message, handle_dollar_olish_amount, buying_rate)
    elif message.text == 'Sotish': # Если пользователь выбрал "Sotish" (Продать)
        selling_rate = kurs - 1000 # Вычисляем курс продажи доллара (курс ЦБ минус наценка)
        # Отправляем сообщение с курсом доллара и запрашиваем сумму для продажи
        bot.send_message(user_id, f'bugun dollar tushti {selling_rate}sum dan, kancha dollar sotasiz?', reply_markup=types.ReplyKeyboardRemove())
        # Регистрируем следующий шаг для обработки введенной суммы долларов при продаже
        bot.register_next_step_handler(message, handle_dollar_sotish_amount, selling_rate)
    else: # Если пользователь ввел что-то другое
        bot.send_message(user_id, 'yoq, Olish va Sotishmi?', reply_markup=types.ReplyKeyboardRemove()) # Отправляем сообщение "Нет" (или "Неверный выбор")


# НОВАЯ ФУНКЦИЯ: Обработчик ответа "Ha" или "Yoq"
def handle_confirmation(message):
    user_id = message.from_user.id # Получаем ID пользователя
    if message.text == 'Ha': # Если пользователь нажал "Ha"
        bot.send_message(user_id, 'Roza buling', reply_markup=types.ReplyKeyboardRemove()) # Отправляем сообщение "Roza buling" и убираем клавиатуру
    elif message.text == 'Yoq': # Если пользователь нажал "Yoq"
        bot.send_message(user_id, 'dosvidaniya', reply_markup=types.ReplyKeyboardRemove()) # Отправляем сообщение "dosvidaniya" и убираем клавиатуру
    else: # Если введен некорректный ответ (не "Ha" и не "Yoq")
        bot.send_message(user_id, '"Ha" va "Yoq" bosing.', reply_markup=ha_yoq_buttons()) # Просим выбрать снова и показываем кнопки
        bot.register_next_step_handler(message, handle_confirmation) # Повторно регистрируем этот же шаг


# Функция для обработки введенной суммы долларов при покупке
def handle_dollar_olish_amount(message, buying_rate):
    user_id = message.from_user.id # Получаем ID пользователя
    user_input = message.text # Получаем текст, введенный пользователем

    if is_int(user_input): # Проверяем, является ли введенный текст целым числом
        amount_dollars = int(user_input) # Преобразуем введенный текст в целое число
        if amount_dollars <= 0: # Проверяем, что сумма положительная
            bot.send_message(user_id, 'yoq, fakat tugri raqam yuzing.', reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, handle_dollar_olish_amount, buying_rate) # Повторно регистрируем этот же шаг
            return

        # Конвертируем сумму долларов в сумы по заявленному курсу
        converted_sum = amount_dollars * buying_rate
        # Округляем в пользу бота (бот продает доллары, значит, получает больше сум, округляем в большую сторону до ближайших 50 000)
        final_sum_for_user = round_up_to_hundred_thousand(converted_sum) # Используем обновленную функцию округления вверх

        # Отправляем финальное сообщение с округленной суммой и прикрепляем кнопки "Ha/Yoq"
        bot.send_message(user_id, f'koro4e {final_sum_for_user} boladi, olasizmi?', reply_markup=ha_yoq_buttons())
        # Регистрируем следующий шаг для обработки ответа "Ha" или "Yoq"
        bot.register_next_step_handler(message, handle_confirmation)
    else: # Если введенный текст не является целым числом
        bot.send_message(user_id, 'yoq, fakat tugri raqam yuzing.', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, handle_dollar_olish_amount, buying_rate) # Повторно регистрируем этот же шаг


# Функция для обработки введенной суммы долларов при продаже
def handle_dollar_sotish_amount(message, selling_rate):
    user_id = message.from_user.id # Получаем ID пользователя
    user_input = message.text # Получаем текст, введенный пользователем

    if is_int(user_input): # Проверяем, можно ли введенный текст преобразовать в целое число
        amount_dollars = int(user_input) # Преобразуем введенный текст в число (сумму долларов)
        if amount_dollars <= 0: # Проверяем, что сумма положительная
            bot.send_message(user_id, 'yoq, fakat tugri raqam yuzing', reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, handle_dollar_sotish_amount, selling_rate) # Повторно регистрируем этот же шаг
            return

        # Конвертируем сумму долларов в сумы по заявленному курсу
        converted_sum = amount_dollars * selling_rate
        # Округляем в пользу бота (бот покупает доллары, значит, платит меньше, округляем в меньшую сторону до ближайших 50 000)
        final_sum_for_user = round_down_to_hundred_thousand(converted_sum) # Используем обновленную функцию округления вниз

        # Отправляем финальное сообщение с округленной суммой и прикрепляем кнопки "Ha/Yoq"
        bot.send_message(user_id, f'koro4e {final_sum_for_user} boladi, olasizmi?', reply_markup=ha_yoq_buttons())
        # Регистрируем следующий шаг для обработки ответа "Ha" или "Yoq"
        bot.register_next_step_handler(message, handle_confirmation)
    else: # Если введенный текст не является числом
        bot.send_message(user_id, 'yoq, fakat tugri raqam yuzing', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, handle_dollar_sotish_amount, selling_rate) # Повторно регистрируем этот же шаг


# Функция для обработки выбора "Купить/Продать" для российского рубля
def Rossiyskiy_olish_sotish(message):
    user_id = message.from_user.id # Получаем ID пользователя
    kurs = get_cb_rate('RUB') # Получаем текущий курс российского рубля от ЦБ (динамически)

    if kurs is None: # Проверяем, удалось ли получить курс
        bot.send_message(user_id, 'Bugun ishlamiymiz', reply_markup=types.ReplyKeyboardRemove())
        return # Прерываем выполнение функции, если курс не получен

    if message.text == 'Olish': # Если пользователь выбрал "Olish" (Купить)
        buying_rate_rubl = kurs + 20 # Вычисляем курс покупки рубля
        # Отправляем сообщение с курсом рубля и запрашиваем сумму для покупки
        bot.send_message(user_id, f'bugun rubl oshti {buying_rate_rubl}sum dan, kancha rubl olasiz?', reply_markup=types.ReplyKeyboardRemove())
        # Регистрируем следующий шаг для обработки введенной суммы рублей при покупке
        bot.register_next_step_handler(message, handle_rubl_olish_amount, buying_rate_rubl)
    elif message.text == 'Sotish': # Если пользователь выбрал "Sotish" (Продать)
        selling_rate_rubl = kurs - 40 # Вычисляем курс продажи рубля
        # Отправляем сообщение с курсом рубля и запрашиваем сумму для продажи
        bot.send_message(user_id, f'bugun rubl tushti{selling_rate_rubl}sum dan, kancha rubl sotasiz?', reply_markup=types.ReplyKeyboardRemove())
        # Регистрируем следующий шаг для обработки введенной суммы рублей при продаже
        bot.register_next_step_handler(message, handle_rubl_sotish_amount, selling_rate_rubl)
    else: # Если пользователь ввел что-то другое
        bot.send_message(user_id, 'yoq, Olish yoki Sotishmi?', reply_markup=types.ReplyKeyboardRemove()) # Отправляем сообщение "Нет" (или "Неверный выбор")


# Функция для обработки введенной суммы рублей при покупке
def handle_rubl_olish_amount(message, buying_rate_rubl):
    user_id = message.from_user.id # Получаем ID пользователя
    user_input = message.text # Получаем текст, введенный пользователем

    if is_int(user_input): # Проверяем, является ли введенный текст целым числом
        amount_rubles = int(user_input) # Преобразуем введенный текст в целое число
        if amount_rubles <= 0: # Проверяем, что сумма положительная
            bot.send_message(user_id, 'yoq, fakat tugri raqam yuzing', reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, handle_rubl_olish_amount, buying_rate_rubl) # Повторно регистрируем этот же шаг
            return

        # Конвертируем сумму рублей в сумы по заявленному курсу
        converted_sum = amount_rubles * buying_rate_rubl
        # Округляем в пользу бота (бот продает рубли, значит, получает больше сум, округляем в большую сторону до ближайших 50 000)
        final_sum_for_user = round_up_to_hundred_thousand(converted_sum) # Используем обновленную функцию округления вверх

        # Отправляем финальное сообщение с округленной суммой и прикрепляем кнопки "Ha/Yoq"
        bot.send_message(user_id, f'koro4e {final_sum_for_user} boladi, olasizmi?', reply_markup=ha_yoq_buttons())
        # Регистрируем следующий шаг для обработки ответа "Ha" или "Yoq"
        bot.register_next_step_handler(message, handle_confirmation)
    else: # Если введенный текст не является целым числом
        bot.send_message(user_id, 'yoq, fakat tugri raqam yuzing', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, handle_rubl_olish_amount, buying_rate_rubl) # Повторно регистрируем этот же шаг


# Функция для обработки введенной суммы рублей при продаже
def handle_rubl_sotish_amount(message, selling_rate_rubl):
    user_id = message.from_user.id # Получаем ID пользователя
    user_input = message.text # Получаем текст, введенный пользователем

    if is_int(user_input): # Проверяем, является ли введенный текст целым числом
        amount_rubles = int(user_input) # Преобразуем введенный текст в целое число
        if amount_rubles <= 0: # Проверяем, что сумма положительная
            bot.send_message(user_id, 'yoq, fakat tugri raqam yuzing', reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, handle_rubl_sotish_amount, selling_rate_rubl) # Повторно регистрируем этот же шаг
            return

        # Конвертируем сумму рублей в сумы по заявленному курсу
        converted_sum = amount_rubles * selling_rate_rubl
        # Округляем в пользу бота (бот покупает рубли, значит, платит меньше, округляем в меньшую сторону до ближайших 50 000)
        final_sum_for_user = round_down_to_hundred_thousand(converted_sum) # Используем обновленную функцию округления вниз

        # Отправляем финальное сообщение с округленной суммой и прикрепляем кнопки "Ha/Yoq"
        bot.send_message(user_id, f'koro4e {final_sum_for_user} boladi, olasizmi?', reply_markup=ha_yoq_buttons())
        # Регистрируем следующий шаг для обработки ответа "Ha" или "Yoq"
        bot.register_next_step_handler(message, handle_confirmation)
    else: # Если введенный текст не является целым числом
        bot.send_message(user_id, 'yoq, fakat tugri raqam yuzing', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, handle_rubl_sotish_amount, selling_rate_rubl) # Повторно регистрируем этот же шаг


# Запуск бота
bot.polling(non_stop=True) # Запускаем бесконечный цикл обработки входящих сообщений. Бот будет работать постоянно, пока не будет остановлен вручную или не возникнет критическая ошибка.
