# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

# Тестовая версия AMPR для Telegram

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

import asyncio, logging

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.filters import CommandObject, Text
from aiogram import html
from aiogram.utils.keyboard import InlineKeyboardBuilder

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

from modules import database, registration

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

bot = Bot(token="6270150808:AAGTSrzismkyQdWJS2CcgPf2Il_IrskDxz4", parse_mode="HTML")
dp = Dispatcher()
dp.include_routers(registration.router)

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

logging.basicConfig(level=logging.INFO)

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

@dp.message()
async def cmd_start(message: types.Message):
    if await database.findBaseData("tg_id", f"{message.from_user.id}") == 0:
        await message.delete()
        await registration.registration_0(message)
    else:
        DATA_USER = await database.getUserData(message.from_user.id)
        if DATA_USER[4] == 1:
            match DATA_USER[3]:
                case 'registration_1_check':
                    await registration.registration_1_check(message, bot)
        else:
            await message.delete()

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())