import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_polling

PROXY_URL = "http://34.253.177.131:3128"
API_TOKEN = os.environ.get("API_KEY")

logging.basicConfig(level=logging.INFO)

DEBUG = os.environ.get("DEBUG")
if DEBUG:
    bot = Bot(token=API_TOKEN, proxy=PROXY_URL)
else:
    bot = Bot(token=API_TOKEN)

dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await types.ChatActions.typing()
    content = "Hello world!"
    await message.answer(content)


@dp.message_handler(commands=['info'])
async def send_info(message: types.Message):
    await message.answer("Информация о боте")


if __name__ == '__main__':
    start_polling(dp, skip_updates=True)
