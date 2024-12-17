import pyautogui
from mss import mss
import telebot
import io
# from pynput import mouse
from pynput import keyboard
import threading
from PIL import Image
import requests, json

# Создание бота
TOKEN = "6952039808:AAGjFpWGt1c_PphsMLivR8eV2l3VVEtPoT0"
bot = telebot.TeleBot(TOKEN)

def take_scr():
    monitor = {"top": 200,
               "left": 200,
               "width": pyautogui.size().width,
               "height": pyautogui.size().height
               }
    # Сделать скриншот
    scr = mss().grab(monitor)

    img = Image.frombytes('RGB', (scr.width, scr.height), scr.rgb)

    # Сохранить скриншот в байтовый буфер
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)  # Установить указатель в начало
    return img_bytes

def osrLib():
    img_bytes = take_scr()
    ocr_result = ocr_space_file(img_bytes)
    ocr_data = json.loads(ocr_result)
    parsed_text = ocr_data["ParsedResults"][0]["ParsedText"]
    return parsed_text

def send_scr():
    chat_id = "2082879504"  # ID чата для отправки
    img_bytes = take_scr()  # Получаем скриншот
    bot.send_photo(chat_id, img_bytes)  # Отправка фото
    bot.send_message(chat_id, osrLib())

def on_press(key):
    thread = threading.Thread(target=send_scr)
    if key == keyboard.Key.caps_lock:
        thread.start()

# Функция для запуска слушателя мыши в отдельном потоке
def start_listener():
    # listener = mouse.Listener(on_click=on_click)
    # listener.start() # Start the listener in the main thread
    # listener.join()
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    listener.join()

def ocr_space_file(image_data, overlay=False, api_key='K85597040988957', language='rus'):
    """ OCR.space API request with image data in bytes.
    :param image_data: Your image as a byte stream.
    :param overlay: Is OCR.space overlay required in your response.
    :param api_key: OCR.space API key.
    :param language: Language code to be used in OCR.
    :return: Result in JSON format.
    """
    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }

    # Указываем правильный MIME-тип и передаем файл как байтовый поток
    files = {'file': ('screenshot.png', image_data, 'image/png')}
    r = requests.post('https://api.ocr.space/parse/image', files=files, data=payload)
    return r.content.decode()

start_listener()