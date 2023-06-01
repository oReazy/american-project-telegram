import asyncio, logging, time

import aiogram.types
# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters.command import Command
from aiogram.filters import CommandObject, Text
from aiogram import html
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from modules import database

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

router = Router()

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

@router.callback_query(Text("mainMenu.Show"))
async def Show(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_USER = await database.getUserData(message.from_user.id)
    DATA_SERVER = await database.getBdData('settings', 'id', "'1'")
    await database.setUserData(message.from_user.id, "tg_timeLastMessage", f"'{int(time.time())}'")
    await database.setUserData(message.from_user.id, "state", "'mainMenu.Show'")
    await database.setUserData(message.from_user.id, "tg_answer", "'0'")

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    if DATA_USER[21] > 0: builder.add(types.InlineKeyboardButton(text="🛠 Админ-панель", callback_data="admin.Check"))
    if DATA_USER[22] > 0: builder.add(types.InlineKeyboardButton(text="🛠 Тестировщик", callback_data="tester.Check"))
    if DATA_USER[49] == 1:
        if DATA_USER[21] > 0 or DATA_USER[22] > 0:
            builder.row(types.InlineKeyboardButton(text="👤", callback_data="mainMenu.Show"))
        else:
            builder.add(types.InlineKeyboardButton(text="👤", callback_data="mainMenu.Show"))
    else:
        if DATA_USER[21] > 0 or DATA_USER[22] > 0:
            builder.row(types.InlineKeyboardButton(text="👤 Действия персонажа", callback_data="characterAction.Show"))
        else:
            builder.add(types.InlineKeyboardButton(text="👤 Действия персонажа", callback_data="characterAction.Show"))
    if DATA_USER[49] == 1: builder.add(types.InlineKeyboardButton(text="📱", callback_data="none"))
    else:
        builder.row(types.InlineKeyboardButton(text="📱 Телефон", callback_data="none"))
    if DATA_USER[49] == 1: builder.add(types.InlineKeyboardButton(text="🗺", callback_data="none"))
    else:
        builder.add(types.InlineKeyboardButton(text="🗺 Карта", callback_data="none"))
    if DATA_USER[49] == 1: builder.add(types.InlineKeyboardButton(text="🤹", callback_data="none"))
    else:
        builder.row(types.InlineKeyboardButton(text="🤹 Навыки", callback_data="none"))
    if DATA_USER[49] == 1:
        builder.add(types.InlineKeyboardButton(text="💎", callback_data="none"))
    else:
        builder.add(types.InlineKeyboardButton(text="💎 Донат", callback_data="none"))
    if DATA_USER[49] == 1: builder.row(types.InlineKeyboardButton(text="⚙ Настройки", callback_data="none"))
    else:
        builder.row(types.InlineKeyboardButton(text="⚙ Настройки персонажа", callback_data="none"))
    if DATA_USER[49] == 1:
        builder.add(types.InlineKeyboardButton(text="📣 Репорт", callback_data="none"))
    else:
        builder.row(types.InlineKeyboardButton(text="📣 Связь с администрацией", callback_data="none"))
    if DATA_USER[49] == 1:
        builder.row(types.InlineKeyboardButton(text="📖 Помощь по игре", callback_data="none"))
    else:
        builder.row(types.InlineKeyboardButton(text="📖 Помощь по игре", callback_data="none"))
    if DATA_USER[49] == 1:
        builder.add(types.InlineKeyboardButton(text="📖 Правила", callback_data="none"))
    else:
        builder.add(types.InlineKeyboardButton(text="📖 Правила", callback_data="none"))
    if DATA_USER[49] == 1:
        builder.row(types.InlineKeyboardButton(text="📃 История наказаний", callback_data="none"))
    else:
        builder.row(types.InlineKeyboardButton(text="📃 История наказаний", callback_data="none"))
    if DATA_USER[49] == 1:
        builder.add(types.InlineKeyboardButton(text="📃 История ников", callback_data="none"))
    else:
        builder.add(types.InlineKeyboardButton(text="📃 История ников", callback_data="none"))

    num1 = await database.pretty(DATA_USER[12])
    num2 = await database.pretty(DATA_USER[13])
    num3 = await database.pretty(DATA_USER[14])
    num4 = await database.pretty(DATA_USER[15])
    await bot.edit_message_text(text=f"🎯 Главное меню{DATA_SERVER[13]}\n<code>⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯</code>\n💵 Доллары на руках » <b>{num1}</b>\n"
                                     f"💶 Евро на руках » <b>{num2}</b>\n"
                                     f"💴 Иены на руках » <b>{num3}</b>\n"
                                     f"💷 Фунты на руках » <b>{num4}</b>",
                                chat_id=message.from_user.id,
                                message_id=DATA_USER[3],
                                reply_markup=builder.as_markup())