from PIL import Image
import io
from io import BytesIO
import os
import cv2
import numpy as np
from face_detector import detect_face
from pydub import AudioSegment
import uuid
from configs import default_config
# download photo as binary 
def get_photo(bot, message):
    photo = message.photo[-1]
    file_id = photo.file_id
    file_info = bot.get_file(file_id)
    file_path = file_info.file_path
    binary_image = bot.download_file(file_path)

    return binary_image

# create a saving directory
def create_save_dir(bot, message,faces=None): 
    message_content_type = message.content_type
    root_folder = default_config['collected_data_path']
    os.makedirs(root_folder, exist_ok=True)

    chat_id = message.chat.id
    chat_folder_path = os.path.join(root_folder, str(chat_id))
    os.makedirs(chat_folder_path, exist_ok=True)

    voice_message_folder = os.path.join(chat_folder_path,"voice_messages")
    os.makedirs(voice_message_folder, exist_ok=True)

    other_docs = os.path.join(chat_folder_path,"others")
    os.makedirs(other_docs, exist_ok=True)

    # image_folder_name = str(uuid.uuid4())
    image_folder_path = os.path.join(chat_folder_path, "images")
    os.makedirs(image_folder_path, exist_ok=True)
    #creat two subfolders for images
    image_subfolder1 = os.path.join(image_folder_path,"images_with_faces")
    os.makedirs(image_subfolder1, exist_ok=True)

    image_subfolder2 = os.path.join(image_folder_path, "images_without_faces")
    os.makedirs(image_subfolder2, exist_ok=True)
    if message_content_type=='photo' and faces == True:
        return image_subfolder1
    elif message_content_type=='photo' and faces==False:
        return image_subfolder2
    elif message_content_type=='voice':
        return voice_message_folder
    else:
        return other_docs


# save photo to the device and replay with confirmation message containing the path to the saved photo
def save_photo(bot, message, dir):
    photo = message.photo[-1] # det the largest available photo
    image_file_id = photo.file_id
    image_info = bot.get_file(image_file_id)
    image_file = bot.download_file(image_info.file_path)
    image_extension = os.path.splitext(image_info.file_path)[1]
    image_filename = f"{str(uuid.uuid4())}{image_extension}"
    image_with_face__save_path = os.path.join(dir, image_filename)
    
    with open(image_with_face__save_path, "wb") as file:
        file.write(image_file)
        bot.reply_to(message, f"Image Saved as:{image_filename}")

# send a photo from the device
def send_photo(bot, chat_id, path_to_photo='/home/alhasan/Desktop/alhosin/output/frame0364.png'):
    with open(path_to_photo, 'rb') as photo:
        bot.send_photo(chat_id, photo)

# return the dimensions of the send photo
def photo_dimensions(bot, message):
    binary_image = get_photo(bot, message)
    image = Image.open(io.BytesIO(binary_image))
    width, height = image.size
    bot.reply_to(message, f"Received photo dimensions: {width} x {height}")

# detect the faces in the photo and return the bounding box of each face and the image with rectangle that indicate the face
def run_face_detctor(bot, message):
    # get photo
    bianry_image = get_photo(bot, message)
    # convert binary to RGB
    image_array = np.frombuffer(bianry_image, dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    # image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # call face detection module
    faces = detect_face(image)
    # detected image
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 4)
    # detected_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # return faces
    return faces, image

# download voice message as .wav and send its sampling rate
def download_voice_message(bot, message,dir):
    #Generate unique file names
    unique_id = str(uuid.uuid4())
    ogg_filename = f"{unique_id}.ogg"
    wav_filename = f"{unique_id}.wav"
    resampled_wav_filename = f"{unique_id}_resampled.wav"

    # Recieve and save the voice message
    voice_data = bot.get_file(message.voice.file_id)
    voice_file = bot.download_file(voice_data.file_path)

    # save voice message inside the chat's voice_message folder
    # voice_message_folder = os.path.join(chat_folder_path,"voice_messages")
    # os.makedirs(voice_message_folder, exist_ok=True)
    with open(os.path.join(dir, ogg_filename), "wb") as file:
        file.write(voice_file)

    #Convert to wav and get the sampling rate
    audio = AudioSegment.from_ogg(io.BytesIO(voice_file))
    audio.export(os.path.join(dir, wav_filename), format="wav")
    original_sampling_rate = audio.frame_rate

    #Resample to 16KHz
    audio = audio.set_frame_rate(16000)
    audio.export(os.path.join(dir, resampled_wav_filename), format="wav")
    new_sampling_rate = 16000

    #send the sampling rates
    bot.reply_to(message, f"Original sampling rate: {original_sampling_rate}\n"
                 f"Resampled sampling rate: {new_sampling_rate}")
   
# download other types of messages
def save_others(bot, message, dir):
    # get file id and file type
    file_id = message.document.file_id if message.content_type == 'document' else \
            message.audio.file_id if message.content_type == 'audio' else \
            message.vedio.file_id if message.content_type == 'vedio' else \
            message.animation.file_id if message.content_type == 'animation' else \
            message.sticker.file_id if message.content_type == 'sticker' else \
            message.vedio.file_id if message.content_type == 'vedio' else \
            message.location.file_id if message.content_type == 'location' else \
            message.contact.file_id if message.content_type == 'contact' else None
    if file_id:
        #get file details
        file_info = bot.get_file(file_id)
        file_extension = file_info.file_path.split(".")[-1]

        # save file to folder
        file_path = os.path.join(dir, f"received_file.{file_extension}")
        with open(file_path, "wb") as file:
            file.write(bot.download_file(file_info.file_path))
        # respond to the user
        bot.reply_to(message, f"File saved as:{file_path}")
