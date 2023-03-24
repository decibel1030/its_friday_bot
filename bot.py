import datetime
import logging
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

import main
from config import TOKEN, FRIDAY_GROUP_LINK

bot = Bot(TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

chat_id = ""
last_sent_date = None


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply("it's Friday Bot! \n"
                        "The bot will notify you when it's Friday")
    global chat_id
    chat_id = message.chat.id


async def send_message_on_friday():
    global last_sent_date
    today = datetime.datetime.today()
    if today.weekday() == 4 and today.hour == 12 and today.minute >= 0:
        if last_sent_date != today.date():
            try:
                message_data = main.get_last_friday_pic(FRIDAY_GROUP_LINK)
                await bot.send_message(chat_id=chat_id, text=f"{message_data[0]}")
                await bot.send_photo(chat_id=chat_id, photo=f"{message_data[1]}")
                last_sent_date = today.date()
            except Exception as e:
                logging.error(f"Error sending message: {e}")


async def scheduled(send_message):
    while True:
        await send_message()
        await asyncio.sleep(10)


async def on_startup(_):
    asyncio.create_task(scheduled(send_message_on_friday))


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)