import os
import time
import threading
from flask import Flask
import telebot
from telebot import types

# --- Налаштування ---
TOKEN = "8785665273:AAFikmkrKRnR9rYr4RoiSicvgDfGqz-VSeY"  # Токен вашого бота
ADMIN_ID = "1014079912"    # Telegram ID куратора / адміна

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
    markup.add("⚖️ ст. 173-2 Домашнє насильство", "🚸 ст. 184 Невиконання обов'язків")
    markup.add("🏫 ст. 173-4 Булінг", "🤪 ст. 173 Дрібне хуліганство")
    markup.add("📜 Постанови/Накази", "🧠 Алгоритми")
    markup.add("ℹ️ Про бота")
    return markup

# 2. Підменю видів насильства
def get_violence_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("👊 Фізичне насильство", "🗣 Психологічне насильство")
    markup.add("💰 Економічне насильство", "👶 Насильство відносно дитини")
    markup.add("🔙 Головне меню")
    return markup

# 3. Підменю "Постанови / Накази / Закони / Кодекси"
def get_docs_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("⚖️ КУпАП", "⚖️ Кримінальний кодекс")
    markup.add("⚖️ Сімейний кодекс", "👮 ЗУ Про Національну поліцію")
    markup.add("🎓 ЗУ Про освіту", "🏫 ЗУ Про загальну середню освіту")
    markup.add("👶 ЗУ Про охорону дитинства", "🏛 Постанова № 684")
    markup.add("🏛 Постанова № 1245", "🏛 Постанова № 70")
    markup.add("📋 Наказ № 663", "📋 Наказ № 1646")
    markup.add("📋 Наказ № 685/1013", "🔙 Головне меню")
    return markup

# 4. Підменю "Алгоритми"
def get_algorithms_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add("🚨 Алгоритм дій у разі булінгу")
    markup.add("💣 Алгоритм дій при виявленні ВНП")
    markup.add("🛡 Алгоритм дій при домашньому насильстві")
    markup.add("🔙 Головне меню")
    return markup


# --- Обробка команд та меню ---

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id, 
        f"Вітаю, {message.from_user.first_name}!\n"
        f"Я ваш робочий помічник. Оберіть потрібний розділ меню нижче:", 
        reply_markup=get_main_menu()
    )

# Повернення до головного меню
@bot.message_handler(func=lambda message: message.text and ("Головне меню" in message.text or message.text == "/menu"))
def back_to_main_menu(message):
    bot.send_message(
        message.chat.id, 
        "Повертаємось до головного меню:", 
        reply_markup=get_main_menu()
    )


# --- Розділ: Алгоритми ---

@bot.message_handler(func=lambda message: message.text and "Алгоритми" in message.text)
def algorithms_category_select(message):
    bot.send_message(
        message.chat.id, 
        "Оберіть потрібний алгоритм дій:", 
        reply_markup=get_algorithms_menu()
    )

