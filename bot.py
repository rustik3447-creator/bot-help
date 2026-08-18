import os
import threading
import time
from flask import Flask
import telebot
from telebot import types

# --- Налаштування ---
TOKEN = os.environ.get(
    'BOT_TOKEN', '8785665273:AAFikmkrKRnR9rYr4RoiSicvgDfGqz-VSeY'
)
ADMIN_ID = 1014079912  # Ваш особистий Telegram ID

# 🔗 ПОСИЛАННЯ НА ГООГЛ ФОРМИ ДЛЯ ЩОДЕННОГО ЗВІТУ
URL_ZZSO_3 = "https://docs.google.com/forms/d/e/1FAIpQLSf7UMP606jWHYeo_AK3jJDQGgottGra_5RqBXUVvEC6ynSEsg/viewform?usp=sharing&ouid=113896150269870747135"
URL_ZZSO_48 = "https://docs.google.com/forms/d/e/1FAIpQLScptL7an8je5Pf6JA1x1A7WzuvEfo4nLq62wGm_FtaK1Pvb7g/viewform?usp=sharing&ouid=113896150269870747135"
URL_ZZSO_83 = "https://docs.google.com/forms/d/e/1FAIpQLSe3ORtsZxfBZbkcjDSGjrvYJBCDZxyF5IWO0Q7gxV5lChN09w/viewform?usp=sharing&ouid=113896150269870747135"
URL_ZZSO_88 = "https://docs.google.com/forms/d/e/1FAIpQLSehRiroXcjcUg8O_V35nCwpyUMgrj05k7yekKz7zz9hkt-NUQ/viewform?usp=sharing&ouid=113896150269870747135"
URL_ZZSO_91 = "https://docs.google.com/forms/d/e/1FAIpQLSfLIHh74OqWWtIFwdGRqTmpsUn2LYMvZEFj70nVvPisMs1Fdg/viewform?usp=sharing&ouid=113896150269870747135"
URL_ZZSO_105 = "https://docs.google.com/forms/d/e/1FAIpQLSc4GrMxEuVhPhlf4DHo1k8N97NEJWM88N5jA2pZNCNgkEIMFQ/viewform?usp=sharing&ouid=113896150269870747135"
URL_ZZSO_107 = "https://docs.google.com/forms/d/e/1FAIpQLSczgWsRoi24xSvOvUytDcenibGmYaizzoHnLytAmuak3f3CVg/viewform?usp=sharing&ouid=113896150269870747135"
URL_ZZSO_124 = "https://docs.google.com/forms/d/e/1FAIpQLSc4_vvLkrjpBPBGnZZ_cKrpViMi_s473XYQJmgzz4TASle0JA/viewform?usp=sharing&ouid=113896150269870747135"
URL_ZZSO_138 = "https://docs.google.com/forms/d/e/1FAIpQLSdXKbNTVbpJKrPVvu7c7SqrofG4-_Dlz_KMoJihxMCdxSa0hQ/viewform?usp=sharing&ouid=113896150269870747135"
URL_ZZSO_152 = "https://docs.google.com/forms/d/e/1FAIpQLSdNL_1NCPnDlOYUxoNu2CWrFmL5AgD7vRhYO44ZPdfeF9eNtQ/viewform?usp=header"
URL_ZZSO_153 = "https://docs.google.com/forms/d/e/1FAIpQLScNZIQQHbMUVV_COMfPfHDu5Otl6yX4rC-b_VVjUYHz4D-e9w/viewform?usp=header"
URL_ZZSO_173 = "https://docs.google.com/forms/d/e/1FAIpQLScwt5Yj8vNVrAD5-5uJe1B63BqFCAh42Y9JK4cscM7jIvLAeg/viewform?usp=header"
URL_ZZSO_MOBIL = "https://docs.google.com/forms/d/e/1FAIpQLSe_74oFERvLuLm9SIsiLGJklKeFr9RaJos4vZxEmSBjKMszeg/viewform?usp=header"
URL_ZZSO_KOROTYCH = "https://docs.google.com/forms/d/e/1FAIpQLSeiwliHwey-IzZOGwNR2d4Ehxf1ByZCatFkSnj8SsMOQz7_bg/viewform?usp=header"
URL_ZZSO_DZHERELO = "https://docs.google.com/forms/d/e/1FAIpQLScQPXp8-MjZC1rRHQYfDSCiHL1129lHJhqq14bDCKlS7h_RuA/viewform?usp=header"

# 📋 Список особистих Telegram ID людей, які отримують тривожні SOS в приватні повідомлення:
SOS_RECIPIENTS = [
    1014079912,  # Ваш ID
    902469327,   # Могилка В.О.
    178637753,   # Кравченко О.Ю.
    818368898,   # Кутєпов Є.С.
    333265010,   # Пєтухов М.Г.
    317864289,   # Щербак В.Ю.
    395300656,   # Разіньков Р.О.
    169691119,   # Ридванська Г.В.
    388133629,   # Піднебенна Ю.Ю.
    600698645,   # Адамович Т.О.
    816795374,   # Монишева А.В.
    538974554    # Гойденко А.С.
]

# 👤 Кастомні імена для конкретних ID при надсиланні SOS
CUSTOM_NAMES = {
    902469327: 'Могилка В.О. (старший з ОД)',
    178637753: 'Кравченко О.Ю.',
    818368898: 'Кутєпов Є.С.',
    333265010: 'Пєтухов М.Г.',
    317864289: 'Щербак В.Ю.',
    395300656: 'Разіньков Р.О.',
    169691119: 'Ридванська Г.В.',
    388133629: 'Піднебенна Ю.Ю.',
    600698645: 'Адамович Т.О.',
    816795374: 'Монишева А.В.',
    538974554: 'Гойденко А.С.'
}

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Веб-сервер для утримання бота в активному стані (Keep-Alive)
@app.route('/')
def home():
    return 'Бот працює!'

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# --- Клавіатури Головного Та Вкладених Меню ---

def get_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add('🚗 ст. 122 ПДР', '🚶 ст. 127 Порушення ПДР пішоходами')
    markup.add('🍻 ст. 178 Алкоголь/П’яний вигляд', '⚖️ ст. 173-2 Домашнє насильство')
    markup.add("🚸 ст. 184 Невиконання обов'язків", '🚷 Булінг')
    markup.add('🤪 ст. 173 Дрібне хуліганство', '🚬 ст. 175-1 Куріння')
    markup.add('📜 Постанови/Накази', '🧠 Алгоритми')
    markup.add('📊 Звіти', 'ℹ️ Про бота')
    markup.add('🚨 SOS (ТРИВОГА)')
    return markup

def get_reports_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add('📅 Щоденний звіт')
    markup.add('🔙 Головне меню')
    return markup

def get_daily_reports_inline():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("ЗЗСО №3", url=URL_ZZSO_3))
    markup.add(types.InlineKeyboardButton("ЗЗСО №48", url=URL_ZZSO_48))
    markup.add(types.InlineKeyboardButton("ЗЗСО №83", url=URL_ZZSO_83))
    markup.add(types.InlineKeyboardButton("ЗЗСО №88", url=URL_ZZSO_88))
    markup.add(types.InlineKeyboardButton("ЗЗСО №91", url=URL_ZZSO_91))
    markup.add(types.InlineKeyboardButton("ЗЗСО №105", url=URL_ZZSO_105))
    markup.add(types.InlineKeyboardButton("ЗЗСО №107", url=URL_ZZSO_107))
    markup.add(types.InlineKeyboardButton("ЗЗСО №124", url=URL_ZZSO_124))
    markup.add(types.InlineKeyboardButton("ЗЗСО №138", url=URL_ZZSO_138))
    markup.add(types.InlineKeyboardButton("ЗЗСО №152", url=URL_ZZSO_152))
    markup.add(types.InlineKeyboardButton("ЗЗСО №153", url=URL_ZZSO_153))
    markup.add(types.InlineKeyboardButton("ЗЗСО №173", url=URL_ZZSO_173))
    markup.add(types.InlineKeyboardButton("ЗЗСО Мобіль", url=URL_ZZSO_MOBIL))
    markup.add(types.InlineKeyboardButton("ЗЗСО Коротичанський ліцей", url=URL_ZZSO_KOROTYCH))
    markup.add(types.InlineKeyboardButton("ЗЗСО Джерело", url=URL_ZZSO_DZHERELO))
    return markup

def get_art178_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add('🍺 ч. 1 ст. 178 КУпАП', '🍻 ч. 2 ст. 178 КУпАП')
    markup.add('🍷 ч. 3 ст. 178 КУпАП', '🔙 Головне меню')
    return markup

def get_art122_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add('🛑 Порушення вимог дорожніх знаків', '🅿️ Порушення правил зупинки')
    markup.add('🚘 Порушення правил стоянки', '♿️ Зупинка/стоянка для осіб з інвалідністю')
    markup.add('🔙 Головне меню')
    return markup

def get_smoking_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add('🚬 ч. 1 ст. 175-1', '🚭 ч. 2 ст. 175-1')
    markup.add('🔙 Головне меню')
    return markup

def get_violence_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add('👶 Насильство відносно дитини / у присутності дитини')
    markup.add('🔙 Головне меню')
    return markup

def get_docs_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add('⚖️ КУпАП', '⚖️ Кримінальний кодекс')
    markup.add('⚖️ Сімейний кодекс', '👮 ЗУ Про Національну поліцію')
    markup.add('🎓 ЗУ Про освіту', '🏫 ЗУ Про загальну середню освіту')
    markup.add('👶 ЗУ Про охорону дитинства', '🏛 Постанова № 684')
    markup.add('🏛 Постанова № 1245', '🏛 Постанова № 70')
    markup.add('📋 Наказ № 663', '📋 Наказ № 1646')
    markup.add('📋 Наказ № 685/1013', '📋 Наказ № 1395')
    markup.add('📋 Наказ № 1376', '📋 Наказ № 70')
    markup.add('🔙 Головне меню')
    return markup

def get_algorithms_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add('🚨 Домашнє насильство')
    markup.add('💜 Сексуальне домагання')
    markup.add('💣 Алгоритм дій при виявленні ВНП')
    markup.add('💊 Дії у разі виявлення наркотичних речовин в учня')
    markup.add('🧑‍🎓 Дії у разі правопорушення особою від 16 до 18 років')
    markup.add('🎒 Дії у разі правопорушення особою від 14 до 16 років')
    markup.add('👶 Дії у разі правопорушення особою до 14 років')
    markup.add('🔙 Головне меню')
    return markup

# --- Inline-клавіатури для розділу "Домашнє насильство" ---

def dv_main_inline():
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_zzso = types.InlineKeyboardButton("🏫 В ЗЗСО", callback_data="dv_zzso")
    btn_home = types.InlineKeyboardButton("🏠 Вдома", callback_data="dv_home")
    markup.add(btn_zzso, btn_home)
    return markup

def back_to_dv_main_inline():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("⬅️ Назад до вибору локації", callback_data="dv_main"))
    return markup

# --- Inline-клавіатури для розділу "Булінг" ---

