from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

button_test = InlineKeyboardButton(text="Тест", callback_data="start_test")
button_add = InlineKeyboardButton(text="Добавить", callback_data="start_add")

keyboard_menu = InlineKeyboardMarkup(inline_keyboard=[[button_add,button_test]])

button_check = InlineKeyboardButton(text="Посмотреть ответ", callback_data="check")

keyboard_check = InlineKeyboardMarkup(inline_keyboard=[[button_check]])

button_correct = InlineKeyboardButton(text='✅',callback_data='correct')
button_incorrect = InlineKeyboardButton(text='❌', callback_data='incorrect')

keyboard_correct = InlineKeyboardMarkup(inline_keyboard=[[button_correct, button_incorrect]])

keyboard_empty = InlineKeyboardMarkup(inline_keyboard=[])