# 1. Алгоритм булінгу
@bot.message_handler(func=lambda message: message.text and "Алгоритм дій у разі булінгу" in message.text)
def bullying_algorithm_info(message):
    alg_text_1 = (
        "🚨 **АЛГОРИТМ ДІЙ ІНСПЕКТОРА СЛУЖБИ ОСВІТНЬОЇ БЕЗПЕКИ ПРИ ВИЯВЛЕННІ БУЛІНГУ**\n\n"
        "1️⃣ **Отримання інформації**\n"
        "Повідомлення може надійти:\n"
        "• анонімно;\n"
        "• від учня;\n"
        "• від батьків;\n"
        "• від учителя;\n"
        "• від адміністрації закладу освіти;\n"
        "• від свідків;\n"
        "• із соціальних мереж або чатів;\n"
        "• через АІКОМ.\n\n"
        "───────────────────\n\n"
        "2️⃣ **Забезпечення безпеки**\n"
        "• Негайно припинити протиправні дії.\n"
        "• Відокремити кривдника від потерпілого.\n"
        "• Не допускати продовження конфлікту.\n"
        "• За потреби надати домедичну допомогу або викликати швидку.\n\n"
        "───────────────────\n\n"
        "3️⃣ **Первинне з’ясування обставин**\n"
        "Окремо опитати:\n"
        "• потерпілого;\n"
        "• кривдника;\n"
        "• свідків;\n"
        "• класного керівника;\n"
        "• соціального педагога або психолога.\n\n"
        "Встановити:\n"
        "• коли розпочалися події;\n"
        "• як часто вони повторювалися;\n"
        "• які саме дії вчинялися;\n"
        "• чи були погрози;\n"
        "• чи застосовувалося насильство через інтернет.\n\n"
        "───────────────────\n\n"
        "4️⃣ **Встановити наявність ознак булінгу**\n"
        "Булінг має 4 обов’язкові ознаки:\n"
        "1. Систематичність (повторюваність).\n"
        "2. Наявність кривдника.\n"
        "3. Наявність потерпілого.\n"
        "4. Заподіяння або можливість заподіяння психічної чи фізичної шкоди.\n\n"
        "⚠️ *Якщо хоча б однієї ознаки немає — це може бути конфлікт, а не булінг.*"
    )

    alg_text_2 = (
        "5️⃣ **Зібрати докази**\n"
        "• письмові пояснення;\n"
        "• фото;\n"
        "• відеозаписи;\n"
        "• листування;\n"
        "• скріншоти;\n"
        "• аудіозаписи;\n"
        "• медичні документи;\n"
        "• характеристику зі школи.\n\n"
        "───────────────────\n\n"
        "6️⃣ **Повідомити адміністрацію школи**\n"
        "Керівник закладу:\n"
        "• створює комісію з розгляду випадку булінгу;\n"
        "• повідомляє батьків;\n"
        "• організовує розгляд.\n\n"
        "───────────────────\n\n"
        "7️⃣ **Повідомити батьків**\n"
        "Повідомити:\n"
        "• батьків потерпілого;\n"
        "• батьків кривдника.\n\n"
        "───────────────────\n\n"
        "8️⃣ **Юридична оцінка**\n"
        "Якщо встановлено факт булінгу:\n"
        "• скласти протокол за ст. 173-4 КУпАП щодо особи, яка підлягає адміністративній відповідальності;\n"
        "• якщо кривднику від 14 до 16 років — відповідальність несуть батьки;\n"
        "• якщо кривднику 16 років і більше — протокол складається на нього.\n\n"
        "───────────────────\n\n"
        "9️⃣ **Передача матеріалів**\n"
        "Матеріали направляються до суду для розгляду справи.\n\n"
        "───────────────────\n\n"
        "🔟 **Профілактична робота**\n"
        "Після оформлення матеріалів:\n"
        "• провести бесіду з класом;\n"
        "• провести бесіду з батьками;\n"
        "• залучити практичного психолога;\n"
        "• контролювати недопущення повторних випадків.\n\n"
        "📌 **Що потрібно пам’ятати інспектору СОБ:**\n"
        "• **Булінг ≠ конфлікт.** Конфлікт — одноразова суперечка між рівними сторонами. Булінг — це систематичне цькування з дисбалансом сил.\n"
        "• **Кібербулінг** також підпадає під ст. 173-4 КУпАП.\n"
        "• Якщо під час булінгу дитині заподіяно тілесні ушкодження або є ознаки кримінального правопорушення, інспектор забезпечує реєстрацію події та діє відповідно до ККУ.\n\n"
        "⚖️ **Санкція ст. 173-4 КУпАП:**\n"
        "• **Булінг (перше вчинення):** штраф від 50 до 100 НМДГ або громадські роботи 20–40 годин.\n"
        "• **Повторне вчинення протягом року або групою осіб:** штраф від 100 до 200 НМДГ або громадські роботи 40–60 годин."
    )

    bot.send_message(message.chat.id, alg_text_1, parse_mode="Markdown")
    bot.send_message(message.chat.id, alg_text_2, parse_mode="Markdown")

