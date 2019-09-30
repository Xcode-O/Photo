# -*- coding: utf-8 -*-

import telebot
import config
import dbworker
from spapi.spapi import SpApi

bot = telebot.TeleBot(config.token)
spapi = SpApi()

# Начало диалога
@bot.message_handler(commands=["start"])
def cmd_start(message):
    state = dbworker.get_current_state(message.chat.id)
    if state == config.States.S_ENTER_TEXT:
        bot.send_message(message.chat.id, "Кажется, кто-то обещал отправить своё имя, но так и не сделал этого ")
    else:  # Под "остальным" понимаем состояние "0" - начало диалога
        bot.send_message(message.chat.id, "Hello! Let's start.Send selfie and photo")
        dbworker.set_state(message.chat.id, config.States.S_ENTER_NAME)


# По команде /reset будем сбрасывать состояния, возвращаясь к началу диалога
@bot.message_handler(commands=["reset"])
def cmd_reset(message):
    bot.send_message(message.chat.id, "Hello! Let's start. Send selfie and photo")
    dbworker.set_state(message.chat.id, config.States.S_ENTER_NAME)


@bot.message_handler(content_types=["photo"])
def user_sending_photo(message):

 try:

    file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    src = config.photo_path + str(message.chat.id)

    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.reply_to(message, "Photo Accepted. Wait few seconds, please...")
 except Exception as e:
    bot.reply_to(message, e)


@bot.message_handler(content_types=["text"])
def process_text(message):
    result_urls = spapi.pipeline_process(message.text, str(message.chat.id))
    for link in result_urls:
        bot.send_message(message.chat.id, link)



if __name__ == "__main__":
    bot.polling(none_stop=True)