def bullying_main_inline():
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_alg = types.InlineKeyboardButton("📌 Алгоритм реагування", callback_data="bull_alg")
    markup.add(btn_alg)
    return markup

def bullying_alg_inline():
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_head = types.InlineKeyboardButton("🏛 Алгоритм керівника ЗЗСО", callback_data="bull_head")
    btn_actions = types.InlineKeyboardButton("📝 Подальші дії", callback_data="bull_actions")
    markup.add(btn_head, btn_actions)
    return markup

def bullying_actions_inline():
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_under_16 = types.InlineKeyboardButton("👶 До 16 років", callback_data="bull_under_16")
    btn_16_18 = types.InlineKeyboardButton("🧑 16–18 років", callback_data="bull_16_18")
    btn_over_18 = types.InlineKeyboardButton("👨 Від 18 років", callback_data="bull_over_18")
    btn_back = types.InlineKeyboardButton("⬅️ Назад до Алгоритму", callback_data="bull_alg")
    markup.add(btn_under_16, btn_16_18, btn_over_18, btn_back)
    return markup

def back_to_bull_alg_inline():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("⬅️ Назад до Алгоритму", callback_data="bull_alg"))
    return markup

def back_to_bull_actions_inline():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("⬅️ Назад до категорій віку", callback_data="bull_actions"))
    return markup

# --- Inline-клавіатури для розділу "Сексуальне домагання" ---

def sex_harass_main_inline():
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_16_18 = types.InlineKeyboardButton("🧒 16-18 років", callback_data="sh_16_18")
    btn_18_plus = types.InlineKeyboardButton("👨 18+ років", callback_data="sh_18_plus")
    btn_14_16 = types.InlineKeyboardButton("🎒 14-16 років", callback_data="sh_14_16")
    btn_under_14 = types.InlineKeyboardButton("👶 До 14 років", callback_data="sh_under_14")
    markup.add(btn_16_18, btn_18_plus, btn_14_16, btn_under_14)
    return markup

def back_to_sh_main_inline():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("⬅️ Назад до вибору віку", callback_data="sh_main"))
    return markup

# --- Основні обробники ---

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        f'Вітаю, {message.from_user.first_name}!\n'
        'Я ваш робочий помічник. Оберіть потрібний розділ меню нижче:',
        reply_markup=get_main_menu(),
    )

@bot.message_handler(
    func=lambda message: bool(message.text)
    and ('Головне меню' in message.text or message.text == '/menu')
)
def back_to_main_menu(message):
    bot.send_message(
        message.chat.id, 'Повертаємось до головного меню:', reply_markup=get_main_menu()
    )

# --- РОЗДІЛ: ЗВІТИ ---

@bot.message_handler(
    func=lambda message: bool(message.text) and 'Звіти' in message.text
)
def handle_reports_section(message):
    bot.send_message(
        message.chat.id,
        '📋 **Розділ подачі звітів**\nОберіть потрібну категорію:',
        reply_markup=get_reports_menu(),
        parse_mode='Markdown'
    )

@bot.message_handler(
    func=lambda message: bool(message.text) and 'Щоденний звіт' in message.text
)
def handle_daily_reports_select(message):
    bot.send_message(
        message.chat.id,
        '📅 **Оберіть ваш навчальний заклад (ЗЗСО) для подачі щоденного звіту:**',
        reply_markup=get_daily_reports_inline(),
        parse_mode='Markdown'
    )

# --- ОБРОБНИК SOS ---

@bot.message_handler(
    func=lambda message: bool(message.text) and 'SOS' in message.text
)
def handle_sos_alert(message):
    user = message.from_user

    if user.id in CUSTOM_NAMES:
        sender_name = CUSTOM_NAMES[user.id]
    else:
        full_name = f'{user.first_name} {user.last_name or ""}'.strip()
        sender_name = full_name if full_name else 'Невідомий користувач'

    username_str = f'@{user.username}' if user.username else 'не вказано'

    sos_text = (
        '🚨 <b>УВАГА! СИГНАЛ ТРИВОГИ (SOS)!</b> 🚨\n\n'
        f'👤 <b>Відправник:</b> {sender_name}\n'
        f'🆔 <b>ID:</b> <code>{user.id}</code>\n'
        f'🔗 <b>Профіль:</b> {username_str}\n\n'
        '⚠️ <b>Потрібна термінова допомога або реагування!</b>'
    )

    successful_sends = 0
    failed_sends = 0

    for recipient_id in SOS_RECIPIENTS:
        try:
            bot.send_message(recipient_id, sos_text, parse_mode='HTML')
            successful_sends += 1
        except Exception as e:
            failed_sends += 1
            print(f'❌ Помилка надсилання для ID {recipient_id}: {e}')

    status_msg = (
        f'🚨 <b>Сигнал SOS успішно передано!</b>\n\n✅ Доставлено в приват:'
        f' {successful_sends}'
    )
    if failed_sends > 0:
        status_msg += (
            f'\n⚠️ Не доставлено: {failed_sends} (користувач має натиснути /start у'
            ' боті)'
        )

    bot.reply_to(message, status_msg, parse_mode='HTML')

# --- РОЗДІЛ: АЛГОРИТМ ДІЙ ПРИ ДОМАШНЬОМУ НАСИЛЬСТВІ ---

@bot.message_handler(func=lambda message: bool(message.text) and '🚨 Домашнє насильство' in message.text)
def handle_domestic_violence_algorithm(message):
    text = (
        "<b>🚨 АЛГОРИТМ ДІЙ ІНСПЕКТОРА СОБ У РАЗІ ВИЯВЛЕННЯ ДОМАШНЬОГО НАСИЛЬСТВА</b>\n\n"
        "Оберіть де саме відбувається / було виявлено правопорушення:"
    )
    bot.send_message(message.chat.id, text, parse_mode="HTML", reply_markup=dv_main_inline())

@bot.callback_query_handler(func=lambda call: call.data.startswith("dv_"))
def handle_dv_callbacks(call):
    bot.answer_callback_query(call.id)

    if call.data == "dv_main":
        text = (
            "<b>🚨 АЛГОРИТМ ДІЙ ІНСПЕКТОРА СОБ У РАЗІ ВИЯВЛЕННЯ ДОМАШНЬОГО НАСИЛЬСТВА</b>\n\n"
            "Оберіть де саме відбувається / було виявлено правопорушення:"
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            parse_mode="HTML",
            reply_markup=dv_main_inline()
        )

    elif call.data == "dv_zzso":
        text = (
            "<b>🏫 Алгоритм дій інспектора СОБ у разі виявлення домашнього насильства в ЗЗСО</b>\n\n"
            "1. <b>ОБОВ'ЯЗКОВО ВМИКАЄМО БОДІ-КАМЕРУ</b>\n"
            "<b>Отримання інформації:</b>\n"
            "• Анонімно\n"
            "• Від учнів\n"
            "• Від батьків\n"
            "• Від вчителів\n"
            "• Від адміністрації школи\n"
            "• Особисто побачили\n"
            "• Через АІКОМ\n\n"
            "2. <b>Встановити учасників:</b>\n"
            "• Постраждала особа\n"
            "• Кривдник\n"
            "• Свідки (за наявності)\n\n"
            "3. <b>Форми домашнього насильства:</b>\n"
            "• Фізичне\n"
            "• Психологічне\n"
            "• Економічне\n"
            "• Сексуальне\n\n"
            "4. <b>Кваліфікуючі ознаки:</b>\n"
            "• Потерпіла особа належить до визначеного кола осіб (члени сім'ї)\n"
            "• Наслідки (фізичні або психологічні страждання, розлади здоров'я, втрата працездатності, погіршення якості життя потерпілої особи)\n\n"
            "5. <b>Повідомлення адміністрації школи та психолога</b>\n"
            "<b>Дії керівника ЗЗСО:</b>\n"
            "• Повідомити службу у справах дітей та соціальну службу\n"
            "• Забезпечити психологічну та соціально-педагогічну підтримку\n"
            "• Зберегти конфіденційність інформації\n\n"
            "6. <b>Повідомлення керівництва відділу СОБ</b>\n\n"
            "7. <b>Припинити правопорушення</b>\n\n"
            "8. <b>Запитати чи потрібна домедична/медична допомога:</b>\n"
            "• У разі необхідності надаємо домедичну допомогу чи викликаємо БШМД\n\n"
            "9. <b>Окремо спілкуємось з постраждалою особою та кривдником</b>\n\n"
            "10. <b>Проводимо опитування</b> (дитину опитуємо в присутності психолога)\n\n"
            "11. <b>Якщо підтверджується, подальші дії:</b>\n"
            "• Збирання доказів або будь-яких фактичних даних, які свідчать про вчинення правопорушення\n"
            "• Робимо реєстрацію на лінію 102\n"
            "• Складаємо матеріали згідно ст. 173-2 КУпАП\n"
            "• Пишемо електронний та письмовий рапорт\n\n"
            "<b>📎 ДО ПРОТОКОЛУ ДОДАЄТЬСЯ:</b>\n"
            "• Рапорт\n"
            "• Пояснення учасників події\n"
            "• ТЗП (якщо складався)\n"
            "• Відео з бодікамери\n"
            "• Копія паспорта\n"
            "• Інші фактичні дані"
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            parse_mode="HTML",
            reply_markup=back_to_dv_main_inline()
        )

    elif call.data == "dv_home":
        text = (
            "<b>🏠 Алгоритм дій інспектора СОБ у разі виявлення домашнього насильства, якщо це відбувається вдома</b>\n\n"
            "1. <b>Отримання інформації:</b>\n"
            "• Анонімно\n"
            "• Від учнів\n"
            "• Від батьків\n"
            "• Від вчителів\n"
            "• Від адміністрації школи\n"
            "• Особисто побачили\n"
            "• Через АІКОМ\n\n"
            "2. <b>Встановити учасників:</b>\n"
            "• Постраждала особа\n"
            "• Кривдник\n"
            "• Свідки (за наявності)\n\n"
            "3. <b>Форми домашнього насильства:</b>\n"
            "• Фізичне\n"
            "• Психологічне\n"
            "• Економічне\n"
            "• Сексуальне\n\n"
            "4. <b>Кваліфікуючі ознаки:</b>\n"
            "• Потерпіла особа належить до визначеного кола осіб (члени сім'ї)\n"
            "• Наслідки (фізичні або психологічні страждання, розлади здоров'я, втрата працездатності, погіршення якості життя потерпілої особи)\n\n"
            "5. <b>Повідомлення адміністрації школи та психолога</b>\n"
            "<b>Дії керівника ЗЗСО:</b>\n"
            "• Повідомити службу у справах дітей та соціальну службу\n"
            "• Забезпечити психологічну та соціально-педагогічну підтримку\n"
            "• Зберегти конфіденційність інформації\n\n"
            "6. <b>Повідомлення керівництва відділу СОБ</b>\n\n"
            "7. <b>Забезпечення безпеки постраждалої особи</b>\n\n"
            "8. <b>В присутності психолога опитати дитину</b>\n\n"
            "9. <b>Реєстрація на лінію 102</b> (за необхідності викликаємо БШМД) та повідомляємо СЮП, які повинні прибути на місце події\n\n"
            "10. <b>Документування:</b>\n"
            "• Відбираємо пояснення від вчителів, психолога, соціального педагога\n"
            "• Записуємо дані екіпажу патрульної поліції, працівника ювенальної превенції та БШМД, які працювали на місці події\n\n"
            "11. <b>Пишемо письмовий та електронний рапорт.</b>"
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            parse_mode="HTML",
            reply_markup=back_to_dv_main_inline()
        )

