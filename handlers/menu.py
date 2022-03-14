import time

from aiogram import types
from aiogram.dispatcher import FSMContext
import asyncio
from app import dp, bot
from database import db
from config import admin_id
from keyboards import replys
from states import way_choose
from filters import flood
from states.way_choose import Form
from aiogram.dispatcher.filters.state import StatesGroup, State
from states.questions import Form_Q

quest = [("<b><u>Будут ли мне платить зарплату?</u></b>",
          "Конечно, да, работа каждого стажёра оплачивается. Конкретная зарплата зависит от фактического времени работы. Стажёр является полноправным работником и имеет право на социальный пакет."),
         ("<b><u>В каких городах я могу постажироваться?</u></b>",
          "В Гринатом достаточно широкая география. Наши офисы есть в таких городах, как: Ангарск, Глазов, Димитровград, Екатеринбург, Зеленогорск, Казань, Ковров, Москва, Нижний Новгород, Новосибирск, Новоуральск, Ростов-на-Дону, Санкт-Петербург, Северск, Томск, Уфа."),
         ("<b><u>Можно ли проходить стажировку удалённо?</u></b>",
          "В зависимости от эпидемиологической ситуации в регионе мы можем предложить временно стажироваться удалённо, но после снятия ограничений нужно будет выйти в офис, так как работа предполагает очное присутствие."),
         ("<b><u>Сколько длится стажировка?</u></b>",
          "Минимально стажировка рассчитана на 3 месяца. Бывают программы и большей продолжительности. Срок определяется из вашего графика и специфики направления"),
         ("<b><u>Смогу ли я совмещать учёбу и стажировку?</u></b>",
          "Да, можно работать парттайм и выбрать удобное время. Тем не менее, стажировка проходит по будням в рабочие часы"),
         ("<b><u>У меня нет опыта, но я очень хочу научиться, возьмёте меня?</u></b>",
          "Да, опыта работы от стажера мы не требуем. Однако ждем, что вы уже обладаете всеми необходимыми для работы знаниями. Для тех, кто хочет начать с нуля у нас действуют программы подготовки."),
         ("<b><u>Что будет, когда стажировка закончится?</u></b>",
          "Лучшим стажёрам мы предлагаем заключить бессрочный контракт — устроиться на постоянную работу в Гринатом."),
         ("<b><u>Что нужно уметь стажеру?</u></b>",
          "Всем стажёрам нужны отличные знания базовых алгоритмов и структур данных, а также умение писать код на одном из языков программирования. Остальные требования зависят от направления. При отборе кандидатов мы обращаем внимание на анкеты и достижения. Не стесняйтесь писать о своих успехах: победах на олимпиадах, высокой успеваемости, публикациях на конференциях и так далее."),
         ("<b><u>А могут отчислить?</u></b>",
          "Да, могут, стажировка — это настоящая работа, и если стажёр с ней не справляется, то по результатам очередной промежуточной оценки может быть не рекомендовал к продолжению участия в программе."),
         ("<b><u>А что ещё я получу?</u></b>",
          "Мы надеемся, что ты станешь частью большой команды Гринатом, и готовы помогать.\nМы гарантируем:\n  • помощь руководителя-наставника\n  • регулярную оценку и обратную связь\n  •  участие в профильных конференциях\n  •  тренинги по soft skills"),
         ]


class Sending(StatesGroup):
    sms = State()


class FAQ(StatesGroup):
    faq_id = State()


