import asyncio, logging

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters.command import Command
from aiogram.filters import CommandObject, Text
from aiogram import html
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from modules import database, registration, mainMenu, admin, characterAction

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

STATES = {
    'registration.registration_1': registration.registration_1,
    'registration.registration_1_check': registration.registration_1,
    'registration.registration_2': registration.registration_2,
    'registration.registration_2 man': registration.registration_2_man,
    'registration.registration_2 woman': registration.registration_2_woman,
    'registration.registration_3': registration.registration_3,
    'registration.registration_3_1': registration.registration_3_1,
    'registration.registration_3_2': registration.registration_3_2,
    'registration.registration_3_3': registration.registration_3_3,
    'registration.registration_3_4': registration.registration_3_4,
    'registration.registration_3_5': registration.registration_3_5,
    'registration.registration_3_6': registration.registration_3_6,
    'registration.registration_3_7': registration.registration_3_7,
    'registration.registration_3_8': registration.registration_3_8,
    'registration.registration_3_9': registration.registration_3_9,
    'registration.registration_3_10': registration.registration_3_10,
    'registration.registration_4': registration.registration_4,
    'registration.registration_5': registration.registration_5,
    'registration.registration_5_1': registration.registration_5_1,
    'registration.registration_5_2': registration.registration_5_2,
    'registration.registration_5_3': registration.registration_5_3,
    'registration.registration_5_4': registration.registration_5_4,
    'registration.registration_5_5': registration.registration_5_5,
    'registration.registration_6': registration.registration_6,
    'registration.registration_6 1': registration.registration_6_1,
    'registration.registration_6 2': registration.registration_6_2,
    'registration.registration_7': registration.registration_7,
    'registration.registration_8': registration.registration_8,
    'registration.registration_9': registration.registration_9,
    'mainMenu.Show': mainMenu.Show,
    'admin.Check': admin.Check,
    'admin.list1': admin.list1,
    'admin.list2': admin.list2,
    'admin.Panel8': admin.Panel8,
    'admin.Panel8_NewAccaunt': admin.Panel8_NewAccaunt,
    'characterAction.Show': characterAction.Show,
}