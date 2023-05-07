import asyncio, logging

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

async def registration_0(message: types.Message):
    await database.registerNewAccaunt(message.from_user.id)
    await registration_1(message)
    await database.setUserData(message.from_user.id, "is_answer", "'1'")

async def registration_1(message: types.Message):
    MAIN = await message.answer("👋 <b>Приветствуем вас на American Project на сервер Test</b>\n\n"
                         "❌ Данный аккаунт не зарегистрирован\n\n"
                         "📝 Придумайте ник для игры (от 3 до 15 символов)")
    print(MAIN)
    await database.setUserData(message.from_user.id, "tg_main_message", f"'{MAIN.message_id}'")


async def registration_1_check(message: types.Message, bot: Bot):
    RESULT = len(await database.getMultiBdData("users", "nick", f"'{message.text}'"))
    Nick = message.text.replace('<', '')
    Nick = Nick.replace('>', '')
    await message.delete()
    if len(Nick) > 15:
        MESSAGE_DELITE = await message.answer('❌ <i><b>Ошибка.</b>\n⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯\nДанный ник слишком длинный</i>')
        await asyncio.sleep(5)
        await MESSAGE_DELITE.delete()
    else:
        if RESULT > 0:
            MESSAGE_DELITE = await message.answer('❌ <i><b>Ошибка.</b>\n⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯\nДанный ник уже занят</i>')
            await asyncio.sleep(5)
            await MESSAGE_DELITE.delete()
        else:
            await database.setUserData(message.from_user.id, 'nick', f"'{Nick}'")
            await registration_2(message, bot)


async def registration_2(message: types.Message, bot: Bot):
    DATA_USER = await database.getUserData(message.from_user.id)
    await database.setUserData(message.from_user.id, "is_answer", "'0'")
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="👨 Мужчина",
        callback_data="registration_3")
    )
    builder.add(types.InlineKeyboardButton(
        text="👩 Женщина",
        callback_data="registration_3")
    )

    await bot.edit_message_text(text="🚻 Выберите пол вашего персонажа\n\n⤵ Для выбора нажмите на одну из кнопок ниже",
                                chat_id=message.from_user.id,
                                message_id=DATA_USER[2],
                                reply_markup=builder.as_markup())


@router.callback_query(Text("registration_3"))
async def send_random_value(callback: types.CallbackQuery):
    pear_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇸 Американец", callback_data="registration_4"),
            InlineKeyboardButton(text="🇨🇦 Канадец", callback_data="registration_4")
        ],
        [
            InlineKeyboardButton(text="🇨🇳 Китаец", callback_data="registration_4"),
            InlineKeyboardButton(text="🇮🇹 Итальянец", callback_data="registration_4")
        ],
        [
            InlineKeyboardButton(text="🇮🇪 Ирландец", callback_data="registration_4"),
            InlineKeyboardButton(text="🇯🇵 Японец", callback_data="registration_4")
        ],
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="registration_4"),
            InlineKeyboardButton(text="🇺🇦 Украинец", callback_data="registration_4")
        ],
        [
            InlineKeyboardButton(text="🇷🇸 Серб", callback_data="registration_4"),
            InlineKeyboardButton(text="🇻🇳 Вьетнамец", callback_data="registration_4")
        ]
    ])

    await callback.message.edit_text(text="⤵ Выберите национальность вашему персонажу",
                                reply_markup=pear_keyboard)