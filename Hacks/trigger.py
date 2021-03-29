from API.entity import *
from Utils import time

def main(csgo):
  while 1:
    time.sleep(1)
    player = Player()
    entity = player.in_crosshair
    if entity.is_valid and entity.team != player.team:
      player.shot()
