import logging
import os
import re

from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_polling
from pymorphy2 import MorphAnalyzer

from converter_bot.converter import MassVolumeConverter
from converter_bot.measurements import Measurements
from converter_bot.message_parser import MessageParser

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
message_parser = MessageParser('ru')
converter = MassVolumeConverter(measurements)
morph = MorphAnalyzer()


def is_correct_message(message: types.Message):
    return re.match(r"^\d+[,.]?\d*\s+[\w\s]+>[\w\s]+$", message.text)


def result_message(base_quantity, base_measure, target_quantity, target_measure, substance):
    target_quantity = round(target_quantity, 2)
    base_measure = measurements.get_measurements_at_lang('ru')[base_measure]
    target_measure = measurements.get_measurements_at_lang('ru')[target_measure]
    substance = measurements.get_substances_at_lang('ru')[substance]
    target_measure = morph.parse(target_measure)[0].make_agree_with_number(target_quantity).word
    return f"{base_quantity} {base_measure} {substance} = " + \
           f"{target_quantity} {target_measure}"


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await types.ChatActions.typing(1)
    await message.answer("Вас приветствует бот-конвертер")
    await send_info(message)


@dp.message_handler(commands=['info'])
async def send_info(message: types.Message):
    await types.ChatActions.typing(1)
    with open("info_text.md", 'r') as info_file:
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


@dp.message_handler(is_correct_message)
async def convert_values(message: types.Message):
    parsed_message = message_parser.parse(message.text)
    await types.ChatActions.typing(1)
    if not parsed_message:
        await message.answer("Не удаётся распознать величины в сообщении! Обратитесь к /info, "
                             "/measures и /substances.")
    else:
        quantity, base_measure, substance, target_measure = parsed_message
        target_quantity = converter.convert(substance, base_measure, target_measure, quantity)
        await message.answer(result_message(quantity, base_measure, target_quantity,
                                            target_measure, substance))


@dp.message_handler(lambda x: True)
async def convert_values(message: types.Message):
    await message.answer("Не удаётся распознать сообщение! Обратитесь к /info")


if __name__ == '__main__':
    start_polling(dp, skip_updates=True)
