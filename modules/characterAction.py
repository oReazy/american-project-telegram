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

@router.callback_query(Text("characterAction.Show"))
async def Show(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_USER = await database.getUserData(message.from_user.id)
    await database.setUserData(message.from_user.id, "tg_timeLastMessage", f"'{int(time.time())}'")
    await database.setUserData(message.from_user.id, "state", "'characterAction.Show'")
    await database.setUserData(message.from_user.id, "tg_answer", "'0'")

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    pear_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="◀ Назад", callback_data="mainMenu.Show"),
        ],
        [
            InlineKeyboardButton(text="📊 Моя статистика", callback_data="none"),
        ],
        [
            InlineKeyboardButton(text="💼 Инвентарь", callback_data="none"),
        ],
        [
            InlineKeyboardButton(text="🚗 Меню автомобилей", callback_data="none"),
            InlineKeyboardButton(text="🏠 Меню домов", callback_data="none"),
        ],
        [
            InlineKeyboardButton(text="🏪 Меню бизнесов", callback_data="none"),
            InlineKeyboardButton(text="🤠 Меню лидера", callback_data="none"),
        ],
        [
            InlineKeyboardButton(text="⏏ Улучшения", callback_data="none"),
        ],
        [
            InlineKeyboardButton(text="📕 Мой паспорт", callback_data="none"),
            InlineKeyboardButton(text="📒 Мои лицензии", callback_data="none"),
        ],
        [
            InlineKeyboardButton(text="👕 Моя одежда", callback_data="none"),
        ],
        [
            InlineKeyboardButton(text="🐯 Татуировки", callback_data="none"),
            InlineKeyboardButton(text="👥 Меню семьи", callback_data="none"),
        ]
    ])

    await bot.edit_message_text(text="🎯 » 👤 Действия персонажа",
                                chat_id=message.from_user.id,
                                message_id=DATA_USER[3],
                                reply_markup=pear_keyboard)