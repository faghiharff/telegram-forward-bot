from telethon.sync import TelegramClient
from telethon import events
import os
from flask import Flask
import threading

# سرور Flask برای health check
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Robot is running!", 200

def run_flask():
    app.run(host='0.0.0.0', port=8000)  # پورت 80 برای health check

# اطلاعات ربات
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone = os.getenv('PHONE_NUMBER')
source_chat = os.getenv('SOURCE_CHAT_ID')
destination_chat = os.getenv('DESTINATION_CHAT_ID')

# لیست کلمات کلیدی
keywords = ['entry1' , 'entry']  # کلمات مورد نظرتون

# ایجاد کلاینت تلگرام
client = TelegramClient('session', api_id, api_hash)

async def main():
    await client.start(phone=phone)
    print("ربات شروع به کار کرد!")

    @client.on(events.NewMessage(chats=int(source_chat)))
    async def handler(event):
        # گرفتن متن پیام یا کپشن
        message_text = event.message.message or ""
        # بررسی کلمات کلیدی
        for keyword in keywords:
            if message_text and keyword.lower() in message_text.lower():
                await client.forward_messages(int(destination_chat), event.message)
                print(f"پیام فوروارد شد: {event.message.id} (حاوی '{keyword}')")
                break

    await client.run_until_disconnected()

# اجرای Flask در نخ جداگانه
flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

# اجرای ربات
with client:
    client.loop.run_until_complete(main())
