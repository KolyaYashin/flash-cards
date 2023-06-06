from create_bot import dp, bot
import handlers
import data.create_table
from main_menu import set_main_menu

if __name__=='__main__':
    dp.startup.register(set_main_menu)
    dp.include_router(handlers.router)
    dp.run_polling(bot)