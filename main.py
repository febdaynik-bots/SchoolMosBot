import asyncio
import logging

from config import dp, bot
from database.models import init_db
from handlers import start, auth_user, callback_back, client
from middlewares.user import UsersMiddleware

logger = logging.getLogger(__name__)


async def on_startup():
    print('Starting bot')
    init_db()


async def main():

    dp.startup.register(on_startup)

    dp.message.outer_middleware(UsersMiddleware())
    dp.callback_query.outer_middleware(UsersMiddleware())

    dp.include_routers(
        callback_back.router,

        auth_user.router,
        start.router,

        client.register_routers(),
    )

    await bot.me()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, skip_updates=False, аllowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    try:
        print('Starting script bot')
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.error("Exit")
