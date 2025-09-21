from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🎬 Video 720p', callback_data='dl:video:720:<id>'), InlineKeyboardButton(text='🎬 Video 1080p', callback_data='dl:video:1080:<id>')],
    [InlineKeyboardButton(text='🎧 Audio (mp3)', callback_data='dl:audio:<id>')]])
