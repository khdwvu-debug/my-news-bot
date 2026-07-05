import telebot
from telebot import types
import time
from flask import Flask
import threading

TOKEN = '8872056075:AAF4kOOWSf37S0O6UeWRTCZH5o0KcBTTWJk'
bot = telebot.TeleBot(TOKEN)

app = Flask('')

@app.route('/')
def home():
    return "Бот онлайн!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def get_main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_tech = types.InlineKeyboardButton("💻 Технологии", callback_data="news_tech")
    btn_science = types.InlineKeyboardButton("🔬 Наука", callback_data="news_science")
    btn_world = types.InlineKeyboardButton("🌍 Весь мир", callback_data="news_world")
    markup.add(btn_tech, btn_science, btn_world)
    return markup

@bot.message_handler(commands=['start', 'news'])
@bot.message_handler(func=lambda message: message.text.lower() in ['новости', 'меню'])
def send_welcome(message):
    bot.send_message(
        message.chat.id, 
        "📰 **Добро пожаловать в Новостной Центр!**\n\nВыбери интересующую тебя категорию с помощью кнопок ниже:", 
        reply_markup=get_main_menu(),
        parse_mode='Markdown'
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("news_"))
def handle_news_categories(call):
    back_markup = types.InlineKeyboardMarkup()
    btn_back = types.InlineKeyboardButton("⬅️ Назад в меню", callback_data="to_menu")
    back_markup.add(btn_back)

    if call.data == "news_tech":
        text = "💻 **НОВОСТИ ТЕХНОЛОГИЙ**\n\n• Нейросети научились писать полноценные mobile-приложения по голосовому описанию.\n• Представлен новый тип гибких экранов, которые не царапаются и не бьются.\n• Популярные мессенджеры внедряют сквозное шифрование для групповых видеозвонков."
    elif call.data == "news_science":
        text = "🔬 **НОВОСТИ НАУКИ**\n\n• Ученые успешно протестировали биопринтер для создания тканей организма.\n• Физики приблизились к созданию стабильного термоядерного реактора.\n• Археологи нашли древний подземный город на глубине более 20 метров."
    elif call.data == "news_world":
        text = "🌍 **МИРОВЫЕ СОБЫТИЯ**\n\n• В крупнейших столицах мира проходят масштабные фестивали цифрового искусства.\n• Международные авиалинии начали тестировать первые пассажирские самолеты на эко-топливе.\n• Глобальные климатические миссии зафиксировали восстановление лесных массивов в тропиках."

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=back_markup,
        parse_mode='Markdown'
    )

@bot.callback_query_handler(func=lambda call: call.data == "to_menu")
def handle_back_to_menu(call):
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="📰 **Добро пожаловать в Новостной Центр!**\n\nВыбери интересующую тебя категорию с помощью кнопок ниже:",
        reply_markup=get_main_menu(),
        parse_mode='Markdown'
    )

if __name__ == "__main__":
    t = threading.Thread(target=run_flask)
    t.start()
    
    print("Бот запущен...")
    while True:
        try:
            bot.polling(none_stop=True, interval=2, timeout=20)
        except Exception as e:
            time.sleep(5)
