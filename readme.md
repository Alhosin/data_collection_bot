# Telegram Bot for data collection

This Python script is a Telegram bot that receives photos and run face detection on them, replying with photos with boundary box in case it finds faces or reply with "face not found" message if it could not detect faces in the photo. Also this bot save received voice messages and resamples them to 16KHz. all photos and voice messages recieved are saved in unique folders. If this bot receive any other file, will save it to .

## Features

- Receives and saves files sent by users.
- Organizes files into unique folders.
- Supports various types of files, including documents, audio, video, animations, stickers.
- Provides feedback to users when files are saved.

## Prerequisites

- Python 3.x
- opencv-python 4.8.0
- pydub 0.25.1
- telebot 0.0.5
- ffmpeg
## Setup

1. Clone this repository to your local machine.
2. Create a Telegram bot and obtain the API token. Follow [Telegram's guide](https://core.telegram.org/bots#botfather) to create a bot and get the token.
3. Add token to system environment variables
   In Linux `export BOT_TOKEN=...`
   In Windows `set BOT_TOKEN=...`
4. Install the required library using pip install python-telegram-bot.
5. Run the script using `python run_bot.py`


## Usage

- Send various types of files to the bot.
- The bot will save the received files to unique folders within the specified directory.
- The bot will detect faces in photos.
- The bot saves voice messages, return the original sampling rate and resample them to 16Khz
- It will respond to the user with the saved file path.
