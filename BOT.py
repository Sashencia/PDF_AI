from openai import OpenAI
import sys
import telebot
import requests  # Для получения контекста из внешнего источника
from bs4 import BeautifulSoup
#from dotenv import load_dotenv
import os
import time
import threading
import fitz
import docx
import pytesseract
from PIL import Image
from io import StringIO
import re
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import pdfplumber
import os
import io
from PyPDF2 import PdfReader
import pytesseract
from pdf2image import convert_from_bytes
import extraction_from_PDF as efp

bot = telebot.TeleBot("7187962789:AAF7lnrkbKfxEwNil_DxNHEGeOCb5DTaorI", threaded=True, num_threads=300)
# Подключение к локальному серверу OpenAI
client = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="not-needed")
behavior = ""
messages = [{"role": "system", "content":  "Ты умный ассистент Саяпиной Александры. Отвечаешь на вопросы, используя контекст предоставленный ниже.\
Твои ответы короткие и четкие и содержат конкретные инструкции в ответ на вопрос пользователя."}]


# Функция для извлечения текстового контента из ссылки
'''
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
'''

def typing_animation(message):
    for i in range(90):
        time.sleep(0.5)
        bot.send_chat_action(message.chat.id, action='typing')
        time.sleep(0.5)
        bot.send_chat_action(message.chat.id, action='typing')

page_cache = {}
def extract_text_from_url(url):
    # Проверяем, есть ли уже данные в кеше для этой страницы
    if url in page_cache:
        return page_cache[url]

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Находим и извлекаем текстовый контент из HTML
        text = ' '.join([p.get_text() for p in soup.find_all('p')])
        # Сохраняем данные в кеше
        page_cache[url] = text
        return text
    except Exception as e:
        print("Ошибка при извлечении контента:", e)
        return None

# Функция для извлечения текста из DOCX-файла
def extract_text_from_docx(file_path):
    try:
        doc = docx.Document(file_path)
        text = []
        for paragraph in doc.paragraphs:
            text.append(paragraph.text)
        return '\n'.join(text)
    except Exception as e:
        print("Ошибка при извлечении текста из DOCX:", e)
        return None

'''
def extract_text_from_pdf(file_path):
    try:
        document = fitz.open(file_path)
        text = ""
        for page_num in range(len(document)):
            page = document.load_page(page_num)
            text += page.get_text()
        return text
    except Exception as e:
        print("Ошибка при извлечении текста из PDF:", e)
        return None
'''

# Функция для извлечения текста из PDF
'''
THE NORMAL EXTRACT
def extract_text_from_pdf(pdf_path):
    extracted_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Извлекаем текст с каждой страницы
            page_text = page.extract_text()
            # Добавляем текст страницы к общему извлеченному тексту
            extracted_text += page_text + "\n"
    return extracted_text
    '''

'''
# Обработчик PDF- и DOCX-документов
@bot.message_handler(content_types=["document"])
def handle_document(message):
    text = ""
    if message.document.mime_type == "application/pdf":
        try:
            # Создаем каталог "Загрузки", если он не существует
            if not os.path.exists("Загрузки"):
                os.makedirs("Загрузки")

            # Скачивание PDF-файла
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            # Сохранение файла
            file_path = os.path.join("Загрузки", message.document.file_name)
            with open(file_path, 'wb') as new_file:
                new_file.write(downloaded_file)

            file_chunks = split_file(file_path)
            # Обрабатываем каждую часть файла
            for chunk in file_chunks:
                text += extract_text_from_pdf(chunk)
            # Извлечение текста из PDF
            #text = extract_text_from_pdf(file_path)
            if text:
                #return text
                bot.send_message(message.chat.id,
                                 "Извлеченный текст:\n" + text)  # Ограничение на длину сообщения
                print("text: ", text)
            else:
                bot.send_message(message.chat.id, "Не удалось извлечь текст из PDF.")

            # Удаление файла после обработки
            os.remove(file_path)
        except Exception as e:
            bot.send_message(message.chat.id, "Произошла ошибка при обработке PDF-файла.")
            print("Ошибка при обработке PDF-файла:", e)
    elif message.document.mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        try:
            # Создаем каталог "Загрузки", если он не существует
            if not os.path.exists("Загрузки"):
                os.makedirs("Загрузки")

            # Скачивание DOCX-файла
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            # Сохранение файла
            file_path = os.path.join("Загрузки", message.document.file_name)
            with open(file_path, 'wb') as new_file:
                new_file.write(downloaded_file)

            # Извлечение текста из PDF
            text = extract_text_from_docx(file_path)
            if text:
                # return text
                bot.send_message(message.chat.id,
                                 "Извлеченный текст:\n" + text)  # Ограничение на длину сообщения
                print("text: ", text)
            else:
                bot.send_message(message.chat.id, "Не удалось извлечь текст из DOCX.")

            # Удаление файла после обработки
            os.remove(file_path)
        except Exception as e:
            bot.send_message(message.chat.id, "Произошла ошибка при обработке DOCX-файла.")
            print("Ошибка при обработке DOCX-файла:", e)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, отправьте PDF- или DOCX-файл.")
'''


