from aiogram.dispatcher import FSMContext

from app import dp, bot
from filters import flood
from config import admin_id
from aiogram import types
from keyboards import replys
from database import db


@dp.throttled(flood.anti_flood, rate=1)
async def start_command(message: types.Message, state: FSMContext):
    #  Чтобы старт работал как сброс стейтов
    if await state.get_state() is not None:
        await state.finish()

    message_array = list(message.text.split(" "))

    #  Если нажат старт без реферальной ссылки
    if len(message_array) == 1:
        #  Если чел в БД, то бот перезапущен
        if await db.user_exists(message):
            if message.from_user.id not in admin_id:
                await message.answer(text=f"<b>Бот перезапущен 🤖</b>", parse_mode="HTML", reply_markup=await replys.user_menu())
                await message.answer_sticker(r"CAACAgIAAxkBAAEEIvViLY2Kua9o4VcyxScnQgb3D9HuFAACYRYAApbdaElUV9RhPf2A8iME")
            if message.from_user.id in admin_id:
                await message.answer_sticker(r"CAACAgIAAxkBAAEEIvViLY2Kua9o4VcyxScnQgb3D9HuFAACYRYAApbdaElUV9RhPf2A8iME")
                await message.answer(text=f"<b>Бот перезапущен 🤖</b>", parse_mode="HTML", reply_markup=await replys.admin_menu())
        if not await db.user_exists(message):
            await message.answer_sticker(r"CAACAgIAAxkBAAEEIvViLY2Kua9o4VcyxScnQgb3D9HuFAACYRYAApbdaElUV9RhPf2A8iME")
            await message.answer(f"<b>🔹 Добро пожаловать, <code>{message.from_user.first_name}</code>\n\nВыбери то, что интересует ⬇</b>", parse_mode="HTML", reply_markup=await replys.user_menu())
            await db.user_create(message)
    #  Прописан старт с реферальной ссылкой
    elif len(message_array) == 2:
        #  Корректна ли вообще реферальная ссылка
        if message_array[1].isdigit():
            #  Нет ли уже в БД
            if not await db.user_exists(message):
                await db.user_create(message)
                await db.update_referals(slave_id=str(message.from_user.id), master_id=str(message_array[1]))
                await message.answer_sticker(r"CAACAgIAAxkBAAEEIvViLY2Kua9o4VcyxScnQgb3D9HuFAACYRYAApbdaElUV9RhPf2A8iME")
                await message.answer(f"<b>🔹 Добро пожаловать, <code>{message.from_user.first_name}</code>\n\nВыбери то, что интересует ⬇</b>", parse_mode="HTML", reply_markup=await replys.user_menu())
            elif await db.user_exists(message):
                if message.from_user.id not in admin_id:
                    await message.answer_sticker(r"CAACAgIAAxkBAAEEIvViLY2Kua9o4VcyxScnQgb3D9HuFAACYRYAApbdaElUV9RhPf2A8iME")
                    await message.answer(text=f"<b>Бот перезапущен 🤖</b>", parse_mode="HTML", reply_markup=await replys.user_menu())
                if message.from_user.id in admin_id:
                    await message.answer_sticker(r"CAACAgIAAxkBAAEEIvViLY2Kua9o4VcyxScnQgb3D9HuFAACYRYAApbdaElUV9RhPf2A8iME")
                    await message.answer(text=f"<b>Бот перезапущен 🤖</b>", parse_mode="HTML", reply_markup=await replys.admin_menu())
        elif not message_array[1].isdigit():
            await message.answer(f"<b>Проверьте правильность введенного кода 🟡</b>", parse_mode="HTML")