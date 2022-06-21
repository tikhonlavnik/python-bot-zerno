from aiogram.utils import executor
from create_bot import dp
from data_base import db
from keyboards import rm_kb


async def on_startup(_):
  print('Processing...')
  db.start_db()

from handlers import client, common

client.return_client_handlers(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)