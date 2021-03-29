from ctypes import *

from .entity import Entity
from Utils import time
from offsets import *

from Process.Structures import *

class Player(Entity):

  def jump(self):
    self._write_client(dwForceJump, 0x5, c_int)
    time.sleep(30)
    self._write_client(dwForceJump, 0x4, c_int)

  def shot(self):
    self._write_client(dwForceAttack, 0x5, c_int)
    time.sleep(5)
    self._write_client(dwForceAttack, 0x4, c_int)

  def aim_at(self, entity):
    pass
  
  @property
  def pos(self):
    vec_ = self.read(m_vecOrigin, Vector3)
    vec_.z += self.aim.z
    return Vector3(vec_.x, vec_.y, vec_.z)

  @property
  def in_crosshair(self):
    return Entity(self.read(m_iCrosshairId, c_int))

  def __init__(self):
    Entity.__init__(self, 1)