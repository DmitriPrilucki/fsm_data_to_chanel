from aiogram import Bot, Dispatcher, types, executor
import logging

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from config import TOKEN, CHAT_ID

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=storage)


class Register(StatesGroup):
    name = State()
    age = State()
    desc = State()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    await message.reply('Здравствуйте, я бот для йоги!\nЗапишитесь командой /yoga ←')


@dp.message_handler(commands=['yoga'])
async def cmd_start(message: types.Message) -> None:
    await message.answer('Ок! Введи имя')
    await Register.name.set()


@dp.message_handler(state=Register.name)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await message.reply('А теперь отправь нам возраст!')
    await Register.next()


@dp.message_handler(state=Register.age)
async def load_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text

    await message.reply('А теперь отправь нам описание!')
    await Register.next()


@dp.message_handler(state=Register.desc)
async def load_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['desc'] = message.text
        await message.reply(text='<b>Вот твои данные</b>:', parse_mode='html')
        await bot.send_message(chat_id=CHAT_ID,
                               text=f"Имя: {data['name']}\nВозраст: {data['age']}\nОписание: {data['desc']}")


@dp.message_handler()
async def bot_not_know(message: types.Message):
    await bot.send_message(message.from_user.id, "Чел ты чё несёшь!?")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)