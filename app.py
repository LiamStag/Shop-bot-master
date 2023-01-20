
import os
import handlers
from keyboards.default.markups import *
from aiogram import executor, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from data import config
from loader import dp, db, bot
import filters
import logging

filters.setup(dp)

WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.environ.get("PORT", 5000))
user_message = 'Пользователь'
admin_message = 'Админ'


@dp.message_handler(commands='start')
@dp.message_handler(text=user_message)
async def user_mode(message: types.Message):
    cid = message.chat.id
    if cid in config.ADMINS:
        # await message.answer('Не знаю, как Вы угадали кодовое слово, но у вас нет прав просматривать этот раздел) ', reply_markup=user_menu_markup())
        config.ADMINS.remove(cid)
    await message.answer('''Привет! 👋

🤖 Я бот-магазин по продаже товаров магазина MrHeroGeek.
    
🛍️ Тут всё как принято, товары в каталоге, ваши деньги в пункте "баланс", есть корзина, а ещё вы можете узнать статус своего заказа

    ''', reply_markup=user_menu_markup())



@dp.message_handler(text=admin_message)
async def admin_mode(message: types.Message):

    cid = message.chat.id
    print(cid)
    if cid not in config.ADMINS:
        await message.answer('Не знаю, как Вы угадали кодовое слово, но у вас нет прав просматривать этот раздел) ', reply_markup=user_menu_markup())
        # config.ADMINS.append(cid)
    else: 
        await message.answer('Включен админский режим.', reply_markup=admin_menu_markup())


async def on_startup(dp):
    logging.basicConfig(level=logging.INFO)
    db.create_tables()

    await bot.delete_webhook()
    await bot.set_webhook(config.WEBHOOK_URL)


async def on_shutdown():
    logging.warning("Shutting down..")
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning("Bot down")


if __name__ == '__main__':

    if "HEROKU" in list(os.environ.keys()):

        executor.start_webhook(
            dispatcher=dp,
            webhook_path=config.WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host=WEBAPP_HOST,
            port=WEBAPP_PORT,
        )

    else:

        executor.start_polling(dp, on_startup=on_startup, skip_updates=False)
