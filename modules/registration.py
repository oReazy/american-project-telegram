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

async def registration_0(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getBdData('settings', 'id', "'1'")

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    if DATA_SERVER[17] == 1:
        await database.registerNewAccaunt(message.from_user.id)
        await registration_1(message, bot)
    else:
        MESSAGE_DELITE = await message.answer(
            '❌ <i><b>Ошибка.</b>\n⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯\nВ данный момент сервер закрыт.\n\nПопробуйте попытку регистрации позже\nвведя любое сообщение</i>')
        await asyncio.sleep(5)
        await MESSAGE_DELITE.delete()


async def registration_1(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_SERVER = await database.getBdData('settings', 'id', "'1'")
    await database.setUserData(message.from_user.id, "tg_answer", "'1'")
    await database.setUserData(message.from_user.id, "state", "'registration.registration_1_check'")

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    MAIN = await bot.send_message(
        chat_id=message.from_user.id,
        text=f"👋 <b>Приветствуем вас на {DATA_SERVER[1]} \nна сервер {DATA_SERVER[2]}</b>\n<code>⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯</code>\n"
             "❌ Данный аккаунт не зарегистрирован\n<code>⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯</code>\n"
             "📝 Придумайте ник для \nигры (от 3 до 15 символов)"
    )
    await database.setUserData(message.from_user.id, "tg_mainMessage", f"'{MAIN.message_id}'")


async def registration_1_check(message: types.Message, bot: Bot):
    RESULT = len(await database.getMultiBdData("users", "nick", f"'{message.text}'"))
    Nick = message.text.replace('<', '')
    Nick = Nick.replace('>', '')
    await message.delete()
    if len(Nick) < 3 or len(Nick) > 15:
        if len(Nick) < 3:
            MESSAGE_DELITE = await message.answer(
                '❌ <i><b>Ошибка.</b>\n⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯\nДанный ник слишком короткий</i>')
            await asyncio.sleep(5)
            await MESSAGE_DELITE.delete()
        else:
            MESSAGE_DELITE = await message.answer(
                '❌ <i><b>Ошибка.</b>\n⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯\nДанный ник слишком длинный</i>')
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
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_USER = await database.getUserData(message.from_user.id)
    await database.setUserData(message.from_user.id, "state", "'registration.registration_2'")
    await database.setUserData(message.from_user.id, "tg_answer", "'0'")

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="👨 Мужчина",
        callback_data="registration.registration_2 man")
    )
    builder.add(types.InlineKeyboardButton(
        text="👩 Женщина",
        callback_data="registration.registration_2 woman")
    )
    await bot.edit_message_text(
        text="🚻 Выберите пол вашего персонажа\n<code>⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯</code>\n⤵ Для выбора нажмите на \nодну из кнопок ниже",
        chat_id=message.from_user.id,
        message_id=DATA_USER[3],
        reply_markup=builder.as_markup())


@router.callback_query(Text("registration.registration_2 man"))
async def registration_2_man(message: types.Message, bot: Bot):
    DATA_USER = await database.getUserData(message.from_user.id)
    await database.setUserData(message.from_user.id, "tg_timeLastMessage", f"'{int(time.time())}'")
    await database.setUserData(message.from_user.id, "state", "'registration.registration_3'")
    await database.setUserData(message.from_user.id, "sex", "'Мужчина'")
    await registration_3(message, bot)


@router.callback_query(Text("registration.registration_2 woman"))
async def registration_2_woman(message: types.Message, bot: Bot):
    DATA_USER = await database.getUserData(message.from_user.id)
    await database.setUserData(message.from_user.id, "tg_timeLastMessage", f"'{int(time.time())}'")
    await database.setUserData(message.from_user.id, "state", "'registration.registration_3'")
    await database.setUserData(message.from_user.id, "sex", "'Женщина'")
    await registration_3(message, bot)


