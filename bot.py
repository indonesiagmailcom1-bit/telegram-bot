import telebot
from telebot import types

# =========================
# 🔴 ТОКЕНИ БОТАТРО ИН ҶО НАВИС
TOKEN = "8918809181:AAHgLrZFuuEOJMU4H9gyZyJ9v-c4dzln6NM"

# 🔴 TELEGRAM ID-И ХУДАТРО ИН ҶО НАВИС
ADMIN_ID = 7704259976

# 🔴 РАҚАМИ КОРТАТРО ИН ҶО НАВИС
CARD_NUMBER = "DC-ALIF   +992 815 23 4444"
# =========================

bot = telebot.TeleBot(TOKEN)
user_orders = {}


def back_button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("⬅️ Ба ақиб"))
    return markup


@bot.message_handler(commands=['start'])
def start(message):

    user_orders.pop(message.chat.id, None)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add(
        types.KeyboardButton("💎 Алмаз харидан"),
        types.KeyboardButton("👨‍💻 Муроҷиат ба Админ")
    )

    bot.send_message(
        message.chat.id,
        "👋 Хуш омадед!",
        reply_markup=markup
    )


@bot.message_handler(func=lambda message: message.text == "💎 Алмаз харидан")
def diamonds(message):

    markup = types.InlineKeyboardMarkup()

    products = [
        ("💎 100 Алмаз — 10 см", "100 Алмаз — 10 см"),
        ("💎 200 Алмаз — 20 см", "200 Алмаз — 20 см"),
        ("💎 300 Алмаз — 30 см", "300 Алмаз — 30 см"),
        ("💎 400 Алмаз — 40 см", "400 Алмаз — 40 см"),
        ("🎫 Ваунчер Ниделя — 20 см", "Ваунчер Ниделя — 20 см"),
        ("🎫 Ваунчер Месяц — 85 см", "Ваунчер Месяц — 85 см")
    ]

    for text, data in products:
        markup.add(
            types.InlineKeyboardButton(
                text,
                callback_data=data
            )
        )

    markup.add(
        types.InlineKeyboardButton(
            "⬅️ Ба ақиб",
            callback_data="BACK"
        )
    )

    bot.send_message(
        message.chat.id,
        "💎 Нархномаро интихоб кунед:",
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    user_id = call.message.chat.id

    if call.data == "BACK":

        user_orders.pop(user_id, None)

        bot.answer_callback_query(call.id)

        start(call.message)

        return

    user_orders[user_id] = {
        "product": call.data
    }

    bot.answer_callback_query(call.id)

    msg = bot.send_message(
        user_id,
        "🎮 ID-и Free Fire-ро нависед:",
        reply_markup=back_button()
    )

    bot.register_next_step_handler(
        msg,
        get_freefire_id
    )


def get_freefire_id(message):

    user_id = message.chat.id

    if message.text == "⬅️ Ба ақиб":

        user_orders.pop(user_id, None)

        diamonds(message)

        return

    if user_id not in user_orders:
        return

    # Танҳо рақам қабул мешавад
    if not message.text.isdigit():

        msg = bot.send_message(
            user_id,
            "❌ Танҳо рақам нависед!\n\n🎮 ID-и Free Fire:"
        )

        bot.register_next_step_handler(
            msg,
            get_freefire_id
        )

        return

    user_orders[user_id]["freefire_id"] = message.text

    msg = bot.send_message(
        user_id,
        f"💳 <b>ПУЛРО БА ИН КОРТ ФИРИСТЕД:</b>\n\n"
        f"<b>💳 {CARD_NUMBER}</b>\n\n"
        f"📸 <b>ЧЕКРО СУРАТ ГИРИФТА ФИРИСТЕД</b>",
        parse_mode="HTML",
        reply_markup=back_button()
    )

    bot.register_next_step_handler(
        msg,
        get_receipt
    )


def get_receipt(message):

    user_id = message.chat.id

    if message.text == "⬅️ Ба ақиб":

        user_orders.pop(user_id, None)

        diamonds(message)

        return

    if user_id not in user_orders:
        return

    if not message.photo:

        msg = bot.send_message(
            user_id,
            "❌ ЧЕКРО ҲАМЧУН СУРАТ ФИРИСТЕД 📸"
        )

        bot.register_next_step_handler(
            msg,
            get_receipt
        )

        return

    username = message.from_user.username

    if username:
        username = "@" + username
    else:
        username = "Надорад"

    product = user_orders[user_id]["product"]
    freefire_id = user_orders[user_id]["freefire_id"]

    order_text = (
        "🔔 ЗАКАЗИ НАВ!\n\n"
        f"👤 Ном: {message.from_user.first_name}\n"
        f"📱 Username: {username}\n"
        f"🆔 Telegram ID: {message.from_user.id}\n\n"
        f"💎 ЗАКАЗ: {product}\n"
        f"🎮 FREE FIRE ID: {freefire_id}"
    )

    # 📩 МАЪЛУМОТИ ЗАКАЗ БА АДМИН
    bot.send_message(
        ADMIN_ID,
        order_text
    )

    # 📸 СУРАТИ ЧЕК БА АДМИН
    bot.send_photo(
        ADMIN_ID,
        message.photo[-1].file_id,
        caption=f"📸 ЧЕК | {product}"
    )

    # ✅ ҶАВОБ БА ХАРИДОР
    bot.send_message(
        user_id,
        "✅ Закази шумо ба Админ равон шуд!\n\n"
        "📩 Худи ҳозир Админ ба шумо менависад."
    )

    user_orders.pop(user_id, None)


@bot.message_handler(
    func=lambda message: message.text == "👨‍💻 Муроҷиат ба Админ"
)
def admin_contact(message):

    bot.send_message(
        message.chat.id,
        "👨‍💻 WhatsApp  +992 815 23 4444"
    )


print("🤖 Бот фаъол шуд...")

bot.infinity_polling()