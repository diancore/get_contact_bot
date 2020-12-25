import logging, asyncio
from aiogram import Bot, Dispatcher, executor, filters, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import *
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup

token="token"

storage: MemoryStorage = MemoryStorage()
bot: Bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp: Dispatcher = Dispatcher(bot, storage=storage)

class States(StatesGroup):
    contact = State()

request = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('☎ Send my contact', request_contact=True)
)

@dp.message_handler(command=['start', 'send'])
async def start_handler(msg: types.Message):
    await msg.answer('Hi, send me ur contact!', reply_markup=request)

@dp.message_handler(state=States.contact)
async def start_handler(msg: types.Message, state):
    number = None
    uid = msg.from_user.id
    uname = msg.from_user.first_name
    # add '+' to number (+xxxx)
    if (msg.contact.phone_number.find('+') >= 0):
        number = msg.contact.phone_number
    else:
        number = f"+{msg.contact.phone_number}"

    await msg.answer(f'{uname}, ur phone number is {number}!')

    await state.finish()