# --- РОЗДІЛ: СЕКСУАЛЬНЕ ДОМАГАННЯ ---

@bot.message_handler(func=lambda message: bool(message.text) and 'Сексуальне домагання' in message.text)
def handle_sex_harassment_section(message):
    text = (
        "<b>💜 РЕАГУВАННЯ НА ВИПАДКИ СЕКСУАЛЬНОГО ДОМАГАННЯ</b>\n\n"
        "📹 <b>УВІМКНУТИ БОДІКАМ</b>\n\n"
        "<b>Загальні кроки реагування:</b>\n"
        "1. Отримання інформації від учнів, вчителів тощо.\n"
        "2. Повідомити безпосереднє керівництво, адміністрацію ЗЗСО та батьків учасників події.\n"
        "3. Спільно з адміністрацією ЗЗСО провести опитування учасників події.\n"
        "4. Кваліфікувати правопорушення (встановити наявність відомостей кримінального чи адміністративного характеру).\n"
        "5. За наявності відомостей кримінального характеру повідомити чергового ВП та здійснити реєстрацію за лінією 102.\n"
        "6. У разі відсутності відомостей кримінального характеру:\n"
        "   <i>У всіх випадках намагатись знайти якомога більше доказів (свідків, відео з відеокамер).</i>\n\n"
        "<b>Оберіть вікову категорію правопорушника нижче:</b>"
    )
    bot.send_message(
        message.chat.id,
        text,
        parse_mode="HTML",
        reply_markup=sex_harass_main_inline()
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("sh_"))
def handle_sex_harassment_callbacks(call):
    bot.answer_callback_query(call.id)

    if call.data == "sh_main":
        text = (
            "<b>💜 РЕАГУВАННЯ НА ВИПАДКИ СЕКСУАЛЬНОГО ДОМАГАННЯ</b>\n\n"
            "📹 <b>УВІМКНУТИ БОДІКАМ</b>\n\n"
            "<b>Оберіть вікову категорію правопорушника нижче:</b>"
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            parse_mode="HTML",
            reply_markup=sex_harass_main_inline()
        )

    elif call.data == "sh_16_18":
        text = (
            "<b>🧒 ВІК ПРАВОПОРУШНИКА: 16-18 РОКІВ</b>\n\n"
            "В присутності батьків відібрати від нього пояснення (а також пояснення від батьків) "
            "та на загальних підставах скласти адміністративний протокол за <b>ст. 173-7 КУпАП</b>.\n\n"
            "<b>📝 ФАБУЛА:</b>\n"
            "<i>«25.05.2025 о 10 год. 00 хв. за адресою м. Харків вул. Садова буд. 75 гр. _________ 10.01.1979 р.н., "
            "перебуваючи у приміщенні КЗ ХЛ 138 ХМР допустив дії сексуального характеру щодо гр. _________ 10.09.2010 р.н., "
            "які полягали у принизливих вербальних висловлюваннях та непристойних жестах сексуального характеру, що принижувало "
            "гідність та створювало образливу, принизливу і психологічно дискомфортну обстановку, чим порушив вимоги ст. 1 ЗУ "
            "''Про забезпечення рівних прав та можливостей жінок та чоловіків'' та ч.2 ст. 54 ЗУ ''Про освіту''.»</i>\n\n"
            "<b>📎 ДО ПРОТОКОЛУ ДОДАЄТЬСЯ:</b>\n"
            "• Рапорт поліцейського\n"
            "• Пояснення (свідків, учасників події, правопорушника, потерпілого)\n"
            "• Відео з бодікамери\n"
            "• Копія паспорта (правопорушника)\n"
            "• Інші фактичні дані, які можуть свідчити про вчинення правопорушення (відео, фото, інше...)"
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            parse_mode="HTML",
            reply_markup=back_to_sh_main_inline()
        )

    elif call.data == "sh_18_plus":
        text = (
            "<b>👨 ВІК ПРАВОПОРУШНИКА: 18+ РОКІВ</b>\n\n"
            "Якщо правопорушнику 18+ років, відібрати пояснення та скласти протокол за <b>ст. 173-7 КУпАП</b>.\n\n"
            "<b>📝 ФАБУЛА:</b>\n"
            "<i>«25.05.2025 о 10 год. 00 хв. за адресою м. Харків вул. Садова буд. 75 гр. _________ 10.01.1979 р.н., "
            "перебуваючи у приміщенні КЗ ХЛ 138 ХМР допустив дії сексуального характеру щодо гр. _________ 10.09.2010 р.н., "
            "які полягали у принизливих вербальних висловлюваннях та непристойних жестах сексуального характеру, що принижувало "
            "гідність та створювало образливу, принизливу і психологічно дискомфортну обстановку, чим порушив вимоги ст. 1 ЗУ "
            "''Про забезпечення рівних прав та можливостей жінок та чоловіків'' та ч.2 ст. 54 ЗУ ''Про освіту''.»</i>\n\n"
            "<b>📎 ДО ПРОТОКОЛУ ДОДАЄТЬСЯ:</b>\n"
            "• Рапорт поліцейського\n"
            "• Пояснення (свідків, учасників події, правопорушника, потерпілого)\n"
            "• Відео з бодікамери\n"
            "• Копія паспорта (правопорушника)\n"
            "• Інші фактичні дані, які можуть свідчити про вчинення правопорушення (відео, фото, інше...)"
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            parse_mode="HTML",
            reply_markup=back_to_sh_main_inline()
        )

    elif call.data == "sh_14_16":
        text = (
            "<b>🎒 ВІК ПРАВОПОРУШНИКА: 14-16 РОКІВ</b>\n\n"
            "Якщо правопорушнику від 14 до 16 років, в присутності батьків відібрати пояснення від дитини та батьків, "
            "зробити копію свідоцтва про народження дитини, зробити копію паспорта батьків. "
            "Скласти протокол за <b>ч. 3 ст. 184 КУпАП</b>.\n\n"
            "<b>📝 ФАБУЛА:</b>\n"
            "<i>«25.05.2025 о 10 год. 00 хв. за адресою м. Харків вул. Садова 15 гр. _________ р.н., ухилився "
            "від належного виконання батьківських обов'язків внаслідок чого його син _________ 17.07.2012 р.н., "
            "перебуваючи у приміщенні КЗ ХЛ 153 ХМР вчинив правопорушення передбачене ч. 1 ст. 173-7 КУпАП, а саме показував "
            "нецензурні жести та словесно схиляв до сексуальних дій у бік гр. _________ 10.10.2010 р.н., що принижувало "
            "гідність та створювало образливу, принизливу і психологічно дискомфортну обстановку. Чим порушив ч. 1 ст. 150 Сімейного кодексу України.»</i>\n\n"
            "<b>📎 ДО ПРОТОКОЛУ ДОДАЄТЬСЯ:</b>\n"
            "• Рапорт поліцейського\n"
            "• Пояснення (свідків, учасників події, правопорушника, потерпілого)\n"
            "• Відео з бодікамери\n"
            "• Копія свідоцтва про народження\n"
            "• Копія паспорта (одного з батьків, або інших законних представників)"
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            parse_mode="HTML",
            reply_markup=back_to_sh_main_inline()
        )

    elif call.data == "sh_under_14":
        text = (
            "<b>👶 ВІК ПРАВОПОРУШНИКА: ДО 14 РОКІВ</b>\n\n"
            "Якщо правопорушник від 0 до 14 років, в присутності батьків відібрати пояснення від дитини, "
            "відібрати пояснення від батьків, зробити копію свідоцтва про народження дитини, копію паспорта батьків. "
            "Відносно матері (батька) правопорушника складається протокол за <b>ч. 1 ст. 184 КУпАП</b>.\n\n"
            "<b>📝 ФАБУЛА:</b>\n"
            "<i>«25.05.2025 о 10 год. 00 хв. за адресою м. Харків вул. Садова буд. 75 гр. _________ р.н., ухилився "
            "від належного виконання батьківських обов'язків, внаслідок чого його малолітній син _________ 26.10.2015 р.н., "
            "перебуваючи у приміщенні КЗ ХЛ 138 ХМР вчинив дії сексуального характеру щодо учня _________ 30.07.2015 р.н., "
            "які полягали у образливих рухах тіла та висловлюваннях сексуального характеру, що принижувало гідність та "
            "створювало образливу, принизливу і психологічно дискомфортну обстановку. Чим порушив ч. 1 ст. 150 Сімейного кодексу України.»</i>\n\n"
            "<b>📎 ДО ПРОТОКОЛУ ДОДАЄТЬСЯ:</b>\n"
            "• Рапорт поліцейського\n"
            "• Пояснення (свідків, учасників події, правопорушника, потерпілого)\n"
            "• Відео з бодікамери\n"
            "• Копія свідоцтва про народження\n"
            "• Копія паспорта (одного з батьків, або інших законних представників)"
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            parse_mode="HTML",
            reply_markup=back_to_sh_main_inline()
        )

# --- РОЗДІЛ: БУЛІНГ ---

