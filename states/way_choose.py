from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from app import dp, bot
from config import admin_id
from database import db
from filters import flood
from keyboards import replys


class Form(StatesGroup):
    want_programming = State()
    exp = State()
    lang = State()


async def state_1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            if message.text == "✅" or message.text == "❌" or message.text == "Отмена 🚪":
                data['want_programming'] = message.text

                if message.text == "✅":
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    yes_button = types.KeyboardButton(text="✅")
                    no_button = types.KeyboardButton(text="❌")
                    cancel = types.KeyboardButton(text="Отмена 🚪")
                    markup.add(yes_button, no_button)
                    markup.add(cancel)

                    await message.answer(f"<b>У Вас есть опыт в программировании?</b>", parse_mode="HTML", reply_markup=markup)
                    await Form.exp.set()
                if message.text == "❌":
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    yes_button = types.KeyboardButton(text="✅")
                    no_button = types.KeyboardButton(text="❌")
                    cancel = types.KeyboardButton(text="Отмена 🚪")
                    markup.add(yes_button, no_button)
                    markup.add(cancel)

                    await message.answer(f"<b>Вы немного понимаете основы программирования и хотите оптимизировать бизнес-процессы?</b>", parse_mode="HTML", reply_markup=markup)
                    await Form.exp.set()
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
            else:
                await message.answer(f"<i>Я вас не понимаю, нажмите на кнопку ниже ⬇</i>", parse_mode="HTML")
        except Exception as e:
            await message.answer(f"<b>Что-то пошло не так...</b>", parse_mode="HTML")
            await state.finish()
            print(e)


async def state_2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            if message.text == "✅" or message.text == "❌" or message.text == "Отмена 🚪":
                data['exp'] = message.text

                if data['want_programming'] == "❌" and data['exp'] == "❌":
                    markup1 = types.InlineKeyboardMarkup()
                    url1 = types.InlineKeyboardButton(text="Изучить 🔥", url="https://edu.greenatom.ru/caselab/support/")
                    markup1.add(url1)
                    await message.answer_sticker(r"CAACAgIAAxkBAAEEIvNiLY2H3XmWnDrRSb_JlmGynkmziQACDRgAAoQ0aUmrGCEWFqnXIyME")
                    await message.answer(f"<b>👀 Мне кажется, Вам подойдет курс <i>CaseLab SUPPORT 🔥</i></b>", parse_mode="HTML", reply_markup=markup1)
                    await state.finish()

                    if message.from_user.id not in admin_id:
                        await message.answer(text="<b>Направление выбрано</b>✅", reply_markup=await replys.user_menu(),
                                             parse_mode="HTML")
                    else:
                        await message.answer(text="<b>Направление выбрано</b>✅", reply_markup=await replys.admin_menu(),
                                             parse_mode="HTML")

                if data['want_programming'] == "❌" and data['exp'] == "✅":
                    markup2 = types.InlineKeyboardMarkup()
                    url2 = types.InlineKeyboardButton(text="Изучить 🔥", url="https://edu.greenatom.ru/caselab/sap/")
                    markup2.add(url2)
                    await message.answer_sticker(r"CAACAgIAAxkBAAEEIvNiLY2H3XmWnDrRSb_JlmGynkmziQACDRgAAoQ0aUmrGCEWFqnXIyME")
                    await message.answer(f"<b>👀 Мне кажется, Вам подойдет курс <i>CaseLab SAP 🔥</i></b>", parse_mode="HTML", reply_markup=markup2)
                    await state.finish()

                    if message.from_user.id not in admin_id:
                        await message.answer(text="<b>Направление выбрано</b>✅", reply_markup=await replys.user_menu(),
                                             parse_mode="HTML")
                    else:
                        await message.answer(text="<b>Направление выбрано</b>✅", reply_markup=await replys.admin_menu(),
                                             parse_mode="HTML")

                if data['want_programming'] == "✅" and data['exp'] == "✅":
                    markup3 = types.InlineKeyboardMarkup()
                    url3 = types.InlineKeyboardButton(text="Изучить 🔥", url="https://edu.greenatom.ru/caselab/web/")
                    markup3.add(url3)
                    await message.answer_sticker(r"CAACAgIAAxkBAAEEIvNiLY2H3XmWnDrRSb_JlmGynkmziQACDRgAAoQ0aUmrGCEWFqnXIyME")
                    await message.answer(f"<b>👀 Мне кажется, Вам подойдет курс <i>CaseLab WEB 🔥</i></b>", parse_mode="HTML", reply_markup=markup3)
                    await state.finish()

                    if message.from_user.id not in admin_id:
                        await message.answer(text="<b>Направление выбрано</b>✅", reply_markup=await replys.user_menu(),
                                             parse_mode="HTML")
                    else:
                        await message.answer(text="<b>Направление выбрано</b>✅", reply_markup=await replys.admin_menu(),
                                             parse_mode="HTML")

                if data['want_programming'] == "✅" and data['exp'] == "❌":
                    markup4 = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    yes_button = types.KeyboardButton(text="✅")
                    no_button = types.KeyboardButton(text="❌")
                    cancel = types.KeyboardButton(text="Отмена 🚪")
                    markup4.add(yes_button, no_button)
                    markup4.add(cancel)

                    await message.answer(f"<b>Вы хотите заниматься <i>WEB-сайтами?</i></b>", parse_mode="HTML", reply_markup=markup4)
                    await Form.lang.set()

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

            else:
                await message.answer(f"<i>Я вас не понимаю, нажмите на кнопку ниже ⬇</i>", parse_mode="HTML")
        except Exception as e:
            await message.answer(f"<b>Что-то пошло не так...</b>", parse_mode="HTML")
            await state.finish()
            print(e)


