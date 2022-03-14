from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from app import dp, bot
from config import admin_id
from database import db
from filters import flood
from keyboards import replys


class Answer(StatesGroup):
    id = State()


@dp.throttled(flood.anti_flood, rate=1)
async def call_pars(call: types.CallbackQuery, state: FSMContext):
    if call.data == "cancel_sms":
        try:
            await bot.delete_message(message_id=call.message.message_id, chat_id=call.from_user.id)
            await call.message.answer(text=f"<b>Сообщение удалено</b> ✅", parse_mode="HTML",
                                      reply_markup=await replys.user_menu())
            await state.finish()
        except:
            await state.finish()

    if "sms_check" in call.data and call.from_user.id in admin_id:
        await bot.delete_message(message_id=call.message.message_id, chat_id=call.from_user.id)
        array_sms = await db.get_sms(call.data[0])
        for sms in array_sms:
            markup = types.InlineKeyboardMarkup(row_width=2)
            answer = types.InlineKeyboardButton(text="Ответить 🟢", callback_data=f"answer?{sms[0]}")
            print(f"answer?{sms[0]}")
            markup.add(answer)
            await call.message.answer(f"<b>Author: </b><code>{sms[0]}</code>\n\n{str(sms[1])}", reply_markup=markup,
                                      parse_mode="HTML")

    if "answer" in call.data and call.from_user.id in admin_id:
        await call.message.answer(text=f"<b>Введите ответ пользователю ⬇</b>", parse_mode="HTML")
        await Answer.id.set()
        async with state.proxy() as data:
            author_id = list(call.data.split("?"))
            data['id'] = int(author_id[1])


async def answer(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await bot.send_message(text=f"<b>Ответ от администратора 🛎</b>\n\n{message.text}", chat_id=data['id'], parse_mode="HTML")
        db.cur.execute("delete from mail where id=%s", (str(data['id']),))
        db.conn.commit()
        await state.finish()

