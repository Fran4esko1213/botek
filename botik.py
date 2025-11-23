import asyncio
from telethon import TelegramClient, events, errors
from telegram import Bot

API_ID = 34969496
API_HASH = "92893c3fa67e7d33ba6c633ecc29250a"
SESSION_NAME = "session"

CHANNELS = [
    "brago222",
    "starswinner",
    "s27channel",
    "Starkiska",
    "me4ffa1",
    # ... остальные каналы
]

BOT_TOKEN = "8310987804:AAFFIRQsLj1eEgRT92HLJMAihcc5XSLRT2w"
SUBSCRIBERS = [7822675059, 5996959124, 7764827033]

# Теги, на которые нужно реагировать
KEYWORDS = ["giveaway", "contest", "nft", "gift", "нфт"]

tele_client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
bot = Bot(token=BOT_TOKEN)

# Множество для хранения уже отправленных постов (chat_id + msg_id)
sent_posts = set()

@tele_client.on(events.NewMessage(chats=CHANNELS))
async def handler(event):
    try:
        text = event.message.message or ""
        chat_id = event.chat_id
        msg_id = event.message.id

        # Проверяем, был ли уже отправлен этот пост
        post_key = f"{chat_id}_{msg_id}"
        if post_key in sent_posts:
            print(f"Пропущен дубликат: {post_key}")
            return

        # Проверяем наличие кнопок
        has_buttons = False
        if event.message.reply_markup:
            if hasattr(event.message.reply_markup, "buttons") and event.message.reply_markup.buttons:
                has_buttons = True
            elif hasattr(event.message.reply_markup, "rows") and event.message.reply_markup.rows:
                has_buttons = True

        # Проверяем наличие ключевых тегов
        has_keyword = any(keyword.lower() in text.lower() for keyword in KEYWORDS)

        # Триггерим, если есть кнопки или нужные теги
        if has_buttons or has_keyword:
            # Формируем ссылку на сообщение
            if hasattr(event.chat, "username") and event.chat.username:
                link = f"https://t.me/{event.chat.username}/{msg_id}"
            elif str(chat_id).startswith("-100"):
                link = f"https://t.me/c/{str(chat_id)[4:]}/{msg_id}"
            else:
                link = f"https://t.me/c/{chat_id}/{msg_id}"

            message = f"🎉 Найден пост в {getattr(event.chat, 'title', str(chat_id))}!\n\n{text}\n\n{link}"

            # Отправляем подписчикам
            for user_id in SUBSCRIBERS:
                try:
                    await bot.send_message(chat_id=user_id, text=message)
                except Exception as e:
                    print(f"Не удалось отправить пользователю {user_id}: {e}")

            print(f"Отправлено сообщение: {link}")

            # Добавляем в множество обработанных постов
            sent_posts.add(post_key)

    except Exception as e:
        print(f"Ошибка при обработке Telethon-сообщения: {e}")


async def main():
    await tele_client.start()
    print("Telethon клиент запущен!")

    for chat in CHANNELS:
        try:
            entity = await tele_client.get_entity(chat)
            print(f"✅ Подключен к {getattr(entity, 'title', chat)}")
        except (errors.UsernameNotOccupiedError, ValueError, errors.ChannelInvalidError) as e:
            print(f"❌ Ошибка подключения к {chat}: {e}")

    await tele_client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
