import sqlite3

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text

from functions import *

connect = sqlite3.connect("db.db")
cursor = connect.cursor()

TOKEN = "5799026042:AAFeO2O1A89-AS4HIO9GPTAZ4uCOolMuwFc"

storage = MemoryStorage()

bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=storage)

login_kb = ReplyKeyboardMarkup(resize_keyboard=True)
login_kb.add(KeyboardButton("Войти"), KeyboardButton("Зарегистрироваться"))

start_kb = ReplyKeyboardMarkup(resize_keyboard=True)
start_kb.add(KeyboardButton("Создать событие"), KeyboardButton("Присоединиться к событию"))


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Для начала работы с ботом войдите в аккаунт или зарегистрируйтесь", reply_markup=login_kb)


@dp.message_handler(state=None)
def all_message(message: types.Message, state: FSMContext):
    pass
    # if remove_space(message.text) == ""


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)