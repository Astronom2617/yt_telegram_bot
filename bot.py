import asyncio
import logging
import contextlib
from aiogram import Bot, Dispatcher, types
from config import TOKEN
from app.handlers import router
from app.state import stop_event

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    dp.include_router(router)
    polling_task = asyncio.create_task(dp.start_polling(bot))
    await stop_event.wait()
    polling_task.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await polling_task

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting...")