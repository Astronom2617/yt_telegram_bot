from aiogram.filters.command import Command

import asyncio
from app.state import stop_event
from validators import validate
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, FSInputFile
from youtube_service import get_video_info, format_duration, download_audio, download_video
import app.keyboards as kb
from pathlib import Path
from aiogram.exceptions import TelegramAPIError

router = Router()

# START COMMAND
@router.message(Command('start'))
async def start_command(message: Message):
    await message.answer('Привет! Я бот для скачивания видео и аудио с YouTube.')

# STOP COMMAND
@router.message(Command('stop'))
async def stop_command(message: Message):
    await message.answer("Удачи 👋")
    stop_event.set()


@router.message(F.text)
async def handle_text(message: Message):
    video_id, error = validate(message.text)
    if error == "NO_URL":
        await message.answer("Не вижу ссылки. Пришли мне URL на YouTube.")
    elif error == "NO_VIDEO_ID":
        await message.answer("Не удалось найти video_id. Используй ссылку вида: https://www.youtube.com/watch?v=...")
    elif error == "UNSUPPORTED_HOST":
        await message.answer("Ссылка не на YouTube. Поддерживаю только youtube.com и youtu.be.")
    try:
        info = get_video_info(video_id)
        caption = f"Нашёл видео:\n{info['title']}\nДлительность: {format_duration(info.get('duration'))}"

        await message.answer_photo(photo=info["thumbnail"], caption=caption, reply_markup=kb.main)



    except (ValueError, KeyError, OSError):
        await message.answer("Не удалось получить информацию о видео. Попробуй другую ссылку.")

@router.callback_query(F.data.startswith("dl:"))
async def handle_download(callback: CallbackQuery):
    await callback.answer()
    parts = callback.data.split(":")
    action = parts[1]
    quality = parts[2] if len(parts) > 2 else None
    video_id = parts[-1]
    file_path = None

    try:
        if action == 'audio':
            file_path = await asyncio.to_thread(download_audio, video_id)
            await callback.message.answer("Готовлю файл… это может занять пару минут.")
            await callback.message.answer_audio(FSInputFile(file_path))
            return

        elif action == 'video':
            if quality is None:
                await callback.message.answer("Не указанок качество")
                return
            await callback.message.answer("Готовлю файл… это может занять пару минут.")
            file_path = await asyncio.to_thread(download_video, video_id, int(quality))
            try:
                await callback.message.answer_video(FSInputFile(file_path))
            except (OSError, ValueError) as e:
                await callback.message.answer(f"Ошибка при работе с файлом: {e}")
            except TelegramAPIError as e:
                await callback.message.answer(f"Ошибка Telegram API: {e}")
    finally:
        if file_path:
            Path(file_path).unlink(missing_ok=True)
