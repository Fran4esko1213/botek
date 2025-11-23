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
    "Division_Stars",
    "MISHAPROSTOI",
    "Mythic_NFT",
    "m1ve_nft",
    "Moon_NFTT",
    "hlebniyQ",
    "andrew_gifts",
    "rep_horoshi",
    "Steam_newsss",
    "MarenGift",
    "zonargifts",
    "VieYab",
    "crosssovki",
    "GoldenGigg",
    "nftgiftssvsem",
    "itogistars",
    "desnity_gift",
    "tgcryptogift",
    "celestialstars2",
    "kevin_nft_tg",
    "gromodelaaaet",
    "cat_kind333",
    "cstars1",
    "distributionsd",
    "Tomulovic",
    "Cryptoznikk13",
    "Gift_Verse_Nft",
    "nftTELEGRAMN",
    "kipkogifts",
]

tele_client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
BOT_TOKEN = "8310987804:AAFFIRQsLj1eEgRT92HLJMAihcc5XSLRT2w"
bot = Bot(token=BOT_TOKEN)

# Подписчики вручную
SUBSCRIBERS = [
    7822675059,
    5996959124,
    7764827033
               ]

@tele_client.on(events.NewMessage(chats=CHANNELS))
async def handler(event):
    try:
        text = event.message.message or ""
        chat_id = event.chat_id
        msg_id = event.message.id

        # Проверяем наличие кнопок
        has_buttons = False
        if event.message.reply_markup:
            if hasattr(event.message.reply_markup, "buttons") and event.message.reply_markup.buttons:
                has_buttons = True
            elif hasattr(event.message.reply_markup, "rows") and event.message.reply_markup.rows:
                has_buttons = True

        if has_buttons:  # <-- триггерим на любое сообщение с кнопкой
            if hasattr(event.chat, "username") and event.chat.username:
                link = f"https://t.me/{event.chat.username}/{msg_id}"
            elif str(chat_id).startswith("-100"):
                link = f"https://t.me/c/{str(chat_id)[4:]}/{msg_id}"
            else:
                link = f"https://t.me/c/{chat_id}/{msg_id}"

            message = f"🎉 Найден пост с кнопкой в {getattr(event.chat, 'title', str(chat_id))}!\n\n{text}\n\n{link}"

            for user_id in SUBSCRIBERS:
                try:
                    await bot.send_message(chat_id=user_id, text=message)
                except Exception as e:
                    print(f"Не удалось отправить пользователю {user_id}: {e}")

            print(f"Отправлено сообщение: {link}")

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















