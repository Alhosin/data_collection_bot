import os
import telebot
from bot_utils import get_photo, send_photo, run_face_detctor, photo_dimensions, download_voice_message, save_photo, create_save_dir, save_others
import cv2

# define the bot_token of the telebot
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)
print(BOT_TOKEN)

# replay to the start message
@bot.message_handler(commands=['start'])
def send_welcome(message) :
    bot.reply_to(message, "Hi, what is your name?")


@bot.message_handler(func=lambda msg:True, content_types=['text'])    
def echo_all(message):
    name = str(message.text)
    bot.reply_to(message,f"hello {name}")

# if the recieved message is photo, process it and replay with confirmation message, photo dimensions and photo with detected faces if any faces were found
@bot.message_handler(func=lambda msg:True , content_types=['photo'])
def default_command(message):
    faces, detected_image = run_face_detctor(bot, message)
    # binary_image = cv2.imread(detected_image)
    _, buffer = cv2.imencode('.jpg', detected_image)
    binary_stream = buffer.tobytes()
    if len(faces) == 0:
        bot.send_message(message.chat.id, "face not found")
        faces = False
        dir = create_save_dir(bot,message,faces)

    else:
        bot.send_message(message.chat.id, f"face found : {faces}")
        photo_dimensions(bot, message)
        bot.send_photo(message.chat.id, binary_stream)
        faces=True
        dir = create_save_dir(bot, message, faces)
    save_photo(bot, message, dir)

# download voice message
@bot.message_handler(content_types=['voice'])
def default_command(message):
    dir = create_save_dir(bot,message)
    download_voice_message (bot, message,dir)

# download other messages

@bot.message_handler(content_types=['document','audio', 'video', 'animation', 'sticker', 'video_note', 'location', 'contact'])
def handle_others(message):
    #save other messages to a file
    dir = create_save_dir(bot,message)
    save_others (bot,message,dir)

                   
bot.infinity_polling()

