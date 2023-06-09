from aiogram import Router, F
from aiogram.filters import Command, Text
from aiogram.types import Message, CallbackQuery
from buttons import keyboard_menu, keyboard_check, keyboard_correct, keyboard_empty
import filters as f
from constants import admin_ids
import sqlite3
import random

info = {}

def create_empty(user_id):
    info[user_id] = {'state': 'menu',
                    'front':'',
                    'back':'',
                    'ticket':0,
                    'data':[],
                    'i':0}

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
    await message.answer('Главное меню.\n\nЧитающий это, у тебя получится всё сдать, и помни главное: "Кто не падал, тот не поднимался. Кто не срал, тот не подтирался" © Стэтхэм',reply_markup=keyboard_menu)

@router.message(Command(commands='show'))
async def show_tickets(message: Message):
    dp = sqlite3.connect('data/cards.db')
    sql = dp.cursor()
    select = sql.execute('SELECT DISTINCT ticket FROM cards')
    tickets_list = map(str,sorted([x[0] for x in list(select)]))
    tickets = ", ".join(tickets_list)
    await message.answer('Уже добавлены карточки по билетам - '+ tickets)
    sql.close()
    dp.close()


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
async def test_button_clicked(callback:CallbackQuery):
    await callback.message.answer("Напиши номер билета, который хотите повторить")
    user_id=callback.from_user.id
    create_empty(user_id)
    await callback.answer()
    info[user_id]['state'] = 'in_test_ticket'


async def start_test(message: Message, ticket_number: int):
    user_id=message.from_user.id
    info[user_id]['ticket'] = ticket_number
    db=sqlite3.connect('data/cards.db')
    sql=db.cursor()
    select = sql.execute(f'SELECT front, back FROM cards WHERE ticket={ticket_number}')
    info[user_id]['data']=list(select.fetchall())
    sql.close()
    db.close()
    if len(info[user_id]['data'])==0:
        await message.answer('Такого билета нет, или карточки не заполнены.\nВведите другой билет')
    else:
        info[user_id]['state'] = 'in_test'
        i=0
        info[user_id]['i']=i
        info[user_id]['front'] = info[user_id]['data'][i][0]
        info[user_id]['back'] = info[user_id]['data'][i][1]
        await message.answer('Ответьте на вопрос:\n'+info[user_id]['front'], reply_markup=keyboard_check)

@router.message(F.text, f.IsNumber(), f.InTestTicket(info=info))
async def start_by_number(message: Message):
    await start_test(message,int(message.text))


@router.message(Command(commands=['random']))
async def random_start_test(message: Message):
    db = sqlite3.connect('data/cards.db')
    sql = db.cursor()
    tickets = list(sql.execute('SELECT DISTINCT ticket FROM cards'))
    sql.close()
    db.close()
    create_empty(message.from_user.id)
    choice = random.choice(tickets)[0]
    await message.answer(f'Вам попался билет - {choice}.\nУдачи!')
    await start_test(message, choice)

@router.callback_query(Text(text=['check']), f.InTest(info=info))
async def show_answer(callback: CallbackQuery):
    user_id = callback.from_user.id
    await callback.message.edit_text('Правильный ответ:\n'+info[user_id]['back'])
    await callback.message.edit_reply_markup(reply_markup=keyboard_correct)

@router.callback_query(Text(text=['correct']), f.InTest(info=info))
async def if_correct(callback: CallbackQuery):
    user_id = callback.from_user.id
    await callback.answer()
    i = info[user_id]['i']
    del info[user_id]['data'][i]

    if len(info[user_id]['data'])==0:
        await callback.message.answer(f'Карточки по билету {info[user_id]["ticket"]} закончились.\nМожете написать номер следующего билета.')
        info[user_id]['state'] = 'in_test_ticket'
    else:
        if i+1>=len(info[user_id]['data']):
            info[user_id]['i'] = 0
            i = info[user_id]['i']

        info[user_id]['front'] = info[user_id]['data'][i][0]
        info[user_id]['back'] = info[user_id]['data'][i][1]
        await callback.message.edit_text('Ответьте на следующий вопрос:\n'+info[user_id]['front'])
        await callback.message.edit_reply_markup(reply_markup=keyboard_check)

@router.callback_query(Text(text=['incorrect']), f.InTest(info=info))
async def if_incorrect(callback: CallbackQuery):
    user_id = callback.from_user.id
    await callback.answer()
    i = info[user_id]['i']
    if i+1 >= len(info[user_id]['data']):
        info[user_id]['i']=0
        i = info[user_id]['i']
    else:
        info[user_id]['i']+=1
        i = info[user_id]['i']
    info[user_id]['front'] = info[user_id]['data'][i][0]
    info[user_id]['back'] = info[user_id]['data'][i][1]
    await callback.message.edit_text('Ответьте на следующий вопрос:\n'+info[user_id]['front'])
    await callback.message.edit_reply_markup(reply_markup=keyboard_check)