@bot.message_handler(func=lambda message: bool(message.text) and 'Булінг' in message.text)
def handle_bullying_section(message):
    bot.send_message(
        message.chat.id,
        "<b>Розділ: Реагування на випадки булінгу</b>\n\nОберіть потрібний підрозділ:",
        parse_mode="HTML",
        reply_markup=bullying_main_inline()
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("bull_"))
def handle_bullying_callbacks(call):
    bot.answer_callback_query(call.id)

    if call.data == "bull_main":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="<b>Розділ: Реагування на випадки булінгу</b>\n\nОберіть потрібний підрозділ:",
            parse_mode="HTML",
            reply_markup=bullying_main_inline()
        )

    elif call.data == "bull_alg":
        text = (
            "<b>📌 АЛГОРИТМ ВИЯВЛЕННЯ ТА КВАЛІФІКАЦІЇ БУЛІНГУ</b>\n\n"
            "<b>1. ОБОВ'ЯЗКОВО ВМИКАЄМО БОДІКАМ Отримання інформації:</b>\n"
            "• Анонімно\n"
            "• Від учня\n"
            "• Від батьків\n"
            "• Від учителя\n"
            "• Від адміністрації школи\n"
            "• Через АІКОМ\n\n"
            "<b>2. Встановити учасників:</b>\n"
            "• Постраждала особа\n"
            "• Булер\n"
            "• Спостерігачі\n\n"
            "<b>3. Кваліфікуючі ознаки:</b>\n"
            "1. Систематичність (повторюваність)\n"
            "2. Наслідки\n"
            "3. Нерівність сил\n\n"
            "⚠️ <i>Якщо все вищеперераховане сходиться — далі працюємо за алгоритмом булінгу.\n"
            "Якщо НІ — проводимо профілактичні бесіди, заняття та можливе складання протоколу за ст. 184 КУпАП.</i>\n\n"
            "<b>📩 Повідомити керівника ЗЗСО (ОБОВ'ЯЗКОВО)</b>"
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            parse_mode="HTML",
            reply_markup=bullying_alg_inline()
        )

    elif call.data == "bull_head":
        text = (
            "<b>🏛 ПОВІДОМЛЕННЯ КЕРІВНИКА ЗЗСО ТА РОБОТА КОМІСІЇ</b>\n\n"
            "<b>Алгоритм керівника ЗЗСО:</b>\n"
            "1. <b>Невідкладно (не пізніше 1 доби):</b> Повідомлення поліції, служби у справах дітей та батьків керівником закладу.\n"
            "2. <b>Не пізніше 3 робочих днів:</b> Скликання керівником закладу засідання комісії з розгляду випадку булінгу з дня отримання заяви або повідомлення.\n"
            "3. <b>До 10 робочих днів:</b> Загальний строк проведення розслідування комісією та ухвалення рішень з дня отримання заяви.\n\n"
            "<b>Склад комісії з розгляду випадків булінгу (за наказом МОН № 1646):</b>\n"
            "Затверджується наказом керівника закладу освіти на постійній основі (має складатися з голови, заступника, секретаря та не менше ніж п'яти інших членів).\n\n"
            "<b>До складу входять:</b>\n"
            "• Голова комісії — керівник закладу освіти (директор)\n"
            "• Заступник голови та секретар комісії\n"
            "• Педагогічні працівники, у тому числі практичний психолог та соціальний педагог\n"
            "• Представники служби у справах дітей та центру соціальних служб для сім’ї, дітей та молоді (за згодою)\n\n"
            "<b>До участі в засіданні залучаються:</b> Батьки або інші законні представники сторін булінгу, самі сторони (за потреби), а також інші суб'єкти реагування (зокрема представники ювенальної превенції / поліції)."
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            parse_mode="HTML",
            reply_markup=back_to_bull_alg_inline()
        )

    elif call.data == "bull_actions":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="<b>📝 Подальші дії після засідання комісії</b>\n\nОберіть вікову категорію правопорушника:",
            parse_mode="HTML",
            reply_markup=bullying_actions_inline()
        )

    elif call.data == "bull_under_16":
        text = (
            "<b>👶 ПОДАЛЬШІ ДІЇ — ДО 16 РОКІВ</b>\n\n"
            "1. Збирання доказів або будь-яких фактичних даних, які свідчать про вчинення правопорушення (пояснення від всіх учасників, фото/відео докази).\n"
            "2. Складаємо протокол за <b>ч. 3-4 ст. 173-4 КУпАП на батьків</b> (або інших законних представників: переконатись в правильності документів).\n\n"
            "<b>📝 ФАБУЛА:</b>\n"
            "<i>«15.05.2025 о 10год.00хв. знаходячись за адресою вул.Світла,2, гр.(ПІБ), не здійснив належного контролю за поведінкою свого сина (ПІБ), 25.05.2016 р.н., який в приміщенні КЗ Харківський ліцей №153 Харківської міської ради вчинив булінг фізичного та психологічного характеру відносно свого однокласника Фролова І.І., 23.03.2015 р.н., а саме штовхав його та виражався нецензурною лайкою в його бік, подія відбувається систематично. Чим було завдано шкоди психологічному та фізичному здоров'ю потерпілого.»</i>\n\n"
            "<b>📎 ДО ПРОТОКОЛУ ДОДАЄТЬСЯ:</b>\n"
            "1. РАПОРТ\n"
            "2. ПРОТОКОЛ ЗАСІДАННЯ (копія)\n"
            "3. ПОЯСНЕННЯ УЧАСНИКІВ ПОДІЇ\n"
            "4. ВІДЕО З Б/К\n"
            "5. КОПІЇ СВІДОЦТВА ПРО НАРОДЖЕННЯ (ПРАВОПОРУШНИКА)\n"
            "6. КОПІЇ ПАСПОРТА (БАТЬКІВ)\n"
            "7. Інші фактичні дані, які можуть свідчити про вчинення правопорушення (відео, фото, інше...)\n\n"
            "⚠️ <b>НЕ ЗАБУВАЄМО ЕЛЕКТРОННИЙ РАПОРТ В ЧАТ</b>"
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            parse_mode="HTML",
            reply_markup=back_to_bull_actions_inline()
        )

    elif call.data == "bull_16_18":
        text = (
            "<b>🧑 ПОДАЛЬШІ ДІЇ — 16-18 РОКІВ</b>\n\n"
            "1. Збирання доказів або будь-яких фактичних даних, які свідчать про вчинення правопорушення (пояснення від всіх учасників, фото/відео докази).\n"
            "2. Складання протоколу за <b>ч. 1 ст. 173-4 КУпАП на особу правопорушника</b> (в присутності батьків).\n\n"
            "<b>📝 ФАБУЛА:</b>\n"
            "<i>«25.05.2025 о 10год. 00хв. за адресою вул. Світла,2, гр. (ПІБ)., вчинив булінг психологічного та фізичного характеру відносно учня (ПІБ), а саме штовхав та виражався нецензурною лайкою, подія відбувається систематично. Чим було завдано шкоди психологічного та фізичного характеру потерпілого.»</i>\n\n"
            "<b>📎 ДО ПРОТОКОЛУ ДОДАЄТЬСЯ:</b>\n"
            "1. РАПОРТ\n"
            "2. ПРОТОКОЛ ЗАСІДАННЯ\n"
            "3. ПОЯСНЕННЯ УЧАСНИКІВ ПОДІЇ\n"
            "4. ВІДЕО З Б/К\n"
            "5. КОПІЯ ПАСПОРТА (ПРАВОПОРУШНИКА)\n"
            "7. Інші фактичні дані, які можуть свідчити про вчинення правопорушення (відео, фото, інше...)\n\n"
            "⚠️ <b>НЕ ЗАБУВАЄМО ЕЛЕКТРОННИЙ РАПОРТ В ЧАТ</b>"
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            parse_mode="HTML",
            reply_markup=back_to_bull_actions_inline()
        )

    elif call.data == "bull_over_18":
        text = (
            "<b>👨 ПОДАЛЬШІ ДІЇ — ВІД 18 РОКІВ</b>\n\n"
            "1. Збирання доказів або будь-яких фактичних даних, які свідчать про вчинення правопорушення (пояснення від всіх учасників, фото/відео докази).\n"
            "2. Складання протоколу за <b>ч. 1 ст. 173-4 КУпАП на особу правопорушника</b>.\n\n"
            "<b>📝 ФАБУЛА:</b>\n"
            "<i>«25.05.2025 о 10год. 00хв. за адресою вул. Світла,2, гр. (ПІБ), вчинив булінг психологічного та фізичного характеру відносно учня (ПІБ), а саме штовхав та виражався нецензурною лайкою, подія відбувається систематично. Чим було завдано шкоди психологічного та фізичного характеру потерпілого.»</i>\n\n"
            "<b>📎 ДО ПРОТОКОЛУ ДОДАЄТЬСЯ:</b>\n"
            "1. РАПОРТ\n"
            "2. ПРОТОКОЛ ЗАСІДАННЯ\n"
            "3. ПОЯСНЕННЯ УЧАСНИКІВ ПОДІЇ\n"
            "4. ВІДЕО З Б/К\n"
            "5. КОПІЯ ПАСПОРТА (ПРАВОПОРУШНИКА)\n"
            "7. Інші фактичні дані, які можуть свідчити про вчинення правопорушення (відео, фото, інше...)\n\n"
            "⚠️ <b>НЕ ЗАБУВАЄМО ЕЛЕКТРОННИЙ РАПОРТ В ЧАТ</b>"
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            parse_mode="HTML",
            reply_markup=back_to_bull_actions_inline()
        )

# --- КУпАП: ст. 127 ---

