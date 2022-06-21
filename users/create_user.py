class User:
  def __init__(self, id, role, dists = 0, regs = 0, cults = 0):         
    self.id = id
    self.role = role
    self.dists = []
    self.regs = []
    self.cults = []

  def set_dist(self, dist):
    self.dists.append(dist)

  def get_dists(self):
    return self.dists

  def remove_dist(self, dist):
    self.dists.remove(dist)

  def set_reg(self, reg):
    self.regs.append(reg)

  def get_regs(self):
    return self.regs

  def remove_reg(self, reg):
    self.regs.remove(reg)

  def set_cult(self, cul):
    self.cults.append(cul)

  def get_cults(self):
    return self.cults

  def remove_cult(self, cul):
    self.cults.remove(cul)

def create_user(id, role):
  user = User(int(id), str(role))
  users.append(user)
  return user

def getUser(id):
  for user in users:
    if user.id == id:
      return user

def clearUser(id):
  for user in users:
    if user.id == id:
      user.dists = []
      user.regs = []
      user.cults = []
      return user

def deleteUser(user):
  users.remove(user)

users = []