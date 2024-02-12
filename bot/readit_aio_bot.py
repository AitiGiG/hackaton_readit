import asyncio
import logging
from decouple import config
from aiogram import Bot, Dispatcher,types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery
from checking import *
from btn import reg_btn, main_menu_commands
from parsing import *

logging.basicConfig(level=logging.INFO)

bot = Bot(config('BOT_TOKEN'))

dp = Dispatcher()
async def set_main_menu(bot: Bot):
    await bot.set_my_commands(main_menu_commands)


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer('Добро пожаловать! Выберите действие: ', reply_markup=reg_btn.as_markup())

@dp.callback_query(F.data == 'register')
async def process_buttons_press(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UserRegisterState.email)
    await callback.message.answer('Введите email: ')

@dp.message(UserRegisterState.email)
async def get_email(message: types.Message, state: FSMContext):
    if is_valid_email(message.text):
        await state.update_data(email=message.text)
        await state.set_state(UserRegisterState.username)
        await message.answer('Введите username: ')
    else:
        await message.answer('Введите корректный email: ')

@dp.message(UserRegisterState.username)
async def get_username(message: types.Message, state: FSMContext):
    if type(message.text) == str:
        await state.update_data(username=message.text)
        await state.set_state(UserRegisterState.password)
        await message.answer('Введите пароль: ')
    else:
        await message.answer('Введите корректный username: ')

@dp.message(UserRegisterState.password)
async def get_password(message: types.Message, state: FSMContext):
    if is_valid_password(message.text):
        await state.update_data(password=message.text)
        await state.set_state(UserRegisterState.password_confirm)
        await message.answer('Подтвердите пароль: ')
    else:
        await message.answer('Пароль должен быть не меньше 8ми символов: ')
@dp.message(UserRegisterState.password_confirm)
async def get_password_confirm(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if data['password'] == message.text:
        await state.update_data(password_confirm=message.text)
        data['password_confirm'] = message.text
        res_reg = await UserRegister(data).register_api()
        if res_reg:
            await state.set_state(UserRegisterState.activation_code)
            await message.answer(res_reg)
    else:
        await message.answer('Пароли не совпадают')

@dp.message(UserRegisterState.activation_code)
async def activate(message: types.Message, state: FSMContext):
    data = await state.get_data()
    res_activate = await UserRegister(data).activate_api()


async def main():
    dp.startup.register(set_main_menu)
    await dp.start_polling(bot)


asyncio.run(main())


