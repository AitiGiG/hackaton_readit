from aiogram.types import InlineKeyboardButton, BotCommand, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardBuilder


reg_btn = InlineKeyboardBuilder(
    markup=[
        [InlineKeyboardButton(text = 'Регистрация',callback_data='register')],
        [InlineKeyboardButton(text = 'Вход',callback_data='login')],
        [InlineKeyboardButton(text = 'Профиль',callback_data='profile')]    
    ],
)


main_menu_commands = [
        BotCommand(command='/help',
                   description='Справка по работе бота'),
        BotCommand(command='/contacts',
                   description='Другие способы связи'),
        BotCommand(command='/start',
                   description='Начать')
    ]

