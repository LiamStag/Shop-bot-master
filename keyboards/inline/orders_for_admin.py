from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

order_cb = CallbackData('product', 'id', 'action')

def order_markup(order):

    global order_cb

    markup = InlineKeyboardMarkup()
    delete_btn = InlineKeyboardButton('Удалить', callback_data=order_cb.new(id=order[3], action='delete_order'))
    change_btn = InlineKeyboardButton('Изменить', callback_data=order_cb.new(id=order[3], action='change_order'))
    markup.row(delete_btn, change_btn)

    return markup