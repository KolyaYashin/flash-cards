from aiogram import Bot
from aiogram.types import BotCommand

async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/menu', description='Открыть меню'),
        BotCommand(command='/show', description='Показать какие билеты расписаны'),
        BotCommand(command='/random', description='Рандомный билет'),
        BotCommand(command='/list',description='Показать список всех билетов')
    ]

    await bot.set_my_commands(main_menu_commands)