import os
import threading
import time
from flask import Flask
import telebot
from telebot import types

# --- Налаштування ---
TOKEN = "8785665273:AAFikmkrKRnR9rYr4RoiSicvgDfGqz-VSeY"  # Токен вашого бота[cite: 1]
ADMIN_ID = "1014079912"  # Telegram ID куратора / адміна[cite: 1]

bot = telebot.TeleBot(TOKEN)[cite: 1]
app = Flask(__name__)[cite: 1]


# Мінімальний веб-сервер для утримання хостингу
@app.route('/')[cite: 1]
def home():[cite: 1]
  return "Bot is alive!"[cite: 1]


def run_flask():[cite: 1]
  app.run(host='0.0.0.0', port=8080)[cite: 1]


# --- Клавіатури ---


# 1. Головне меню
def get_main_menu():[cite: 1]
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)[cite: 1]
  markup.add(
      "⚖️ ст. 173-2 Домашнє насильство", "🚸 ст. 184 Невиконання обов'язків"
  )[cite: 1]
  markup.add("🏫 ст. 173-4 Булінг", "🤪 ст. 173 Дрібне хуліганство")[cite: 1]
  markup.add("🚬 ст. 175-1 Куріння", "📜 Постанови/Накази")[cite: 1]
  markup.add("🧠 Алгоритми", "ℹ️ Про бота")[cite: 1]
  return markup[cite: 1]


# 2. Підменю "ст. 175-1 Куріння"
def get_smoking_menu():[cite: 1]
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)[cite: 1]
  markup.add("🚬 ч. 1 ст. 175-1", "🚭 ч. 2 ст. 175-1")[cite: 1]
  markup.add("🔙 Головне меню")[cite: 1]
  return markup[cite: 1]


# 3. Підменю видів насильства
def get_violence_menu():[cite: 1]
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)[cite: 1]
  markup.add("👊 Фізичне насильство", "🗣 Психологічне насильство")[cite: 1]
  markup.add("💰 Економічне насильство", "👶 Насильство відносно дитини")[cite: 1]
  markup.add("🔙 Головне меню")[cite: 1]
  return markup[cite: 1]


# 4. Підменю "Постанови / Накази / Закони / Кодекси"
def get_docs_menu():[cite: 1]
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)[cite: 1]
  markup.add("⚖️ КУпАП", "⚖️ Кримінальний кодекс")[cite: 1]
  markup.add("⚖️ Сімейний кодекс", "👮 ЗУ Про Національну поліцію")[cite: 1]
  markup.add("🎓 ЗУ Про освіту", "🏫 ЗУ Про загальну середню освіту")[cite: 1]
  markup.add("👶 ЗУ Про охорону дитинства", "🏛 Постанова № 684")[cite: 1]
  markup.add("🏛 Постанова № 1245", "🏛 Постанова № 70")[cite: 1]
  markup.add("📋 Наказ № 663", "📋 Наказ № 1646")[cite: 1]
  markup.add("📋 Наказ № 685/1013", "🔙 Головне меню")[cite: 1]
  return markup[cite: 1]


# 5. Підменю "Алгоритми"
def get_algorithms_menu():[cite: 1]
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)[cite: 1]
  markup.add("🚨 Алгоритм дій у разі булінгу")[cite: 1]
  markup.add("💣 Алгоритм дій при виявленні ВНП")[cite: 1]
  markup.add("🛡 Алгоритм дій при домашньому насильстві")[cite: 1]
  markup.add("🔙 Головне меню")[cite: 1]
  return markup[cite: 1]


# --- Обробка команд та головного меню ---


@bot.message_handler(commands=['start'])[cite: 1]
def start(message):[cite: 1]
  bot.send_message(
      message.chat.id,
      f"Вітаю, {message.from_user.first_name}!\nЯ ваш робочий помічник. Оберіть"
      " потрібний розділ меню нижче:",
      reply_markup=get_main_menu(),
  )[cite: 1]


