from openai import OpenAI
import sys
import telebot
import requests  # Для получения контекста из внешнего источника
from bs4 import BeautifulSoup
#from dotenv import load_dotenv
import os

bot = telebot.TeleBot("7187962789:AAF7lnrkbKfxEwNil_DxNHEGeOCb5DTaorI", threaded=True, num_threads=300)
# Подключение к локальному серверу OpenAI
client = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="not-needed")
behavior = ""

# Функция для извлечения текстового контента из ссылки
def extract_text_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Находим и извлекаем текстовый контент из HTML
        text = ' '.join([p.get_text() for p in soup.find_all('p')])
        return text
    except Exception as e:
        print("Ошибка при извлечении контента:", e)
        return None

# Обработчик команды /start
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id,
                     "Привет! Напиши команду /context, пришли мне ссылку, и мы ее с тобой обсудим!")

# Обработчик команды /context
@bot.message_handler(commands=["context"])
def context_command(message):
    bot.send_message(message.chat.id, "Пожалуйста, отправьте ссылку для извлечения контекста.")

messages = [{"role": "system", "content":  "Ты умный ассистент Саяпиной Александры. Отвечаешь на вопросы, используя контекст предоставленный ниже.\
Твои ответы короткие и четкие и содержат конкретные инструкции в ответ на вопрос пользователя."}]

# Обработчик текстовых сообщений от пользователя
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global context
    global messages
    if message.text.startswith("http"):
        context = extract_text_from_url(message.text)
        if context:
            bot.reply_to(message, "Ссылка получена! Задавайте свой вопрос по информации по ссылке.")
        else:
            bot.reply_to(message, "Не удалось извлечь контекст из указанной ссылки.")
        return

    if context:
        print("context: ", context)
        messages.append({"role": "user", "content": "Ответь на следующий вопрос используя сведения из контекста ниже.\nКонтекст: {context}\nВопрос: {message.text}\nОтвет:"})


        completion = client.chat.completions.create(
            model="local-model",
            temperature=0.7,
            messages=messages
        )
        response = completion.choices[0].message.content
        # Отправляем ответ по частям, если он слишком длинный
        while response:
            bot.send_message(message.chat.id, response[:4096])
            response = response[4096:]
    else:
        bot.reply_to(message, "Пожалуйста, отправьте ссылку для извлечения контекста командой /context.")


# Запуск бота
bot.polling()