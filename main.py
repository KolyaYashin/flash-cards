from create_bot import dp, bot
import handlers

if __name__=='__main__':
    dp.include_router(handlers.router)
    dp.run_polling(bot)