@bot.message_handler(
    func=lambda message: bool(message.text)
    and ('127' in message.text or 'пішоходами' in message.text.lower())
)
def art127_info(message):
    text = (
        '🚶 **ПРИКЛАД ФАБУЛИ ЗА ч.1 ст. 127 КУпАП (Пішохід)**\n\n'
        '• 11.04.2023р. о 12 год. 00 хв. в м. Рівне по вул. Соборна 10 пішохід'
        ' рухався по проїзній частині (велосипедній доріжці), коли поруч знаходився'
        ' тротуар (пішохідна доріжка), чим порушив п.4.1 ПДР.\n\n'
        '• 11.04.2023р. о 22 год. 00 хв. в м. Рівне по вул. Соборна 10 пішохід'
        ' рухаючись по проїзній частині (узбіччі) в темну пору доби (в умовах'
        ' недостатньої видимості) не використовував світлоповертальні елементи та'
        ' був в одязі, який не має світлоповертальні елементи, чим порушив п.4.4'
        ' ПДР.\n\n'
        '• 11.04.2023р. о 22 год. 00 хв. в м. Рівне по вул. Соборна 10 пішохід'
        ' перейшов проїзну частину у невстановленому місці, а саме поза'
        ' пішохідним переходом, чим порушив п.4.7 ПДР.\n\n'
        '• 11.04.2023р. о 22 год. 00 хв. в м. Рівне по вул. Соборна 10 пішохід'
        ' раптово вийшов на проїзну частину не переконавшись у відсутності'
        ' транспортних засобів, що наближаються, перейшовши проїзну частину'
        ' безпосередньо перед транспортним засобом, чим порушив п.4.10 та п.4.14а'
        ' ПДР.'
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

# --- КУпАП: ст. 122 ---

@bot.message_handler(
    func=lambda message: bool(message.text)
    and ('122' in message.text or 'ст. 122 ПДР' in message.text)
    and not any(
        x in message.text
        for x in [
            'знаків',
            'правил зупинки',
            'правил стоянки',
            'інвалідністю',
        ]
    )
)
def art122_category_select(message):
    bot.send_message(
        message.chat.id,
        '🚘 **ст. 122 КУпАП — Порушення ПДР**\nОберіть категорію правопорушення:',
        reply_markup=get_art122_menu(),
        parse_mode='Markdown',
    )

@bot.message_handler(
    func=lambda message: bool(message.text)
    and 'Порушення вимог дорожніх знаків' in message.text
)
def art122_signs_info(message):
    text = (
        '🛑 **Порушення вимог дорожніх знаків (ст. 122 КУпАП)**\n\n'
        '11.04.2023р. о 12 год. 00 хв. в м. Рівне по вул. Соборна 10 водій керуючи'
        ' транспортним засобом ЗАЗ 969, НЗ АА0101АА, порушив вимогу дорожнього'
        ' знака:\n\n'
        '• **3.1 «Рух заборонено»**, а саме здійснив рух в зону дії знака, чим'
        ' порушив п.3.1, додатку 1, розділу 34 ПДР.\n'
        '• керуючи механічним транспортним засобом ЗАЗ 969, НЗ АА0101АА, порушив'
        ' вимогу дорожнього знаку **3.2 «Рух механічних транспортних засобів'
        ' заборонено»**, а саме здійснив рух в зону дії знака, чим порушив'
        ' п.3.2, додатку 1, розділу 34 ПДР.\n'
        '• **3.21 «В’їзд заборонено»**, а саме здійснив в’їзд в зону дії знака,'
        ' чим порушив п.3.21, додатку 1, розділу 34 ПДР.\n'
        '• **3.34 «Зупинку заборонено»**, а саме здійснив зупинку в зоні дії'
        ' знака, чим порушив п.3.34, додатку 1, розділу 34 ПДР.\n'
        '• **3.35 «Стоянку заборонено»**, а саме здійснив стоянку в зоні дії'
        ' знака, чим порушив п.3.35, додатку 1, розділу 34 ПДР.'
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(
    func=lambda message: bool(message.text)
    and 'Порушення правил зупинки' in message.text
)
def art122_stopping_info(message):
    text = (
        '🅿️ **Порушення правил зупинки (ст. 122 КУпАП)**\n\n'
        '11.04.2023р. о 12 год. 00 хв. в м. Рівне по вул. Соборна 10 водій керуючи'
        ' транспортним засобом ЗАЗ 969, НЗ АА0101АА, порушив правила зупинки, а'
        ' саме здійснив зупинку:\n\n'
        '• **на пішохідному переході** (на відстані 8м. від пішохідного переходу),'
        ' чим порушив п.15.9г ПДР.\n'
        '• **на перехресті** (на відстані 8м. від края перехрещуваної проїзної'
        ' частини), чим порушив п.15.9ґ ПДР.\n'
        '• **на відстані 25м., від посадкового майданчику** для зупинки'
        ' маршрутних транспортних засобів, чим порушив п.15.9е ПДР.\n'
        '• **безпосередньо в місці** (на відстані 8м. від) виїзду з прилеглої'
        ' території, чим порушив п.15.9и ПДР.\n'
        '• **у другому ряді** (поруч з іншим транспортним засобом, який стоїть'
        ' біля краю проїзною частини (на узбіччі)), чим порушив п.15.4 ПДР.'
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(
    func=lambda message: bool(message.text)
    and 'Порушення правил стоянки' in message.text
)
def art122_parking_info(message):
    text = (
        '🚘 **ПРИКЛАД ФАБУЛИ ЗА ч. 1 ст. 122 КУпАП (Порушення правил'
        ' стоянки)**\n\n'
        '11.04.2023р. о 12 год. 00 хв. в м. Рівне по вул. Соборна 10 водій керуючи'
        ' транспортним засобом ЗАЗ 969, НЗ АА0101АА, порушив правила стоянки, а'
        ' саме здійснив стоянку:\n'
        '• на тротуарі, де для руху пішоходів залишається менше 1.5 метри, чим'
        ' порушив п.15.10в ПДР.\n'
        '• на відстані 4 метри від контейнерів (контейнерних майданчиків) для'
        ' збирання побутових відходів, чим порушив п.15.10е ПДР.\n'
        '• на газонах, чим порушив п.15.10є ПДР.\n\n'
        '───────────────────\n\n'
        '11.04.2023р. о 12 год. 00 хв. в м. Рівне по вул. Соборна 10 водій керуючи'
        ' вантажним транспортним засобом ЗИЛ 130, НЗ АА0101АА, порушив правила'
        ' стоянки, а саме здійснив стоянку на тротуарі, чим порушив п.15.10б'
        ' ПДР.'
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(
    func=lambda message: bool(message.text)
    and 'Зупинка/стоянка для осіб з інвалідністю' in message.text
)
def art122_disability_info(message):
    text = (
        '♿️ **Зупинка/стоянка на місцях для осіб з інвалідністю (ст. 122'
        ' КУпАП)**\n\n'
        '11.04.2023р. о 12 год. 00 хв. в м. Рівне по вул. Соборна 10 водій керуючи'
        ' транспортним засобом ЗАЗ 969, НЗ АА0101АА:\n\n'
        '• здійснив зупинку (стоянку) у місці, що позначено **дорожнім знаком'
        ' 5.42.1 (5.42.2) «Місце для стоянки» (5.43 «Зона стоянки») з табличкою'
        ' 7.17 «Особи з інвалідністю»**, не будучи при цьому особою, визначеною'
        ' ЗУ «Про основи соціальної захищеності інвалідів в Україні», а також не'
        ' перевозивши таких осіб, чим порушив п.15.1 та п.5.42.1 додатку 1,'
        ' р.33 ПДР.\n\n'
        '• здійснив зупинку (стоянку) у місці, що позначено **дорожньою розміткою'
        ' 1.35**, яка позначає місця для паркування транспорту осіб з'
        ' інвалідністю, не будучи при цьому особою, визначеною ЗУ «Про основи'
        ' соціальної захищеності інвалідів в Україні», а також не перевозивши'
        ' таких осіб, чим порушив п.15.1 та п.1.35 додатку 2, розділу 34 ПДР.'
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

# --- КУпАП: ст. 178 ---

@bot.message_handler(
    func=lambda message: bool(message.text)
    and ('178' in message.text or 'Алкоголь' in message.text)
    and not any(x in message.text for x in ['ч. 1', 'ч. 2', 'ч. 3'])
)
def art178_category_select(message):
    bot.send_message(
        message.chat.id,
        '🍻 **ст. 178 КУпАП — Розпивання алкоголю / Поява у п’яному вигляді**\n\n'
        'Оберіть частину статті для перегляду фабул:',
        reply_markup=get_art178_menu(),
        parse_mode='Markdown',
    )

@bot.message_handler(
    func=lambda message: bool(message.text)
    and 'ч. 1' in message.text
    and '178' in message.text
)
def art178_part1_info(message):
    text = (
        '🍺 **ПРИКЛАДИ ФАБУЛ ЗА Ч. 1 ст. 178 КУпАП**\n\n'
        '📌 **1. Поява у п’яному вигляді:**\n'
        '21.11.2016 об 17.00 у м.Київ, Солом’янський р-н, по вул. Донецька 10, гр.'
        ' (ПІБ) біля (зупинки громадського транспорту, під’їзд житлового'
        ' будинку, громадському транспорті, дитячому майданчику, школа, лікарня,'
        ' аптека, магазин, на вулицях, у закритих спортивних спорудах, у скверах,'
        ' парках, та інше) перебував у п’яному вигляді (ішов та хитався, мав'
        ' неохайний зовнішній вигляд, брудний, мокрий одяг, безцільно пересувається'
        ' з місця на місце, нечітка мова, лежав на землі,) чим ображав людську'
        ' гідність та громадську мораль.\n\n'
        '───────────────────\n\n'
        '📌 **2. Розпивання:**\n'
        '21.11.2016 об 17.00 у м.Київ, Солом’янський р-н, по вул. Донецька 10, гр.'
        ' (ПІБ) біля (зупинки громадського транспорту, під’їзд житлового'
        ' будинку, громадському транспорті, дитячому майданчику, школа, лікарня,'
        ' аптека, магазин, на вулицях, у закритих спортивних спорудах, у скверах,'
        ' парках, та інше) розпивав пиво «Оболонь», ємкістю 0,5 л. (алкогольний'
        ' напій – горілка «Державна», слабоалкогольний напій – «Бірмікс»).'
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(
    func=lambda message: bool(message.text)
    and 'ч. 2' in message.text
    and '178' in message.text
)
def art178_part2_info(message):
    text = (
        '🍻 **ПРИКЛАДИ ФАБУЛ ЗА Ч. 2 ст. 178 КУпАП (Повторно протягом'
        ' року)**\n\n'
        '📌 **1. Поява у п’яному вигляді (повторність):**\n'
        '21.11.2016 об 17.00 у м.Київ, Солом’янський р-н, по вул. Донецька 10, гр.'
        ' (ПІБ) біля (зупинки громадського транспорту, під’їзд житлового'
        ' будинку, громадському транспорті, дитячому майданчику, школа, лікарня,'
        ' аптека, магазин, на вулицях, у закритих спортивних спорудах, у скверах,'
        ' парках, та інше) перебував у п’яному вигляді (ішов та хитався, мав'
        ' неохайний зовнішній вигляд, брудний, мокрий одяг, безцільно пересувається'
        ' з місця на місце, нечітка мова, лежав на землі,) чим ображав людську'
        ' гідність та громадську мораль, чим вчинив повторно порушення протягом'
        ' року.\n\n'
        '───────────────────\n\n'
        '📌 **2. Розпивання (повторність):**\n'
        '21.11.2016 об 17.00 у м.Київ, Солом’янський р-н, по вул. Донецька 10, гр.'
        ' (ПІБ) біля (зупинки громадського транспорту, під’їзд житлового'
        ' будинку, громадському транспорті, дитячому майданчику, школа, лікарня,'
        ' аптека, магазин, на вулицях, у закритих спортивних спорудах, у скверах,'
        ' парках, та інше) розпивав пиво «Оболонь», ємкістю 0,5 л. (алкогольний'
        ' напій – горілка «Державна», слабоалкогольний напій – «Бірмікс»), чим'
        ' вчинив повторно порушення протягом року.'
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(
    func=lambda message: bool(message.text)
    and 'ч. 3' in message.text
    and '178' in message.text
)
def art178_part3_info(message):
    text = (
        '🍷 **ПРИКЛАДИ ФАБУЛ ЗА Ч. 3 ст. 178 КУпАП (Двічі піддавався стягненню'
        ' протягом року)**\n\n'
        '📌 **1. Поява у п’яному вигляді:**\n'
        '21.11.2016 об 17.00 у м.Київ, Солом’янський р-н, по вул. Донецька 10, гр.'
        ' (ПІБ) біля (зупинки громадського транспорту, під’їзд житлового'
        ' будинку, громадському транспорті, дитячому майданчику, школа, лікарня,'
        ' аптека, магазин, на вулицях, у закритих спортивних спорудах, у скверах,'
        ' парках, та інше) перебував у п’яному вигляді (ішов та хитався, мав'
        ' неохайний зовнішній вигляд, брудний, мокрий одяг, безцільно пересувається'
        ' з місця на місце, нечітка мова, лежав на землі,) чим ображав людську'
        ' гідність та громадську мораль, та двічі протягом року піддавався'
        ' адміністративному стягненню.\n\n'
        '───────────────────\n\n'
        '📌 **2. Розпивання:**\n'
        '21.11.2016 об 17.00 у м.Київ, Солом’янський р-н, по вул. Донецька 10, гр.'
        ' (ПІБ) біля (зупинки громадського транспорту, під’їзд житлового'
        ' будинку, громадському транспорті, дитячому майданчику, школа, лікарня,'
        ' аптека, магазин, на вулицях, у закритих спортивних спорудах, у скверах,'
        ' парках, та інше) розпивав пиво «Оболонь», ємкістю 0,5 л. (алкогольний'
        ' напій – горілка «Державна», слабоалкогольний напій – «Бірмікс»), та'
        ' двічі протягом року піддавався адміністративному стягненню.'
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

# --- КУпАП: ст. 175-1 ---

@bot.message_handler(
    func=lambda message: bool(message.text)
    and ('175-1' in message.text or 'Куріння' in message.text)
    and 'ч. 1' not in message.text
    and 'ч. 2' not in message.text
)
def smoking_category_select(message):
    bot.send_message(
        message.chat.id,
        'Оберіть частину ст. 175-1 КУпАП для перегляду фабули та нормативної'
        ' бази:',
        reply_markup=get_smoking_menu(),
    )

@bot.message_handler(
    func=lambda message: bool(message.text)
    and ('ч. 1' in message.text or 'ч.1' in message.text or 'ч 1' in message.text)
    and '175-1' in message.text
)
def smoking_part1_info(message):
    text = (
        '🚬 **ч. 1 ст. 175-1 КУпАП — Куріння тютюнових виробів у заборонених'
        ' місцях**\n\n'
        '📜 **Закон України від 22.09.2005 № 2899-IV.**\n\n'
        '⚖️ **Приклад фабули:**\n'
        '21.11.2016 об 17.00 у м. Рівному по вул. Київській, гр. (ПІБ) біля'
        ' (зупинки громадського транспорту, під’їзд житлового будинку,'
        ' громадському транспорті, дитячому майданчику, школа, лікарня, аптека,'
        ' магазин та інше) курив тютюновий виріб - сигарети «Море», у місці де це'
        ' заборонено Законом від 22.09.2005 № 2899-IV.\n\n'
        '───────────────────\n\n'
        "🏛 **Громадське місце** - частина (частини) будь-якої будівлі, споруди, яка доступна або відкрита для населення вільно, чи за запрошенням, або за плату, постійно, періодично або час від часу, в том числі під'їзди, а також підземні переходи, стадіони.\n\n"
        '📌 **Стаття 13 Закону № 2899-IV:**\n'
        '1) у ліфтах і таксофонах;\n'
        '2) у приміщеннях та на території закладів охорони здоров’я;\n'
        '3) у приміщеннях та на території навчальних закладів;\n'
        '4) на дитячих майданчиках;\n'
        '5) у приміщеннях та на території спортивних і фізкультурно-оздоровчих'
        ' споруд та закладів фізичної культури і спорту;\n'
        '6) у під’їздах житлових будинків;\n'
        '7) у підземних переходах;\n'
        '8) у транспорті загального користування, що використовується для'
        ' перевезення пасажирів;\n'
        '9) у приміщеннях закладів ресторанного господарства;\n'
        '10) у приміщеннях об’єктів культурного призначення;\n'
        '11) у приміщеннях органів державної влади та органів місцевого'
        ' самоврядування, інших державних установ;\n'
        '12) на стаціонарно обладнаних зупинках маршрутних транспортних засобів.\n\n'
        '⛔️ **За забороняється, крім спеціально відведених для цього місць,'
        ' куріння тютюнових виробів:**\n'
        '1) у приміщеннях підприємств, установ та організацій усіх форм'
        ' власності;\n'
        '2) у приміщеннях готелів та аналогічних засобів розміщення громадян;\n'
        '3) у приміщеннях гуртожитків;\n'
        '4) в аеропортах та на вокзалах.'
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(
    func=lambda message: bool(message.text)
    and ('ч. 2' in message.text or 'ч.2' in message.text or 'ч 2' in message.text)
    and '175-1' in message.text
)
def smoking_part2_info(message):
    text = (
        '🚭 **ч. 2 ст. 175-1 КУпАП — Повторне протягом року вчинення'
        ' правопорушення**\n\n'
        '⚖️ **Приклад фабули:**\n'
        '21.11.2016 об 17.00 у м. Рівному по вул. Київській, гр. (ПІБ) біля'
        ' (зупинки громадського транспорту, під’їзд житлового будинку,'
        ' громадському транспорті, дитячому майданчику, школа, лікарня, аптека,'
        ' магазин та інше) курив тютюновий виріб - сигарети «Море», у місці де це'
        ' заборонено Законом від 22.09.2005 № 2899-IV, чим повторно вчинив'
        ' правопорушення.'
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

# --- Алгоритми ---

@bot.message_handler(
    func=lambda message: bool(message.text) and 'Алгоритми' in message.text
)
def algorithms_category_select(message):
    bot.send_message(
        message.chat.id,
        'Оберіть потрібний алгоритм дій:',
        reply_markup=get_algorithms_menu(),
    )

@bot.message_handler(
    func=lambda message: bool(message.text) and 'виявленні ВНП' in message.text
)
def explosives_algorithm_info(message):
    text = (
        "💣 <b>При виявленні ВНП потрібно діяти за наступним алгоритмом та обов'язково увімкнути БОДІКАМ:</b>\n\n"
        "1. <b>Власна безпека:</b>\n"
        "   • не наближатись;\n"
        "   • використовувати засоби індивідуального захисту (бронежилет, каска) та мати при собі аптечку;\n"
        "   • категорично заборонено торкатися та пересувати предмет.\n\n"
        "2. <b>Забезпечити охорону місця події:</b>\n"
        "   • огородити місце події;\n"
        "   • не допускати сторонніх осіб.\n\n"
        "3. <b>Негайне інформування:</b>\n"
        "   • повідомити керівника ЗЗСО;\n"
        "   • повідомити безпосереднього керівника;\n"
        "   • повідомити ЧЧ КУПОЛ;\n"
        "   • повідомити ЧЧ (ВП ХРУП);\n"
        "   • потрібно зробити реєстрацію на лінію 102.\n\n"
        "4. <b>Організація евакуації:</b>\n"
        "   • за вказівкою керівника ЗЗСО (якщо цього вимагає ситуація, за погодженням керівника ЗЗСО) провести організовану евакуацію учнів та персоналу;\n"
        "   • діяти згідно з розробленим та затвердженим планом евакуації та алгоритмом дій у разі нападу або ризику нападу.\n\n"
        "5. <b>Здійснювати охорону місця події до прибуття СОГ та вибухотехніків.</b>\n\n"
        "6. <b>Далі діяти за їх вказівкою до завершення події.</b>\n\n"
        "7. <b>Зафіксувати, хто працював на місці (старшого СОГ, представника ДСНС, екіпажа ПП та інші).</b>\n\n"
        "8. <b>Подача електронного рапорта в групу.</b>\n\n"
        "9. <b>В планшеті з додаванням фотографій, осіб, речей та дій.</b>\n\n"
        "10. <b>За потреби письмовий рапорт.</b>"
    )
    
    markup = types.InlineKeyboardMarkup()
    btn_report = types.InlineKeyboardButton("📋 Приклад рапорту", callback_data="vnp_report_example")
    markup.add(btn_report)
    
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=markup)

# --- Callback обробник для прикладу рапорту ВНП ---

@bot.callback_query_handler(func=lambda call: call.data == "vnp_report_example")
def handle_vnp_report_example(call):
    bot.answer_callback_query(call.id)
    text = (
        "📋 <b>ПРИКЛАД РАПОРТУ (ВНП)</b>\n\n"
        "<b>СОБ 107</b>\n"
        "Вул. Академіка Барабашова, 38Б.\n\n"
        "04.05.2026 близько 09 год 45 хв до інспектора СОБ звернувся технічний працівник ЗЗСО, "
        "який повідомив, що помітив підозрілий предмет біля школи. Інспектором було здійснено "
        "додатковий обхід території та у клумбі навпроти входу до ЗЗСО було виявлено предмет "
        "за зовнішніми ознаками схожий на СВП. Про подію було проінформовано директора Харківського "
        "ліцею № 107 Єсауленко Світлану Володимирівну. Інспектором СОБ було огороджено місце події "
        "та вжито усіх необхідних заходів задля забезпечення безпеки усіх учасників освітнього процесу. "
        "Про виявлення предмету було повідомлено ЧЧ УПП в Х/о ДПП, ЧЧ ХРУП 1 та сповіщено на лінію 102.\n\n"
        "На місці працювали екіпаж КУПОЛ 1202, СОГ ХРУП 1 капітан поліції Лучкін В. В., ДСНС начальник "
        "ДПРЧ 18 підполковник ДСНС Завірюха, ВТС - старший інспектор ВЗВ УВТМ Лемішка О. А., СБУ.\n\n"
        "За результатами перевірки вибухонебезпечних предметів не виявлено. Об'єктом була батарейка 18650 "
        "з перемикачем.\n\n"
        "<b>ЄО 14051 ХРУП 1.</b>"
    )
    bot.send_message(call.message.chat.id, text, parse_mode="HTML")

# --- АЛГОРИТМ: ДІЇ У РАЗІ ВИЯВЛЕННЯ НАРКОТИЧНИХ РЕЧОВИН ---

@bot.message_handler(
    func=lambda message: bool(message.text) and 'наркотичних речовин' in message.text.lower()
)
def drugs_algorithm_info(message):
    text = (
        "🚨 <b>УВАГА! ПОВЕРХНЕВА ПЕРЕВІРКА ОСІБ, ЯКІ НЕ ДОСЯГЛИ 18 РОКІВ, ЗАБОРОНЕНА!</b>\n\n"
        "1. Увімкнути бодікамеру у разі надходження інформації про наявність заборонених речовин у учнів ЗЗСО.\n"
        "2. Повідомити класного керівника та директора, спільно з ними необхідно провести бесіду та наполягати на добровільній видачі."
    )
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_voluntary = types.InlineKeyboardButton("✅ У разі добровільної видачі", callback_data="drugs_voluntary")
    btn_refusal = types.InlineKeyboardButton("❌ Відмова від добровільної видачі", callback_data="drugs_refusal")
    markup.add(btn_voluntary, btn_refusal)
    
    bot.send_message(message.chat.id, text, parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("drugs_"))
def handle_drugs_callbacks(call):
    bot.answer_callback_query(call.id)
    
    if call.data == "drugs_voluntary":
        text = (
            "✅ <b>У разі добровільної видачі:</b>\n\n"
            "1. Повідомити безпосереднього керівника, викликати батьків та СОГ.\n"
            "2. Здійснювати охорону місця подій та чекати на їх прибуття.\n\n"
            "<b>Документування:</b>\n"
            "• Внести всі відомості до ІПНП (електронний рапорт, додати річ, особа, дія, фото).\n"
            "• Написати письмовий рапорт. У рапорті з дитиною прописуємо Прізвище, ім'я, по батькові, "
            "дата народження, контактний телефон дитини, місце проживання (фактичне), "
            "інформація про батьків (телефон, місце проживання, дата народження, контактний телефон, місце проживання (фактичне))."
        )
        bot.send_message(call.message.chat.id, text, parse_mode="HTML")
        
    elif call.data == "drugs_refusal":
        text = (
            "❌ <b>У разі відмови від добровільної видачі:</b>\n\n"
            "Викликати батьків (або законних представників) для того, щоб вони самостійно перевірили наявність заборонених речовин у власної дитини.\n\n"
            "<b>Дії при відмові дитини від добровільної видачі заборонених речовин:</b>\n"
            "• Очікувати прибуття батьків на місце події, при прибутті батьків наполягати на тому, щоб вони перевірили речі дитини на наявність заборонених речовин.\n"
            "• У разі наявності такої речовини повідомити безпосереднього керівника або старшого з ОД.\n"
            "• Зробити реєстрацію на 102 та очікувати прибуття СОГ.\n\n"
            "<b>Документування:</b>\n"
            "• Внести всі відомості до ІПНП (електронний рапорт, додати річ, особа, дія, фото).\n"
            "• Написати письмовий рапорт. У рапорті з дитиною прописуємо Прізвище, ім'я, по батькові, "
            "дата народження, контактний телефон дитини, місце проживання (фактичне), "
            "інформація про батьків (телефон, місце проживання, дата народження, контактний телефон, місце проживання (фактичне))."
        )
        bot.send_message(call.message.chat.id, text, parse_mode="HTML")

@bot.message_handler(
    func=lambda message: bool(message.text)
    and 'від 16 до 18 років' in message.text
)
def over16_algorithm_info(message):
    text = (
        '🧑‍🎓 **Фіксування адміністративного правопорушення, вчиненого'
        ' неповнолітнім, віком від 16 до 18 років**\n\n'
        '📌 *Примітка: складається протокол на неповнолітнього*\n\n'
        '• **Фіксація правопорушення**, збирання доказів або отримання будь-яких'
        ' фактичних даних, які свідчать про вчинення правопорушення.\n'
        '*(Примітка: реєстрація події — потрібно уточнювати)*\n'
        '• **Встановлення особи** (учень якого класу, хто класний керівник).\n'
        '• **Повідомити** адміністрацію навчального закладу, безпосереднього'
        ' керівника СОБ, батьків (запросити до навчального закладу).\n'
        '• **За згодою батьків** або інших законних представників та у їх'
        ' присутності, відібрати пояснення у неповнолітнього, який вчинив'
        ' правопорушення.\n'
        '• **Кваліфікувати** правопорушення відповідно до КУпАП.\n'
        '• **Роз’яснити права** особи, яка притягається до адміністративної'
        ' відповідальності, визначені статтею 268 КУпАП та **скласти протокол на'
        ' неповнолітнього** (обов’язково у присутності батьків, усиновителів,'
        ' опікунів або піклувальників).\n\n'
        '📎 **ДО ПРОТОКОЛУ ДОДАЄТЬСЯ:**\n'
        '1. РАПОРТ\n'
        '2. ПРОТОКОЛ ЗАСІДАННЯ\n'
        '3. ПОЯСНЕННЯ УЧАСНИКІВ ПОДІЇ\n'
        '4. ВІДЕО З Б/К\n'
        '5. КОПІЯ ПАСПОРТА (ПРАВОПОРУШНИКА)\n'
        '7. Інші фактичні дані, які можуть свідчити про вчинення правопорушення (відео, фото, інше...)'
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(
    func=lambda message: bool(message.text)
    and 'від 14 до 16 років' in message.text
)
def over14_algorithm_info(message):
    text = (
        '🎒 **Фіксування адміністративного правопорушення, вчиненого'
        ' неповнолітнім, віком від 14 до 16 років**\n\n'
        '📌 *Примітка: складається протокол за ч.3 ст. 184 КУпАП*\n\n'
        '• **Фіксація правопорушення**, збирання доказів або будь-яких фактичних'
        ' даних, які свідчать про вчинення правопорушення.\n'
        '*(Примітка: реєстрація події — потрібно уточнювати)*\n'
        '• **Встановлення особи** (учень якого класу, хто класний керівник).\n'
        '• **Повідомити** адміністрацію навчального закладу, безпосереднього'
        ' керівника СОБ, батьків (запросити до навчального закладу).\n'
        '• **За згодою батьків** або інших законних представників, у присутності'
        ' психолога, класного керівника відібрати пояснення у неповнолітнього,'
        ' який вчинив правопорушення, та свідків.\n'
        '• **Кваліфікувати** правопорушення відповідно до КУпАП.\n'
        '• **Роз’яснити права** особи, яка притягається до адміністративної'
        ' відповідальності, визначені статтею 268 КУпАП та статтею 63 КУ,'
        ' **скласти протокол на одного із батьків** або усиновителів, опікунів,'
        ' піклувальників за **ч.3 ст. 184 КУпАП**.\n\n'
        '📎 **ДО ПРОТОКОЛУ ДОДАЄТЬСЯ:**\n'
        '1. РАПОРТ\n'
        '2. ПРОТОКОЛ ЗАСІДАННЯ\n'
        '3. ПОЯСНЕННЯ УЧАСНИКІВ ПОДІЇ\n'
        '4. ВІДЕО З Б/К\n'
        '5. КОПІЯ ПАСПОРТА (ПРАВОПОРУШНИКА)\n'
        '7. Інші фактичні дані, які можуть свідчити про вчинення правопорушення (відео, фото, інше...)'
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(
    func=lambda message: bool(message.text) and 'до 14 років' in message.text
)
def under14_algorithm_info(message):
    text = (
        '👶 **Фіксування адміністративного правопорушення, вчиненого малолітніми,'
        ' віком до 14 років, або ухилення батьків чи осіб, які їх замінюють, від'
        " виконання передбачених законодавством обов'язків**\n\n"
        '📌 *Примітка: в такому випадку складається протокол за ч.1 ст. 184 КУпАП'
        ' (можлива повторність за ч.2 ст.184 КУпАП)*\n\n'
        '• **Фіксація правопорушення**, збирання доказів або отримання будь-яких'
        ' фактичних даних, які свідчать про вчинення правопорушення.\n'
        '*(Примітка: реєстрація події — потрібно уточнювати)*\n'
        '• **Встановлення особи** (учень якого класу, хто класний керівник).\n'
        '• **Повідомити** адміністрацію навчального закладу, безпосереднього'
        ' керівника СОБ, батьків (запросити до навчального закладу).\n'
        '• **За згодою батьків** або інших законних представників, у присутності'
        ' психолога, класного керівника відібрати пояснення у малолітнього, який'
        ' вчинив правопорушення, та свідків.\n'
        '• **Кваліфікувати** правопорушення відповідно до КУпАП, **перевірити'
        ' повторність** (повторними вважаються правопорушення, вчинені протягом'
        ' року з моменту набрання законної сили рішення суду).\n'
        '• **Роз’яснити права** особи, яка притягається до адміністративної'
        ' відповідальності, визначені статтею 268 КУпАП та статтею 63 КУ,'
        ' **скласти протокол на одного із батьків** або усиновителів, опікунів,'
        ' піклувальників за **ч.1 ст. 184** (у разі повторності — **ч.2 ст. 184**)'
        ' КУпАП за ухилення від обов’язків щодо виховання.\n\n'
        '📎 **ДО ПРОТОКОЛУ ДОДАЄТЬСЯ:**\n'
        '1. РАПОРТ\n'
        '2. ПРОТОКОЛ ЗАСІДАННЯ (копія)\n'
        '3. ПОЯСНЕННЯ УЧАСНИКІВ ПОДІЇ\n'
        '4. ВІДЕО З Б/К\n'
        '5. КОПІЇ СВІДОЦТВА ПРО НАРОДЖЕННЯ (ПРАВОПОРУШНИКА)\n'
        '6. КОПІЇ ПАСПОРТА (БАТЬКІВ)\n'
        '7. Інші фактичні дані, які можуть свідчити про вчинення правопорушення (відео, фото, інше...)'
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

# --- Нормативно-правова база ---

@bot.message_handler(
    func=lambda message: bool(message.text)
    and (
        'Постанови/Накази' in message.text
        or 'Постанови' in message.text
        or 'Накази' in message.text
    )
)
def docs_category_select(message):
    bot.send_message(
        message.chat.id,
        'Оберіть потрібну постанову, наказ, закон або кодекс:',
        reply_markup=get_docs_menu(),
    )

@bot.message_handler(
    func=lambda message: bool(message.text) and 'купап' in message.text.lower()
)
def doc_kupap_info(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            '🔗 Відкрити КУпАП на Zakon.Rada',
            url='https://zakon.rada.gov.ua/laws/show/8073-10#Text',
        )
    )
    bot.send_message(
        message.chat.id,
        '⚖️ **Кодекс України про адміністративні правопорушення (КУпАП)**',
        parse_mode='Markdown',
        reply_markup=markup,
    )

@bot.message_handler(
    func=lambda message: bool(message.text)
    and 'кримінальний кодекс' in message.text.lower()
)
def doc_kk_info(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            '🔗 Відкрити ККУ на Zakon.Rada',
            url='https://zakon.rada.gov.ua/laws/show/2341-14#Text',
        )
    )
    bot.send_message(
        message.chat.id,
        '⚖️ **Кримінальний кодекс України (ККУ)**',
        parse_mode='Markdown',
        reply_markup=markup,
    )

@bot.message_handler(
    func=lambda message: bool(message.text)
    and 'сімейний кодекс' in message.text.lower()
)
def doc_family_code_info(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            '🔗 Відкрити Сімейний кодекс на Zakon.Rada',
            url='https://zakon.rada.gov.ua/laws/show/2947-14#Text',
        )
    )
    bot.send_message(
        message.chat.id,
        '⚖️ **Сімейний кодекс України**',
        parse_mode='Markdown',
        reply_markup=markup,
    )

@bot.message_handler(
    func=lambda message: bool(message.text)
    and 'національну поліцію' in message.text.lower()
)
def doc_police_law_info(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            '🔗 Відкрити ЗУ «Про Національну поліцію»',
            url='https://zakon.rada.gov.ua/laws/show/580-19#Text',
        )
    )
    bot.send_message(
        message.chat.id,
        '👮 **Закон України «Про Національну поліцію»**',
        parse_mode='Markdown',
        reply_markup=markup,
    )

@bot.message_handler(
    func=lambda message: bool(message.text) and message.text == '🎓 ЗУ Про освіту'
)
def doc_education_law_info(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            '🔗 Відкрити ЗУ «Про освіту»',
            url='https://zakon.rada.gov.ua/laws/show/2145-19#Text',
        )
    )
    bot.send_message(
        message.chat.id,
        '🎓 **Закон України «Про освіту»**',
        parse_mode='Markdown',
        reply_markup=markup,
    )

@bot.message_handler(
    func=lambda message: bool(message.text)
    and 'середню освіту' in message.text.lower()
)
def doc_sec_education_law_info(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            '🔗 Відкрити ЗУ «Про загальну середню освіту»',
            url='https://zakon.rada.gov.ua/laws/show/651-14#Text',
        )
    )
    bot.send_message(
        message.chat.id,
        '🏫 **Закон України «Про повну загальну середню освіту»**',
        parse_mode='Markdown',
        reply_markup=markup,
    )

@bot.message_handler(
    func=lambda message: bool(message.text)
    and 'охорону дитинства' in message.text.lower()
)
def doc_child_protection_info(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            '🔗 Відкрити ЗУ «Про охорону дитинства»',
            url='https://zakon.rada.gov.ua/laws/show/2402-14#Text',
        )
    )
    bot.send_message(
        message.chat.id,
        '👶 **Закон України «Про охорону дитинства»**',
        parse_mode='Markdown',
        reply_markup=markup,
    )

@bot.message_handler(
    func=lambda message: bool(message.text) and '684' in message.text
)
def doc_684_info(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            '🔗 Відкрити Постанову № 684',
            url='https://zakon.rada.gov.ua/laws/show/684-2017-%D0%BF#Text',
        )
    )
    bot.send_message(
        message.chat.id,
        '🏛 **Постанова КМУ № 684**',
        parse_mode='Markdown',
        reply_markup=markup,
    )

@bot.message_handler(
    func=lambda message: bool(message.text) and '663' in message.text
)
def doc_663_info(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            '🔗 Відкрити Наказ № 663',
            url='https://zakon.rada.gov.ua/laws/show/z1590-24#Text',
        )
    )
    bot.send_message(
        message.chat.id,
        '📋 **Наказ МВС України № 663**',
        parse_mode='Markdown',
        reply_markup=markup,
    )

@bot.message_handler(
    func=lambda message: bool(message.text) and '1646' in message.text
)
def doc_1646_info(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            '🔗 Відкрити Наказ № 1646',
            url='https://zakon.rada.gov.ua/laws/show/z0111-20#Text',
        )
    )
    bot.send_message(
        message.chat.id,
        '📋 **Наказ МОН України № 1646**',
        parse_mode='Markdown',
        reply_markup=markup,
    )

@bot.message_handler(
    func=lambda message: bool(message.text) and '1245' in message.text
)
def doc_1245_info(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            '🔗 Відкрити Постанову № 1245',
            url='https://zakon.rada.gov.ua/laws/show/1245-2024-%D0%BF#Text',
        )
    )
    bot.send_message(
        message.chat.id,
        '🏛 **Постанова КМУ № 1245**',
        parse_mode='Markdown',
        reply_markup=markup,
    )

@bot.message_handler(
    func=lambda message: bool(message.text) and message.text == '🏛 Постанова № 70'
)
def doc_70_info(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            '🔗 Відкрити Постанову № 70',
            url='https://zakon.rada.gov.ua/laws/show/70-2026-%D0%BF#Text',
        )
    )
    bot.send_message(
        message.chat.id,
        '🏛 **Постанова КМУ № 70**',
        parse_mode='Markdown',
        reply_markup=markup,
    )

