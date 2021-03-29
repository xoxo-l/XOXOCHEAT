from API.entity import *
from Utils import time

def main(csgo):
  def mark_spotted(entity):
    entity.spotted = True
  while 1:
    time.sleep(20)
    set(
      map(
        mark_spotted,
        {Entity(i) for i in range(1, 16)}
      )
    )