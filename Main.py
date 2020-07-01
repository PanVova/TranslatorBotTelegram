# -*- coding: utf8 -*-

import pandas as pd
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,CallbackQueryHandler
from gtts import gTTS
from google.cloud import translate
import os
import cv2
import pytesseract
from PIL import Image, ImageFilter, ImageEnhance
pytesseract.pytesseract.tesseract_cmd = r'TESSERACT LOCATION'
import subprocess
import speech_recognition as sr


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "CREDENTIALS"
pd.options.mode.chained_assignment = None
src_filename = 'Chats+Records/1.ogg'
dest_filename = 'Chats+Records/audio.wav'

class MyClass:
  to_lang = 'ru'
  from_lang = 'ru'
  data = pd.read_csv('Chats+Records/users.csv')
  check = False
  id = 1
  from_to = False

user_text = []

def start(update, context):

    print(p1.data.head(4))
    t =  p1.data['Unique_ID']
    for i in t.values :
        if i == update.message.from_user.id:
            p1.check = True
        else :
            print(i)

    if p1.check == False:
        da = p1.data.append({'Name': update.message.from_user.first_name, 'Username': update.message.from_user.username,
                             'Unique_ID': update.message.from_user.id, 'To-Language': 'ru', 'From-Language': 'en'}, ignore_index=True)
        da.to_csv('Chats+Records/users.csv', index=False)

        print("Added new user")
        p1.check = True
    else :
        print("Already exists")
        p1.check = False

    update.message.reply_text('Привіт! Перекладіть речення будь-якою мовою')
    update.message.reply_text('Можливі команди : /start , /help , /get - отримати всі слова, які коли-небудь перекладалися  , /to_lang - обрати кінцеву мову перекладу (за замовчуванням мовою перекладу є російська), /from_lang - обрати мову аунтифікації для аудіоповідомлень (за замовчуванням мовою перекладу є англійська)')

def button(update, context):
    print('button')
    if p1.from_to== True:

        data = pd.read_csv('Chats+Records/users.csv')
        a = data[['Unique_ID', 'To-Language']]
        global j
        i = 0

        for p_id, p_info in a.items():
            for key in p_info:
                if key == p1.id:
                    j = i
                else:
                    i = i + 1

        query = update.callback_query

        p1.to_lang = query.data

        data["To-Language"][j] = str(p1.to_lang)
        data.to_csv('Chats+Records/users.csv', index=False)
        query.edit_message_text(text="Обрана мова: {}".format(query.data))

    else:
        data = pd.read_csv('Chats+Records/users.csv')
        a = data[['Unique_ID', 'From-Language']]
        global c
        i = 0

        for p_id, p_info in a.items():
            for key in p_info:
                if key == p1.id:
                    c = i
                else:
                    i = i + 1

        query = update.callback_query

        p1.from_lang = query.data

        data["From-Language"][c] = str(p1.from_lang)
        data.to_csv('Chats+Records/users.csv', index=False)
        query.edit_message_text(text="Обрана мова: {}".format(query.data))



def help(update, context):
    update.message.reply_text('Мови які підтримаються: English , Russian , Ukranian , Japanese')
    update.message.reply_text('Можливі команди : /start , /help , /get - отримати всі слова, які коли-небудь перекладалися  , /to_lang - обрати кінцеву мову перекладу (за замовчуванням мовою перекладу є російська), /from_lang - обрати мову аунтифікації для аудіоповідомлень (за замовчуванням мовою перекладу є англійська)')


