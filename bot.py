#RUNNING FILE
import asyncio
import logging.config, os
import contextlib
from aiogram import Bot, Dispatcher
from config import TOKEN
from app.handlers import router
from app.state import stop_event

os.makedirs("logs", exist_ok=True)
logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)
logger.info("Starting bot...")

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
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting...")