# Повернення до головного меню
@bot.message_handler(
    func=lambda message: message.text
    and ("Головне меню" in message.text or message.text == "/menu")
)[cite: 1]
def back_to_main_menu(message):[cite: 1]
  bot.send_message(
      message.chat.id, "Повертаємось до головного меню:", reply_markup=get_main_menu()
  )[cite: 1]


# --- РОЗДІЛ: ст. 175-1 КУпАП (КУРІННЯ) ---


@bot.message_handler(
    func=lambda message: message.text
    and ("175-1" in message.text or "Куріння" in message.text)
    and "ч. 1" not in message.text
    and "ч. 2" not in message.text
)[cite: 1]
def smoking_category_select(message):[cite: 1]
  bot.send_message(
      message.chat.id,
      "Оберіть частину ст. 175-1 КУпАП для перегляду фабули та нормативної"
      " бази:",
      reply_markup=get_smoking_menu(),
  )[cite: 1]


@bot.message_handler(
    func=lambda message: message.text
    and (
        "ч. 1" in message.text
        or "ч.1" in message.text
        or "ч 1" in message.text
    )
    and "175-1" in message.text
)[cite: 1]
def smoking_part1_info(message):[cite: 1]
  text = (
      "🚬 **ч. 1 ст. 175-1 КУпАП — Куріння тютюнових виробів у заборонених"
      " місцях**\n\n📜 **Закон України від 22.09.2005 № 2899-IV.**\n\n⚖️"
      " **Приклад фабули:**\n21.11.2016 об 17.00 у м. Рівному по вул. Київській,"
      " гр. Іванов І.І. біля (зупинки громадського транспорту, під’їзд житлового"
      " будинку, громадському транспорті, дитячому майданчику, школа, лікарня,"
      " аптека, магазин та інше) курив тютюновий виріб - сигарети «Море», у"
      " місці де це заборонено Законом від 22.09.2005 №"
      " 2899-IV.\n\n───────────────────\n\n🏛 **Громадське місце** - частина"
      " (частини) будь-якої будівлі, споруди, яка доступна або відкрита для"
      " населення вільно, чи за запрошенням, або за плату, постійно,"
      " періодично або час від часу, в тому числі під'їзди, а також підземні"
      " переходи, стадіони.\n\n📌 **Стаття 13 Закону № 2899-IV:**\n1) у ліфтах і"
      " таксофонах;\n2) у приміщеннях та на території закладів охорони"
      " здоров’я;\n3) у приміщеннях та на території навчальних закладів;\n4)"
      " на дитячих майданчиках;\n5) у приміщеннях та на території спортивних і"
      " фізкультурно-оздоровчих споруд та закладів фізичної культури і"
      " спорту;\n6) у під’їздах житлових будинків;\n7) у підземних переходах;\n8)"
      " у транспорті загального користування, що використовується для"
      " перевезення пасажирів;\n9) у приміщеннях закладів ресторанного"
      " господарства;\n10) у приміщеннях об’єктів культурного призначення;\n11)"
      " у приміщеннях органів державної влади та органів місцевого"
      " самоврядування, інших державних установ;\n12) на стаціонарно"
      " обладнаних зупинках маршрутних транспортних засобів.\n\n⛔️"
      " **За забороняється, крім спеціально відведених для цього місць,"
      " куріння тютюнових виробів:**\n1) у приміщеннях підприємств, установ та"
      " організацій усіх форм власності;\n2) у приміщеннях готелів та аналогічних"
      " засобів розміщення громадян;\n3) у приміщеннях гуртожитків;\n4) в"
      " аеропортах та на вокзалах."
  )[cite: 1]
  bot.send_message(message.chat.id, text, parse_mode="Markdown")[cite: 1]


@bot.message_handler(
    func=lambda message: message.text
    and (
        "ч. 2" in message.text
        or "ч.2" in message.text
        or "ч 2" in message.text
    )
    and "175-1" in message.text
)[cite: 1]
def smoking_part2_info(message):[cite: 1]
  text = (
      "🚭 **ч. 2 ст. 175-1 КУпАП — Повторне протягом року вчинення"
      " правопорушення**\n\n⚖️ **Приклад фабули:**\n21.11.2016 об 17.00 у м."
      " Рівному по вул. Київській, гр. Іванов І.І. біля (зупинки громадського"
      " транспорту, під’їзд житлового будинку, громадському транспорті,"
      " дитячому майданчику, школа, лікарня, аптека, магазин та інше) курив"
      " тютюновий виріб - сигарети «Море», у місці де це заборонено Законом від"
      " 22.09.2005 № 2899-IV, чим повторно вчинив правопорушення."
  )[cite: 1]
  bot.send_message(message.chat.id, text, parse_mode="Markdown")[cite: 1]


