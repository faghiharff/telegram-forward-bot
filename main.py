        from telethon.sync import TelegramClient
        from telethon import events
        import os

        # اطلاعات ربات
        api_id = os.getenv('API_ID')  # از متغیرهای محیطی
        api_hash = os.getenv('API_HASH')
        phone = os.getenv('PHONE_NUMBER')
        source_chat = os.getenv('SOURCE_CHAT_ID')  # آیدی چت مبدا
        destination_chat = os.getenv('DESTINATION_CHAT_ID')  # آیدی چت مقصد

        # لیست کلمات کلیدی برای فیلتر
        keywords = ['entry1', 'entry']  # کلمات مورد نظرتون رو اینجا وارد کنید

        # ایجاد کلاینت تلگرام
        client = TelegramClient('session', api_id, api_hash)

        async def main():
            await client.start(phone=phone)
            print("ربات شروع به کار کرد!")

            @client.on(events.NewMessage(chats=int(source_chat)))
            async def handler(event):
                # گرفتن متن پیام یا کپشن
                message_text = event.message.message or ""  # کپشن یا متن پیام (اگر وجود داشته باشه)
                # بررسی وجود کلمات کلیدی در متن یا کپشن
                for keyword in keywords:
                    if message_text and keyword.lower() in message_text.lower():  # حساسیت به حروف کوچک/بزرگ نادیده گرفته می‌شه
                        await client.forward_messages(int(destination_chat), event.message)
                        print(f"پیام فوروارد شد: {event.message.id} (حاوی '{keyword}')")
                        break  # بعد از فوروارد، حلقه رو متوقف کن

            await client.run_until_disconnected()

        with client:
            client.loop.run_until_complete(main())