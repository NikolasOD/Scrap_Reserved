import json

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
from main import collect_data
import os

bot = Bot(token=os.getenv('RESERVED_BOT_TOKEN'), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
print('Bot start working ...')


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['Woman', 'Man']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    # await message.answer('Products with maximum discount', reply_markup=keyboard)
    b_n = await bot.get_me()
    u_n = message.from_user
    await bot.send_message(message.chat.id,
                           f'Welcome, {u_n.first_name}!\n I am <b>{b_n.first_name}</b>, bot created to help you shop.',
                           parse_mode='html',
                           reply_markup=keyboard)


@dp.message_handler(Text(equals=['Woman', 'Man']))
async def get_best_discounts(message: types.Message):
    await message.answer('Please wait .....')

    url_id = 1 if message.text == 'Woman' else 2
    collect_data(url_id)

    with open('result_data.json', encoding='utf-8') as file:
        data = json.load(file)

    for item in data:
        card = f'{hlink(item.get("title"), item.get("url"))}\n' \
               f'{hbold("Discount: ")} {item.get("discount_percent")}% 🔥\n' \
               f'{hbold("Old price: ")} {item.get("old_price")}\n' \
               f'{hbold("New price: ")} {item.get("new_price")}'

        await message.answer(card)


def main():
    executor.start_polling(dp)


if __name__ == '__main__':
    main()
