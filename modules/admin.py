import asyncio, logging, time

import aiogram.types
# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters.command import Command
from aiogram.filters import CommandObject, Text
from aiogram import html
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from modules import database, mainMenu

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

router = Router()

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

@router.callback_query(Text("admin.Check"))
async def Check(message: types.Message, bot: Bot):
    DATA_USER = await database.getUserData(message.from_user.id)

    if DATA_USER[21] > 0:
        await list1(message, bot)
    else:
        await bot.edit_message_text(
            text=f"❌ <i><b>Ошибка.</b>\n⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯\nНедостаточно прав.</i>",
            chat_id=message.from_user.id,
            message_id=DATA_USER[3])
        await asyncio.sleep(4)
        await mainMenu.Show(message, bot)



@router.callback_query(Text("admin.list1"))
async def list1(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_USER = await database.getUserData(message.from_user.id)
    DATA_SERVER = await database.getBdData('settings', 'id', "'1'")
    await database.setUserData(message.from_user.id, "state", "'admin.list1'")
    await database.setUserData(message.from_user.id, "tg_timeLastMessage", f"'{int(time.time())}'")
    await database.setUserData(message.from_user.id, "tg_answer", "'0'")

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="◀ Назад", callback_data="mainMenu.Show"))
    builder.add(types.InlineKeyboardButton(text="❌", callback_data="none"))
    builder.add(types.InlineKeyboardButton(text="▶", callback_data="admin.list2"))
    if DATA_USER[21] >= 8: builder.row(types.InlineKeyboardButton(text="⚙ Панель основателя [8]", callback_data="admin.Panel8"))
    if DATA_USER[21] >= 7: builder.row(types.InlineKeyboardButton(text="⚙ Панель руководства проекта [7]", callback_data="admin.Panel7"))
    if DATA_USER[21] >= 6: builder.row(types.InlineKeyboardButton(text="👹 Панель ГА [6]", callback_data="admin.Panel6"))
    if DATA_USER[21] >= 5: builder.row(types.InlineKeyboardButton(text="🤠 Панель ЗГА [5]", callback_data="admin.Panel5"))
    if DATA_USER[21] >= 4: builder.row(types.InlineKeyboardButton(text="😎 Старший администратор [4]", callback_data="admin.Panel4"))
    if DATA_USER[21] >= 3: builder.row(types.InlineKeyboardButton(text="🙂 Администратор [3]", callback_data="admin.Panel3"))
    if DATA_USER[21] >= 2: builder.row(types.InlineKeyboardButton(text="🤨 Младший администратор [2]", callback_data="admin.Panel2"))
    if DATA_USER[21] >= 1: builder.row(types.InlineKeyboardButton(text="😀 Хелпер [1]", callback_data="admin.Panel1"))

    await bot.edit_message_text(
        text=f"🎯 » 🛠 Админ-панель\n<code>⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯</code>\nЗдраствуйте {DATA_USER[8]}, вы являетесь администратором <b>{DATA_USER[21]}</b> уровня\n"
             f"<code>⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯</code>\n"
             f"📢 Количество репорта » <b>no working</b>\n",
        chat_id=message.from_user.id,
        message_id=DATA_USER[3],
        reply_markup=builder.as_markup())


@router.callback_query(Text("admin.list2"))
async def list2(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_USER = await database.getUserData(message.from_user.id)
    DATA_SERVER = await database.getBdData('settings', 'id', "'1'")
    await database.setUserData(message.from_user.id, "state", "'admin.list2'")
    await database.setUserData(message.from_user.id, "tg_timeLastMessage", f"'{int(time.time())}'")
    await database.setUserData(message.from_user.id, "tg_answer", "'0'")

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="◀ Назад", callback_data="mainMenu.Show"))
    builder.add(types.InlineKeyboardButton(text="◀", callback_data="admin.list1"))
    builder.add(types.InlineKeyboardButton(text="❌", callback_data="none"))
    builder.row(types.InlineKeyboardButton(text="📟 Консоль [1]", callback_data="admin.Console"))
    builder.row(types.InlineKeyboardButton(text="📖 Устав администрации [1]", callback_data="admin.Rules"))
    builder.row(types.InlineKeyboardButton(text="📖 FAQ для администрации [1]", callback_data="admin.FAQ"))

    await bot.edit_message_text(
        text=f"🎯 » 🛠 Админ-панель\n<code>⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯</code>\nЗдраствуйте {DATA_USER[8]}, вы являетесь администратором <b>{DATA_USER[21]}</b> уровня\n"
             f"<code>⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯</code>\n"
             f"📢 Количество репорта » <b>no working</b>\n",
        chat_id=message.from_user.id,
        message_id=DATA_USER[3],
        reply_markup=builder.as_markup())


# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

# АДМИНКА 8-ГО УРОВНЯ
@router.callback_query(Text("admin.Panel8"))
async def Panel8(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_USER = await database.getUserData(message.from_user.id)
    DATA_SERVER = await database.getBdData('settings', 'id', "'1'")
    await database.setUserData(message.from_user.id, "state", "'admin.Panel8'")
    await database.setUserData(message.from_user.id, "tg_timeLastMessage", f"'{int(time.time())}'")
    await database.setUserData(message.from_user.id, "tg_answer", "'0'")

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    if DATA_USER[21] >= 8:
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(text="◀ Назад", callback_data="admin.list1"))
        builder.add(types.InlineKeyboardButton(text="❌", callback_data="none1"))
        builder.add(types.InlineKeyboardButton(text="❌", callback_data="none2"))
        builder.row(types.InlineKeyboardButton(text="👤 Управление администрацией", callback_data="admin.Panel8_ControlAdmins"))
        builder.row(types.InlineKeyboardButton(text="💎 Донат", callback_data="admin.Panel8_Donate"))
        builder.row(types.InlineKeyboardButton(text="➕ Создать новый аккаунт", callback_data="admin.Panel8_NewAccaunt"))
        await bot.edit_message_text(
            text=f"🎯 » 🛠 » ⚙ Панель основателя [8]",
            chat_id=message.from_user.id,
            message_id=DATA_USER[3],
            reply_markup=builder.as_markup())
    else:
        await message.answer(
            text=f"❌ Тебе рано сюда еще"
        )


@router.callback_query(Text("admin.Panel8_NewAccaunt"))
async def Panel8_NewAccaunt(message: types.Message, bot: Bot):
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————

    DATA_USER = await database.getUserData(message.from_user.id)
    DATA_SERVER = await database.getBdData('settings', 'id', "'1'")
    await database.setUserData(message.from_user.id, "state", "'admin.Panel8_NewAccaunt'")
    await database.setUserData(message.from_user.id, "tg_timeLastMessage", f"'{int(time.time())}'")
    await database.setUserData(message.from_user.id, "tg_answer", "'0'")

    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    if DATA_USER[21] >= 8:
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(text="❇️ Создать новый аккаунт", callback_data="registration.newAccount"))
        builder.add(types.InlineKeyboardButton(text="❌ Отказаться", callback_data="admin.Panel8"))
        await bot.edit_message_text(
            text=f"🎯 » 🛠 » ⚙ » ➕ Создать новый аккаунт\n<code>⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯</code>\n"
                 f"⚠ Нажимая на кнопку «Создать аккаунт», вы даете согласие на то, что "
                 f"все ваши данные будут безвозвратно обнулены. Ваш ID, ваш уровень администрирования, "
                 f"деньги и имущество также будет обнулено (удалено). В случае, если вы не хотите этого, "
                 f"то нажмите на кнопку «Отказаться»\n<code>⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯</code>\n"
                 f"⚠ В случае, если у вас есть права администратора, то вы должны получить разрешение на нажатие "
                 f"этой кнопки у руководителей проекта, либо у основателя.",
            chat_id=message.from_user.id,
            message_id=DATA_USER[3],
            reply_markup=builder.as_markup())
    else:
        await message.answer(
            text=f"❌ Тебе рано сюда еще"
        )