async def registration_3(message: types.Message, bot: Bot):
    DATA_USER = await database.getUserData(message.from_user.id)
    await database.setUserData(message.from_user.id, "state", "'registration.registration_3'")
    pear_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇸 Американец", callback_data="registration.registration_3 1"),
            InlineKeyboardButton(text="🇨🇦 Канадец", callback_data="registration.registration_3 2")
        ],
        [
            InlineKeyboardButton(text="🇨🇳 Китаец", callback_data="registration.registration_3 3"),
            InlineKeyboardButton(text="🇮🇹 Итальянец", callback_data="registration.registration_3 4")
        ],
        [
            InlineKeyboardButton(text="🇮🇪 Ирландец", callback_data="registration.registration_3 5"),
            InlineKeyboardButton(text="🇯🇵 Японец", callback_data="registration.registration_3 6")
        ],
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="registration.registration_3 7"),
            InlineKeyboardButton(text="🇺🇦 Украинец", callback_data="registration.registration_3 8")
        ],
        [
            InlineKeyboardButton(text="🇷🇸 Серб", callback_data="registration.registration_3 9"),
            InlineKeyboardButton(text="🇻🇳 Вьетнамец", callback_data="registration.registration_3 10")
        ]
    ])

    await bot.edit_message_text(text="⤵ Выберите национальность вашему персонажу",
                                chat_id=message.from_user.id,
                                message_id=DATA_USER[3],
                                reply_markup=pear_keyboard)


@router.callback_query(Text("registration.registration_3 1"))
async def registration_3_1(message: types.Message, bot: Bot):
    DATA_USER = await database.getUserData(message.from_user.id)
    await database.setUserData(message.from_user.id, "tg_timeLastMessage", f"'{int(time.time())}'")
    await database.setUserData(message.from_user.id, "state", "'registration.registration_4'")
    await database.setUserData(message.from_user.id, "nationality", "'Американец'")
    await registration_4(message, bot)


@router.callback_query(Text("registration.registration_3 2"))
async def registration_3_2(message: types.Message, bot: Bot):
    DATA_USER = await database.getUserData(message.from_user.id)
    await database.setUserData(message.from_user.id, "tg_timeLastMessage", f"'{int(time.time())}'")
    await database.setUserData(message.from_user.id, "state", "'registration.registration_4'")
    await database.setUserData(message.from_user.id, "nationality", "'Канадец'")
    await registration_4(message, bot)


@router.callback_query(Text("registration.registration_3 3"))
async def registration_3_3(message: types.Message, bot: Bot):
    DATA_USER = await database.getUserData(message.from_user.id)
    await database.setUserData(message.from_user.id, "tg_timeLastMessage", f"'{int(time.time())}'")
    await database.setUserData(message.from_user.id, "state", "'registration.registration_4'")
    await database.setUserData(message.from_user.id, "nationality", "'Китаец'")
    await registration_4(message, bot)


@router.callback_query(Text("registration.registration_3 4"))
async def registration_3_4(message: types.Message, bot: Bot):
    DATA_USER = await database.getUserData(message.from_user.id)
    await database.setUserData(message.from_user.id, "tg_timeLastMessage", f"'{int(time.time())}'")
    await database.setUserData(message.from_user.id, "state", "'registration.registration_4'")
    await database.setUserData(message.from_user.id, "nationality", "'Итальянец'")
    await registration_4(message, bot)


@router.callback_query(Text("registration.registration_3 5"))
async def registration_3_5(message: types.Message, bot: Bot):
    DATA_USER = await database.getUserData(message.from_user.id)
    await database.setUserData(message.from_user.id, "tg_timeLastMessage", f"'{int(time.time())}'")
    await database.setUserData(message.from_user.id, "state", "'registration.registration_4'")
    await database.setUserData(message.from_user.id, "nationality", "'Ирландец'")
    await registration_4(message, bot)


@router.callback_query(Text("registration.registration_3 6"))
async def registration_3_6(message: types.Message, bot: Bot):
    DATA_USER = await database.getUserData(message.from_user.id)
    await database.setUserData(message.from_user.id, "tg_timeLastMessage", f"'{int(time.time())}'")
    await database.setUserData(message.from_user.id, "state", "'registration.registration_4'")
    await database.setUserData(message.from_user.id, "nationality", "'Японец'")
    await registration_4(message, bot)


