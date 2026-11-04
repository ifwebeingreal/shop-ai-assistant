import asyncio
import logging

from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.chat_action import ChatActionSender

import app.keyboards.reply as rkb
import app.keyboards.inline as ikb
import app.keyboards.builder as bkb
from app.ai_agent.agent import get_ai_response

from app.database.requests.user.add import set_user

user = Router()


@user.message(CommandStart())
async def start_command(message: Message):
    await set_user(message.from_user.id, message.from_user.full_name)

    await message.answer("""👋 Привет! Я виртуальный помощник интернет-магазина.

Помогу узнать информацию о товарах, доставке и возвратах.

Просто напишите свой вопрос!""")


@user.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        """📋 Я могу помочь с вопросами:

📦 Наличие и стоимость товара
🚚 Доставка
🔄 Возврат товара
🛠️ Брак и неисправности
💰 Скидки

Просто напишите свой вопрос в чат."""
    )


@user.message(F.text)
async def handle_question(message: Message, bot: Bot):
    msg = await message.answer("⏳ Ваш вопрос получен. Обрабатываю…")

    try:
        async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
            response = await get_ai_response(message.text)

    except Exception as e:
        logging.exception(f"Ошибка при обращении к AI-ассистенту: {str(e)}")
        await message.answer("❌ Не удалось обработать вопрос. Попробуйте чуть позже.")
        return

    finally:
        try:
            await msg.delete()
        except Exception as e:
            logging.exception(f"Не удалось удалить сообщение об обработке: {str(e)}")

    await message.answer(response)


@user.message()
async def echo_handle(message: Message):
    await message.answer("❌ Пока я могу обрабатывать только текстовые сообщения. Пожалуйста, напишите ваш вопрос текстом.")