from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data_base import db

def role_kb():
  kb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Агент', callback_data='rl_Агент')).\
    add(InlineKeyboardButton(text='Трейдер', callback_data='rl_Трейдер')).add(InlineKeyboardButton(text='Экспортер', callback_data='rl_Экспортер')).\
    add(InlineKeyboardButton(text='Завод-переработчик', callback_data='rl_Завод-переработчик'))
  return kb

def start_kb():
  kb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Поиск фремеров', callback_data='search')).\
    add(InlineKeyboardButton(text='Зачем нужен этот бот?', callback_data='bot_targets')).add(InlineKeyboardButton(text='Обратная связь', callback_data='feedback'))
  return kb

def target_back_kb():
  kb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Назад', callback_data='back_to_menu'))
  return kb

# Клавиатура для округов

def dists_kb():
  districts = db.get_dists()
  kb = InlineKeyboardMarkup(row_width=2)
  count = 0
  check = {}
  check2 = {}
  for dist in districts:
    count += 1
    if count % 2 == 0:
      check2 = InlineKeyboardButton(f"{dist[0]}", callback_data=f"ds_{dist[0]}")
      kb.row(check, check2)
    elif count == len(districts):
      kb.add(InlineKeyboardButton(f"{dist[0]}", callback_data=f"ds_{dist[0]}"))
    else:
      check = InlineKeyboardButton(f"{dist[0]}", callback_data=f"ds_{dist[0]}")
  kb.add(InlineKeyboardButton(f"Выбрать все", callback_data=f"ad_Выбрать все"))
  kb.add(InlineKeyboardButton(f"Назад", callback_data=f"Назад_ds"))
  return kb
  
def change_dists_kb(res, user):
  districts = db.get_dists()
  kb = InlineKeyboardMarkup(row_width=2)
  if "ds_" in res:
    count = 0
    check = {}
    check2 = {}
    for dist in districts:
      count += 1
      if count % 2 == 0:
        if dist[0] == res.split('_')[1]:
          check2 = InlineKeyboardButton(f"✔️ {dist[0]}", callback_data=f"ch_{dist[0]}")
        elif dist[0] in user.dists:
          check2 = InlineKeyboardButton(f"✔️ {dist[0]}", callback_data=f"ch_{dist[0]}")
        else:
          check2 = InlineKeyboardButton(f"{dist[0]}", callback_data=f"ds_{dist[0]}")
        kb.row(check, check2)
      elif count == len(districts):
        if dist[0] == res.split('_')[1]:
          kb.add(InlineKeyboardButton(f"✔️ {dist[0]}", callback_data=f"ch_{dist[0]}"))
        elif dist[0] in user.dists:
          kb.add(InlineKeyboardButton(f"✔️ {dist[0]}", callback_data=f"ch_{dist[0]}"))
        else:
          kb.add(InlineKeyboardButton(f"{dist[0]}", callback_data=f"ds_{dist[0]}"))
      else:
        if dist[0] == res.split('_')[1]:
          check = InlineKeyboardButton(f"✔️ {dist[0]}", callback_data=f"ch_{dist[0]}")
        elif dist[0] in user.dists:
          check = InlineKeyboardButton(f"✔️ {dist[0]}", callback_data=f"ch_{dist[0]}")
        else:
          check = InlineKeyboardButton(f"{dist[0]}", callback_data=f"ds_{dist[0]}")
  if "ch_" in res:
    count = 0
    check = {}
    check2 = {}
    for dist in districts:
      count += 1
      if count % 2 == 0:
        if dist[0] == res.split('_')[1]:
          check2 = InlineKeyboardButton(f"{dist[0]}", callback_data=f"ds_{dist[0]}")
        elif dist[0] in user.dists:
          check2 = InlineKeyboardButton(f"✔️ {dist[0]}", callback_data=f"ch_{dist[0]}")
        else:
          check2 = InlineKeyboardButton(f"{dist[0]}", callback_data=f"ds_{dist[0]}")
        kb.row(check, check2)
      elif count == len(districts):
        if dist[0] == res.split('_')[1]:
          kb.add(InlineKeyboardButton(f"{dist[0]}", callback_data=f"ds_{dist[0]}"))
        elif dist[0] in user.dists:
          kb.add(InlineKeyboardButton(f"✔️ {dist[0]}", callback_data=f"ch_{dist[0]}"))
        else:
          kb.add(InlineKeyboardButton(f"{dist[0]}", callback_data=f"ds_{dist[0]}"))
      else:
        if dist[0] == res.split('_')[1]:
          check = InlineKeyboardButton(f"{dist[0]}", callback_data=f"ds_{dist[0]}")
        elif dist[0] in user.dists:
          check = InlineKeyboardButton(f"✔️ {dist[0]}", callback_data=f"ch_{dist[0]}")
        else:
          check = InlineKeyboardButton(f"{dist[0]}", callback_data=f"ds_{dist[0]}")
  if res == 'Выбрать все':
    count = 0
    check = {}
    check2 = {}
    for dist in districts:
      count += 1
      if count % 2 == 0:
        check2 = InlineKeyboardButton(f"✔️ {dist[0]}", callback_data=f"ch_{dist[0]}")
        kb.row(check, check2)
      elif count == len(districts):
        kb.add(InlineKeyboardButton(f"✔️ {dist[0]}", callback_data=f"ch_{dist[0]}"))
      else:
        check = InlineKeyboardButton(f"✔️ {dist[0]}", callback_data=f"ch_{dist[0]}")
  kb.add(InlineKeyboardButton(f"Выбрать все", callback_data=f"ad_Выбрать все"))
  kb.add(InlineKeyboardButton(f"Назад", callback_data=f"Назад_ds"))
  if len(user.get_dists()) == 1:
    kb.add(InlineKeyboardButton(f"Подтвердить", callback_data=f"Подтвердить_ds"))
  elif len(user.get_dists()) > 1:
    kb.add(InlineKeyboardButton(f"Подтвердить", callback_data=f"Подтвердить_many_ds"))
  return kb