# --- РОЗДІЛ: Алгоритми ---


@bot.message_handler(
    func=lambda message: message.text and "Алгоритми" in message.text
)[cite: 1]
def algorithms_category_select(message):[cite: 1]
  bot.send_message(
      message.chat.id,
      "Оберіть потрібний алгоритм дій:",
      reply_markup=get_algorithms_menu(),
  )[cite: 1]


@bot.message_handler(
    func=lambda message: message.text
    and "Алгоритм дій у разі булінгу" in message.text
)[cite: 1]
def bullying_algorithm_info(message):[cite: 1]
  alg_text_1 = (
      "🚨 **АЛГОРИТМ ДІЙ ІНСПЕКТОРА СЛУЖБИ ОСВІТНЬОЇ БЕЗПЕКИ ПРИ ВИЯВЛЕННІ"
      " БУЛІНГУ**\n\n1️⃣ **Отримання інформації** (анонімно, від учня, батьків,"
      " учителя, адміністрації, через АІКОМ).\n2️⃣ **Забезпечення безпеки**"
      " (припинити дії, відокремити кривдника, надати допомогу).\n3️⃣"
      " **Первинне з’ясування обставин** (опитати потерпілого, кривдника,"
      " свідків, психолога).\n4️⃣ **Встановити наявність ознак булінгу**"
      " (систематичність, кривдник, потерпілий, шкода)."
  )[cite: 1]
  alg_text_2 = (
      "5️⃣ **Зібрати докази** (пояснення, фото, відео, скріншоти).\n6️⃣"
      " **Повідомити адміністрацію школи.**\n7️⃣ **Повідомити батьків.**\n8️⃣"
      " **Юридична оцінка** (протокол за ст. 173-4 КУпАП).\n9️⃣ **Передача"
      " матеріалів до суду.**\n🔟 **Профілактична робота.**"
  )[cite: 1]
  bot.send_message(message.chat.id, alg_text_1, parse_mode="Markdown")[cite: 1]
  bot.send_message(message.chat.id, alg_text_2, parse_mode="Markdown")[cite: 1]


@bot.message_handler(
    func=lambda message: message.text and "виявленні ВНП" in message.text
)[cite: 1]
def explosives_algorithm_info(message):[cite: 1]
  alg_text_1 = (
      "💣 **АЛГОРИТМ ДІЙ ІНСПЕКТОРА СОБ ПРИ ВИЯВЛЕННІ ЗБРОЇ/ВНП**\n\n1️⃣"
      " **Виявлення предмета** (не торкатися, не переміщувати).\n2️⃣"
      " **Забезпечення власної безпеки.**\n3️⃣ **Обмеження доступу** (відвести"
      " дітей, ізолювати приміщення).\n4️⃣ **Негайне повідомлення**"
      " (адміністрація, 102, чергова частина)."
  )[cite: 1]
  alg_text_2 = (
      "5️⃣ **Організація евакуації.**\n6️⃣ **Охорона місця події.**\n7️⃣ **Зустріч"
      " спеціалізованих служб (вибухотехніки, СОГ).**"
  )[cite: 1]
  bot.send_message(message.chat.id, alg_text_1, parse_mode="Markdown")[cite: 1]
  bot.send_message(message.chat.id, alg_text_2, parse_mode="Markdown")[cite: 1]


