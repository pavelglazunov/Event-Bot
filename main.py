import hashlib
import sqlite3

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text

from functions import *
from forms import *

# connect = sqlite3.connect("db.db")
# cursor = connect.cursor()

TOKEN = "5799026042:AAFeO2O1A89-AS4HIO9GPTAZ4uCOolMuwFc"

storage = MemoryStorage()

bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=storage)

login_kb = ReplyKeyboardMarkup(resize_keyboard=True)
login_kb.add(KeyboardButton("Войти"), KeyboardButton("Зарегистрироваться"))

start_kb = ReplyKeyboardMarkup(resize_keyboard=True)
start_kb.add(KeyboardButton("Создать событие"), KeyboardButton("Присоединиться к событию"))


@dp.message_handler(commands=["start"], state=None)
async def start(message: types.Message, state: FSMContext):
    await message.answer("Для начала работы с ботом войдите в аккаунт или зарегистрируйтесь", reply_markup=login_kb)
    await Registration.answer.set()


@dp.message_handler(state=Registration.answer)
async def registration(message: types.Message, state: FSMContext):
    msg = await remove_space(message.text)

    if msg not in ["Войти", "Зарегистрироваться"]:
        await message.answer("Такого ответа нет!")
        return
    await state.finish()
    if msg == "Войти":
        await LogIn.email.set()
        await message.answer("Введите почту")
    if msg == "Зарегистрироваться":
        await message.answer("Введите ваше ФИО", reply_markup=ReplyKeyboardRemove())
        await SignUp.full_name.set()


@dp.message_handler(state=LogIn.email)
async def login__email(message: types.Message, state: FSMContext):
    async with state.proxy() as login_data:
        login_data["email"] = await remove_space(message.text)

    if not cursor.execute(f"""SELECT * FROM users WHERE email='{login_data["email"]}'""").fetchone():
        # reg_btn = InlineKeyboardButton()
        await message.answer("Такого пользователя не существует, повторите попытку или зарегистрируйтесь")
        return

    await message.answer("Введите пароль")
    await LogIn.next()


@dp.message_handler(state=LogIn.password)
async def login__password(message: types.Message, state: FSMContext):
    async with state.proxy() as login_data:
        login_data["password"] = await remove_space(message.text)

    password, name = cursor.execute(f"""SELECT password, name FROM users WHERE
                                    email='{login_data["email"]}'""").fetchone()
    if hashlib.sha256(login_data["password"].encode()).hexdigest() == password:
        await message.answer(f"Добро пожаловать, {name}")
    else:
        await message.answer("Пароль неверный")
        return


@dp.message_handler(state=SignUp.full_name)
async def signup__name(message: types.Message, state: FSMContext):
    if not (await correct_input(msg := await remove_space(message.text), full_name=True)):
        await input_error(message)
        return
    async with state.proxy() as signup_data:
        signup_data["surname"] = msg.split()[0]
        signup_data["name"] = msg.split()[1]
        signup_data["middle_name"] = msg.split()[2]

    await message.answer("Введите ваш возраст")
    await SignUp.next()


@dp.message_handler(state=SignUp.age)
async def signup__age(message: types.Message, state: FSMContext):
    if not await correct_input(msg := await remove_space(message.text), age=True):
        await input_error(message)
        return
    async with state.proxy() as signup_data:
        signup_data["age"] = msg

    await message.answer("Введите ваш телефон")
    await SignUp.next()


@dp.message_handler(state=SignUp.phone)
async def signup__phone(message: types.Message, state: FSMContext):
    if not await correct_input(msg := await remove_space(message.text), phone=True):
        await input_error(message)
        return
    async with state.proxy() as signup_data:
        signup_data["phone"] = msg

    await message.answer("Введите вашу почту")
    await SignUp.next()


@dp.message_handler(state=SignUp.email)
async def signup__email(message: types.Message, state: FSMContext):
    if not await correct_input(msg := await remove_space(message.text), email=True):
        await input_error(message)
        return
    async with state.proxy() as signup_data:
        signup_data["email"] = msg

    await message.answer("Введите пароль")
    await SignUp.next()


@dp.message_handler(state=SignUp.password)
async def signup__password(message: types.Message, state: FSMContext):
    if not await correct_input(msg := await remove_space(message.text), password=True):
        await input_error(message)
        return
    async with state.proxy() as signup_data:
        signup_data["password"] = msg

    cursor.execute(f"""INSERT INTO users
                    (
                    tg_id, username, name, surname, middle_name, age, phone, email, password, status, prime
                    )
                     VALUES
                     (
                     '{message.from_user.id}',
                      '{message.from_user.username}',
                      '{signup_data["name"]}',
                      '{signup_data["surname"]}',
                      '{signup_data["middle_name"]}',
                      '{signup_data["age"]}',
                      '{signup_data["phone"]}',
                      '{signup_data["email"]}',
                      '{hashlib.sha256(str(signup_data["password"]).encode()).hexdigest()}',
                      'menu',
                      '0'
                     )
                     """)
    connect.commit()

    await message.answer("Регистрация успешно завершена")
    await state.finish()


@dp.message_handler(state=None)
def all_message(message: types.Message, state: FSMContext):
    pass
    # if remove_space(message.text) == ""


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
