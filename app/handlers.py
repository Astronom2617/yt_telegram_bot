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
from yt_dlp.utils import DownloadError, ExtractorError

router = Router()

# START COMMAND
@router.message(Command('start'))
async def start_command(message: Message):
    await message.answer_photo(photo='AgACAgIAAxkBAAPOaNBE_ycvlmoqmZePb-gd4qoOEKUAAp75MRvCIoBKBCGsGuhK11UBAAMCAAN5AAM2BA', caption="""👋 Привет!  
Я — твой YouTube Downloader Bot.  

Что я умею:  
🎬 Скачивать видео в 720p и 1080p  
🎧 Конвертировать аудио в MP3  
📸 Показывать превью и длительность ролика   

Просто пришли мне ссылку с YouTube — и выбери нужный формат. 🚀
""")

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
        caption = f"Нашёл видео:\nНазвание: {info['title']}\nДлительность: {format_duration(info.get('duration'))}"

        await message.answer_photo(photo=info["thumbnail"], caption=caption, reply_markup=kb.build_download_kb(video_id))



    except (ValueError, KeyError, OSError):
        await message.answer("Не удалось получить информацию о видео. Попробуй другую ссылку.")

@router.callback_query(F.data.startswith("dl:"))
async def handle_download(callback: CallbackQuery):
    await callback.answer()

    parts = callback.data.split(":")
    action = parts[1] if len(parts) > 1 else None
    quality = parts[2] if action == "video" and len(parts) > 3 or (action == "video" and len(parts) > 2) else (parts[2] if action == "video" and len(parts) > 2 else None)
    video_id = parts[-1] if len(parts) >= 3 else None
    file_path = None

    try:
        if action == "audio":
            await callback.message.answer("Готовлю файл… это может занять пару минут.")
            try:
                file_path = await asyncio.to_thread(download_audio, video_id)
            except (DownloadError, ExtractorError):
                await callback.message.answer("Не удалось скачать аудио. Попробуй другую ссылку или позже.")
                return
            except Exception:
                await callback.message.answer("Что-то пошло не так при скачивании аудио.")
                return

            await callback.message.answer_audio(FSInputFile(file_path))
            return

        elif action == "video":
            if quality is None:
                await callback.message.answer("Не указано качество.")
                return
            try:
                q = int(quality)
                if q not in (720, 1080):
                    await callback.message.answer("Поддерживаю 720p и 1080p.")
                    return
            except ValueError:
                await callback.message.answer("Некорректное значение качества.")
                return

            await callback.message.answer("Готовлю файл… это может занять пару минут.")
            try:
                file_path = await asyncio.to_thread(download_video, video_id, q)
            except (DownloadError, ExtractorError):
                await callback.message.answer("Не удалось скачать видео в выбранном качестве. Попробуй другое.")
                return
            except Exception:
                await callback.message.answer("Сбой при скачивании видео.")
                return

            try:
                await callback.message.answer_video(FSInputFile(file_path))
            except TelegramAPIError:
                await callback.message.answer_document(FSInputFile(file_path))
            return

        else:
            await callback.message.answer("Некорректный запрос.")
            return

    finally:
        if file_path:
            Path(file_path).unlink(missing_ok=True)