@bot.message_handler(
    func=lambda message: bool(message.text)
    and ('685' in message.text or '1013' in message.text)
)
def doc_685_1013_info(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            '🔗 Відкрити Наказ № 685/1013',
            url='https://zakon.rada.gov.ua/laws/show/z1583-23#Text',
        )
    )
    bot.send_message(
        message.chat.id,
        '📋 **Спільний наказ № 685/1013**',
        parse_mode='Markdown',
        reply_markup=markup,
    )

@bot.message_handler(
    func=lambda message: bool(message.text) and '1395' in message.text
)
def doc_1395_info(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            '🔗 Відкрити Наказ № 1395',
            url='https://zakon.rada.gov.ua/laws/show/z1408-15#Text',
        )
    )
    bot.send_message(
        message.chat.id,
        '📋 **Наказ МВС України № 1395**',
        parse_mode='Markdown',
        reply_markup=markup,
    )

@bot.message_handler(
    func=lambda message: bool(message.text) and '1376' in message.text
)
def doc_1376_info(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            '🔗 Відкрити Наказ № 1376',
            url='https://zakon.rada.gov.ua/laws/show/z1496-15#Text',
        )
    )
    bot.send_message(
        message.chat.id,
        '📋 **Наказ МВС України № 1376**',
        parse_mode='Markdown',
        reply_markup=markup,
    )