# 2. Алгоритм дій при виявленні зброї/ВНП
@bot.message_handler(func=lambda message: message.text and "виявленні ВНП" in message.text)
def explosives_algorithm_info(message):
    alg_text_1 = (
        "💣 **АЛГОРИТМ ДІЙ ІНСПЕКТОРА СОБ ПРИ ВИЯВЛЕННІ ЗБРОЇ, БОЄПРИПАСІВ, ВИБУХОНЕБЕЗПЕЧНОГО АБО ІНШОГО НЕБЕЗПЕЧНОГО ПРЕДМЕТА**\n\n"
        "1️⃣ **Виявлення предмета**\n"
        "Небезпечним предметом можуть бути:\n"
        "• вогнепальна або травматична зброя;\n"
        "• ніж, кастет, телескопічний кийок;\n"
        "• граната, міна, патрони;\n"
        "• саморобний вибуховий пристрій;\n"
        "• безхазяйна сумка, коробка, рюкзак із невідомим вмістом.\n\n"
        "⛔️ **Головне правило:** *не торкатися, не відкривати, не переміщувати предмет.*\n\n"
        "───────────────────\n\n"
        "2️⃣ **Забезпечення власної безпеки**\n"
        "• оцінити обстановку;\n"
        "• переконатися, що немає безпосередньої загрози для життя;\n"
        "• не допускати паніки.\n\n"
        "───────────────────\n\n"
        "3️⃣ **Обмеження доступу**\n"
        "• відвести дітей і працівників на безпечну відстань;\n"
        "• зачинити або ізолювати приміщення (якщо це безпечно);\n"
        "• не дозволяти нікому наближатися до предмета;\n"
        "• не допускати фотографування, відеозйомки чи спроб торкатися предмета.\n\n"
        "───────────────────\n\n"
        "4️⃣ **Негайне повідомлення**\n"
        "Повідомити:\n"
        "• адміністрацію закладу освіти;\n"
        "• чергову частину поліції (102 або через службовий зв’язок);\n"
        "• безпосереднього керівника.\n\n"
        "📞 **Під час повідомлення вказати:** точну адресу, місце знаходження предмета, короткий опис, чи є поруч люди."
    )

    alg_text_2 = (
        "5️⃣ **Організація евакуації**\n"
        "• організувати евакуацію відповідно до плану закладу;\n"
        "• вивести дітей та персонал у визначене безпечне місце.\n\n"
        "───────────────────\n\n"
        "6️⃣ **Охорона місця події**\n"
        "• не допускати сторонніх осіб;\n"
        "• зберегти обстановку;\n"
        "• встановити можливих свідків.\n\n"
        "───────────────────\n\n"
        "7️⃣ **Зустріч спеціалізованих служб**\n"
        "• передати інформацію вибухотехнікам та СОГ.\n\n"
        "📌 **ОСНОВНЕ ЗАВДАННЯ:** захистити дітей, організувати безпечну зону та зберегти місце події."
    )

    bot.send_message(message.chat.id, alg_text_1, parse_mode="Markdown")
    bot.send_message(message.chat.id, alg_text_2, parse_mode="Markdown")

