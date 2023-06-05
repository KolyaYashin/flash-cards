from aiogram import Router, F
from aiogram.filters import Command, Text
from aiogram.types import Message, CallbackQuery
from buttons import keyboard_menu

info = {}

def create_empty(user_id):
    info[user_id] = {'state': 'menu',
                    'front':'',
                    'back':''}

router = Router()


@router.message(Command(commands='start'))
async def start_command(message: Message):
    create_empty(message.from_user.id)
    await message.answer('Бот сделан для подготовки к экзамену. \nНажмите /menu чтобы начать пользоваться.')

@router.message(Command(commands='menu'))
async def menu_command(message: Message):
    await message.answer('"Кто не падал, тот не поднимался. Кто не срал, тот не подтирался" © Стэтхэм',reply_markup=keyboard_menu)


@router.callback_query()


@router.callback_query(Text(text=['start_add']))
async def start_add(callback:CallbackQuery):
    await callback.message.answer('К сожалению, вам нельзя добавлять flash карточки. \nОбратитесь к админу https://t.me/lelouchviabritannia.')
    await callback.message.answer('"Кто не падал, тот не поднимался. Кто не срал, тот не подтирался" © Стэтхэм',reply_markup=keyboard_menu)
