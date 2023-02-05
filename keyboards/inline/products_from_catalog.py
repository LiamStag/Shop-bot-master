from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from loader import db

product_cb = CallbackData('product', 'id', 'action')


def product_markup(idx='', price=0, count=0, i=0):

    global product_cb

    markup = InlineKeyboardMarkup()

    back_btn = InlineKeyboardButton('⬅️', callback_data=product_cb.new(id=idx, action='back'))
    add_btn = InlineKeyboardButton(f'Добавить в корзину - {price}₽', callback_data=product_cb.new(id=idx, action='add'))
    next_btn = InlineKeyboardButton('➡️', callback_data=product_cb.new(id=idx, action='next'))
    if i>0:
        markup.insert(back_btn)
    if i!=(count-1):
        markup.insert(next_btn)
    markup.add(add_btn)

    return markup