from aiogram import Bot
from aiogram.types import BotCommand

async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/menu', description='Открыть меню'),
        BotCommand(command='/show', description='Показать какие билеты расписаны')
    ]

    await bot.set_my_commands(main_menu_commands)