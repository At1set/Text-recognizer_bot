from aiogram.filters import Filter
from aiogram.types import Message
from aiogram.enums import ContentType

class IsPtoho(Filter):
  async def __call__(self, message: Message) -> bool:
    return message.content_type == ContentType.PHOTO