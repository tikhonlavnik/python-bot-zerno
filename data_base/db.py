import sqlite3 as sq
import random

def start_db():
  global db, cur
  db = sq.connect('database.db')
  cur = db.cursor()
  if db:
    print('Database connected')

def get_dists():
  dists = cur.execute('SELECT * FROM districts;').fetchall()
  return dists

def get_regs(user):
  regs = cur.execute(f"SELECT * FROM regions WHERE district = '{user.dists[0]}';").fetchall() 
  return regs

def get_cults():
  cults = cur.execute(f"SELECT * FROM cultures;").fetchall() 
  return cults

def get_farmers(user, cul, dists, regs):
  farms = []
  if len(user.dists) > 1 and len(cul) > 1:
    x = cur.execute(f"SELECT * FROM farmers WHERE district IN {dists} AND culture IN {cul};").fetchall()
    farms = random.sample(x, len(x)) 
  elif len(user.dists) > 1 and len(cul) == 1:
    x = cur.execute(f"SELECT * FROM farmers WHERE district IN {dists} AND culture = '{cul[0]}';").fetchall()
    farms = random.sample(x, len(x)) 
  elif len(user.regs) > 1 and len(cul) > 1:
    x = cur.execute(f"SELECT * FROM farmers WHERE region IN {regs} AND culture IN {cul};").fetchall()
    farms = random.sample(x, len(x)) 
  elif len(user.regs) > 1 and len(cul) == 1:
    x = cur.execute(f"SELECT * FROM farmers WHERE region IN {regs} AND culture = '{cul[0]}';").fetchall()
    farms = random.sample(x, len(x)) 
  elif len(user.regs) == 1 and len(cul) > 1:
    x = cur.execute(f"SELECT * FROM farmers WHERE region = '{regs[0]}' AND culture IN {cul};").fetchall()
    farms = random.sample(x, len(x)) 
  elif len(user.regs) == 1 and len(cul) == 1:
    x = cur.execute(f"SELECT * FROM farmers WHERE region = '{regs[0]}' AND culture = '{cul[0]}';").fetchall()
    farms = random.sample(x, len(x)) 
  return farms