@bot.message_handler(
    func=lambda message: message.text
    and "домашньому насильстві" in message.text
)[cite: 1]
def domestic_violence_algorithm_info(message):[cite: 1]
  alg_text_1 = (
      "🛡 **АЛГОРИТМ ДІЙ ІНСПЕКТОРА СОБ ПРИ ДОМАШНЬОМУ НАНОСИЛЬСТВІ ЩОДО"
      " ДИТИНИ**\n\n1️⃣ **Отримання інформації.**\n2️⃣ **Оцінити рівень"
      " небезпеки.**\n3️⃣ **Забезпечити безпеку дитини.**\n4️⃣ **При наявності"
      " тілесних ушкоджень** — викликати 103.\n5️⃣ **Первинне опитування** (у"
      " присутності психолога).\n6️⃣ **Визначити вид насильства.**"
  )[cite: 1]
  alg_text_2 = (
      "7️⃣ **Зафіксувати інформацію.**\n8️⃣ **Повідомити відповідні служби**"
      " (адміністрацію, 102, ювеналів, ССД).\n9️⃣ **Правова оцінка** (ст. 173-2"
      " КУпАП або ЄРДР).\n🔟 **Забезпечити подальший супровід дитини.**"
  )[cite: 1]
  bot.send_message(message.chat.id, alg_text_1, parse_mode="Markdown")[cite: 1]
  bot.send_message(message.chat.id, alg_text_2, parse_mode="Markdown")[cite: 1]


# --- РОЗДІЛ: Постанови, Накази, Кодекси ---


@bot.message_handler(
    func=lambda message: message.text
    and (
        "Постанови/Накази" in message.text
        or "Постанови" in message.text
        or "Накази" in message.text
    )
)[cite: 1]
def docs_category_select(message):[cite: 1]
  bot.send_message(
      message.chat.id,
      "Оберіть потрібну постанову, наказ, закон або кодекс:",
      reply_markup=get_docs_menu(),
  )[cite: 1]


@bot.message_handler(
    func=lambda message: message.text and "купап" in message.text.lower()
)[cite: 1]
def doc_kupap_info(message):[cite: 1]
  markup = types.InlineKeyboardMarkup()[cite: 1]
  markup.add(
      types.InlineKeyboardButton(
          "🔗 Відкрити КУпАП на Zakon.Rada",
          url="https://zakon.rada.gov.ua/laws/show/8073-10#Text",
      )
  )[cite: 1]
  bot.send_message(
      message.chat.id,
      "⚖️ **Кодекс України про адміністративні правопорушення (КУпАП)**",
      parse_mode="Markdown",
      reply_markup=markup,
  )[cite: 1]


@bot.message_handler(
    func=lambda message: message.text
    and "кримінальний кодекс" in message.text.lower()
)[cite: 1]
def doc_kk_info(message):[cite: 1]
  markup = types.InlineKeyboardMarkup()[cite: 1]
  markup.add(
      types.InlineKeyboardButton(
          "🔗 Відкрити ККУ на Zakon.Rada",
          url="https://zakon.rada.gov.ua/laws/show/2341-14#Text",
      )
  )[cite: 1]
  bot.send_message(
      message.chat.id,
      "⚖️ **Кримінальний кодекс України (ККУ)**",
      parse_mode="Markdown",
      reply_markup=markup,
  )[cite: 1]


@bot.message_handler(
    func=lambda message: message.text
    and "сімейний кодекс" in message.text.lower()
)[cite: 1]
def doc_family_code_info(message):[cite: 1]
  markup = types.InlineKeyboardMarkup()[cite: 1]
  markup.add(
      types.InlineKeyboardButton(
          "🔗 Відкрити Сімейний кодекс на Zakon.Rada",
          url="https://zakon.rada.gov.ua/laws/show/2947-14#Text",
      )
  )[cite: 1]
  bot.send_message(
      message.chat.id,
      "⚖️ **Сімейний кодекс України**",
      parse_mode="Markdown",
      reply_markup=markup,
  )[cite: 1]


@bot.message_handler(
    func=lambda message: message.text
    and "національну поліцію" in message.text.lower()
)[cite: 1]
def doc_police_law_info(message):[cite: 1]
  markup = types.InlineKeyboardMarkup()[cite: 1]
  markup.add(
      types.InlineKeyboardButton(
          "🔗 Відкрити ЗУ «Про Національну поліцію»",
          url="https://zakon.rada.gov.ua/laws/show/580-19#Text",
      )
  )[cite: 1]
  bot.send_message(
      message.chat.id,
      "👮 **Закон України «Про Національну поліцію»**",
      parse_mode="Markdown",
      reply_markup=markup,
  )[cite: 1]


