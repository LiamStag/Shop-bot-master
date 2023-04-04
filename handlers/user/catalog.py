
import logging
from aiogram.types import Message, CallbackQuery
from keyboards.inline.categories import categories_markup, category_cb
from keyboards.inline.products_from_catalog import product_markup, product_cb
from aiogram.utils.callback_data import CallbackData
from aiogram.types.chat import ChatActions
from loader import dp, db, bot
from .menu import catalog
from filters import IsUser


@dp.message_handler(IsUser(), text=catalog)
async def process_catalog(message: Message):
    await message.answer('Выберите раздел, чтобы вывести список товаров:',
                         reply_markup=categories_markup())


@dp.callback_query_handler(IsUser(), category_cb.filter(action='view'))
async def category_callback_handler(query: CallbackQuery, callback_data: dict):

    products = db.fetchall('''SELECT * FROM products product
    WHERE product.tag = (SELECT title FROM categories WHERE idx=?)''',
                           (callback_data['id'], ))

    await query.answer('Все доступные товары.')
    await show_products(query.message, products)


@dp.callback_query_handler(IsUser(), product_cb.filter(action='add'))
@dp.callback_query_handler(IsUser(), product_cb.filter(action='next'))
@dp.callback_query_handler(IsUser(), product_cb.filter(action='back'))
async def add_product_callback_handler(query: CallbackQuery, callback_data: dict):
    product = db.fetchone('SELECT quantity FROM cart WHERE cid = ? AND idx = ?', (query.message.chat.id, callback_data['id']))
    if product == None:
        db.query('INSERT INTO cart VALUES (?, ?, 1)',
             (query.message.chat.id, callback_data['id']))
    else:
        db.query('UPDATE cart SET quantity = ? WHERE cid = ? AND idx = ?',
             (product[0]+1, query.message.chat.id, callback_data['id']))
    await query.answer('Товар добавлен в корзину!')


async def show_products(m, products):

    if len(products) == 0:

        await m.answer('Здесь ничего нет 😢')

    else:
        count = len(products)
        await bot.send_chat_action(m.chat.id, ChatActions.TYPING)

        markup = product_markup(products[0][0], products[0][4], count, 0)
        text = f'<b>{products[0][1]}</b>\n\n{products[0][2]}'

        await m.answer_photo(photo=products[0][3],
                                 caption=text,
                                 reply_markup=markup)

@dp.callback_query_handler(IsUser(), product_cb.filter(action='next'))
async def show_product(m, products, i):
    await bot.send_chat_action(m.chat.id, ChatActions.TYPING)

    markup = product_markup(products[i][0], products[i][4], count, 0)
    text = f'<b>{products[i][1]}</b>\n\n{products[i][2]}'

    await m.answer_photo(photo=products[i][3],
                                 caption=text,
                                 reply_markup=markup)