@bot.message_handler(
    func=lambda message: bool(message.text) and message.text == '📋 Наказ № 70'
)
def doc_70_order_info(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            '🔗 Відкрити Наказ № 70',
            url='https://zakon.rada.gov.ua/laws/show/z0250-16#Text',
        )
    )
    bot.send_message(
        message.chat.id,
        '📋 **Наказ МВС України № 70**',
        parse_mode='Markdown',
        reply_markup=markup,
    )

# --- КУпАП: ст. 173-2 (Домашнє насильство - фабули) ---

@bot.message_handler(
    func=lambda message: bool(message.text)
    and ('173-2' in message.text or 'Домашнє насильство' in message.text)
)
def violence_category_select(message):
    bot.send_message(
        message.chat.id,
        'Оберіть потрібний розділ:',
        reply_markup=get_violence_menu(),
    )

@bot.message_handler(
    func=lambda message: bool(message.text)
    and ('дитини' in message.text.lower() or 'дитин' in message.text.lower())
    and '122' not in message.text
)
def child_violence_info(message):
    fabula_text_1 = (
        '⚖️ **ПРИКЛАД ФАБУЛИ ЗА Ч. 2 СТ. 173-2 КУпАП**\n'
        '*(постраждала особа — присутня дитина)*\n\n'
        '«01.01.2026 близько 20:00 в приміщенні ПРУ КЗ «Харківський ліцей #153»'
        ' який знаходився за адресою: м. Харків, просп. Аерокосмічний, буд.1, кв.'
        ' 1, ПІБ (кривдник) вчинив домашнє насильство психологічного характеру у'
        ' відношенні дружини, ПІБ (постраждала особа), у присутності дитини'
        ' (сина, дочки, племінника…) ПІБ, дата народження, чим була завдана'
        ' шкода ПСИХІЧНОМУ здоров’ю потерпілого».\n\n'
        'ℹ️ *Якщо при вчиненні домашнього насильства (адміністративного'
        ' характеру) відносно дорослої особи присутня дитина (від народження до 18'
        ' років) складаються окремі протоколи: постраждала доросла особа та'
        ' постраждала присутня дитина!*'
    )

    fabula_text_2 = (
        '⚖️ **ПРИКЛАД ФАБУЛИ ЗА СТ. 173-2 КУпАП**\n'
        '*(насильство відносно неповнолітньої/малолітньої дитини)*\n\n'
        '«01.01.2026 близько 20:00 в приміщенні ПРУ КЗ «Харківський ліцей #153»'
        ' який знаходиться за адресою: м. Харків, просп. Аерокосмічний, буд.1, ПІБ'
        ' (кривдник) вчинив домашнє насильство психологічного характеру у'
        ' відношенні малолітньої/неповнолітньої доньки/сина, ПІБ (постраждала'
        ' особа), дата народження, а саме: ображав, принижував, залякував, чим'
        ' була завдана шкода ПСИХІЧНОМУ здоров’ю потерпілої».'
    )

    bot.send_message(message.chat.id, fabula_text_1, parse_mode='Markdown')
    bot.send_message(message.chat.id, fabula_text_2, parse_mode='Markdown')

