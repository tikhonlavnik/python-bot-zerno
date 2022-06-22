from aiogram import Dispatcher, types 
from create_bot import bot
from google_sheets import sheet
from data_base import db
import time

start_text = 'Приветствую! Я – Зерновик. Бот, который поможет вам получать\
  самые актуальные на текущий момент торговые предложения от фермеров. Вам остается лишь только выбрать необходимую культуру,\
  регион или округ и моментально получить информацию по заданным критериям.'

bot_target = 'Данный бот поможет вам получать\
  самые актуальные на текущий момент торговые предложения от фермеров. Вам остается лишь только выбрать необходимую культуру,\
  регион или округ и моментально получить информацию по заданным критериям.'

async def read_farmers_sheet(message:types.Message):
  res = sheet.read_farmers()
  db.cur.execute("DELETE FROM farmers;")
  for f in res:
    # print(f[0], f[1], f[2], f[3])
    db.cur.execute("INSERT OR IGNORE INTO farmers VALUES(?, ?, ?, ?, ?);", (int(round(time.time() * 1000)),f[0], f[1], f[2], f[3]))
    time.sleep(0.005)
  db.db.commit()


def return_common_handlers(dp: Dispatcher):
  dp.register_message_handler(read_farmers_sheet, commands=['read_farmers_sheet'])
