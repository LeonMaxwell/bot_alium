from aiogram import executor, types
from loguru import logger

from loader import dp
import middlewares, filters, handlers
from utils.set_bot_commands import set_default_commands
from utils.notify_admins import on_startup_notify


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)
    logger.info("Бот запущен")

if __name__ == '__main__':
    executor.start_polling(
        dispatcher=dp,
        on_startup=on_startup,
        skip_updates=True,
        allowed_updates=types.AllowedUpdates.all()
    )