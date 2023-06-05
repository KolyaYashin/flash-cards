from aiogram import Router, F
from aiogram.filters import Command, Text
from aiogram.types import Message, CallbackQuery
from buttons import keyboard_menu
import filters as f
from constants import admin_ids
import sqlite3


info = {}

def create_empty(user_id):
    info[user_id] = {'state': 'menu',
                    'front':'',
                    'back':'',
                    'ticket':0}

router = Router()

def add_to_db(user_id,inf):
    db = sqlite3.connect('data/cards.db')
    sql = db.cursor()
    sql.execute(f"INSERT INTO cards VALUES ('{info[user_id]['front']}','{info[user_id]['back']}',{info[user_id]['ticket']})")
    db.commit()
    sql.close()
    db.close()


@router.message(Command(commands='start'))
async def start_command(message: Message):
    create_empty(message.from_user.id)
    await message.answer('Бот сделан для подготовки к экзамену. \nНажмите /menu чтобы начать пользоваться.')

@router.message(Command(commands='menu'))
async def menu_command(message: Message):
    await message.answer('"Кто не падал, тот не поднимался. Кто не срал, тот не подтирался" © Стэтхэм',reply_markup=keyboard_menu)



@router.callback_query(Text(text=['start_add']), f.IsAdmin(admin_lists=admin_ids))
async def start_add_admin(callback: CallbackQuery):
    user_id = callback.from_user.id
    create_empty(user_id)
    info[user_id]['state']='in_add_front'
    await callback.message.answer('Напишите верхнюю часть флэш карточки: ')
    await callback.answer()


@router.message(F.text, ~Text(startswith='/'), f.InAddFront(info=info))
async def add_front(message: Message):
    user_id = message.from_user.id
    info[user_id]['front'] = message.text
    info[user_id]['state'] = 'in_add_back'
    await message.answer("Напишите нижнюю часть флэш карточки: ")


@router.message(F.text, ~Text(startswith='/'), f.InAddBack(info=info))
async def add_back(message: Message):
    user_id = message.from_user.id
    info[user_id]['back'] = message.text
    info[user_id]['state'] = 'in_add_ticket'
    await message.answer('Напишите номер билета, к которому относится данная карточка: ')

@router.message(F.text, f.IsNumber(), f.InAddTicket(info=info))
async def add_ticket(message: Message):
    user_id = message.from_user.id
    ticket_number = int(message.text)
    info[user_id]['ticket'] = ticket_number
    add_to_db(user_id, info)
    await message.answer('Карточка успешно добавлена. \nВы можете добавить следующую или выйти в меню - /menu')
    info[user_id]['state'] = 'in_add_front'



@router.callback_query(Text(text=['start_add']))
async def start_add(callback:CallbackQuery):
    await callback.answer()
    await callback.message.answer('К сожалению, вам нельзя добавлять flash карточки. \nОбратитесь к админу https://t.me/lelouchviabritannia.')
    await callback.message.answer('"Кто не падал, тот не поднимался. Кто не срал, тот не подтирался" © Стэтхэм',reply_markup=keyboard_menu)


@router.callback_query(Text(text=['start_test']))
async def start_test(callback:CallbackQuery):
    await callback.message.answer("Напиши номер билета, который хотите повторить")
    user_id=callback.from_user.id
    create_empty(user_id)
    info[user_id]['state'] = 'in_test_ticket'
