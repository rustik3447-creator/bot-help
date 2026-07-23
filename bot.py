import os
import time
import threading
from flask import Flask
import telebot
from telebot import types

# --- Налаштування ---
TOKEN = "8785665273:AAFikmkrKRnR9rYr4RoiSicvgDfGqz-VSeY"  # Вкажіть токен вашого бота
ADMIN_ID = "1014079912"    # Вкажіть ваш Telegram ID (або ID куратора)

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Мінімальний веб-сервер для утримання хостингу
@app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# --- Клавіатури ---

# 1. Головне меню
def get_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(" ст.173-2 Домашнє насильство", " База знань", " Заставити питання", " Про бота")
    return markup

# 2. Підменю видів насильства
def get_violence_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(" Фізичне насильство", " Психологічне насильство")
    markup.add(" Економічне насильство", " 🔙 Головне меню")
    return markup

# 3. Кнопка завершення чату
def get_finish_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(" Завершити діалог", callback_data="finish_chat"))
    return markup


# --- Обробка команд та меню ---

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id, 
        f"Вітаю, {message.from_user.first_name}! \n"
        f"Я ваш робочий помічник. Оберіть потрібний розділ меню нижче:", 
        reply_markup=get_main_menu()
    )

# Повернення до головного меню
@bot.message_handler(func=lambda message: message.text == " 🔙 Головне меню")
def back_to_main_menu(message):
    bot.send_message(
        message.chat.id, 
        "Повертаємось до головного меню:", 
        reply_markup=get_main_menu()
    )

# --- Розділ: ст. 173-2 КУпАП ---

@bot.message_handler(func=lambda message: message.text == " ст.173-2 Домашнє насильство")
def violence_category_select(message):
    bot.send_message(
        message.chat.id, 
        " Оберіть вид домашнього насильства для перегляду фабули та матеріалів:", 
        reply_markup=get_violence_menu()
    )

# 1. Фізичне насильство
@bot.message_handler(func=lambda message: message.text == " Фізичне насильство")
def physical_violence_info(message):
    fabula_text = (
        "⚖️ **Фабула правопорушення (ч. 1 ст. 173-2 КУпАП — Фізичне насильство):**\n\n"
        "01.04.2026 о 21 год 00 хв Петренко Петро Петрович за місцем свого проживання, "
        "а саме: на вул. Пряма, 10, кв. 15, у місті Житомир, перебуваючи з ознаками "
        "алкогольного сп’яніння (запах алкоголю з порожнини рота, порушення мови), "
        "учинив стосовно своєї дружини Петренко С. С. домашнє насильство фізичного характеру, "
        "а саме умисні дії, ‒ стусани та штовхання, чим завдав шкоди фізичному здоров’ю "
        "Петренко С. С., а саме завдав їй фізичного болю."
    )
    bot.send_message(message.chat.id, fabula_text, parse_mode="Markdown")

# 2. Психологічне насильство
@bot.message_handler(func=lambda message: message.text == " Психологічне насильство")
def psychological_violence_info(message):
    fabula_text = (
        "⚖️ **Фабула правопорушення (ч. 1 ст. 173-2 КУпАП — Психологічне насильство):**\n\n"
        "01.07.2025 о 01 год 20 хв Петренко Петро Петрович за місцем свого "
        "тимчасового проживання, на вул. Миру, 16-Б, кв. 10, в місті Київ, "
        "учинив стосовно своєї дружини Петренко С. С. домашнє насильство, "
        "а саме умисні дії психологічного характеру ‒ ображав нецензурною лайкою, "
        "погрожував убити матір Петренко С. С., чим завдав їй психологічних страждань, "
        "унаслідок чого завдано шкоди психічному здоров’ю Петренко С. С."
    )
    bot.send_message(message.chat.id, fabula_text, parse_mode="Markdown")

# 3. Економічне насильство
@bot.message_handler(func=lambda message: message.text == " Економічне насильство")
def economic_violence_info(message):
    fabula_text = (
        "⚖️ **Фабули правопорушення (ч. 1 ст. 173-2 КУпАП — Економічне насильство):**\n\n"
        "📌 **Приклад 1 (Заборона працювати / позбавлення заробітку):**\n"
        "01.05.2026 о 01 год 20 хв Петренко Петро Петрович, перебуваючи за адресою: "
        "вул. Правди, 18-Г, кв. 17, у місті Львів, учинив стосовно своєї нареченої "
        "Петренко С. С. домашнє насильство, а саме умисні дії економічного характеру, "
        "які проявились у забороні йти на роботу через ревнощі до колег, що призвело "
        "до звільнення Петренко С. С. з місця роботи, чим було завдано майнової шкоди Петренко С. С.\n\n"
        "───────────────────\n\n"
        "📌 **Приклад 2 (Пошкодження / знищення майна):**\n"
        "01.02.2026 о 01 год 20 хв Петренко Петро Петрович, за місцем проживання Петренко С. С., "
        "на вул. Миру, 16-Б, кв. 10, в місті Київ, перебуваючи з ознаками алкогольного "
        "сп’яніння (порушення координації рухів, порушення мови), учинив стосовно своєї дружини "
        "Петренко С. С. домашнє насильство, а саме умисні дії економічного характеру ‒ "
        "на ґрунті ревнощів розбив мобільний телефон, який належить Петренко С. С. на праві "
        "власності, чим було завдано майнової шкоди Петренко С. С."
    )
    bot.send_message(message.chat.id, fabula_text, parse_mode="Markdown")