@bot.message_handler(
    func=lambda message: message.text and message.text == "🎓 ЗУ Про освіту"
)[cite: 1]
def doc_education_law_info(message):[cite: 1]
  markup = types.InlineKeyboardMarkup()[cite: 1]
  markup.add(
      types.InlineKeyboardButton(
          "🔗 Відкрити ЗУ «Про освіту»",
          url="https://zakon.rada.gov.ua/laws/show/2145-19#Text",
      )
  )[cite: 1]
  bot.send_message(
      message.chat.id,
      "🎓 **Закон України «Про освіту»**",
      parse_mode="Markdown",
      reply_markup=markup,
  )[cite: 1]


@bot.message_handler(
    func=lambda message: message.text
    and "середню освіту" in message.text.lower()
)[cite: 1]
def doc_sec_education_law_info(message):[cite: 1]
  markup = types.InlineKeyboardMarkup()[cite: 1]
  markup.add(
      types.InlineKeyboardButton(
          "🔗 Відкрити ЗУ «Про загальну середню освіту»",
          url="https://zakon.rada.gov.ua/laws/show/651-14#Text",
      )
  )[cite: 1]
  bot.send_message(
      message.chat.id,
      "🏫 **Закон України «Про повну загальну середню освіту»**",
      parse_mode="Markdown",
      reply_markup=markup,
  )[cite: 1]


@bot.message_handler(
    func=lambda message: message.text
    and "охорону дитинства" in message.text.lower()
)[cite: 1]
def doc_child_protection_info(message):[cite: 1]
  markup = types.InlineKeyboardMarkup()[cite: 1]
  markup.add(
      types.InlineKeyboardButton(
          "🔗 Відкрити ЗУ «Про охорону дитинства»",
          url="https://zakon.rada.gov.ua/laws/show/2402-14#Text",
      )
  )[cite: 1]
  bot.send_message(
      message.chat.id,
      "👶 **Закон України «Про охорону дитинства»**",
      parse_mode="Markdown",
      reply_markup=markup,
  )[cite: 1]


@bot.message_handler(
    func=lambda message: message.text and "684" in message.text
)[cite: 1]
def doc_684_info(message):[cite: 1]
  markup = types.InlineKeyboardMarkup()[cite: 1]
  markup.add(
      types.InlineKeyboardButton(
          "🔗 Відкрити Постанову № 684",
          url="https://zakon.rada.gov.ua/laws/show/684-2017-%D0%BF#Text",
      )
  )[cite: 1]
  bot.send_message(
      message.chat.id,
      "🏛 **Постанова КМУ № 684**",
      parse_mode="Markdown",
      reply_markup=markup,
  )[cite: 1]


@bot.message_handler(
    func=lambda message: message.text and "663" in message.text
)[cite: 1]
def doc_663_info(message):[cite: 1]
  markup = types.InlineKeyboardMarkup()[cite: 1]
  markup.add(
      types.InlineKeyboardButton(
          "🔗 Відкрити Наказ № 663",
          url="https://zakon.rada.gov.ua/laws/show/z1590-24#Text",
      )
  )[cite: 1]
  bot.send_message(
      message.chat.id,
      "📋 **Наказ МВС України № 663**",
      parse_mode="Markdown",
      reply_markup=markup,
  )[cite: 1]


@bot.message_handler(
    func=lambda message: message.text and "1646" in message.text
)[cite: 1]
def doc_1646_info(message):[cite: 1]
  markup = types.InlineKeyboardMarkup()[cite: 1]
  markup.add(
      types.InlineKeyboardButton(
          "🔗 Відкрити Наказ № 1646",
          url="https://zakon.rada.gov.ua/laws/show/z0111-20#Text",
      )
  )[cite: 1]
  bot.send_message(
      message.chat.id,
      "📋 **Наказ МОН України № 1646**",
      parse_mode="Markdown",
      reply_markup=markup,
  )[cite: 1]