# Клавиатура для регионов

def regs_kb(user):
  regs = db.get_regs(user)
  kb = InlineKeyboardMarkup(row_width=2)
  count = 0
  check = {}
  check2 = {}
  for reg in regs:
    count += 1
    if count % 2 == 0:
      check2 = InlineKeyboardButton(f"{reg[0]}", callback_data=f"rg_{reg[0]}")
      kb.row(check, check2)
    elif count == len(regs):
      kb.add(InlineKeyboardButton(f"{reg[0]}", callback_data=f"rg_{reg[0]}"))
    else:
      check = InlineKeyboardButton(f"{reg[0]}", callback_data=f"rg_{reg[0]}")
  kb.add(InlineKeyboardButton(f"Выбрать все", callback_data=f"ar_Выбрать все"))
  kb.add(InlineKeyboardButton(f"Назад", callback_data=f"Назад_rg"))
  return kb

def change_regs_kb(res, user):
  regs = db.get_regs(user)
  kb = InlineKeyboardMarkup(row_width=2)
  if "rg_" in res:
    count = 0
    check = {}
    check2 = {}
    for reg in regs:
      count += 1
      if count % 2 == 0:
        if reg[0] == res.split('_')[1]:
          check2 = InlineKeyboardButton(f"✔️ {reg[0]}", callback_data=f"chr_{reg[0]}")
        elif reg[0] in user.regs:
          check2 = InlineKeyboardButton(f"✔️ {reg[0]}", callback_data=f"chr_{reg[0]}")
        else:
          check2 = InlineKeyboardButton(f"{reg[0]}", callback_data=f"rg_{reg[0]}")
        kb.row(check, check2)
      elif count == len(regs):
        if reg[0] == res.split('_')[1]:
          kb.add(InlineKeyboardButton(f"✔️ {reg[0]}", callback_data=f"chr_{reg[0]}"))
        elif reg[0] in user.regs:
          kb.add(InlineKeyboardButton(f"✔️ {reg[0]}", callback_data=f"chr_{reg[0]}"))
        else:
          kb.add(InlineKeyboardButton(f"{reg[0]}", callback_data=f"rg_{reg[0]}"))
      else:
        if reg[0] == res.split('_')[1]:
          check = InlineKeyboardButton(f"✔️ {reg[0]}", callback_data=f"chr_{reg[0]}")
        elif reg[0] in user.regs:
          check = InlineKeyboardButton(f"✔️ {reg[0]}", callback_data=f"chr_{reg[0]}")
        else:
          check = InlineKeyboardButton(f"{reg[0]}", callback_data=f"rg_{reg[0]}")
  if "chr_" in res:
    count = 0
    check = {}
    check2 = {}
    for reg in regs:
      count +=1
      if count % 2 == 0:
        if reg[0] == res.split('_')[1]:
          check2 = InlineKeyboardButton(f"{reg[0]}", callback_data=f"rg_{reg[0]}")
        elif reg[0] in user.regs:
          check2 = InlineKeyboardButton(f"✔️ {reg[0]}", callback_data=f"chr_{reg[0]}")
        else:
          check2 = InlineKeyboardButton(f"{reg[0]}", callback_data=f"rg_{reg[0]}")
        kb.row(check, check2)
      elif count == len(regs):
        if reg[0] == res.split('_')[1]:
          kb.add(InlineKeyboardButton(f"{reg[0]}", callback_data=f"rg_{reg[0]}"))
        elif reg[0] in user.regs:
          kb.add(InlineKeyboardButton(f"✔️ {reg[0]}", callback_data=f"chr_{reg[0]}"))
        else:
          kb.add(InlineKeyboardButton(f"{reg[0]}", callback_data=f"rg_{reg[0]}"))
      else:
        if reg[0] == res.split('_')[1]:
          check = InlineKeyboardButton(f"{reg[0]}", callback_data=f"rg_{reg[0]}")
        elif reg[0] in user.regs:
          check = InlineKeyboardButton(f"✔️ {reg[0]}", callback_data=f"chr_{reg[0]}")
        else:
          check = InlineKeyboardButton(f"{reg[0]}", callback_data=f"rg_{reg[0]}")
  if res == 'Выбрать все':
    count = 0
    check = {}
    check2 = {}
    for reg in regs:
      count += 1
      if count % 2 == 0:
        check2 = InlineKeyboardButton(f"✔️ {reg[0]}", callback_data=f"chr_{reg[0]}")
        kb.row(check, check2)
      elif count == len(regs):
        kb.add(InlineKeyboardButton(f"✔️ {reg[0]}", callback_data=f"chr_{reg[0]}"))
      else:
        check = InlineKeyboardButton(f"✔️ {reg[0]}", callback_data=f"chr_{reg[0]}")
  kb.add(InlineKeyboardButton(f"Выбрать все", callback_data=f"ar_Выбрать все"))
  kb.add(InlineKeyboardButton(f"Назад", callback_data=f"Назад_rg"))
  if len(user.get_regs()) >= 1:
    kb.add(InlineKeyboardButton(f"Подтвердить", callback_data=f"Подтвердить_rg"))
  # print(kb)
  return kb

