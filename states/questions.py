from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from app import dp, bot
from config import admin_id
from database import db
from filters import flood
from keyboards import replys


class Form_Q(StatesGroup):
    sms = State()


async def question_state_1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            if message.text == "Отмена 🚪":
                current_state = await state.get_state()
                if current_state is None:
                    return
                await state.finish()

                if message.from_user.id not in admin_id:
                    await message.answer(text="<b>Вы вернулись в меню</b>✅", reply_markup=await replys.user_menu(),
                                         parse_mode="HTML")
                else:
                    await message.answer(text="<b>Вы вернулись в меню</b>✅", reply_markup=await replys.admin_menu(),
                                         parse_mode="HTML")
            data['sms'] = message.text

            await db.save_question(message.from_user.id, sms=data['sms'])
            await state.finish()

            await message.answer(f"<b>Ваше сообщение было оставлено✅</b>", reply_markup=await replys.user_menu(), parse_mode="HTML")

        except Exception as e:
            await message.answer(f"<b>Что-то пошло не так..</b>", parse_mode="HTML")
            await state.finish()
            print(e)
