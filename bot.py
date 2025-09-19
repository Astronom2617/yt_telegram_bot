import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from validators import validate
from aiogram import F

logging.basicConfig(level=logging.INFO)
bot = Bot(token='7505097627:AAFdThZ86zhmi3WTk3YOToDYLhiROD4n74k')
dp = Dispatcher()

# START COMMAND
@dp.message(Command('start'))
async def start_command(message: types.Message):
    await message.answer('Привет! Я бот для скачивания видео и аудио с YouTube.')

# STOP COMMAND
@dp.message(Command('stop'))
async def stop_command(message: types.Message):
    await message.answer("Удачи 👋")
    await dp.stop_polling()

@dp.message(F.text)
async def handle_text(message: types.Message):
    video_id, error = validate(message.text)
    if error == "NO_URL":
        await message.answer("Не вижу ссылки. Пришли мне URL на YouTube.")
    elif error == "UNSUPPORTED_HOST":
        await message.answer("Ссылка не на YouTube. Поддерживаю только youtube.com и youtu.be.")
    else:
        await message.answer(f"Нашёл видео: {video_id}")


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
