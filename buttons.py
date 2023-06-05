from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

button_test = InlineKeyboardButton(text="Тест", callback_data="start_test")
button_add = InlineKeyboardButton(text="Добавить", callback_data="start_add")

keyboard_menu = InlineKeyboardMarkup(inline_keyboard=[[button_add,button_test]])