# --- ОНОВЛЕНИЙ РОЗДІЛ: ст. 184 КУпАП ---

@bot.message_handler(
    func=lambda message: bool(message.text) and '184' in message.text
)
def art_184_info(message):
    text = (
        '🚸 **ст. 184 КУпАП — Невиконання батьками або особами, що їх замінюють,'
        " обов'язків щодо виховання дітей**\n\n📌 **Ч. 1:** Ухилення батьків або"
        ' осіб, які їх замінюють, від виконання передбачених законодавством'
        ' обов’язків щодо забезпечення необхідних умов життя, навчання та'
        ' виховання неповнолітніх дітей.\n\n⚖️ **Приклад фабули за ч. 1 ст. 184'
        ' КУпАП:**\n26.10.2025 о 10 год. 00хв. за адресою місто Харків вул. Грубника, 24, в приміщенні КЗ "Харківський ліцей №153"  (ПІБ) 07.01.1979 р.н., ухилився від належного виконання батьківських обов\'язків передбачених ч.1 ст.150 "Сімейного Кодексу України " , внаслідок чого її малолітній син (ПІБ) 14.10.2015 р.н., палив тютюнові вироби а саме електронну сигарету не встановленого типу.\n\n───────────────────\n\n📌 **Ч. 3:** Вчинення'
        ' неповнолітніми віком від 14 до 16 років правопорушення, відповідальність'
        ' за яке передбачено цим Кодексом (крім ч. 3 або ч. 4 ст.'
        ' 173-4).\n\n⚖️ **Приклад фабули за ч. 3 ст. 184 КУпАП:**\nГромадянка'
        " (ПІБ) будучи матір'ю неповнолітнього (ПІБ) 2011 року народження, який не досяг 16-річного віку, 15.06.2026 вчинив домашнє насильство відносно своєї сестри, а саме умисні дії психологічного характеру: ображав словесно, погрожував вбити, чим завдав їй психологічних страждань, унаслідок чого завдано шкоди психічному здоров’ю (ПІБ) відповідальність за яке передбачена ст. 173-2 КУпАП, чим вчинила правопорушення, передбачене ч. 3 ст. 184 КУпАП."
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(
    func=lambda message: bool(message.text)
    and '173' in message.text
    and '173-2' not in message.text
    and '173-4' not in message.text
    and '173-7' not in message.text
    and '178' not in message.text
)
def art_173_info(message):
    text = (
        '🤪 **ст. 173 КУпАП — Дрібне хуліганство**\n\nДрібне хуліганство, тобто'
        ' нецензурна лайка в громадських місцях, образливе чіпляння до громадян та'
        ' інші подібні дії, що порушують громадський порядок і спокій'
        ' громадян.\n\n⚖️ **Приклади фабул:**\n\n📌 **Варіант 1 (Нецензурна'
        ' лайка):**\n01.01.2015 о 20 год. 05 хв. гр. (ПІБ),'
        ' перебуваючи в стані алкогольного сп’яніння, у громадському місці біля'
        ' буд. № 76/1 по просп. Миру в Хмельницькому, висловлювався нецензурною'
        ' лайкою на адресу гр. (ПІБ) (або перехожих), чим порушував'
        ' громадський порядок і спокій громадян.\n\n📌 **Варіант 2 (Справляння'
        ' природних потреб):**\n10.09.2015 о 20 год. 05 хв. гр. (ПІБ)'
        ' в м. Хмельницькому по вул. Проскурівського підпілля, 15,'
        ' справляв природні потреби поблизу дверей офісу «Сонечко», чим своїми'
        ' діями порушував громадський порядок.'
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(
    func=lambda message: bool(message.text) and 'Про бота' in message.text
)
def about_bot_info(message):
    about_text = (
        'ℹ️ **Про робочий помічник СОБ**\n\nЦей бот розроблений для швидкого'
        ' доступу до необхідної нормативно-правової бази, фабул адміністративних'
        ' правопорушень та алгоритмів дій Інспектора Служби Освітньої'
        ' Безпеки.\n\n👨‍💻 **З питань роботи бота звертайтеся до куратора.**'
    )
    bot.send_message(message.chat.id, about_text, parse_mode='Markdown')

# --- Запуск ---

if __name__ == '__main__':
    threading.Thread(target=run_flask, daemon=True).start()
    print('Бот успішно запущений...')

    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f'Помилка під час виконання: {e}')
            time.sleep(5)
