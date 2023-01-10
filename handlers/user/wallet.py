
from loader import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram import types
from aiogram.types.message import ContentType
from filters import IsUser
from data import config
from .menu import balance

# shopArticleId 538350
PRICE = types.LabeledPrice(label="Подписка на 1 месяц",
                           amount=500*100)  # в копейках (руб)


@dp.message_handler(IsUser(), text=balance)
async def process_balance(message: Message, state: FSMContext):
    await message.answer('Ваш кошелек пуст! ')


@ dp.message_handler(commands=['buy'])
async def buy(message: types.Message):
    if config.PAYMENTS_TOKEN.split(':')[1] == 'TEST':
        await bot.send_message(message.chat.id, "Тестовый платеж!!!")

    await bot.send_invoice(message.chat.id,
                           title="Подписка на бота",
                           description="Активация подписки на бота на 1 месяц",
                           provider_token=config.PAYMENTS_TOKEN,
                           currency="rub",
                           photo_url="https://sun9-30.userapi.com/impf/00qoO2bkMzrVNTmNj-T1Fb4pKI9cQUqIaHRcHw/W5bO31J1B7Q.jpg?size=795x265&quality=95&crop=639,0,1198,399&sign=ba91c23070a435ac0de38e78a5349a7e&type=cover_group",
                           photo_width=416,
                           photo_height=234,
                           photo_size=416,
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="one-month-subscription",
                           payload="test-invoice-payload")


# pre checkout  (must be answered in 10 seconds)
@ dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


# successful payment
@ dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    print("SUCCESSFUL PAYMENT:")
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k} = {v}")

    await bot.send_message(message.chat.id,
                           f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно!!!")