@bot.message_handler(
    func=lambda message: message.text and "1245" in message.text
)[cite: 1]
def doc_1245_info(message):[cite: 1]
  markup = types.InlineKeyboardMarkup()[cite: 1]
  markup.add(
      types.InlineKeyboardButton(
          "🔗 Відкрити Постанову № 1245",
          url="https://zakon.rada.gov.ua/laws/show/1245-2024-%D0%BF#Text",
      )
  )[cite: 1]
  bot.send_message(
      message.chat.id,
      "🏛 **Постанова КМУ № 1245**",
      parse_mode="Markdown",
      reply_markup=markup,
  )[cite: 1]


@bot.message_handler(
    func=lambda message: message.text and "70" in message.text
)[cite: 1]
def doc_70_info(message):[cite: 1]
  markup = types.InlineKeyboardMarkup()[cite: 1]
  markup.add(
      types.InlineKeyboardButton(
          "🔗 Відкрити Постанову № 70",
          url="https://zakon.rada.gov.ua/laws/show/70-2026-%D0%BF#Text",
      )
  )[cite: 1]
  bot.send_message(
      message.chat.id,
      "🏛 **Постанова КМУ № 70**",
      parse_mode="Markdown",
      reply_markup=markup,
  )[cite: 1]


@bot.message_handler(
    func=lambda message: message.text
    and ("685" in message.text or "1013" in message.text)
)[cite: 1]
def doc_685_1013_info(message):[cite: 1]
  markup = types.InlineKeyboardMarkup()[cite: 1]
  markup.add(
      types.InlineKeyboardButton(
          "🔗 Відкрити Наказ № 685/1013",
          url="https://zakon.rada.gov.ua/laws/show/z1583-23#Text",
      )
  )[cite: 1]
  bot.send_message(
      message.chat.id,
      "📋 **Спільний наказ № 685/1013**",
      parse_mode="Markdown",
      reply_markup=markup,
  )[cite: 1]


# --- РОЗДІЛ: ст. 173-2 КУпАП (Домашнє насильство) ---


@bot.message_handler(
    func=lambda message: message.text
    and ("173-2" in message.text or "Домашнє насильство" in message.text)
)[cite: 1]
def violence_category_select(message):[cite: 1]
  bot.send_message(
      message.chat.id,
      "Оберіть вид домашнього насильства:",
      reply_markup=get_violence_menu(),
  )[cite: 1]


@bot.message_handler(
    func=lambda message: message.text and "Фізичне" in message.text
)[cite: 1]
def physical_violence_info(message):[cite: 1]
  fabula_text = (
      "⚖️ **Фабула правопорушення (ч. 1 ст. 173-2 КУпАП — Фізичне"
      " насильство):**\n\n01.04.2026 о 21 год 00 хв Петренко Петро Петрович за"
      " місцем свого проживання, а саме: на вул. Пряма, 10, кв. 15, у місті"
      " Житомир, перебуваючи з ознаками алкогольного сп’яніння, учинив стосовно"
      " своєї дружини Петренко С. С. домашнє насильство фізичного характеру"
      " (стусани та штовхання), чим завдав їй фізичного болю."
  )[cite: 1]
  bot.send_message(message.chat.id, fabula_text, parse_mode="Markdown")[cite: 1]


@bot.message_handler(
    func=lambda message: message.text and "Психологічне" in message.text
)[cite: 1]
def psychological_violence_info(message):[cite: 1]
  fabula_text = (
      "⚖️ **Фабула правопорушення (ч. 1 ст. 173-2 КУпАП — Психологічне"
      " насильство):**\n\n01.07.2025 о 01 год 20 хв Петренко Петро Петрович за"
      " місцем проживання учинив стосовно своєї дружини Петренко С. С. домашнє"
      " насильство психологічного характеру: ображав нецензурною лайкою та"
      " погрожував фізичною розправою, чим завдав шкоди її психічному здоров’ю."
  )[cite: 1]
  bot.send_message(message.chat.id, fabula_text, parse_mode="Markdown")[cite: 1]


