from aiogram.types import InlineKeyboardButton, BotCommand
from aiogram.utils.keyboard import InlineKeyboardBuilder


reg_btn = InlineKeyboardBuilder(
    markup=[
        [InlineKeyboardButton(text = 'Регистрация',callback_data='register')],
        [InlineKeyboardButton(text = 'Вход',callback_data='login')],
        [InlineKeyboardButton(text = 'Профиль',callback_data='profile')]    
    ],
)

activate_kb = InlineKeyboardBuilder(
    markup=[[InlineKeyboardButton(text = "Все,я активировал",callback_data='activate')]]
)
main_menu_commands = [
        BotCommand(command='/help',
                   description='Справка по работе бота'),
        BotCommand(command='/support',
                   description='Поддержка'),
        BotCommand(command='/contacts',
                   description='Другие способы связи'),
        BotCommand(command='/payments',
                   description='Платежи')
    ]