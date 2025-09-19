import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from validators import validate
from aiogram import F
from youtube_service import get_video_info

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
    elif error == "NO_VIDEO_ID":
        await message.answer("Не удалось найти video_id. Используй ссылку вида: https://www.youtube.com/watch?v=...")
    elif error == "UNSUPPORTED_HOST":
        await message.answer("Ссылка не на YouTube. Поддерживаю только youtube.com и youtu.be.")
    try:
        info = get_video_info(video_id)
        dur = info.get("duration") or 0
        mm = dur // 60
        ss = dur % 60
        caption = f"Нашёл видео:\n{info.get('title')}\nДлительность: {mm:02d}:{ss:02d}"

        await message.answer(caption)

    except Exception as e:
        await message.answer("Не удалось получить информацию о видео. Попробуй другую ссылку.")


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