@bot.message_handler(
    func=lambda message: message.text and "Економічне" in message.text
)[cite: 1]
def economic_violence_info(message):[cite: 1]
  fabula_text = (
      "⚖️ **Фабула правопорушення (ч. 1 ст. 173-2 КУпАП — Економічне"
      " насильство):**\n\n01.05.2026 Петренко П. П., перебуваючи за адресою"
      " проживання, учинив стосовно своєї дружини Петренко С. С. домашнє"
      " насильство економічного характеру, яке полягало у свідомому"
      " позбавленні її житла/коштів/майна або пошкодженні власного майна (розбив"
      " телефон), чим було завдано майнової шкоди."
  )[cite: 1]
  bot.send_message(message.chat.id, fabula_text, parse_mode="Markdown")[cite: 1]


@bot.message_handler(
    func=lambda message: message.text
    and (
        "дитини" in message.text.lower() or "дитин" in message.text.lower()
    )
)[cite: 1]
def child_violence_info(message):[cite: 1]
  fabula_text_1 = (
      "⚖️ **Фабула (ч. 1 ст. 173-2 КУпАП — Насильство відносно"
      " дитини):**\n\n03.06.2026 о 01 год 20 хв Петренко П. П. за місцем"
      " спільного проживання учинив стосовно свого неповнолітнього сина"
      " Петренко С. С., 2011 р.н., домашнє насильство фізичного та"
      " психологічного характеру (ображав нецензурною лайкою, штовхав), чим"
      " завдав шкоди його здоров'ю.\n\n───────────────────\n\n⚖️ **Фабула (ч."
      " 2 ст. 173-2 КУпАП — Насильство у присутності дитини):**\n\n08.02.2026"
      " гр. Іванов І. І. учинив стосовно своєї дружини Іванової А. П. у"
      " присутності малолітньої дитини Іванової О. І., 2018 р. н., домашнє"
      " насильство, чим заподіяв шкоду психічному здоров’ю малолітньої дитини."
  )[cite: 1]
  fabula_text_2 = (
      "⚖️ **Фабула (ч. 3 ст. 173-2 КУпАП — Повторність протягом"
      " року):**\n\n01.01.2026 Петренко П. П., будучи повторно протягом року"
      " підданим адміністративному стягненню за ч.1 ст.173-2 КУпАП, знову"
      " учинив домашнє насильство за місцем проживання."
  )[cite: 1]
  bot.send_message(message.chat.id, fabula_text_1, parse_mode="Markdown")[cite: 1]
  bot.send_message(message.chat.id, fabula_text_2, parse_mode="Markdown")[cite: 1]


# --- РОЗДІЛИ: ст. 184, ст. 173-4, ст. 173 КУпАП ---


@bot.message_handler(
    func=lambda message: message.text and "184" in message.text
)[cite: 1]
def art_184_info(message):[cite: 1]
  text = (
      "🚸 **ст. 184 КУпАП — Невиконання батьками або особами, що їх замінюють,"
      " обов'язків щодо виховання дітей**\n\n📌 **Ч. 1:** Ухилення батьків або"
      " осіб, які їх замінюють, від виконання передбачених законодавством"
      " обов’язків щодо забезпечення необхідних умов життя, навчання та"
      " виховання неповнолітніх дітей.\n\n⚖️ **Приклад фабули за ч. 1 ст. 184"
      " КУпАП:**\nГромадянин Петров І.О., будучи батьком малолітньої дитини"
      " віком 13 років, ухилявся від виконання передбачених законодавством"
      " обов'язків щодо її виховання та належного контролю за поведінкою, що"
      " сприяло вчиненню дитиною домашнього насильства відносно своєї матері,"
      " чим вчинив правопорушення, передбачене ч. 1 ст. 184"
      " КУпАП.\n\n───────────────────\n\n📌 **Ч. 3:** Вчинення"
      " неповнолітніми віком від 14 до 16 років правопорушення, відповідальність"
      " за яке передбачено цим Кодексом (крім ч. 3 або ч. 4 ст."
      " 173-4).\n\n⚖️ **Приклад фабули за ч. 3 ст. 184 КУпАП:**\nГромадянка"
      " Петрова О.О., будучи матір'ю неповнолітнього Петрова І.І., 2011 року"
      " народження, який не досяг 16-річного віку, 15.06.2026 вчинив домашнє"
      " насильство відносно своєї сестри, а саме умисні дії психологічного"
      " характеру: ображав словесно, погрожував вбити, чим завдав їй"
      " психологічних страждань, унаслідок чого завдано шкоди психічному"
      " здоров’ю Петровій С.О., відповідальність за яке передбачена ст. 173-2"
      " КУпАП, чим вчинила правопорушення, передбачене ч. 3 ст. 184 КУпАП."
  )[cite: 1]
  bot.send_message(message.chat.id, text, parse_mode="Markdown")[cite: 1]


