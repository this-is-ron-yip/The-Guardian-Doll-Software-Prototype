import os
import requests
import time
import threading
from datetime import datetime
import logging
from requests.exceptions import RequestException
from queue import Queue

# Create a custom filter to only allow certain logs to the console
class SelectiveLogFilter(logging.Filter):
    def filter(self, record):
        # Allow only messages that contain these phrases
        important_phrases = [
            "Text message sent successfully",
            "Audio message sent successfully",
            "Received audio file saved",
            "Received message"
        ]
        return any(phrase in record.getMessage() for phrase in important_phrases)

# Formatter with timestamp and level for file logging (detailed logs)
detailed_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

# File handler for detailed logging
file_handler = logging.FileHandler("log.txt", encoding='utf-8')
file_handler.setFormatter(detailed_formatter)

# Console handler with the same formatter (but will filter messages)
console_handler = logging.StreamHandler()
console_handler.setFormatter(detailed_formatter)

# Apply the custom filter to the console handler
console_handler.addFilter(SelectiveLogFilter())

# Set up root logger
logging.basicConfig(level=logging.INFO, handlers=[file_handler, console_handler])

# Telegram Bot API configurations
TELEGRAM_BOT_TOKEN = '7332577191:AAEECUvEijAWozYBPr0Fetun9By2Y4v58Ls'
CHAT_ID = '7965829443'

# Directory to save received recordings
RECEIVED_RECORDINGS_DIR = "Recording_receive"
os.makedirs(RECEIVED_RECORDINGS_DIR, exist_ok=True)

# Global variables
POLLING_INTERVAL = 1  # 1 second polling interval
TIMEOUT = 100  # Long polling timeout in seconds
message_queue = Queue()

# Function to send a text message to a user via Telegram
def send_text_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {'chat_id': chat_id, 'text': text}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        logging.info("Text message sent successfully.")
    except RequestException as e:
        logging.error(f"Failed to send text message: {e}")

# Function to send an audio message to a user via Telegram
def send_audio_message(chat_id, audio_file_path):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendVoice"
    with open(audio_file_path, 'rb') as audio_file:
        files = {'voice': audio_file}
        data = {'chat_id': chat_id}
        try:
            response = requests.post(url, files=files, data=data)
            response.raise_for_status()
            logging.info(f"Audio message sent successfully from {audio_file_path}.")
        except RequestException as e:
            logging.error(f"Failed to send audio message: {e}")

# Polling function to receive updates from Telegram (e.g., new messages)
def poll_updates():
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    last_update_id = None

    while True:
        params = {'timeout': TIMEOUT, 'offset': last_update_id}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            updates = response.json()

            if updates['ok']:
                for result in updates['result']:
                    update_id = result['update_id']
                    message = result.get('message', {})
                    text = message.get('text')

                    if text:
                        logging.info(f"Received message: {text}")
                        message_queue.put({'type': 'text', 'content': text})

                    if 'voice' in message:
                        handle_voice_message(message['voice'])

                    last_update_id = update_id + 1

        except RequestException as e:
            logging.error(f"Error while polling updates: {e}")
            time.sleep(POLLING_INTERVAL)

        time.sleep(POLLING_INTERVAL)

# Function to handle received voice messages
def handle_voice_message(voice_data):
    file_id = voice_data['file_id']
    file_info_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getFile"

    try:
        file_info_response = requests.get(file_info_url, params={'file_id': file_id})
        file_info_response.raise_for_status()
        file_info = file_info_response.json()

        if file_info['ok']:
            file_path = file_info['result']['file_path']
            download_url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}"

            audio_response = requests.get(download_url)
            audio_response.raise_for_status()

            file_extension = os.path.splitext(file_path)[1]
            audio_file_name = f"voice_{datetime.now().strftime('%Y%m%d_%H%M%S')}{file_extension}"
            audio_file_path = os.path.join(RECEIVED_RECORDINGS_DIR, audio_file_name)

            with open(audio_file_path, 'wb') as audio_file:
                audio_file.write(audio_response.content)

            logging.info(f"Received audio file saved at: {audio_file_path}")
            message_queue.put({'type': 'audio', 'content': audio_file_path})

    except RequestException as e:
        logging.error(f"Error handling voice message: {e}")

# Function to interface with the blackbox (sending/receiving messages)
def thirdPartyBlackBox(inputText=None, inputAudio=None, output_list=None):
    # Start polling for updates in the background if not already running
    if not any([thread.name == 'polling_thread' for thread in threading.enumerate()]):
        logging.info("Starting polling thread...")
        polling_thread = threading.Thread(target=poll_updates, name='polling_thread', daemon=True)
        polling_thread.start()
    else:
        logging.info("Polling thread already running.")

    # Send input text message if provided
    if inputText:
        send_text_message(CHAT_ID, inputText)

    # Send input audio if provided
    if inputAudio:
        send_audio_message(CHAT_ID, inputAudio)

    # Return all messages in the queue as a list
    messages = []
    while not message_queue.empty():
        messages.append(message_queue.get())

    return messages
