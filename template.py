import asyncio
import logging
from random import randint

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.filters import CommandObject, Text
from aiogram import html
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token="6270150808:AAGTSrzismkyQdWJS2CcgPf2Il_IrskDxz4", parse_mode="HTML")
# Диспетчер
dp = Dispatcher()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")

@dp.message(Command("test1"))
async def cmd_test1(message: types.Message):
    await message.answer("Test 1!")
    await message.delete()


# Хэндлер на команду /test2

async def cmd_test2(message: types.Message):
    DICE = await message.answer_dice(emoji="🎲")
    return message.answer(f"{DICE.dice.value}")

@dp.message(Command("test3"))
async def any_message(message: types.Message):
    await message.answer("Hello, <b>world</b>!")
    await message.answer("Hello, *world*\!", parse_mode="MarkdownV2")


@dp.message(Command("name"))
async def any_message(message: types.Message, command: CommandObject):
    await message.answer(f"Привет, {html.bold(html.quote(command.args))}")

@dp.message(Command("send"))
async def any_message(message: types.Message):
    await message.answer(f"{message.html_text}\n\nОтправлено с помощью AMPR")


@dp.message(Command("start2"))
async def any_message(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Продолжить",
        callback_data="reg2")
    )

    await message.answer(
        "Нажмите на кнопку, чтобы бот отправил число от 1 до 10",
        reply_markup=builder.as_markup()
    )

@dp.callback_query(Text("reg2"))
async def send_random_value(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Продолжить 45",
        callback_data="reg2")
    )
    await callback.message.edit_text('Итак, вот список', reply_markup=builder.as_markup())
    await callback.answer()
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())