async def state_3(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            if message.text == "✅" or message.text == "❌" or message.text == "Отмена 🚪":
                data['lang'] = message.text

                if data['want_programming'] == "✅" and data['exp'] == "❌" and data['lang'] == "✅":
                    markup = types.InlineKeyboardMarkup()
                    url = types.InlineKeyboardButton(text="Изучить 🔥", url="https://edu.greenatom.ru/caselab/Js/")
                    markup.add(url)
                    await message.answer_sticker(r"CAACAgIAAxkBAAEEIvNiLY2H3XmWnDrRSb_JlmGynkmziQACDRgAAoQ0aUmrGCEWFqnXIyME")
                    await message.answer(f"<b>👀 Мне кажется, Вам подойдет курс по языку <i>JavaScript 🔥</i></b>", parse_mode="HTML",
                                         reply_markup=markup)
                    await state.finish()

                    if message.from_user.id not in admin_id:
                        await message.answer(text="<b>Направление выбрано</b>✅", reply_markup=await replys.user_menu(),
                                             parse_mode="HTML")
                    else:
                        await message.answer(text="<b>Направление выбрано</b>✅", reply_markup=await replys.admin_menu(),
                                             parse_mode="HTML")

                if data['want_programming'] == "✅" and data['exp'] == "❌" and data['lang'] == "❌":
                    markup = types.InlineKeyboardMarkup()
                    url = types.InlineKeyboardButton(text="Изучить 🔥", url="https://edu.greenatom.ru/caselab/1c/")
                    markup.add(url)
                    await message.answer_sticker(r"CAACAgIAAxkBAAEEIvNiLY2H3XmWnDrRSb_JlmGynkmziQACDRgAAoQ0aUmrGCEWFqnXIyME")
                    await message.answer(f"<b>👀 Мне кажется, Вам подойдет курс по языку <i>1С 🔥</i></b>", parse_mode="HTML",
                                         reply_markup=markup)
                    await state.finish()

                    if message.from_user.id not in admin_id:
                        await message.answer(text="<b>Направление выбрано</b>✅", reply_markup=await replys.user_menu(),
                                             parse_mode="HTML")
                    else:
                        await message.answer(text="<b>Направление выбрано</b>✅", reply_markup=await replys.admin_menu(),
                                             parse_mode="HTML")

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

            else:
                await message.answer(f"<i>Я вас не понимаю, нажмите на кнопку ниже ⬇</i>", parse_mode="HTML")
        except Exception as e:
            await message.answer(f"<b>Что-то пошло не так...</b>", parse_mode="HTML")
            await state.finish()
            print(e)
