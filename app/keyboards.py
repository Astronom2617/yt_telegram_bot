#KEYBOARDS

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def build_download_kb(video_id):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🎬 Video 720p', callback_data=f'dl:video:720:{video_id}'),
         InlineKeyboardButton(text='🎬 Video 1080p', callback_data=f'dl:video:1080:{video_id}')],
        [InlineKeyboardButton(text='🎧 Audio (mp3)', callback_data=f'dl:audio:{video_id}'),]
    ])
    return kb
