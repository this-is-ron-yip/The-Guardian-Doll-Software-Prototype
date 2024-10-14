import requests
import time
import os
from datetime import datetime
import threading

# Replace with your actual bot token
TELEGRAM_BOT_TOKEN = '7332577191:AAEECUvEijAWozYBPr0Fetun9By2Y4v58Ls'
CHAT_ID = '6707018481'  # Replace with the actual chat ID

# Directory to save received recordings
RECEIVED_RECORDINGS_DIR = "Recording_receive"
LOG_FILE_PATH = "log.txt"

# Ensure the directory for received recordings exists
os.makedirs(RECEIVED_RECORDINGS_DIR, exist_ok=True)

# Function to send a text message to a user
def send_text_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Text message sent successfully!")
    else:
        print("Failed to send text message.", response.json())

# Function to send an audio message to a user
def send_audio_message(chat_id, audio_file_path):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendVoice"
    files = {'voice': open(audio_file_path, 'rb')}
    data = {'chat_id': chat_id}
    response = requests.post(url, files=files, data=data)
    if response.status_code == 200:
        print("Audio message sent successfully!")
    else:
        print("Failed to send audio message.", response.json())

# Function to poll for updates from Telegram
def poll_updates(output_list):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    last_update_id = None

    while True:
        params = {'timeout': 100, 'offset': last_update_id}
        response = requests.get(url, params=params)
        updates = response.json()

        if updates['ok']:
            for result in updates['result']:
                # Extract update_id, message text, and sender information
                update_id = result['update_id']
                message = result.get('message', {})
                text = message.get('text')
                chat_id = message['chat']['id']

                # Handle received text message
                if text:
                    print(f"\nReceived message from user: {text}")
                    with open(LOG_FILE_PATH, 'a') as log_file:
                        log_file.write(f"[{datetime.now().isoformat()}] Received message: {text}\n")
                    # Store the message to output list for further use
                    output_list.append({'type': 'text', 'content': text})

                # Handle received voice message
                if 'voice' in message:
                    file_id = message['voice']['file_id']
                    file_info_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getFile"
                    file_response = requests.get(file_info_url, params={'file_id': file_id})
                    file_info = file_response.json()

                    if file_info['ok']:
                        file_path = file_info['result']['file_path']
                        download_url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}"
                        audio_response = requests.get(download_url)
                        if audio_response.status_code == 200:
                            audio_file_path = os.path.join(RECEIVED_RECORDINGS_DIR, f"voice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.ogg")
                            with open(audio_file_path, 'wb') as audio_file:
                                audio_file.write(audio_response.content)
                            print(f"\nReceived audio file saved at: {audio_file_path}")
                            with open(LOG_FILE_PATH, 'a') as log_file:
                                log_file.write(f"[{datetime.now().isoformat()}] Received audio file: {audio_file_path}\n")
                            # Store the audio file path to output list for further use
                            output_list.append({'type': 'audio', 'content': audio_file_path})

                # Update the last_update_id to avoid receiving the same message again
                last_update_id = update_id + 1

        # Sleep a bit to avoid hitting Telegram's rate limit
        time.sleep(1)

# Example function to interact with the bot
def thirdPartyBlackBox(inputText: str = None, inputAudio=None, output_list=None):
    if output_list is None:
        output_list = []  # This will hold the received messages and recordings

    # Start polling for updates in the background if not already running
    if not threading.active_count() > 1:  # Ensures only one polling thread runs
        polling_thread = threading.Thread(target=poll_updates, args=(output_list,), daemon=True)
        polling_thread.start()

    # Send input text message if provided
    if inputText:
        send_text_message(CHAT_ID, inputText)

    # Send input audio if provided
    if inputAudio:
        # Save audio to a file
        audio_file_path = "audio_to_send.mp3"
        with open(audio_file_path, 'wb') as f:
            f.write(inputAudio)
        # Send audio message
        send_audio_message(CHAT_ID, audio_file_path)

    # Return the output list containing received messages and recordings
    return output_list

if __name__ == "__main__":
    # Example usage of the function in standalone mode
    print("Starting bot interaction...")
    output_list = []  # Shared output list to store responses
    while True:
        try:
            # You can provide input text or audio for each iteration to interact with the bot
            user_input = input("Enter a message to send (or type 'exit' to quit): ")
            if user_input.lower() == 'exit':
                print("Exiting bot interaction loop.")
                break

            responses = thirdPartyBlackBox(inputText=user_input, output_list=output_list)
            print("Responses received so far:")
            for response in responses:
                print(response)

        except KeyboardInterrupt:
            print("\nExiting bot interaction loop.")
            break