def change_language(update,context):
    p1.from_to = True
    update.message.reply_text('Оберіть мову')
    keyboard = [[InlineKeyboardButton("Russian", callback_data='ru'),
                 InlineKeyboardButton("Ukranian", callback_data='uk')],
                [InlineKeyboardButton("English", callback_data='en')],
                [InlineKeyboardButton("Japanese", callback_data='ja')]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Будь-ласка оберіть:', reply_markup=reply_markup)
    p1.id = update.message.from_user.id

def change_language1(update,context):
    #p1.from_lang = 'en'

    update.message.reply_text('Оберіть мову')
    keyboard = [[InlineKeyboardButton("Russian", callback_data='ru'),
                 InlineKeyboardButton("Ukranian", callback_data='uk')],
                [InlineKeyboardButton("English", callback_data='en')],
                [InlineKeyboardButton("Japanese", callback_data='ja')]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Будь-ласка оберіть:', reply_markup=reply_markup)
    p1.id = update.message.from_user.id

    print('From_Lang')


def google_translation(text):
    client = translate.Client()
    translation = client.translate(text, target_language=p1.to_lang)
    return translation['translatedText']

def send_media(bot, chat_id, media_type, media_id, text, reply_to_id=None):
    bot.send_audio(chat_id=chat_id, audio=media_id, reply_to_message_id=reply_to_id)

def read_txt(update, context):
    f = open('Chats+Records/'+str(update.message.from_user.id)+'.txt','r',encoding='utf-8')
    text = f.read()

    f.close()

    print(len(text))
    n = 4000
    final = [text[i * n:(i + 1) * n] for i in range((len(text) + n - 1) // n)]
    for i in final:
        update.message.reply_text(str(i))

def echo(update, context):

    bot = context.bot
    before_translate = update.message.text
    print(before_translate)

    data = pd.read_csv('Chats+Records/users.csv')
    a = data[['Unique_ID', 'To-Language']]
    global d
    i = 0
    for p_id, p_info in a.items():
        for key in p_info:
            if key == update.message.from_user.id:
                d = i
            else:
                i = i + 1

    p1.to_lang  = a["To-Language"][d] # p1.to

    text = str(google_translation(update.message.text))

    print(text)


    result = before_translate + ' - ' + text
    user_text.append(result)
    update.message.reply_text(text)
    save_send_speech(update,text,bot)

def text_to_speech(text):
    gtts = gTTS(text, lang = str(p1.to_lang))
    gtts.save('Chats+Records/record.ogg')

def save_send_speech(update,text,bot):

    text_to_speech(text)
    with open('Chats+Records/' + str(update.message.from_user.id) + ".txt", "a", encoding='utf-8') as output:
        for item in user_text:
            output.write(str(item) + '\n')

    #update.message.reply_text(text)

    bot.send_audio(chat_id=update.message.from_user.id, audio=open('Chats+Records/record.ogg', 'rb'))


def photo_to_text(update, context):

    bot = context.bot
    file_id = update.message.photo[-1]
    newFile = bot.getFile(file_id)
    newFile.download('Chats+Records/photo.jpg')

    img = Image.open('Chats+Records/photo.jpg')
    img = img.convert('L')
    img = img.filter(ImageFilter.MedianFilter())
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2)
    img = img.convert('1')
    img.save('Chats+Records/image.jpg')
    imagetext = pytesseract.image_to_string(img, lang='jpn+rus+eng+ukr')
    if imagetext=='':
        update.message.reply_text("Вибачте, але нам не вдалось знайти текст на фотографії")
    else:
        update.message.reply_text("Отриманий текст мовою оригіналу: " + imagetext)
        text = str(google_translation(imagetext))

        update.message.reply_text(text)

        save_send_speech(update, text, bot)

def audio_to_text(update, context):

    print("Audio")
    bot = context.bot

    file = bot.getFile(update.message.audio.file_id)
    file.download('Chats+Records/1.ogg')

    process = subprocess.call(['G:/ffmpeg/bin/ffmpeg.exe', '-i', src_filename, '-y', dest_filename], shell=True)

    r = sr.Recognizer()

    harvard = sr.AudioFile('Chats+Records/audio.wav')
    with harvard as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.record(source)

    #a = input("Language detect :")
    a= p1.from_lang
    text = 'Не знайдена така мова , або система не змогла розпізнати текст у цьому аудіофайлі'
    if a.lower() == 'ru' or a.lower() == 'uk' or a.lower() == 'en' or a.lower() == 'ja':
        text = r.recognize_google(audio, language=a)

        text = str(google_translation(text))
        update.message.reply_text(text)
        save_send_speech(update, text, bot)

    else:
        update.message.reply_text(text)

def voice_to_text(update, context):
    
    print("Voice")
    bot = context.bot

    file = bot.getFile(update.message.voice.file_id)
    file.download('Chats+Records/1.ogg')

    process = subprocess.call(['G:/ffmpeg/bin/ffmpeg.exe', '-i', src_filename, '-y', dest_filename], shell=True)

    r = sr.Recognizer()

    harvard = sr.AudioFile('Chats+Records/audio.wav')
    with harvard as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.record(source)

    #a = input("Language detect :")
    a = p1.from_lang
    text = 'Не знайдена така мова , або система не змогла розпізнати текст у цьому аудіофайлі'
    if a.lower() == 'ru' or a.lower() == 'uk' or a.lower() == 'en' or a.lower() == 'ja':
        text = r.recognize_google(audio, language=a)

        text = str(google_translation(text))
        update.message.reply_text(text)
        save_send_speech(update, text, bot)

    else:
        update.message.reply_text(text)


def main():
    updater = Updater("TOKEN", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("get", read_txt))
    dp.add_handler(CommandHandler("to_lang", change_language))
    dp.add_handler(CommandHandler("from_lang", change_language1))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(MessageHandler(Filters.photo, photo_to_text))
    dp.add_handler(MessageHandler(Filters.voice, voice_to_text))
    dp.add_handler(MessageHandler(Filters.audio, audio_to_text))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    p1 = MyClass()
    main()
