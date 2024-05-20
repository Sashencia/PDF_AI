from openai import OpenAI
import sys
import telebot
#from dotenv import load_dotenv
import os

bot = telebot.TeleBot("7187962789:AAF7lnrkbKfxEwNil_DxNHEGeOCb5DTaorI", threaded=True, num_threads=300)
# Подключение к локальному серверу OpenAI
client = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="not-needed")
behavior = ""
# Обработчик команды /start
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id,
                     "Привет! Введите поведение модели (например, <code>Отвечай как Гомер Симпсон</code>)",
                     parse_mode="HTML")

# Обработчик текстовых сообщений от пользователя
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global behavior
    if not behavior:
        behavior = message.text
        bot.reply_to(message, "Получено. Теперь вы можете задавать запросы.")
    else:
        global messages
        messages = [{"role": "system", "content": behavior}]
        new_req = message.text
        if new_req.lower() == "exit":
            sys.exit()
        messages.append({"role": "user", "content": new_req})
        completion = client.chat.completions.create(
            model="local-model",
            temperature=0.7,
            messages=messages
        )
        bot.reply_to(message, completion.choices[0].message.content)

# Запуск бота
bot.polling()