# Клавиатура для зерна

def cults_kb():
  cults = db.get_cults()
  kb = InlineKeyboardMarkup(row_width=2)
  count = 0
  check = {}
  check2 = {}
  for cult in cults:
    count += 1
    if count % 2 == 0:
      check2 = InlineKeyboardButton(f"{cult[0]}", callback_data=f"cl_{cult[0]}")
      kb.row(check, check2)
    elif count == len(cults):
      kb.add(InlineKeyboardButton(f"{cult[0]}", callback_data=f"cl_{cult[0]}"))
    else:
      check = InlineKeyboardButton(f"{cult[0]}", callback_data=f"cl_{cult[0]}")
  kb.add(InlineKeyboardButton(f"Выбрать все", callback_data=f"ac_Выбрать все"))
  kb.add(InlineKeyboardButton(f"Назад", callback_data=f"Назад_cl"))
  return kb

def change_cults_kb(res, user):
  cults = db.get_cults()
  kb = InlineKeyboardMarkup(row_width=2)
  if "cl_" in res:
    count = 0
    check = {}
    check2 = {}
    for cult in cults:
      count += 1
      if count % 2 == 0:
        if cult[0] == res.split('_')[1]:
          check2 = InlineKeyboardButton(f"✔️ {cult[0]}", callback_data=f"chc_{cult[0]}")
        elif cult[0] in user.cults:
          check2 = InlineKeyboardButton(f"✔️ {cult[0]}", callback_data=f"chc_{cult[0]}")
        else:
          check2 = InlineKeyboardButton(f"{cult[0]}", callback_data=f"cl_{cult[0]}")
        kb.row(check, check2)
      elif count == len(cults):
        if cult[0] == res.split('_')[1]:
          kb.add(InlineKeyboardButton(f"✔️ {cult[0]}", callback_data=f"chc_{cult[0]}"))
        elif cult[0] in user.cults:
          kb.add(InlineKeyboardButton(f"✔️ {cult[0]}", callback_data=f"chc_{cult[0]}"))
        else:
          kb.add(InlineKeyboardButton(f"{cult[0]}", callback_data=f"cl_{cult[0]}"))
      else:
        if cult[0] == res.split('_')[1]:
          check = InlineKeyboardButton(f"✔️ {cult[0]}", callback_data=f"chc_{cult[0]}")
        elif cult[0] in user.cults:
          check = InlineKeyboardButton(f"✔️ {cult[0]}", callback_data=f"chc_{cult[0]}")
        else:
          check = InlineKeyboardButton(f"{cult[0]}", callback_data=f"cl_{cult[0]}")
  if "chc_" in res:
    count = 0
    check = {}
    check2 = {}
    for cult in cults:
      count +=1
      if count % 2 == 0:
        if cult[0] == res.split('_')[1]:
          check2 = InlineKeyboardButton(f"{cult[0]}", callback_data=f"cl_{cult[0]}")
        elif cult[0] in user.cults:
          check2 = InlineKeyboardButton(f"✔️ {cult[0]}", callback_data=f"chc_{cult[0]}")
        else:
          check2 = InlineKeyboardButton(f"{cult[0]}", callback_data=f"cl_{cult[0]}")
        kb.row(check, check2)
      elif count == len(cults):
        if cult[0] == res.split('_')[1]:
          kb.add(InlineKeyboardButton(f"{cult[0]}", callback_data=f"cl_{cult[0]}"))
        elif cult[0] in user.cults:
          kb.add(InlineKeyboardButton(f"✔️ {cult[0]}", callback_data=f"chc_{cult[0]}"))
        else:
          kb.add(InlineKeyboardButton(f"{cult[0]}", callback_data=f"cl_{cult[0]}"))
      else:
        if cult[0] == res.split('_')[1]:
          check = InlineKeyboardButton(f"{cult[0]}", callback_data=f"cl_{cult[0]}")
        elif cult[0] in user.cults:
          check = InlineKeyboardButton(f"✔️ {cult[0]}", callback_data=f"chc_{cult[0]}")
        else:
          check = InlineKeyboardButton(f"{cult[0]}", callback_data=f"cl_{cult[0]}")
  if res == 'Выбрать все':
    count = 0
    check = {}
    check2 = {}
    for cult in cults:
      count += 1
      if count % 2 == 0:
        check2 = InlineKeyboardButton(f"✔️ {cult[0]}", callback_data=f"chc_{cult[0]}")
        kb.row(check, check2)
      elif count == len(cults):
        kb.add(InlineKeyboardButton(f"✔️ {cult[0]}", callback_data=f"chc_{cult[0]}"))
      else:
        check = InlineKeyboardButton(f"✔️ {cult[0]}", callback_data=f"chc_{cult[0]}")
  kb.add(InlineKeyboardButton(f"Выбрать все", callback_data=f"ac_Выбрать все"))
  kb.add(InlineKeyboardButton(f"Назад", callback_data=f"Назад_cl"))
  if len(user.get_cults()) >= 1:
    kb.add(InlineKeyboardButton(f"Подтвердить", callback_data=f"Подтвердить_cl"))
  # print(kb)
  return kb