from cgitb import text
from re import I
from aiogram import Dispatcher, types 
from create_bot import bot, dp
from keyboards import rm_kb
from aiogram.dispatcher.filters import Text
from data_base import db
from handlers import common
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from users import create_user as User

# Машина состояний для обработки сообщения обратной связи

class FSMFeedback(StatesGroup):
  feedback = State()

# Начало бота

async def start_message(message:types.Message):
  users = db.cur.execute('SELECT * FROM users;').fetchall()
  res = False
  User.create_user(message.from_user.id, 'None')
  user = User.getUser(message.from_user.id)
  User.clearUser(message.from_user.id)
  for user in users:
    if user[0] == message.from_user.id:
      res = True
  if res:
    await bot.send_message(message.from_user.id, common.start_text, reply_markup=rm_kb.start_kb())
  else:
    await bot.send_message(message.from_user.id, common.start_text + '\nВыберите роль', reply_markup=rm_kb.role_kb())

async def choose_role(call:types.CallbackQuery):
  res = call.data.split('_')[1]
  db.cur.execute("INSERT OR IGNORE INTO users VALUES(?, ?, ?, ?);", (call.from_user.id, f"{call.from_user.first_name} { call.from_user.last_name}", res, True))
  db.db.commit()
  User.create_user(call.from_user.id, res)
  await bot.edit_message_text(f'Вы выбрали роль - {res}', call.from_user.id, call.message.message_id, reply_markup=rm_kb.start_kb())

async def return_to_start(call:types.CallbackQuery):
  await bot.send_message(call.from_user.id, common.start_text, reply_markup=rm_kb.start_kb())

async def bot_targets(call:types.CallbackQuery):
  await bot.edit_message_text( f'Этот бот нужен для...', call.from_user.id, call.message.message_id, reply_markup=rm_kb.target_back_kb())
  await call.answer()

async def feedback(call:types.CallbackQuery):
  await FSMFeedback.feedback.set()
  await bot.edit_message_text( f'Здесь Вы можете поделиться своим мнением о Боте либо задать интересующий Вас вопрос технической поддержке!', call.from_user.id, call.message.message_id)

async def feedback_answer(message:types.Message, state:FSMContext):
  async with state.proxy() as data:
      data[feedback] = message.text
      # print(data[feedback])  ЭТО В БАЗУ ДАННЫХ - ОТВЕТ ОТ ЮЗЕРА
  await bot.send_message(message.from_user.id, 'Спасибо за обратную свзяь!')
  await state.finish()
  await bot.send_message(message.from_user.id, common.start_text, reply_markup=rm_kb.start_kb())

# Стартовое меню настроено, дальше обработка кнопок и тд

async def show_districts(call:types.CallbackQuery):
  await bot.edit_message_text( f'Выберите ФО', call.from_user.id, call.message.message_id, reply_markup=rm_kb.dists_kb())
  await call.answer()

async def choose_district(call:types.CallbackQuery):
  res = call.data.split('_')[1]
  user = User.getUser(call.from_user.id)
  user.set_dist(res)
  await bot.edit_message_text(f'Выберите ФО', call.from_user.id, call.message.message_id, reply_markup=rm_kb.change_dists_kb(call.data, user))
  await call.answer()

async def delete_choosen_district(call:types.CallbackQuery):
  res = call.data.split('_')[1]
  user = User.getUser(call.from_user.id)
  user.remove_dist(res)
  await bot.edit_message_text(f'Выберите ФО', call.from_user.id, call.message.message_id, reply_markup=rm_kb.change_dists_kb(call.data, user))
  await call.answer()

async def choose_all_districts(call:types.CallbackQuery):
  res = call.data.split('_')[1]
  user = User.getUser(call.from_user.id)
  districts = db.get_dists()
  user.dists = []
  for d in districts:
    user.set_dist(d[0])
  await bot.edit_message_text(f'Выберите ФО', call.from_user.id, call.message.message_id, reply_markup=rm_kb.change_dists_kb(res, user))
  await call.answer()

# Вывод регионов, если выбрать один округ

async def show_regs(call:types.CallbackQuery):
  user = User.getUser(call.from_user.id)
  await bot.edit_message_text(f'Выберите регионы', call.from_user.id, call.message.message_id, reply_markup=rm_kb.regs_kb(user))

async def choose_region(call:types.CallbackQuery):
  res = call.data.split('_')[1]
  user = User.getUser(call.from_user.id)
  user.set_reg(res)
  await bot.edit_message_text(f'Выберите регионы', call.from_user.id, call.message.message_id, reply_markup=rm_kb.change_regs_kb(call.data, user))
  await call.answer()

async def delete_choosen_region(call:types.CallbackQuery):
  res = call.data.split('_')[1]
  user = User.getUser(call.from_user.id)
  user.remove_reg(res)
  await bot.edit_message_text(f'Выберите регионы', call.from_user.id, call.message.message_id, reply_markup=rm_kb.change_regs_kb(call.data, user))
  await call.answer()

