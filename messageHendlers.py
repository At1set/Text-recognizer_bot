import asyncio
from TextRecognizer import text_recognition

async def animate_message_loading(bot, message, text, count=2):
  _message = await bot.send_message(message.from_user.id, text)
  # получаем message_id и chat_id отправленного сообщения
  message_id = _message.message_id
  chat_id = _message.chat.id
  for a in range(1, count + 1):
    for b in range(1, 4):
      dotted = "." * b
      await bot.edit_message_text(f"{text}{dotted}", message_id=message_id, chat_id=chat_id)
      await asyncio.sleep(0.3)
    await asyncio.sleep(0.6)
  await asyncio.sleep(0.3)


async def saveImage(bot, message):
  isDone = True
  file_name = None
  try:
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    file_name = file.file_path.split("/")[-1]
    await bot.download(file_id, f"./src/data/{file_name}")
  except:
    isDone = False
  return isDone, file_name


def writeResults(file_name, result):
  file_name = file_name.split(".")[0]
  result_path = f"./src/data/{file_name}.txt"
  with open(result_path, "w", encoding='utf-8') as file:
    result_str = ""
    for line in result:
      result_str += line+"\n\n"
    file.write(result_str[:-2])
  
  return result_path



def readImage(file_path):
  return text_recognition(f"./src/data/{file_path}")