# --- Інші розділи головного меню ---

@bot.message_handler(func=lambda message: message.text == " База знань")
def knowledge_base(message):
    bot.send_message(
        message.chat.id, 
        " Тут розміщені корисні інструкції, нормативно-правові акти та зразки документів."
    )

@bot.message_handler(func=lambda message: message.text == " Про бота")
def about_bot(message):
    bot.send_message(
        message.chat.id,
        "Цей бот створений для швидкого отримання правової інформації, "
        "зразків фабул за ст. 173-2 КУпАП та зв’язку з куратором."
    )


# --- Зв'язок з адміном / куратором ---

@bot.message_handler(func=lambda message: message.text == " Заставити питання")
def ask_question_start(message):
    msg = bot.send_message(
        message.chat.id, 
        " Опишіть ваше питання або ситуацію одним текстовим повідомленням.\n"
        "Куратор отримає його та відповість вам у цьому чаті.", 
        reply_markup=types.ReplyKeyboardRemove()
    )
    bot.register_next_step_handler(msg, send_to_admin)

def send_to_admin(message):
    if not message.text:
        msg = bot.send_message(message.chat.id, "Будь ласка, надішліть саме текстове повідомлення.")
        bot.register_next_step_handler(msg, send_to_admin)
        return

    first_name = message.from_user.first_name or "Користувач"
    username = f"@{message.from_user.username}" if message.from_user.username else "без username"
    
    admin_text = (
        f" Нове звернення | ID: {message.chat.id}\n"
        f" Від: {first_name} ({username})\n\n"
        f" **Текст звернення:**\n{message.text}"
    )
    
    try:
        bot.send_message(ADMIN_ID, admin_text, parse_mode="Markdown")
        bot.send_message(
            message.chat.id, 
            " Ваше повідомлення надіслано куратору. Очікуйте на відповідь!", 
            reply_markup=get_finish_keyboard()
        )
    except Exception as e:
        print(f"Помилка відправки: {e}")
        bot.send_message(message.chat.id, " Не вдалося відправити повідомлення. Перевірте налаштування ADMIN_ID.")


# --- Обробка завершення та пересилки відповідей ---

@bot.callback_query_handler(func=lambda call: call.data == "finish_chat")
def finish_chat(call):
    bot.answer_callback_query(call.id)
    try:
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    except Exception:
        pass
        
    bot.send_message(
        call.message.chat.id, 
        "Діалог завершено. Повертаємось до головного меню.", 
        reply_markup=get_main_menu()
    )

# Пересилка відповіді від адміна до користувача (через Reply)
@bot.message_handler(func=lambda message: str(message.chat.id) == str(ADMIN_ID) and message.reply_to_message)
def admin_reply(message):
    try:
        text = message.reply_to_message.text or message.reply_to_message.caption or ""
        if "ID: " in text:
            user_id = text.split("ID: ")[1].split("\n")[0].strip()
            bot.send_message(
                user_id, 
                f" **Відповідь куратора:**\n{message.text}", 
                parse_mode="Markdown",
                reply_markup=get_finish_keyboard()
            )
            bot.send_message(ADMIN_ID, " Відповідь успішно надіслана користувачу.")
        else:
            bot.send_message(ADMIN_ID, " Не вдалося знайти ID користувача у повідомленні, на яке ви відповіли.")
    except Exception as e:
        bot.send_message(ADMIN_ID, f" Помилка надсилання: {e}")

# Пересилка уточнення від користувача до адміна
@bot.message_handler(func=lambda message: str(message.chat.id) != str(ADMIN_ID) and message.reply_to_message)
def user_reply(message):
    bot.send_message(
        ADMIN_ID, 
        f" Уточнення від користувача (ID: {message.chat.id}):\n\n{message.text}"
    )
    bot.send_message(
        message.chat.id, 
        "Уточнення передано куратору.", 
        reply_markup=get_finish_keyboard()
    )


# --- Запуск бота та веб-сервера ---

if __name__ == "__main__":
    # 1. Запускаємо Flask у фоновому потоці
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # 2. Запуск бота з автовідновленням під час обривів
    while True:
        try:
            print("Бот запущено...")
            bot.infinity_polling(timeout=20, long_polling_timeout=20)
        except Exception as e:
            print(f"Сталася помилка з'єднання: {e}")
            time.sleep(5)