async def choose_all_regions(call:types.CallbackQuery):
  res = call.data.split('_')[1]
  user = User.getUser(call.from_user.id)
  regs = db.get_regs(user)
  user.regs = []
  for r in regs:
    user.set_reg(r[0])
  await bot.edit_message_text(f'Выберите регионы', call.from_user.id, call.message.message_id, reply_markup=rm_kb.change_regs_kb(res, user))
  await call.answer()

# Показ зерна после выбора региона

async def show_cults(call:types.CallbackQuery):
  await bot.edit_message_text(f'Выберите культуры', call.from_user.id, call.message.message_id, reply_markup=rm_kb.cults_kb())

async def choose_cult(call:types.CallbackQuery):
  res = call.data.split('_')[1]
  user = User.getUser(call.from_user.id)
  user.set_cult(res)
  await bot.edit_message_text(f'Выберите культуры', call.from_user.id, call.message.message_id, reply_markup=rm_kb.change_cults_kb(call.data, user))
  await call.answer()

async def delete_choosen_cult(call:types.CallbackQuery):
  res = call.data.split('_')[1]
  user = User.getUser(call.from_user.id)
  user.remove_cult(res)
  await bot.edit_message_text(f'Выберите культуры', call.from_user.id, call.message.message_id, reply_markup=rm_kb.change_cults_kb(call.data, user))
  await call.answer()

async def choose_all_cults(call:types.CallbackQuery):
  res = call.data.split('_')[1]
  user = User.getUser(call.from_user.id)
  cults = db.get_cults()
  user.cults = []
  for c in cults:
    user.set_cult(c[0])
  await bot.edit_message_text(f'Выберите культуры', call.from_user.id, call.message.message_id, reply_markup=rm_kb.change_cults_kb(res, user))
  await call.answer()

async def get_farmers(call:types.CallbackQuery):
  user = User.getUser(call.from_user.id)
  dists = tuple(user.get_dists())
  cul = tuple(user.get_cults())
  regs = tuple(user.get_regs())
  farms = db.get_farmers(user, cul, dists, regs)
  await bot.edit_message_text(f'Доступные фермеры:', call.from_user.id, call.message.message_id)
  if len(farms) == 0:
    await bot.send_message(call.from_user.id, f"Фермеры не найдены")
  else:
    for i in farms:
      res = f"""Телефон: {i[1]}\nКультура: {i[2]}\nРегион: {i[3]}\nФО: {i[4]}"""
      await bot.send_message(call.from_user.id, f"{res}")
  User.deleteUser(user)
  
async def back(call:types.CallbackQuery):
  user = User.getUser(call.from_user.id)
  if call.data == 'Назад_ds':
    user.dists = []
    await bot.edit_message_text(common.start_text,call.from_user.id, call.message.message_id, reply_markup=rm_kb.start_kb())
  elif call.data == 'Назад_rg':
    user.regs = []
    await bot.edit_message_text( f'Выберите ФО', call.from_user.id, call.message.message_id, reply_markup=rm_kb.dists_kb())




def return_client_handlers(dp: Dispatcher):
  dp.register_message_handler(start_message, commands=['start'])
  dp.register_callback_query_handler(choose_role, Text(startswith='rl_'))
  dp.register_callback_query_handler(return_to_start, text='back_to_menu')
  dp.register_callback_query_handler(bot_targets, text='bot_targets')
  dp.register_callback_query_handler(feedback, text='feedback', state=None)

  # Переход к выбору ФО

  dp.register_callback_query_handler(show_districts, text='search')
  dp.register_callback_query_handler(choose_district, Text(startswith='ds_'))
  dp.register_callback_query_handler(delete_choosen_district, Text(startswith='ch_'))
  dp.register_callback_query_handler(choose_all_districts, Text(startswith='ad_'))
  dp.register_callback_query_handler(show_regs, Text('Подтвердить_ds'))

  # Переход к выбору региона

  dp.register_callback_query_handler(choose_region, Text(startswith='rg_'))
  dp.register_callback_query_handler(delete_choosen_region, Text(startswith='chr_'))
  dp.register_callback_query_handler(choose_all_regions, Text(startswith='ar_'))

  # Переход к выбору зерна

  dp.register_callback_query_handler(show_cults, Text('Подтвердить_rg'))
  dp.register_callback_query_handler(show_cults, Text('Подтвердить_many_ds'))
  dp.register_callback_query_handler(choose_cult, Text(startswith='cl_'))
  dp.register_callback_query_handler(delete_choosen_cult, Text(startswith='chc_'))
  dp.register_callback_query_handler(choose_all_cults, Text(startswith='ac_'))

  # Вывод фермеров

  dp.register_callback_query_handler(get_farmers, Text('Подтвердить_cl'))
  
  # Общие хендлеры

  dp.register_callback_query_handler(back, Text(startswith='Назад'))
  dp.register_message_handler(feedback_answer, state=FSMFeedback.feedback)