@dp.throttled(flood.anti_flood, rate=1)  # проверка на спам
async def menu_pars(message, state: FSMContext):
    if message.text == "Выбрать направление 🔍":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        yes_button = types.KeyboardButton(text="✅")
        no_button = types.KeyboardButton(text="❌")
        cancel = types.KeyboardButton(text="Отмена 🚪")
        markup.add(yes_button, no_button)
        markup.add(cancel)

        await message.answer_sticker(r"CAACAgIAAxkBAAEEIvdiLY2PxPsIfvQ3o8okzWMJ9z8QuwAClhkAAloxaEmZucim-hpE3yME")
        await message.answer(f"<b>Вы хотите развиваться в области программирования?</b>", parse_mode="HTML",
                             reply_markup=markup)
        await Form.want_programming.set()

    if message.text == "Стажировка 👨‍💻":
        markup_train = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(text="Хочу узнать больше!", url="https://edu.greenatom.ru/trainee/")
        markup_train.add(url_button)
        await message.answer(f"<b>Список IT-стажировок в атомной отрасли доступны на нашем сайте </b>💻\n",
                             reply_markup=markup_train, parse_mode="HTML")

    if message.text == "FAQ 👀":
        markup_faq = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton(text="➡", callback_data="next_faq")
        btn2 = types.InlineKeyboardButton(text="⬅", callback_data="prev_faq")
        cancel = types.InlineKeyboardButton(text="Отмена 🚪", callback_data="cancel_sms")
        markup_faq.add(btn2, btn1)
        markup_faq.add(cancel)

        await message.answer(f"<b><i>Частые вопросы</i></b>❓\n\n{quest[0][0]}\n\n{quest[0][1]}", parse_mode="HTML",
                             reply_markup=markup_faq)
        await FAQ.faq_id.set()
        async with state.proxy() as data:
            data['faq_id'] = 0

    if message.text == "Профиль 🙋‍♂️":
        profile = await db.get_user_info(message)
        await message.answer(
            f"\t\t<b>Ваш профиль</b> 👨‍💻\n\t└🔗 <b>ID:</b> <code>{message.from_user.id}</code>\n\t└🌐 <b>Статус:</b> <code>{profile[1]}</code>\n\t└🤝 <b>Рефералов:</b> <code>{profile[4]}</code>\n\t└💰 <b>Коинов:</b> <code>{profile[2]}</code>\n\n<b><i>Пригласи друга и получи 5 коинов! 🔥</i></b>\n🔰<b>Ваша реферальная ссылка: <a href='https://t.me/greenatm_bot?start={message.from_user.id}'>СКОПИРОВАТЬ</a></b>",
            parse_mode="HTML")

    if message.text == "Задать вопрос 📜":
        if not await db.is_ban(message.from_user.id):
            markup_q = types.InlineKeyboardMarkup()
            cancel = types.InlineKeyboardButton(text="Отмена 🚪", callback_data="cancel_sms")
            markup_q.add(cancel)

            await message.answer(f"<b>Напишите Вам вопрос и Вам вскоре ответят!</b>", parse_mode="HTML",
                                 reply_markup=markup_q)
            await Form_Q.sms.set()

    if message.text == "Почта 📪" and message.from_user.id in admin_id:
        markup = types.InlineKeyboardMarkup()
        b1 = types.InlineKeyboardButton(text="1", callback_data="1sms_check")
        b2 = types.InlineKeyboardButton(text="2", callback_data="2sms_check")
        b3 = types.InlineKeyboardButton(text="5", callback_data="5sms_check")
        markup.add(b1, b2, b3)

        await message.answer(f"<b>Проверка сообщений от пользователей 📪\n\nСколько сообщений показать? ⬇</b>",
                             parse_mode="HTML", reply_markup=markup)

    if message.text == "Рассылка 📨" and message.from_user.id in admin_id:
        await message.answer(f"<b>Введите сообщение для рассылки ⬇</b>", parse_mode="HTML")
        await Sending.sms.set()


async def faq_active(call: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id, )
    markup_faq2 = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton(text="➡", callback_data="next_faq")
    btn2 = types.InlineKeyboardButton(text="⬅", callback_data="prev_faq")
    cancel = types.InlineKeyboardButton(text="Отмена 🚪", callback_data="cancel_sms")
    markup_faq2.add(btn2, btn1)
    markup_faq2.add(cancel)

    async with state.proxy() as data:
        if call.data == "next_faq":
            if 10 > data['faq_id'] >= 0:
                if data['faq_id'] == 9:
                    data['faq_id'] = -1
                data["faq_id"] += 1
                await bot.edit_message_text(
                    f"<b><i>Частые вопросы</i></b>❓\n\n{quest[data['faq_id']][0]}\n\n{quest[data['faq_id']][1]}",
                    chat_id=call.from_user.id, message_id=call.message.message_id, parse_mode="HTML",
                    reply_markup=markup_faq2)
        if call.data == "prev_faq":
            if data['faq_id'] == 0:
                data['faq_id'] = 10
            if 10 >= data['faq_id'] > 0:
                data['faq_id'] -= 1
                await bot.edit_message_text(
                    f"<b><i>Частые вопросы</i></b>❓\n\n{quest[data['faq_id']][0]}\n\n{quest[data['faq_id']][1]}",
                    chat_id=call.from_user.id, message_id=call.message.message_id, parse_mode="HTML",
                    reply_markup=markup_faq2)

        if call.data == "cancel_sms":
            current_state = await state.get_state()
            if current_state is None:
                return
            await state.finish()
            await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
            if call.from_user.id not in admin_id:
                await call.message.answer(text="<b>Вы вернулись в меню</b>✅", reply_markup=await replys.user_menu(),
                                          parse_mode="HTML")
            else:
                await call.message.answer(text="<b>Вы вернулись в меню</b>✅", reply_markup=await replys.admin_menu(),
                                          parse_mode="HTML")


async def sending(message, state: FSMContext):
    async with state.proxy() as data:
        try:
            data['sms'] = message.text
            db.cur.execute("select id from users")
            ids = db.cur.fetchall()
            start_time = time.time()
            for id in ids:
                try:
                    await bot.send_message(text=f"<b>Рассылка от админов:</b>\n{data['sms']}", chat_id=int(id[0]),
                                           parse_mode="HTML")
                    await asyncio.sleep(3)
                except:
                    await asyncio.sleep(3)
            await state.finish()
            await message.answer(
                f"<b>Рассылка завершена за: <code>{str((time.time() - start_time))[:6]}</code> сек.</b>",
                parse_mode="HTML")
        except:
            await state.finish()