# 3. Алгоритм дій у разі виявлення домашнього насильства
@bot.message_handler(func=lambda message: message.text and "домашньому насильстві" in message.text)
def domestic_violence_algorithm_info(message):
    alg_text_1 = (
        "🛡 **АЛГОРИТМ ДІЙ ІНСПЕКТОРА СОБ ПРИ ВИЯВЛЕННІ ОЗНАК ДОМАШНЬОГО НАНОСИЛЬСТВА ЩОДО ДИТИНИ**\n\n"
        "1️⃣ **Отримання інформації** (від дитини, педагогів, психолога, свідків).\n"
        "2️⃣ **Оцінити рівень небезпеки** (чи є загроза життю/здоров'ю).\n"
        "3️⃣ **Забезпечити безпеку дитини** (відвести у безпечне місце, заспокоїти).\n"
        "4️⃣ **При наявності тілесних ушкоджень** — негайно викликати 103.\n"
        "5️⃣ **Первинне опитування** проводити без тиску, бажано у присутності психолога.\n"
        "6️⃣ **Визначити вид насильства** (фізичне, психологічне, економічне, сексуальне)."
    )

    alg_text_2 = (
        "7️⃣ **Зафіксувати інформацію** (пояснення, свідки, фото ушкоджень).\n"
        "8️⃣ **Повідомити відповідні служби** (адміністрацію, чергову частину, ювенальну превенцію, службу у справах дітей).\n"
        "9️⃣ **Правова оцінка** (ст. 173-2 КУпАП або внесення до ЄРДР за ККУ).\n"
        "🔟 **Забезпечити подальший супровід та підтримку дитини.**"
    )

    bot.send_message(message.chat.id, alg_text_1, parse_mode="Markdown")
    bot.send_message(message.chat.id, alg_text_2, parse_mode="Markdown")


# --- Розділ: Постанови, Накази, Кодекси ---

@bot.message_handler(func=lambda message: message.text and ("Постанови/Накази" in message.text or "Постанови" in message.text or "Накази" in message.text))
def docs_category_select(message):
    bot.send_message(
        message.chat.id, 
        "Оберіть потрібну постанову, наказ, закон або кодекс для перегляду та переходу за посиланням:", 
        reply_markup=get_docs_menu()
    )

