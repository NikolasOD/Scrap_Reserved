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
    gender_markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("Woman", callback_data='im_woman')
    item2 = types.InlineKeyboardButton("Man", callback_data='im_man')
    gender_markup.add(item1, item2)

    b_n = await bot.get_me()
    u_n = message.from_user
    await bot.send_message(message.chat.id,
                           f'Welcome, {u_n.first_name}!\n I am <b>{b_n.first_name}</b>, bot created to help you shop. '
                           f'I will find best discounts in Reserved online-shop for you. Please select your gender '
                           f'first 👇',
                           parse_mode='html',
                           reply_markup=gender_markup)


@dp.callback_query_handler(Text(startswith='im_'))
async def get_size(callback: types.CallbackQuery):
    gender = str(callback.data.split('_')[1])

    size_markup = types.InlineKeyboardMarkup(row_width=4)
    item1 = types.InlineKeyboardButton("XS", callback_data=f'xs_size_{gender}')
    item2 = types.InlineKeyboardButton("S", callback_data=f's_size_{gender}')
    item3 = types.InlineKeyboardButton("M", callback_data=f'm_size_{gender}')
    item4 = types.InlineKeyboardButton("L", callback_data=f'l_size_{gender}')
    size_markup.add(item1, item2, item3, item4)

    await callback.message.answer('Please select your size 👇', reply_markup=size_markup)


@dp.callback_query_handler(Text(contains='_size_'))
async def get_best_discounts(callback: types.CallbackQuery):
    await callback.message.answer('Please wait .....')

    user_data_lst = callback.data.split('_size_')
    size, gender = user_data_lst

    collect_data(size, gender)

    with open('result_data.json', encoding='utf-8') as file:
        data = json.load(file)

    for item in data:
        card = f'{hlink(item.get("title"), item.get("url"))}\n' \
               f'{hbold("Discount: ")} {item.get("discount_percent")}% 🔥\n' \
               f'{hbold("Old price: ")} {item.get("old_price")}\n' \
               f'{hbold("New price: ")} {item.get("new_price")}'

        await callback.message.answer(card)


def main():
    executor.start_polling(dp)


if __name__ == '__main__':
    main()
