from aiogram.dispatcher.filters.state import State, StatesGroup


class Registration(StatesGroup):
    answer = State()


# Вход
class LogIn(StatesGroup):
    email = State()
    password = State()


# Регистрация
class SignUp(StatesGroup):
    full_name = State()
    age = State()
    phone = State()
    email = State()
    password = State()
    photo = State()
