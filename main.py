import asyncio
from aiogram import Bot, Dispatcher

from handlers import crud, commands, registration


async def main():
    bot = Bot(token='6359577108:AAGNikkPI1dLNUN3F7jOYTvBwyC1NomTAJE')
    dp = Dispatcher()

    dp.include_routers(crud.router)
    dp.include_router(registration.router)
    dp.include_router(commands.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
