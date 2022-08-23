import sqlite3
import hashlib

connect = sqlite3.connect("db.db")
cursor = connect.cursor()


async def input_error(message):
    await message.answer("Неверный формат ввода, повторите попытку")


async def correct_input(message: str,
                        full_name: bool = None,
                        age: bool = None,
                        phone: bool = None,
                        email: bool = None,
                        password: bool = None,
                        ) -> bool:
    return True


async def remove_space(message: str) -> str:
    return " ".join(message.split())


async def check_status(user_id, status) -> bool:
    user_status = cursor.execute(f"""SELECT status FROM users WHERE tg_id='{user_id}'""").fetchone()
    return user_status == status


async def set_status(user_id, status) -> None:
    cursor.execute(f"""UPDATE users SET status='{status}' WHERE tg_id='{user_id}'""")
    connect.commit()
