from telethon.sync import TelegramClient
from telethon import events
import os
from flask import Flask
import threading
import logging

# تنظیم لاگ دیباگ
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def health_check():
    logger.info("Health check requested")
    return "Robot is running!", 200

def run_flask():
    logger.info("Starting Flask server on port 8000")
    app.run(host='0.0.0.0', port=8000)

try:
    logger.info("Reading environment variables")
    api_id = os.getenv('API_ID')
    api_hash = os.getenv('API_HASH')
    phone = os.getenv('PHONE_NUMBER')
    source_chat = os.getenv('SOURCE_CHAT_ID')
    destination_chat = os.getenv('DESTINATION_CHAT_ID')

    if not all([api_id, api_hash, phone, source_chat, destination_chat]):
        logger.error("Missing environment variables")
        raise ValueError("One or more environment variables are missing")

    logger.info("Environment variables loaded successfully")

    keywords = ['entry' , 'entry1']
    client = TelegramClient('session', int(api_id), api_hash)

    async def main():
        logger.info("Starting Telegram client")
        await client.start(phone=phone)
        logger.info("ربات شروع به کار کرد!")

        @client.on(events.NewMessage(chats=int(source_chat)))
        async def handler(event):
            message_text = event.message.message or ""
            for keyword in keywords:
                if message_text and keyword.lower() in message_text.lower():
                    await client.forward_messages(int(destination_chat), event.message)
                    logger.info(f"پیام فوروارد شد: {event.message.id} (حاوی '{keyword}')")
                    break

        await client.run_until_disconnected()

    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    logger.info("Starting main loop")
    with client:
        client.loop.run_until_complete(main())

except Exception as e:
    logger.error(f"Error in main script: {str(e)}", exc_info=True)
    raise
