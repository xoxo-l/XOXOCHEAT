from keyboard import is_pressed

from Utils import time
from API.entity import *

def main(csgo):
	while(True):
		time.sleep(1)
		player = Player()
		if is_pressed('space') and player.in_ground:
			player.jump()
