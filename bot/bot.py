from aiogram import Bot, Dispatcher, types
from datetime import datetime
import os

from config import bot_token, channel_id


bot = Bot(bot_token)
dp = Dispatcher(bot)

    
async def send_info(path):
    await bot.send_photo(channel_id, photo= types.InputFile(f'{path}'), 
                        caption = f'<b>Кто-то</b> пришел/ушел\n<i>{datetime.utcnow()}</i>', parse_mode='HTML')
    os.remove(path) #Удаляем картинку из папки images

