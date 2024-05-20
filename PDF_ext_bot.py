'''from telegram.ext import Updater, Bot, CommandHandler

# Обработчик команды /start
def start(update, context):
    update.message.reply_text('Привет! Я бот.')

# Обработчик команды /help
def help(update, context):
    update.message.reply_text('Это помощь.')

# Функция, которая запускает бота
from telegram.ext import Updater
def main():
    # Создаем объект Bot с токеном вашего бота
    bot = Bot(token='6939550032:AAFAcHAugFuO_3ja5D-jLlc28KpcBqYej5')

    # Инициализируем объект Updater с передачей объекта Bot
    updater = Updater(bot=bot)

    # Получаем dispatcher для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Запускаем бота
    updater.start_polling()

    # Бот будет работать до принудительной остановки
    updater.idle()

if __name__ == '__main__':
    main()
'''

import telebot

bot = telebot.TeleBot("7187962789:AAF7lnrkbKfxEwNil_DxNHEGeOCb5DTaorI", threaded=True, num_threads=300)

@bot.message_handler(commands = ['start', 'hello'])
def start(message):
    #print(message.start)
    bot.send_message(message.from_user.id, "Привет!")

@bot.message_handler(commands = ['help'])
def help(message):
    bot.send_message(message.from_user.id, "help!")
bot.infinity_polling(timeout=10, long_polling_timeout = 5)

@bot.message_handler(commands = ['text'])
def text(message):
    bot.send_message(message.from_user.id, "help!")
bot.infinity_polling(timeout=10, long_polling_timeout = 5)

'''
@bot.message_handler(content_types=['text'])
def main1(message):
    print(message.text)
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "hello")
    #bot.send_message(message.from_user.id, "help!")
#bot.infinity_polling(timeout=10, long_polling_timeout = 5)
'''
'''
import threading
threading.Thread().start()
bot.infinity_polling(timeout=10, long_polling_timeout=5)'''
# import asyncio
# import time
# while True:
#     try:
#         asyncio.run(bot.polling(non_stop=True, interval=1, timeout=0))
#     except:
#         time.sleep(5)
'''
import time
import logging
from aiogram import Bot, Dispethcer, executor, types

bot = Bot(token = "6939550032:AAFAcHAugFuO_3ja5D-jLlc28KpcBqYej5o")
dp = Dispethcer(bot = bot)

@dp.message_handler(commands =['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id=} {user_full_name=} {time.asctime()}')

    await message.reply(f"Привет, {user_full_name}")

if __name__ == '__main__':
    executor.start_polling(dp)
'''
