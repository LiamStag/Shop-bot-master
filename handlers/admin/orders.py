
from aiogram.types import Message, CallbackQuery
from loader import dp, db
from handlers.user.menu import orders
from filters import IsAdmin
from keyboards.inline import orders_for_admin
from keyboards.inline.orders_for_admin import order_markup, order_cb

@dp.message_handler(IsAdmin(), text=orders)
async def process_orders(message: Message):
    
    orders = db.fetchall('SELECT * FROM orders')
    
    if len(orders) == 0: await message.answer('У вас нет заказов.')
    else: await order_answer(message, orders)

async def order_answer(message, orders):

    for order in orders:
        res = ''
        res += f'Заказ <b>№{order[3]}</b>\n\n'
        res += f'Имя <b>{order[1]}</b>\n\n'
        res += f'Адрес <b>{order[2]}</b>\n\n'
        res += f'Статус заказа <b>{order[4]}</b>\n\n'
        res += f'___________________________________\n\n'

        await message.answer(res, reply_markup=order_markup(order))

@dp.callback_query_handler(IsAdmin(), order_cb.filter(action='delete_order'))
async def delete_callback_handler(message, callback_data: dict):
    idx = callback_data['id']
    db.query('''DELETE FROM orders
                    WHERE products = ?''', (idx,))

    await message.answer(f'удалил {idx}')


@dp.callback_query_handler(IsAdmin(), order_cb.filter(action='change_order'))
async def delete_callback_handler(message, callback_data: dict):
    idx = callback_data['id']
    await message.answer(f'изменил {idx}')