@router.callback_query(Text("registration.registration_3 7"))
async def registration_3_7(message: types.Message, bot: Bot):
    DATA_USER = await database.getUserData(message.from_user.id)
    await database.setUserData(message.from_user.id, "tg_timeLastMessage", f"'{int(time.time())}'")
    await database.setUserData(message.from_user.id, "state", "'registration.registration_4'")
    await database.setUserData(message.from_user.id, "nationality", "'Русский'")
    await registration_4(message, bot)


@router.callback_query(Text("registration.registration_3 8"))
async def registration_3_8(message: types.Message, bot: Bot):
    DATA_USER = await database.getUserData(message.from_user.id)
    await database.setUserData(message.from_user.id, "tg_timeLastMessage", f"'{int(time.time())}'")
    await database.setUserData(message.from_user.id, "state", "'registration.registration_4'")
    await database.setUserData(message.from_user.id, "nationality", "'Украинец'")
    await registration_4(message, bot)


@router.callback_query(Text("registration.registration_3 9"))
async def registration_3_9(message: types.Message, bot: Bot):
    DATA_USER = await database.getUserData(message.from_user.id)
    await database.setUserData(message.from_user.id, "tg_timeLastMessage", f"'{int(time.time())}'")
    await database.setUserData(message.from_user.id, "state", "'registration.registration_4'")
    await database.setUserData(message.from_user.id, "nationality", "'Серб'")
    await registration_4(message, bot)


@router.callback_query(Text("registration.registration_3 10"))
async def registration_3_10(message: types.Message, bot: Bot):
    DATA_USER = await database.getUserData(message.from_user.id)
    await database.setUserData(message.from_user.id, "tg_timeLastMessage", f"'{int(time.time())}'")
    await database.setUserData(message.from_user.id, "state", "'registration.registration_4'")
    await database.setUserData(message.from_user.id, "nationality", "'Вьетнамец'")
    await registration_4(message, bot)


async def registration_4(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_USER = await database.getUserData(message.from_user.id)
    await database.setUserData(message.from_user.id, "state", "'registration.registration_4'")
    await database.setUserData(message.from_user.id, "tg_answer", "'1'")

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    await bot.edit_message_text(text="📝 Введите возраст персонажа (от 18 до 70 лет)",
                                chat_id=message.from_user.id,
                                message_id=DATA_USER[3])
    return


async def registration_4_check(message: types.Message, bot: Bot):
    if message.text.isdigit():
        age = int(message.text)
        if 18 <= age <= 70:
            await database.setMultiUserData(message.from_user.id,
                                            f"age = '{age}', state = 'registration.registration_5'")
            await registration_5(message, bot)
            await message.delete()
        else:
            await message.delete()
            MESSAGE_DELITE = await message.answer(
                text=f"❌ <i><b>Ошибка.</b>\n⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯\nВведите возраст от 18 до 70</i>"
            )
            await asyncio.sleep(5)
            await MESSAGE_DELITE.delete()
    else:
        await message.delete()
        MESSAGE_DELITE = await message.answer(
            text=f"❌ <i><b>Ошибка.</b>\n⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯\nВведите возраст цифрами</i>и"
        )
        await asyncio.sleep(5)
        await MESSAGE_DELITE.delete()


async def registration_5(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_USER = await database.getUserData(message.from_user.id)
    await database.setUserData(message.from_user.id, "tg_timeLastMessage", f"'{int(time.time())}'")
    await database.setUserData(message.from_user.id, "state", "'registration.registration_5'")
    await database.setUserData(message.from_user.id, "tg_answer", "'0'")

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    pear_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="👥 Узнал от друзей", callback_data="registration.registration_5 1"),
        ],
        [
            InlineKeyboardButton(text="📄 Узнал из списка чат-ботов", callback_data="registration.registration_5 2"),
        ],
        [
            InlineKeyboardButton(text="🔎 Узнал из поисковой системы", callback_data="registration.registration_5 3"),
        ],
        [
            InlineKeyboardButton(text="📺 Узнал от ютубера", callback_data="registration.registration_5 4"),
        ],
        [
            InlineKeyboardButton(text="🔘 Другое", callback_data="registration.registration_5 5"),
        ]
    ])

    await bot.edit_message_text(text="🏃 Откуда вы узнали о нашем сервере?",
                                chat_id=message.from_user.id,
                                message_id=DATA_USER[3],
                                reply_markup=pear_keyboard)


