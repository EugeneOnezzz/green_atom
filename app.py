import asyncio
import aioschedule
import threading

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from config import token
from aiogram.utils import executor

storage = MemoryStorage()
bot = Bot(token=token)
dp = Dispatcher(bot, storage=storage)

if __name__ == "__main__":
    from states import way_choose, questions

    dp.register_message_handler(way_choose.state_1, content_types=["text"], state=way_choose.Form.want_programming)
    dp.register_message_handler(way_choose.state_2, content_types=["text"], state=way_choose.Form.exp)
    dp.register_message_handler(way_choose.state_3, content_types=["text"], state=way_choose.Form.lang)
    dp.register_message_handler(questions.question_state_1, content_types=["text"], state=questions.Form_Q.sms)

    from handlers import start, menu, callbacks
    dp.register_message_handler(callbacks.answer, content_types=["text"], state=callbacks.Answer.id)
    dp.register_message_handler(menu.sending, content_types=["text"], state=menu.Sending.sms)
    dp.register_callback_query_handler(menu.faq_active, lambda c: True, state=menu.FAQ.faq_id)
    dp.register_message_handler(start.start_command, commands=['start'], state="*")
    dp.register_message_handler(menu.menu_pars, content_types=["text"], state="*")
    dp.register_callback_query_handler(callbacks.call_pars, lambda c: True, state="*")

    executor.start_polling(dp, skip_updates=True)
