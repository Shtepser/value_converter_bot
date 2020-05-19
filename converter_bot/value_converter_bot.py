import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_polling

from converter_bot.measurements import Measurements

PROXY_URL = "http://34.253.177.131:3128"
API_TOKEN = os.environ.get("API_KEY")

logging.basicConfig(level=logging.INFO)

DEBUG = os.environ.get("DEBUG")
if DEBUG:
    bot = Bot(token=API_TOKEN, proxy=PROXY_URL)
else:
    bot = Bot(token=API_TOKEN)

dp = Dispatcher(bot)

measurements = Measurements()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await types.ChatActions.typing(1)
    await message.answer("Вас приветствует бот-конвертер")
    await send_info(message)


@dp.message_handler(commands=['info'])
async def send_info(message: types.Message):
    await types.ChatActions.typing(1)
    with open("../info_text.md", 'r') as info_file:
        info_text = info_file.read()
    await message.answer(info_text, parse_mode="MARKDOWN")


@dp.message_handler(commands=['measures'])
async def list_measures(message: types.Message):
    await types.ChatActions.typing(1)
    measures = measurements.get_measurements('ru').keys()
    await message.answer("Поддерживаемые единицы измерения:\n" + '\n'.join(measures))


@dp.message_handler(commands=['substances'])
async def list_substances(message: types.Message):
    await types.ChatActions.typing(1)
    substances = measurements.get_substances('ru').keys()
    await message.answer("Поддерживаемые вещества:\n" + '\n'.join(substances))


if __name__ == '__main__':
    start_polling(dp, skip_updates=True)
