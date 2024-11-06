import asyncio
from aiogram import Bot, Dispatcher
from aiogram.methods import DeleteWebhook
from App.user_handlers import router
from App.admin_handlers import router_admin
from BotData.config import bot_token
import BotData.lab_function as lf
import BotData.database_function as db
async def on_startup():
    await db.db_start()

async def main():
    bot = Bot(token=bot_token)
    dp = Dispatcher()
    dp.include_routers(router, router_admin)
    dp.startup.register(on_startup)
    asyncio.create_task(lf.check_time(bot))
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)



if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt():
        print('Бот выключен')