@bot.message_handler(
    func=lambda message: message.text and "173-4" in message.text
)[cite: 1]
def art_173_4_info(message):[cite: 1]
  text = (
      "🏫 **ст. 173-4 КУпАП — Булінг (цькування) учасника освітнього"
      " процесу**\n\nДіяння учасників освітнього процесу, які полягають у"
      " психологічному, фізичному, економічному чи сексуальному насильстві, що"
      " вчиняються стосовно малолітньої чи неповнолітньої особи."
  )[cite: 1]
  bot.send_message(message.chat.id, text, parse_mode="Markdown")[cite: 1]


# ОНОВЛЕНО: ст. 173 КУпАП з вашими прикладами фабул
@bot.message_handler(
    func=lambda message: message.text
    and "173" in message.text
    and "173-2" not in message.text
    and "173-4" not in message.text
)[cite: 1]
def art_173_info(message):[cite: 1]
  text = (
      "🤪 **ст. 173 КУпАП — Дрібне хуліганство**\n\n"
      "Дрібне хуліганство, тобто нецензурна лайка в громадських місцях, образливе чіпляння до громадян та інші подібні дії, що порушують громадський порядок і спокій громадян.\n\n"
      "⚖️ **Приклади фабул:**\n\n"
      "📌 **Варіант 1 (Нецензурна лайка):**\n"
      "01.01.2015 о 20 год. 05 хв. гр. Іванов Іван Іванович, перебуваючи в стані алкогольного сп’яніння, у громадському місці біля буд. № 76/1 по просп. Миру в Хмельницькому, висловлювався нецензурною лайкою на адресу гр. Петрової Н.П. (або перехожих), чим порушував громадський порядок і спокій громадян.\n\n"
      "📌 **Варіант 2 (Справляння природних потреб):**\n"
      "10.09.2015 о 20 год. 05 хв. гр. Іванов Іван Іванович в м. Хмельницькому по вул. Проскурівського підпілля, 15, справляв природні потреби поблизу дверей офісу «Сонечко», чим своїми діями порушував громадський порядок."
  )[cite: 1]
  bot.send_message(message.chat.id, text, parse_mode="Markdown")[cite: 1]


# --- РОЗДІЛ: Про бота ---


@bot.message_handler(
    func=lambda message: message.text and "Про бота" in message.text
)[cite: 1]
def about_bot_info(message):[cite: 1]
  about_text = (
      "ℹ️ **Про робочий помічник СОБ**\n\nЦей бот розроблений для швидкого"
      " доступу до необхідної нормативно-правової бази, фабул адміністративних"
      " правопорушень та алгоритмів дій Інспектора Служби Освітньої"
      " Безпеки.\n\n👨‍💻 **З питань роботи бота звертайтеся до куратора.**"
  )[cite: 1]
  bot.send_message(message.chat.id, about_text, parse_mode="Markdown")[cite: 1]


# --- Запуск сервера та бота ---

if __name__ == "__main__":[cite: 1]
  threading.Thread(target=run_flask, daemon=True).start()[cite: 1]
  print("Бот успішно запущений!")[cite: 1]

  while True:[cite: 1]
    try:[cite: 1]
      bot.polling(none_stop=True, interval=0, timeout=20)[cite: 1]
    except Exception as e:[cite: 1]
      print(f"Помилка з'єднання: {e}")[cite: 1]
      time.sleep(5)[cite: 1]
