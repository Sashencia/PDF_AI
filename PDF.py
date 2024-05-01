import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
import PyPDF2


# Функция, которая обрабатывает команду /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Отправьте мне PDF файл, и я попробую ответить на ваши вопросы.')


# Функция, которая обрабатывает входящие сообщения с документами
def handle_document(update: Update, context: CallbackContext) -> None:
    file = update.message.document.get_file()
    file.download('input.pdf')
    update.message.reply_text('PDF файл получен. Отправьте ваш вопрос.')


# Функция, которая отвечает на вопросы
def handle_message(update: Update, context: CallbackContext) -> None:
    if not os.path.exists('input.pdf'):
        update.message.reply_text('Пожалуйста, сначала отправьте мне PDF файл.')
        return

    with open('input.pdf', 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        text = ''
        for page_num in range(reader.numPages):
            text += reader.getPage(page_num).extractText()

    # Пример обработки запроса
    if 'шрифт для подписи картинок' in text.lower():
        update.message.reply_text('Шрифт для подписи картинок - Arial.')


# Функция для запуска бота
def main() -> None:
    # Получаем токен бота из переменной окружения
    token = os.environ.get('6939550032:AAFAcHAugFuO_3ja5D-jLlc28KpcBqYej5o')
    if token is None:
        print('Токен бота не найден. Пожалуйста, установите переменную окружения TELEGRAM_BOT_TOKEN.')
        return

    updater = Updater(token)

    dispatcher = updater.dispatcher

    # Обработчики команд
    dispatcher.add_handler(CommandHandler("start", start))

    # Обработчик документов
    dispatcher.add_handler(MessageHandler(Filters.document, handle_document))

    # Обработчик входящих сообщений
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Запускаем бота
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
