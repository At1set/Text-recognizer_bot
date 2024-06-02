from Api_token import *
from config import *

from aiogram import Bot, types, F
from aiogram import Dispatcher
from aiogram.filters import CommandStart, Command
# from Bot_filters import *
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import messageHendlers as main_functions

import asyncio
import os


class State(StatesGroup):
  prozessing = State()


bot = Bot(token=API_TOKEN)
dp = Dispatcher()


@dp.message(State.prozessing)
async def deleteMessages(message: types.Message):
  return await message.delete()


@dp.message(CommandStart())
async def start_command(message: types.Message):
  await message.answer(f"""\
"Привет, @{message.from_user.username} !😉"

Если хочешь узнать, как пользоваться мной ❓: /help
Меня создали👪: /creators
Бонус🎁: /bonus
""")
  return await bot.send_sticker(message.from_user.id, sticker="CAACAgIAAxkBAAEIxyxkTSnLjHcab7Wu08tDHOHsMmVujAACiSIAAsSb6Us7ZFai5iiSfC8E")


@dp.message(Command('help'))
async def help_command(message: types.Message):
  return await message.answer("""\
Данным ботом очень легко пользоваться!
Просто пришли мне любое фото/скриншот,
(Очень желательно хорошее качество и видимость текста)
а я попробую считать текст с изображения и отправить его 
тебе в виде сообщения или могу скинуть файлом.
""")


@dp.message(Command('creators'))
async def creators_command(message: types.Message):
  return await message.answer("""\
Авторы данного бота:

Бацюра Илья @At1set😎 - Главный программист.

Дычко Дмитрий @di4kod🤩 - Помощник по созданию бота, презентации

Аблякимов Селим @bazazakrblta😶‍🌫️ - Создание идеи, презентация
""")


@dp.message(Command('bonus'))
async def bonus_command(message: types.Message):
  return await message.answer("В разработке⚒️")


@dp.message(F.photo)
async def photo_handler(message: types.Message, state: FSMContext):
  isImageSaved, file_name = await main_functions.saveImage(bot, message)
  if (not isImageSaved):
    return await message.answer("Ой, что то пошло не так. Бот не смог загрузить изображение.")
  
  await state.set_state(State.prozessing)
  state = await state.set_data({"file_name": file_name})

  return await bot.send_message(message.from_user.id, "В каком формате вы хотите получить текст с изображения?", reply_markup=\
  InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Текстом", callback_data="out_text"), InlineKeyboardButton(text="Файл .txt", callback_data="out_file")]
  ]))


@dp.message()
async def echo_message(message: types.Message):
  await bot.send_message(message.from_user.id, "Пришлите мне фотографию, а я попробую перенести весь текст с изображения в символы.")


@dp.callback_query()
async def photo_callback_hanler(callback: types.CallbackQuery, state: FSMContext):
  async def exit(message="", photo_path="", txt_path=""):
    await state.clear()
    if len(message) > 0: await bot.send_message(callback.from_user.id, message)
    if len(photo_path) > 0: os.remove(photo_path)
    if len(txt_path) > 0: os.remove(txt_path)
    return await bot.answer_callback_query(callback.id ,text=message)
  
  data = await state.get_data()
  if (data == {}): return await exit("Извините, произошла ошибка, попробуйте еще раз.")
  file_name = data["file_name"]

  await callback.message.delete()
  await main_functions.animate_message_loading(bot, callback, "Подождите пару секунд")
  
  result = main_functions.readImage(file_name)
  if len(result) == 0:
    return await exit("Извините, но бот не нашел текста на вашем изображении.", f"./src/data/{file_name}")
  
  result_path = ""
  if (callback.data == "out_text"):
    await bot.send_message(callback.from_user.id, "Готово, отправляю результат: ")
    await asyncio.sleep(2)
    await bot.send_message(callback.from_user.id, "\n\n".join(result))
  elif (callback.data == "out_file"):
    result_path = main_functions.writeResults(file_name, result)
    await bot.send_document(callback.from_user.id, types.FSInputFile(result_path, "Done.txt"))

  return await exit("", f"./src/data/{file_name}", result_path)


async def main():
  await dp.start_polling(bot)


if __name__ == '__main__':
  asyncio.run(main())