import asyncio
import logging

import uvicorn
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from bot.handlers import setup_routers
from bot.middlewares import setup_middlewares
from core.config import settings
from core.lifespan import lifespan
from api.app import create_app

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


async def start_polling():
    """Start bot in polling mode (for development)."""
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()

    setup_routers(dp)
    setup_middlewares(dp)

    logger.info("Starting bot in polling mode...")
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


async def start_webhook():
    """Start bot in webhook mode with FastAPI (for production)."""
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()

    setup_routers(dp)
    setup_middlewares(dp)

    app = create_app(bot=bot, dp=dp)

    await bot.set_webhook(
        url=f"{settings.WEBHOOK_BASE_URL}/webhook",
        secret_token=settings.WEBHOOK_SECRET,
    )
    logger.info(f"Webhook set to {settings.WEBHOOK_BASE_URL}/webhook")

    config = uvicorn.Config(
        app=app,
        host="0.0.0.0",
        port=settings.PORT,
        log_level="info",
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    if settings.USE_WEBHOOK:
        asyncio.run(start_webhook())
    else:
        asyncio.run(start_polling())
