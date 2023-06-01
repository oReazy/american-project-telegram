# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

# Тестовая версия AMPR для Telegram

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

import asyncio, logging, time, states

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.filters import CommandObject, Text
from aiogram import html
from aiogram.utils.keyboard import InlineKeyboardBuilder

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

from modules import database, registration, mainMenu, admin, characterAction
from misc import Disabling

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

bot = Bot(token="6270150808:AAGTSrzismkyQdWJS2CcgPf2Il_IrskDxz4", parse_mode="HTML")
dp = Dispatcher()
dp.include_routers(registration.router)
dp.include_routers(mainMenu.router)
dp.include_routers(admin.router)
dp.include_routers(characterAction.router)

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

logging.basicConfig(level=logging.INFO)
functions = states.STATES

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

@dp.message()
async def cmd_start(message: types.Message, bot: Bot):
    if await database.findBaseData("tg_id", f"{message.from_user.id}") == 0:
        await message.delete()
        await registration.registration_0(message, bot)
    else:
        DATA_USER = await database.getUserData(message.from_user.id)
        await database.setUserData(message.from_user.id, "tg_timeLastMessage", f"'{int(time.time())}'")
        if DATA_USER[6] == 0:
            await database.setUserData(message.from_user.id, "tg_Connected", "'1'")
            state = DATA_USER[7]
            if DATA_USER[7] == 'registration.registration_1' or DATA_USER[7] == 'registration.registration_1_check':
                await registration.registration_1(message)
                await message.delete()
                return
            else:
                NEW_MESSAGE = await message.answer('📶 Подключаемся к игре...')
                await database.setUserData(message.from_user.id, "tg_mainMessage", f"'{NEW_MESSAGE.message_id}'")
                await functions[state](message, bot)
                await message.delete()
                return
        if DATA_USER[5] == 1:
            match DATA_USER[7]:
                case 'registration.registration_1_check': await registration.registration_1_check(message, bot)
                case 'registration.registration_4': await registration.registration_4_check(message, bot)
        else:
            await message.delete()

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(Disabling.DisablingUsers, "cron", second=0, args=(bot, ))
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())