@router.callback_query(Text("registration.registration_5 1"))
async def registration_5_1(message: types.Message, bot: Bot):
    DATA_SERVER = await database.getBdData('settings', 'id', "'1'")
    await database.setUserData(message.from_user.id, "tg_timeLastMessage", f"'{int(time.time())}'")
    await database.setUserData(message.from_user.id, "state", "'registration.registration_6'")
    await database.setBdData('settings', 'id', "'1'", "statistic_reg_1", f"'{DATA_SERVER[8] + 1}'")
    await registration_6(message, bot)


@router.callback_query(Text("registration.registration_5 2"))
async def registration_5_2(message: types.Message, bot: Bot):
    DATA_SERVER = await database.getBdData('settings', 'id', "'1'")
    await database.setUserData(message.from_user.id, "tg_timeLastMessage", f"'{int(time.time())}'")
    await database.setUserData(message.from_user.id, "state", "'registration.registration_6'")
    await database.setBdData('settings', 'id', "'1'", "statistic_reg_2", f"'{DATA_SERVER[9] + 1}'")
    await registration_6(message, bot)


@router.callback_query(Text("registration.registration_5 3"))
async def registration_5_3(message: types.Message, bot: Bot):
    DATA_SERVER = await database.getBdData('settings', 'id', "'1'")
    await database.setUserData(message.from_user.id, "tg_timeLastMessage", f"'{int(time.time())}'")
    await database.setUserData(message.from_user.id, "state", "'registration.registration_6'")
    await database.setBdData('settings', 'id', "'1'", "statistic_reg_3", f"'{DATA_SERVER[10] + 1}'")
    await registration_6(message, bot)


@router.callback_query(Text("registration.registration_5 4"))
async def registration_5_4(message: types.Message, bot: Bot):
    DATA_SERVER = await database.getBdData('settings', 'id', "'1'")
    await database.setUserData(message.from_user.id, "tg_timeLastMessage", f"'{int(time.time())}'")
    await database.setUserData(message.from_user.id, "state", "'registration.registration_6'")
    await database.setBdData('settings', 'id', "'1'", "statistic_reg_4", f"'{DATA_SERVER[11] + 1}'")
    await registration_6(message, bot)


@router.callback_query(Text("registration.registration_5 5"))
async def registration_5_5(message: types.Message, bot: Bot):
    DATA_SERVER = await database.getBdData('settings', 'id', "'1'")
    await database.setUserData(message.from_user.id, "tg_timeLastMessage", f"'{int(time.time())}'")
    await database.setUserData(message.from_user.id, "state", "'registration.registration_6'")
    await database.setBdData('settings', 'id', "'1'", "statistic_reg_5", f"'{DATA_SERVER[12] + 1}'")
    await registration_6(message, bot)


async def registration_6(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_USER = await database.getUserData(message.from_user.id)
    DATA_SERVER = await database.getBdData('settings', 'id', "'1'")
    await database.setUserData(message.from_user.id, "state", "'registration.registration_5'")
    await database.setUserData(message.from_user.id, "tg_answer", "'0'")

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    pear_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="💚 Подписаться", callback_data="registration.registration_6 1"),
        ],
        [
            InlineKeyboardButton(text="❌ Отказаться", callback_data="registration.registration_6 2"),
        ]
    ])

    await bot.edit_message_text(
        text=f"📬 Не желаете подписаться на \nновостную рассылку проекта?\n<code>⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯</code>\n"
             f"Если вы согласитесь, то при каждой рассылке \nвы будете получать <b>{await database.pretty(DATA_SERVER[22])}</b> долларов (💵)",
        chat_id=message.from_user.id,
        message_id=DATA_USER[3],
        reply_markup=pear_keyboard)


