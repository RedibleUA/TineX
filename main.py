import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.exceptions import BotBlocked
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import TOKEN
from DB import RandomSticker, StickerAdd

API_TOKEN = TOKEN

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Ячейки памяти
class Form(StatesGroup):
    Anime = State()
    Cats = State()
    Meme = State()


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    try:
        await message.answer("Welcome to TineX\nI jast send random sticers🥵", reply_markup=selector_kb)

    except BotBlocked as E:
        pass


# Отправка стикеров


@dp.message_handler(commands=['anime'])
async def send_anime(message: types.Message):
    try:
        await bot.send_sticker(chat_id=message.chat.id, sticker=RandomSticker('Anime'))
    except BotBlocked as E:
        pass


@dp.message_handler(commands=['cats'])
async def send_cats(message: types.Message):
    try:
        await bot.send_sticker(chat_id=message.chat.id, sticker=RandomSticker('Cute cats'))
    except BotBlocked as E:
        pass


@dp.message_handler(commands=['meme'])
async def send_meme(message: types.Message):
    try:
        await bot.send_sticker(chat_id=message.chat.id, sticker=RandomSticker('Meme'))
    except BotBlocked as E:
        pass


# Добавление стикеров


@dp.message_handler(commands=['add'])
async def add_sticker(message: types.Message):
    try:
        await message.answer('Select the category', reply_markup=selectButtons)

    except BotBlocked as E:
        pass


# Ответ на кнопку и запуск ожидания ответа


@dp.callback_query_handler(text='Add Anime')
async def add_anime(callback: types.CallbackQuery):
    try:
        await callback.message.answer(f'You select category: <b>Anime</b>\n\nSend Sticker ID:\n1. You can get ID here @idstickerbot\n2. Send first sticker of the pack\n3. Copy Sticker ID\n4. Send to bot\n\nIf you want exit type "/exit"', parse_mode='HTML')
        await Form.Anime.set()
        await callback.answer()
    except BotBlocked as E:
        pass


@dp.callback_query_handler(text='Add Cute cats')
async def add_cats(callback: types.CallbackQuery):
    try:
        await callback.message.answer(f'You select category: <b>Cute cats</b>\n\nSend Sticker ID:\n1. You can get ID here @idstickerbot\n2. Send first sticker of the pack\n3. Copy Sticker ID\n4. Send to bot\n\nIf you want exit type "/exit"', parse_mode='HTML')
        await Form.Cats.set()
        await callback.answer()
    except BotBlocked as E:
        pass


@dp.callback_query_handler(text='Add Meme')
async def add_meme(callback: types.CallbackQuery):
    try:
        await callback.message.answer(f'You select category: <b>Meme</b>\n\nSend Sticker ID:\n1. You can get ID here @idstickerbot\n2. Send first sticker of the pack\n3. Copy Sticker ID\n4. Send to bot\n\nIf you want exit type "/exit"', parse_mode='HTML')
        await Form.Meme.set()
        await callback.answer()
    except BotBlocked as E:
        pass


# Ответ на Add


@dp.message_handler(state=Form.Anime)
async def process_name(message: types.Message, state: FSMContext):
    if(message.text.lower() != '/exit'):
        if ('CAACA' in message.text):
            await message.answer(StickerAdd('Anime', message.text))
        else:
            await message.answer(f"Wrong text")
    else:
        await message.answer(f"Bye")
    await state.finish()


@dp.message_handler(state=Form.Cats)
async def process_name(message: types.Message, state: FSMContext):
    if (message.text.lower() != '/exit'):
        if ('CAACA' in message.text):
            await message.answer(StickerAdd('Cute cats', message.text))
        else:
            await message.answer(f"Wrong text")
    else:
        await message.answer(f"Bye")
    await state.finish()


@dp.message_handler(state=Form.Meme)
async def process_name(message: types.Message, state: FSMContext):
    if (message.text.lower() != '/exit'):
        if ('CAACA' in message.text):
            await message.answer(StickerAdd('Meme', message.text))
        else:
            await message.answer(f"Wrong text")
    else:
        await message.answer(f"Bye")
    await state.finish()


# Всякая ерунда


@dp.message_handler(commands=['support'])
async def support(message: types.Message):
    try:
        await message.answer('Support', reply_markup=supportButtons)
    except BotBlocked as E:
        pass


@dp.message_handler(commands=['about'])
async def support(message: types.Message):
    try:
        await message.answer('All about us', reply_markup=aboutButtons)
    except BotBlocked as E:
        pass


@dp.message_handler()
async def send_message(message: types.Message):
    try:
        match message.text:
            case 'Anime':
                await bot.send_sticker(chat_id=message.chat.id, sticker=RandomSticker('Anime'))
            case 'Cute cats':
                await bot.send_sticker(chat_id=message.chat.id, sticker=RandomSticker('Cute cats'))
            case 'Meme':
                await bot.send_sticker(chat_id=message.chat.id, sticker=RandomSticker('Meme'))

    except BotBlocked as E:
        pass



# --------Кнопки--------


# Кнопки Anime | Cute cats | Meme
button_Anime = KeyboardButton('Anime')
button_CuteCats = KeyboardButton('Cute cats')
button_Meme = KeyboardButton('Meme')
selector_kb = ReplyKeyboardMarkup(resize_keyboard=True)
selector_kb.add(button_Anime, button_CuteCats, button_Meme)

# Кнопки add
selectButtons = InlineKeyboardMarkup(row_width=1)
selectAnimeButton = InlineKeyboardButton(text='Anime', callback_data='Add Anime')
selectCuteCatsButton = InlineKeyboardButton(text='Cute cats', callback_data='Add Cute cats')
selectMemeButton = InlineKeyboardButton(text='Meme', callback_data='Add Meme')
selectButtons.add(selectAnimeButton, selectCuteCatsButton, selectMemeButton)

# Кнопки support
supportButtons = InlineKeyboardMarkup(row_width=1)
SupportUaButton = InlineKeyboardButton(text='UA 🇺🇦', url='https://fondy.ua/uk/help-ukraine/')
SupportMeButton = InlineKeyboardButton(text='Me 🥰', url='https://www.buymeacoffee.com/FoPPi')
supportButtons.add(SupportUaButton, SupportMeButton)

# Кнопки about
aboutButtons = InlineKeyboardMarkup(row_width=1)
SiteButton = InlineKeyboardButton(text='Site', url='https://linktr.ee/redible')
aboutButtons.add(SiteButton)

if __name__ == '__main__':
    executor.start_polling(dp)
