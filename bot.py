import asyncio
import os
# import sys
# import signal

import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import F
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ["BOT_TOKEN"]
API_BASE = os.getenv("API_BASE", "http://127.0.0.1:8000/api")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

builder = ReplyKeyboardBuilder()
builder.button(text="/register")
builder.button(text="/login")
keyboard = builder.as_markup(resize_keyboard=True)

class Auth(StatesGroup):
    reg_password = State()
    reg_confirm = State()
    login_password = State()


@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await message.answer(
        "Choose one command:",
        reply_markup=keyboard
    )


@dp.message(Command("register"))
async def register_handler(message: Message, state: FSMContext) -> None:
    tg_login = message.from_user.username
    if not tg_login:
        await message.answer(
            "You need a public Telegram username (@handle) to register.\n"
            "Set one in Telegram Settings and try again.",
            reply_markup=ReplyKeyboardRemove()
        )
        return
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{API_BASE}/check-user/",
            json={"tg_login": tg_login},
        ) as resp:

            if resp.status == 409:
                await message.answer(
                    "You are already registered!"
                )
                return

    await state.update_data(tg_login=tg_login)
    await state.set_state(Auth.reg_password)
    await message.answer(
        f"Welcome, @{tg_login}!\n\nPlease set a password for your account (min 8 characters):",
        reply_markup=ReplyKeyboardRemove()
    )


@dp.message(Auth.reg_password)
async def process_password(message: Message, state: FSMContext) -> None:
    if len(message.text) < 8:
        await message.answer("Password must be at least 8 characters. Try again:")
        return

    await state.update_data(password=message.text)
    await state.set_state(Auth.reg_confirm)
    await message.answer("Confirm your password:")


@dp.message(Auth.reg_confirm)
async def process_password_confirm(message: Message, state: FSMContext) -> None:
    data = await state.get_data()

    if message.text != data["password"]:
        await state.set_state(Auth.reg_password)
        await message.answer("Passwords don't match. Please set a new password:")
        return

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{API_BASE}/register/",
            json={"tg_login": data["tg_login"], "password": data["password"]},
        ) as resp:
            body = await resp.json()

            await state.clear()
            await state.update_data(
                token=body["token"]
            )
            if resp.status == 201:
                await message.answer(
                    f"Registration complete!\n\nYour login: @{data['tg_login']}"
                )
            else:
                error = body.get("error") or body
                await message.answer(f"Registration failed: {error}")


@dp.message(Command("login"))
async def login_handler(message: Message, state: FSMContext) -> None:
    tg_login = message.from_user.username
    if not tg_login:
        await message.answer(
            "You need a public Telegram username (@handle) to login.\n"
            "Set one in Telegram Settings and try again.",
            reply_markup=ReplyKeyboardRemove()
        )
        return
    
    await state.set_state(Auth.login_password)
    await message.answer(
        "Please enter a password for your account:",
        reply_markup=ReplyKeyboardRemove()
    )


@dp.message(Auth.login_password)
async def login_process_password(message: Message, state: FSMContext) -> None:
    tg_login = message.from_user.username
    password = message.text
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{API_BASE}/login/",
            json={"identifier": tg_login, "password": password},
        ) as resp:
            body = await resp.json()
    
            await state.clear()
            await state.update_data(
                token=body["token"]
            )
            
            if resp.status == 200:
                await message.answer(
                    f"You are logged in! @{tg_login}"
                )
            elif resp.status == 401:
                await message.answer("Wrong Password.")
            else:
                error = body.get("error") or body
                await message.answer(f"Login failed: {error}")


@dp.message(F.text & ~F.text.startswith("/"))
async def save_user_message(message: Message, state: FSMContext) -> None:
    tg_login = message.from_user.username
    data = await state.get_data()
    user_token = data["token"]
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{API_BASE}/messages/",
            json={
                # "tg_login": tg_login,
                "user_text": message.text
            },
            headers={
                "Authorization": f"Token {user_token}"
            }
        ) as resp:
            body = await resp.json()
            # print("\nbot\n",body, "\n\n")
            if resp.status == 201:
                await message.answer(body["output"])
            else:
                await message.answer("Error")

async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