@bot.message_handler(func=lambda message: message.text and "купап" in message.text.lower())
def doc_kupap_info(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔗 Відкрити КУпАП на Zakon.Rada", url="https://zakon.rada.gov.ua/laws/show/8073-10#Text"))
    bot.send_message(message.chat.id, "⚖️ **Кодекс України про адміністративні правопорушення (КУпАП)**", parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text and "кримінальний кодекс" in message.text.lower())
def doc_kk_info(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔗 Відкрити ККУ на Zakon.Rada", url="https://zakon.rada.gov.ua/laws/show/2341-14#Text"))
    bot.send_message(message.chat.id, "⚖️ **Кримінальний кодекс України (ККУ)**", parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text and "сімейний кодекс" in message.text.lower())
def doc_family_code_info(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔗 Відкрити Сімейний кодекс на Zakon.Rada", url="https://zakon.rada.gov.ua/laws/show/2947-14#Text"))
    bot.send_message(message.chat.id, "⚖️ **Сімейний кодекс України**", parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text and "національну поліцію" in message.text.lower())
def doc_police_law_info(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔗 Відкрити ЗУ «Про Національну поліцію»", url="https://zakon.rada.gov.ua/laws/show/580-19#Text"))
    bot.send_message(message.chat.id, "👮 **Закон України «Про Національну поліцію»**", parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text and message.text == "🎓 ЗУ Про освіту")
def doc_education_law_info(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔗 Відкрити ЗУ «Про освіту»", url="https://zakon.rada.gov.ua/laws/show/2145-19#Text"))
    bot.send_message(message.chat.id, "🎓 **Закон України «Про освіту»**", parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text and "середню освіту" in message.text.lower())
def doc_sec_education_law_info(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔗 Відкрити ЗУ «Про загальну середню освіту»", url="https://zakon.rada.gov.ua/laws/show/651-14#Text"))
    bot.send_message(message.chat.id, "🏫 **Закон України «Про повну загальну середню освіту»**", parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text and "охорону дитинства" in message.text.lower())
def doc_child_protection_info(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔗 Відкрити ЗУ «Про охорону дитинства»", url="https://zakon.rada.gov.ua/laws/show/2402-14#Text"))
    bot.send_message(message.chat.id, "👶 **Закон України «Про охорону дитинства»**", parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text and "684" in message.text)
def doc_684_info(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔗 Відкрити Постанову № 684", url="https://zakon.rada.gov.ua/laws/show/684-2017-%D0%BF#Text"))
    bot.send_message(message.chat.id, "🏛 **Постанова КМУ № 684**", parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text and "663" in message.text)
def doc_663_info(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔗 Відкрити Наказ № 663", url="https://zakon.rada.gov.ua/laws/show/z1590-24#Text"))
    bot.send_message(message.chat.id, "📋 **Наказ МВС України № 663**", parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text and "1646" in message.text)
def doc_1646_info(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔗 Відкрити Наказ № 1646", url="https://zakon.rada.gov.ua/laws/show/z0111-20#Text"))
    bot.send_message(message.chat.id, "📋 **Наказ МОН України № 1646**", parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text and "1245" in message.text)
def doc_1245_info(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔗 Відкрити Постанову № 1245", url="https://zakon.rada.gov.ua/laws/show/1245-2024-%D0%BF#Text"))
    bot.send_message(message.chat.id, "🏛 **Постанова КМУ № 1245**", parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text and "70" in message.text)
def doc_70_info(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔗 Відкрити Постанову № 70", url="https://zakon.rada.gov.ua/laws/show/70-2026-%D0%BF#Text"))
    bot.send_message(message.chat.id, "🏛 **Постанова КМУ № 70**", parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text and ("685" in message.text or "1013" in message.text))
def doc_685_1013_info(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔗 Відкрити Наказ № 685/1013", url="https://zakon.rada.gov.ua/laws/show/z1583-23#Text"))
    bot.send_message(message.chat.id, "📋 **Спільний наказ № 685/1013**", parse_mode="Markdown", reply_markup=markup)


# --- Розділ: ст. 173-2 КУпАП ---

@bot.message_handler(func=lambda message: message.text and ("173-2" in message.text or "Домашнє насильство" in message.text))
def violence_category_select(message):
    bot.send_message(
        message.chat.id, 
        "Оберіть вид домашнього насильства для перегляду фабули та матеріалів:", 
        reply_markup=get_violence_menu()
    )

@bot.message_handler(func=lambda message: message.text and "Фізичне" in message.text)
def physical_violence_info(message):
    fabula_text = (
        "⚖️ **Фабула правопорушення (ч. 1 ст. 173-2 КУпАП — Фізичне насильство):**\n\n"
        "01.04.2026 о 21 год 00 хв Петренко Петро Петрович за місцем свого проживання, "
        "а саме: на вул. Пряма, 10, кв. 15, у місті Житомир, перебуваючи з ознаками "
        "алкогольного сп’яніння, учинив стосовно своєї дружини Петренко С. С. домашнє насильство "
        "фізичного характеру (стусани та штовхання), чим завдав їй фізичного болю."
    )
    bot.send_message(message.chat.id, fabula_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text and "Психологічне" in message.text)
def psychological_violence_info(message):
    fabula_text = (
        "⚖️ **Фабула правопорушення (ч. 1 ст. 173-2 КУпАП — Психологічне насильство):**\n\n"
        "01.07.2025 о 01 год 20 хв Петренко Петро Петрович за місцем проживання "
        "учинив стосовно своєї дружини Петренко С. С. домашнє насильство психологічного характеру: "
        "ображав нецензурною лайкою та погрожував фізичною розправою, чим завдав шкоди її психічному здоров’ю."
    )
    bot.send_message(message.chat.id, fabula_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text and "Економічне" in message.text)
def economic_violence_info(message):
    fabula_text = (
        "⚖️ **Фабула правопорушення (ч. 1 ст. 173-2 КУпАП — Економічне насильство):**\n\n"
        "01.05.2026 Петренко П. П., перебуваючи за адресою проживання, учинив стосовно "
        "своєї дружини Петренко С. С. домашнє насильство економічного характеру, яке полягало "
        "у свідомому позбавленні її житла/коштів/майна або пошкодженні власного майна (розбив телефон), "
        "чим було завдано майнової шкоди."
    )
    bot.send_message(message.chat.id, fabula_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text and ("дитини" in message.text.lower() or "дитин" in message.text.lower()))
def child_violence_info(message):
    fabula_text_1 = (
        "⚖️ **Фабула (ч. 1 ст. 173-2 КУпАП — Насильство відносно дитини):**\n\n"
        "03.06.2026 о 01 год 20 хв Петренко П. П. за місцем спільного проживання учинив стосовно "
        "свого неповнолітнього сина Петренко С. С., 2011 р.н., домашнє насильство фізичного "
        "та психологічного характеру (ображав нецензурною лайкою, штовхав), чим завдав шкоди його здоров'ю.\n\n"
        "───────────────────\n\n"
        "⚖️ **Фабула (ч. 2 ст. 173-2 КУпАП — Насильство у присутності дитини):**\n\n"
        "08.02.2026 гр. Іванов І. І. учинив стосовно своєї дружини Іванової А. П. у присутності "
        "малолітньої дитини Іванової О. І., 2018 р. н., домашнє насильство, чим заподіяв шкоду "
        "психічному здоров’ю малолітньої дитини."
    )
    
    fabula_text_2 = (
        "⚖️ **Фабула (ч. 3 ст. 173-2 КУпАП — Повторність протягом року):**\n\n"
        "01.01.2026 Петренко П. П., будучи повторно протягом року підданим адміністративному "
        "стягненню за ч.1 ст.173-2 КУпАП, знову учинив домашнє насильство за місцем проживання."
    )

    bot.send_message(message.chat.id, fabula_text_1, parse_mode="Markdown")
    bot.send_message(message.chat.id, fabula_text_2, parse_mode="Markdown")


# --- Розділи: ст. 184, ст. 173-4, ст. 173 КУпАП ---

@bot.message_handler(func=lambda message: message.text and "184" in message.text)
def art_184_info(message):
    text = (
        "🚸 **ст. 184 КУпАП — Невиконання батьками обов'язків щодо виховання дітей**\n\n"
        "📌 **Ч. 1:** Ухилення батьків або осіб, які їх замінюють, від виконання передбачених законодавством обов’язків щодо забезпечення необхідних умов життя, навчання та виховання неповнолітніх дітей.\n\n"
        "📌 **Ч. 3:** Вчинення неповнолітніми віком від 14 до 16 років діяння, що містить ознаки адміністративного правопорушення (відповідальність батьків)."
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text and "173-4" in message.text)
def art_173_4_info(message):
    text = (
        "🏫 **ст. 173-4 КУпАП — Булінг (цькування) учасника освітнього процесу**\n\n"
        "Діяння учасників освітнього процесу, які полягають у психологічному, фізичному, економічному чи сексуальному насильстві, що вчиняються стосовно малолітньої чи неповнолітньої особи або такою особою стосовно інших учасників освітнього процесу, внаслідок чого була або могла бути завдана шкода психічному або фізичному здоров’ю потерпілого."
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text and "173" in message.text and "173-2" not in message.text and "173-4" not in message.text)
def art_173_info(message):
    text = (
        "🤪 **ст. 173 КУпАП — Дрібне хуліганство**\n\n"
        "Дрібне хуліганство, тобто нецензурна лайка в громадських місцях, образливе чіпляння до громадян та інші подібні дії, що порушують громадський порядок і спокій громадян."
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")


# --- Розділ: Про бота ---

@bot.message_handler(func=lambda message: message.text and "Про бота" in message.text)
def about_bot_info(message):
    about_text = (
        "ℹ️ **Про робочий помічник СОБ**\n\n"
        "Цей бот розроблений для швидкого доступу до необхідної нормативно-правової бази, "
        "фабул адміністративних правопорушень та алгоритмів дій Інспектора Служби Освітньої Безпеки.\n\n"
        "👨‍💻 **З питань роботи бота звертайтеся до куратора.**"
    )
    bot.send_message(message.chat.id, about_text, parse_mode="Markdown")


# --- Запуск веб-сервера та бота ---

if __name__ == '__main__':
    # Запуск Flask у окремому потоці для задоволення хостингу (Port 8080)
    threading.Thread(target=run_flask, daemon=True).start()
    
    print("Бот успішно запущений!")
    
    # Безперервний запуск бота
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"Помилка з'єднання: {e}")
            time.sleep(5)