# Обработчик команды /process для обработки файла
@bot.message_handler(commands=["process"])
def process_file(message):
    # Проверяем, есть ли у сообщения прикрепленный файл
    if message.document is None:
        bot.reply_to(message, "Пожалуйста, прикрепите файл.")
        return

    # Получаем путь к загруженному файлу
    file_id = message.document.file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # Создаем каталог "Загрузки", если он не существует
    if not os.path.exists("Загрузки"):
        os.makedirs("Загрузки")

    # Сохранение файла
    file_path = os.path.join("Загрузки", message.document.file_name)
    with open(file_path, 'wb') as new_file:
        new_file.write(downloaded_file)

    extracted_text = efp.PDF(file_path) # из файла extraction_from_PDF

    if extracted_text:
        # Отправляем извлеченный текст пользователю по частям
        while extracted_text:
            bot.send_chat_action(message.chat.id, 'typing')  # Имитируем печатание
            bot.send_message(message.chat.id, extracted_text[:4096])
            extracted_text = extracted_text[4096:]
    else:
        bot.send_message(message.chat.id, "Не удалось извлечь текст из PDF.")

    # Удаление файла после обработки
    os.remove(file_path)

# Обработчик документов
@bot.message_handler(content_types=["document"])
def handle_document(message):
    if message.document.mime_type == "application/pdf":
        try:
            bot.send_message(message.chat.id, "Обработка PDF-файла...")
            process_file(message)
        except OSError as e:
            # Если возникает ошибка доступа к файлу, занятому другим процессом
            print("Ошибка доступа к файлу:", e)
            print("Повторная попытка через 1 секунду...")
            time.sleep(1)  # Подождать 1 секунду перед повторной попыткой
            bot.send_message(message.chat.id, "Произошла ошибка при обработке PDF-файла.")
            print("Ошибка при обработке PDF-файла:", e)
            return  # Прекратить выполнение функции после вывода ошибки
        except Exception as e:
            bot.send_message(message.chat.id, "Произошла ошибка при обработке PDF-файла.")
            print("Ошибка при обработке PDF-файла:", e)






# Обработчик команды /start
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id,
                     "Привет! Пришли мне ссылку, и мы ее с тобой обсудим!")
'''
НЕ НУЖНО??????
@bot.message_handler(func=lambda message: True)
def handle_upload(message):
    try:
        file_info = bot.get_file(message.chat.id, message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path).read()

        # Сохраняем файл в заданную папку
        file_name = f'uploaded_file_{message.chat.id}.pdf'
        with open(os.path.join('your_path', file_name), 'wb') as f:
            f.write(downloaded_file)

        # Извлекаем текст из файла
        if file_name.endswith('.pdf'):
            extracted_text = extract_text_from_pdf(os.path.join('your_path', file_name))
        elif file_name.endswith('.docx'):
            extracted_text = extract_text_from_docx(os.path.join('your_path', file_name))

        # Добавляем извлеченный текст к контексту
        global context
        context += extracted_text

        # Отправляем сообщение пользователю
        bot.reply_to(message, "Файл загружен и обработан. Задайте свой вопрос.")

        # Запрашиваем вопрос у пользователя
        bot.send_message(message.chat.id, "Ваш вопрос:")
    except Exception as e:
        print("Ошибка при обработке файла:", e)
        bot.reply_to(message, "Произошла ошибка при обработке файла.")
'''
# Обработчик текстовых сообщений от пользователя
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global context
    global messages

    if message.text.startswith("http"):
        context = extract_text_from_url(message.text)
        if context:
            bot.reply_to(message, "Ссылка получена! Что вы хотите узнать из этой ссылки?")
        else:
            bot.reply_to(message, "Не удалось извлечь контекст из указанной ссылки.")
        return
    else:
        #bot.reply_to(message, "Пожалуйста, отправьте ссылку для извлечения контекста, вновь введя команду /context.")
        print("context: ", context)
        messages.append({"role": "user", "content": f"Ответь на следующий вопрос используя сведения из контекста ниже.\nКонтекст: {context}\nВопрос: {message.text}\nОтвет:"})

        typing_thread = threading.Thread(target=typing_animation, args=(message,))
        typing_thread.start()
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
        typing_thread.join()  # Ждем завершения анимации печати


# Запуск бота
bot.polling()