@router.callback_query(Text("registration.registration_6 1"))
async def registration_6_1(message: types.Message, bot: Bot):
    await database.setUserData(message.from_user.id, "tg_timeLastMessage", f"'{int(time.time())}'")
    await database.setUserData(message.from_user.id, "mailing_project", "'✅ Подписаны'")
    await registration_7(message, bot)


@router.callback_query(Text("registration.registration_6 2"))
async def registration_6_2(message: types.Message, bot: Bot):
    await database.setUserData(message.from_user.id, "tg_timeLastMessage", f"'{int(time.time())}'")
    await database.setUserData(message.from_user.id, "mailing_project", "'❌ Не подписан'")
    await registration_7(message, bot)


async def registration_7(message: types.Message, bot: Bot):
    DATA_SERVER = await database.getBdData('settings', 'id', "'1'")
    await database.setMultiUserData(message.from_user.id,
                                    f"lvl = '{DATA_SERVER[18]}', dollars = '{DATA_SERVER[19]}', donate = '{DATA_SERVER[20]}'")
    await registration_8(message, bot)


async def registration_8(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_USER = await database.getUserData(message.from_user.id)
    DATA_SERVER = await database.getBdData('settings', 'id', "'1'")
    await database.setUserData(message.from_user.id, "tg_timeLastMessage", f"'{int(time.time())}'")
    await database.setUserData(message.from_user.id, "state", "'registration.registration_8'")
    await database.setUserData(message.from_user.id, "tg_answer", "'0'")

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    pear_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="💵 Забрать пособие", callback_data="registration.registration_9"),
        ]
    ])

    await bot.edit_message_text(
        text=f"✈ Каждый человек, который прилетает в штат {DATA_SERVER[2]} получает начальное пособие:\n<code>⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯</code>\n\n"
             f"— 💵 Доллары » <b>{await database.pretty(DATA_SERVER[19])}</b>\n\n<code>⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯</code>\n"
             f"ℹ Данного пособия будет достаточно до того момента, пока вы не найдете себе работу.",
        chat_id=message.from_user.id,
        message_id=DATA_USER[3],
        reply_markup=pear_keyboard)


@router.callback_query(Text("registration.registration_9"))
async def registration_9(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_USER = await database.getUserData(message.from_user.id)
    DATA_SERVER = await database.getBdData('settings', 'id', "'1'")
    await database.setUserData(message.from_user.id, "tg_timeLastMessage", f"'{int(time.time())}'")
    await database.setUserData(message.from_user.id, "state", "'registration.registration_9'")
    await database.setUserData(message.from_user.id, "tg_answer", "'0'")
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    await bot.edit_message_text(text=f"✅ Вы успешно зарегистрировались на нашем проекте",
                                chat_id=message.from_user.id,
                                message_id=DATA_USER[3])
    Sticker = await bot.send_sticker(
        chat_id=message.from_user.id,
        sticker='CAACAgIAAxkBAAEJDodkaqIXao82Px0FYaHJaKmKRsBogQACERMAAhl7uUrmNcz2dcAi3S8E'
    )
    await asyncio.sleep(4)
    await Sticker.delete()

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    pear_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Да", callback_data="excursion.Show1"),
        ],
        [
            InlineKeyboardButton(text="❌ Отказаться", callback_data="mainMenu.Show"),
        ],
    ])

    await bot.edit_message_text(text=f"🔰 Желаете ли вы просмотреть \nдополнительную информацию о нашем сервере?",
                                chat_id=message.from_user.id,
                                message_id=DATA_USER[3],
                                reply_markup=pear_keyboard)


# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

@router.callback_query(Text("registration.newAccount"))
async def newAccount(message: types.Message, bot: Bot):
    DATA_USER = await database.getUserData(message.from_user.id)
    await bot.delete_message(chat_id=message.from_user.id, message_id=DATA_USER[3])
    await database.deleteUserData(message.from_user.id)
    await registration_0(message, bot)
