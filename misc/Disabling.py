import asyncio, logging, time

import aiogram.types.message
# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters.command import Command
from aiogram.filters import CommandObject, Text
from aiogram import html
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from modules import database

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————


async def DisablingUsers(bot: Bot):
    TIME = int(time.time())
    TIME_TASK = TIME - 300
    USERS = await database.getMultiProgramBdData('users', f"tg_timeLastMessage < {TIME_TASK} AND tg_Connected = 1")
    for USER in USERS:
        await database.setUserData(f'{USER[1]}', 'tg_Connected', "'0'")
        await bot.delete_message(
            chat_id=USER[1],
            message_id=USER[3]
        )

        await bot.send_message(
            chat_id=USER[1],
            text='❇️ Чтобы продолжить игру, напишите /start'
        )